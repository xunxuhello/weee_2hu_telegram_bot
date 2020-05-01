# -*- coding: utf-8 -*

import config
import weee_db


premission_error = "二虎躲在床底下了！"

def check_admin_premission(uid):
    return str(uid) == config.get_adminid()

def check_user_premission(uid):
    return str(uid) in weee_db.get_user_list()

def get_premission_error_message():
    return premission_error
