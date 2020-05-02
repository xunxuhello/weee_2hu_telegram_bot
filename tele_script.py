# -*- coding: utf-8 -*

import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import datetime
import re
import random

import weee_lib
import weee_db
import config
import auth


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=config.get_bot_id(), use_context=True)
dispatcher = updater.dispatcher

"""
TOOLS FUNCTIONS
"""
def gettime(t):
    return t.split('T')[-1][:5]

def sent_dic_to_user(context, uid, weee_dic, uzip = None):
    if uzip:
        context.bot.send_message(chat_id=uid, 
                                     text="zip code: %s"%uzip, 
                                     parse_mode='html',
                                     disable_web_page_preview=True)
    weee_text_arr = weee_lib.dic_to_strarr_by_type(weee_dic)
    for weee_text in weee_text_arr:
        context.bot.send_message(chat_id=uid, 
                                     text=weee_text, 
                                     parse_mode='html',
                                     disable_web_page_preview=True)

def sent_time_to_user(context, uid, priv_time, now_time, have_new=True):
    if have_new:
        info_text = "<b>在 %s 到 %s 内有新货上架喔</b>"%(gettime(priv_time), gettime(now_time)) 
    else:
        info_text = "<b>在 %s 到 %s 内没有新货上架喔</b>"%(gettime(priv_time), gettime(now_time)) 
    context.bot.send_message(chat_id=uid, 
                         text=info_text, 
                         parse_mode='html')

def sent_newdic_to_user(context, ulist, priv_time, priv_dict, now_time, now_dict, reply_uid=None):
    new_dic = weee_lib.dic_sub(now_dict, priv_dict)
    if new_dic:
        for uid in ulist:
            f_dic = weee_lib.filter_dic(new_dic, weee_db.get_filter(uid))
            if f_dic:
                sent_time_to_user(context, uid, priv_time, now_time)
                sent_dic_to_user(context, uid, f_dic)
    else:
        if reply_uid:
            sent_time_to_user(context, reply_uid, priv_time, now_time, have_new=False)



"""
command start
"""
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="喵！")

dispatcher.add_handler(CommandHandler('start', start))


"""
command get_my_id
"""
def get_my_id(update, context):
    uid = update.effective_user.id
    text = "喵！你的UID是 %s 喔！"%(uid)
    if auth.check_user_premission(uid):
        text += "\n"
        text += str(weee_db.get_user_info(uid))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

dispatcher.add_handler(CommandHandler('get_my_id', get_my_id))

"""
command get_filter
"""
def get_filter(update, context):
    uid = update.effective_user.id
    if auth.check_user_premission(uid):
        fl = [w.encode('utf8') for w in weee_db.get_filter(uid)]
        if fl:
            info_text = "二虎知道你喜欢吃：" + ", ".join(fl)
        else:
            info_text = "二虎知道你不挑食～"
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=uid, text=info_text)

dispatcher.add_handler(CommandHandler('get_filter', get_filter))


"""
command add_filter
"""
def add_filter(update, context):
    uid = update.effective_user.id
    if auth.check_user_premission(uid):
        if len(context.args) != 0:
            weee_db.add_filter(uid, context.args)
            info_text = "你是一个挑食的小坏蛋喵～\n"
            fl = [w.encode('utf8') for w in weee_db.get_filter(uid)]
            info_text += "二虎知道你喜欢吃：" + ", ".join(fl)
        else:
            info_text = "快告诉二虎你喜欢吃啥～"
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=uid, text=info_text)

dispatcher.add_handler(CommandHandler('add_filter', add_filter))


"""
command clear_filter
"""
def clear_filter(update, context):
    uid = update.effective_user.id
    if auth.check_user_premission(uid):
        weee_db.clear_filter(uid)
        info_text = "二虎知道你不挑食～"
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=uid, text=info_text)

dispatcher.add_handler(CommandHandler('clear_filter', clear_filter))


"""
command update_zipcode
"""
def update_zipcode(update, context):
    def set_zipcode(uid, set_uid, zipcode):
        if not re.match(r"^[0-9]{5}$", zipcode):
            info_text = "请输入正确的 zipcode 喔。"
        elif not auth.check_user_premission(set_uid):
            info_text = "请输入正确的 user id 喔。"
        else:
            weee_db.add_user_info(set_uid, {"zip": zipcode})
            info_text = "更新成功～"
        return info_text
    uid = update.effective_user.id
    if auth.check_admin_premission(uid) and len(context.args) == 2:
        info_text = set_zipcode(uid, context.args[0], context.args[1])
    elif auth.check_user_premission(uid) and len(context.args) == 1:
        info_text = set_zipcode(uid, uid, context.args[0])
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=uid, text=info_text)

