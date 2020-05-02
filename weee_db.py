import json
import redis
import datetime
import collections

import config

r = redis.Redis(host=config.get_redis_host(), 
                port=config.get_redis_port(), 
                db=config.get_redis_db())

"""
TOOLS
"""
def get_zip2uid():
    zip2uid = collections.defaultdict(list)
    for uid in get_user_list():
        uzip = get_user_info(uid)["zip"]
        zip2uid[uzip].append(uid)
    return zip2uid

"""
API for user list
"""
def get_user_list():
    l = r.get("user_list")
    return json.loads(r.get("user_list")) if l else []

def add_user(uid):
    l = get_user_list()
    l = list(set(l + [uid]))
    r.set("user_list", json.dumps(l))

def delete_user(uid):
    l = get_user_list()
    l = [i for i in l if i != uid]
    r.set("user_list", json.dumps(l))

"""
API for user info 
"""
def get_info_key(u):
    return "info_" + str(u)

def add_user_info(u, d):
    r.set(get_info_key(u), json.dumps(d))

def get_user_info(u):
    return json.loads(r.get(get_info_key(u)))

"""
API for update time
"""
def get_time_key(zipcode):
    return "updatetime_" + zipcode

def set_update_time(zipcode, time):
    r.set(get_time_key(zipcode), time)

def get_time(zipcode):
    t = r.get(get_time_key(zipcode))
    return t if t else datetime.datetime.min.isoformat()

"""
API for product
"""
def get_product_key(zipcode, time):
    return "product_%s_%s"%(zipcode, time)

def get_product(zipcode, time):
    key = get_product_key(zipcode, time)
    p = r.get(key)
    return json.loads(p) if p else {}

def set_product(zipcode, time, p):
    key = get_product_key(zipcode, time)
    r.set(key, json.dumps(p))

def get_time_and_product(uzip):
    priv_time = get_time(uzip)
    priv_dict = get_product(uzip, priv_time)
    return priv_time, priv_dict

def set_time_and_product(uzip, now_time, weee_dic):
    set_update_time(uzip, now_time)
    set_product(uzip, now_time, weee_dic)


"""
API for filter
"""
def get_filter_key(u):
    return "filter_" + str(u)

def get_filter(u):
    key = get_filter_key(u)
    fl = r.get(key)
    return json.loads(fl) if fl else []

def set_filter(u, l):
    key = get_filter_key(u)
    r.set(key, json.dumps(l))

def add_filter(u, l):
    arr = get_filter(u)
    for w in l:
        arr.append(w)
    set_filter(u, list(set(arr)))

def delete_filter(u, l):
    arr = get_filter(u)
    arr = [w for w in arr if w not in l]
    set_filter(u, list(set(arr)))

def clear_filter(u):
    set_filter(u, [])


