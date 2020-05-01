import json


config_dic = json.load(open("conf.json"))

def get_bot_id():
    return config_dic["TOKEN"]

def get_redis_host():
    return config_dic["redis_host"]

def get_redis_port():
    return config_dic["redis_port"]

def get_redis_db():
    return config_dic["redis_db"]

def get_adminid():
    return config_dic["adminid"]