dispatcher.add_handler(CommandHandler('update_zipcode', update_zipcode))


"""
command update_weee
"""
update_time = datetime.datetime.min
def update_weee(update, context):
    global update_time
    uid = update.effective_user.id
    if (auth.check_user_premission(uid) and
        (datetime.datetime.now()-update_time).seconds > 10):
        zip2uid = weee_db.get_zip2uid()
        uzip = weee_db.get_user_info(uid)["zip"]
        if (auth.check_admin_premission(uid) and 
            len(context.args) == 2 and 
            re.match(r"^[0-9]{5}$", context.args[1])):
            uzip = context.args[1]
        priv_time, priv_dict = weee_db.get_time_and_product(uzip)

        now_time = datetime.datetime.now().isoformat()
        weee_dic = weee_lib.get_weee_now(uzip)

        if len(context.args) >= 1 and context.args[0] == "all":
            sent_dic_to_user(context, uid, weee_dic, uzip=uzip)

        if len(context.args) >= 1 and context.args[0] == "filter":
            f_dic = weee_lib.filter_dic(weee_dic, weee_db.get_filter(uid))
            sent_dic_to_user(context, uid, f_dic, uzip=uzip)

        sent_newdic_to_user(context, zip2uid[uzip], 
            priv_time, priv_dict, now_time, weee_dic, reply_uid=uid)

        weee_db.set_time_and_product(uzip, now_time, weee_dic)
        update_time = datetime.datetime.now()
    else:
        info_text = auth.get_premission_error_message()
        context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

dispatcher.add_handler(CommandHandler('update_weee', update_weee))


"""
command check_user_list
"""
def check_user_list(update, context):
    info_text = ""
    if auth.check_admin_premission(update.effective_user.id):
        ulist = weee_db.get_user_list()
        info_text = ""
        for u in ulist:
            info_text += u + " " + str(weee_db.get_user_info(u))
            info_text += "\n"
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

dispatcher.add_handler(CommandHandler('check_user_list', check_user_list))

"""
command check_premission
"""
def check_premission(update, context):
    info_text = ""
    if auth.check_admin_premission(update.effective_user.id):
        info_text = "喵！是铲屎官！"
    elif auth.check_user_premission(update.effective_user.id):
        info_text = "二虎亲热的蹭了蹭你！"
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

dispatcher.add_handler(CommandHandler('check_premission', check_premission))


"""
command add_user
"""
def add_user(update, context):
    info_text = ""
    if auth.check_admin_premission(update.effective_user.id):
        if len(context.args) != 2:
            info_text = "Please enter uid and zipcode"
        else:
            uid, zipcode = context.args[0], context.args[1]
            weee_db.add_user(uid)
            weee_db.add_user_info(uid, {"zip": zipcode})
            info_text = str(weee_db.get_user_info(uid))
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

dispatcher.add_handler(CommandHandler('add_user', add_user))


"""
command delete_user
"""
def delete_user(update, context):
    info_text = ""
    if auth.check_admin_premission(update.effective_user.id):
        weee_db.delete_user(context.args[0])
        info_text = str(weee_db.get_user_list())
    else:
        info_text = auth.get_premission_error_message()
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

dispatcher.add_handler(CommandHandler('delete_user', delete_user))


"""
command END
"""


def echo(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="喵喵喵！")

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)



"""
Repeating query
"""
j = updater.job_queue

def callback_hour(context):
    zip2uid = weee_db.get_zip2uid()

    for uzip, ulist in zip2uid.items():
        priv_time, priv_dict = weee_db.get_time_and_product(uzip)

        now_time = datetime.datetime.now().isoformat()
        weee_dic = weee_lib.get_weee_now(uzip)

        sent_newdic_to_user(context, ulist, 
            priv_time, priv_dict, now_time, weee_dic)
        
        weee_db.set_time_and_product(uzip, now_time, weee_dic)



job_minute = j.run_repeating(callback_hour, interval=3600, first=0)

updater.start_polling()















