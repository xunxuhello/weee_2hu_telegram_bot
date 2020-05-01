import requests
import collections
from bs4 import BeautifulSoup
import httplib

httplib._MAXHEADERS = 1000
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

def get_link(pid):
    return "https://www.sayweee.com/product/view/" + pid

def get_weee_now(zip = "90007"):

    def get_cookies():
        payload={"zip_code": zip}
        r = requests.post("https://www.sayweee.com/portal/api_create_preorder_by_zipcode", data=payload, headers=headers)
        return r.cookies

    cookies = get_cookies()

    r = requests.get("https://www.sayweee.com/shopping_list?category=all", cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')     
    arr = soup.find_all("div", class_="product-media")

    def getstat(s):
        pid = s["data-product-id"]
        name = s.find("div", class_="product-title").text.strip()
        p_type = s["data-product-category"]
        have_p = False if s.find("div", class_="sold-out-tag") else True
        data = {
            "name": name,
            "type": p_type
        }
        return pid, data, have_p

    def get_list(arr):
        weee_dic = {}
        for i in arr:
            pid, data, have_p= getstat(i)
            if have_p:
                weee_dic[pid] = data
        return weee_dic

    return get_list(arr)


def get_line(n = 8):
    return "\n" + " ----" * n + "\n"

def dic_to_strarr_by_type(dic):
    max_num = 70
    def split_by_type(raw_dic):
        new_dic = collections.defaultdict(list)
        for pairs in raw_dic.items():
            new_dic[pairs[1]["type"]].append(pairs)
        return new_dic

    def add_a(text, href):
        return "<a href='%s'>%s</a>"%(href, text)

    def arr_to_str(d):
        text_arr = []
        for k, v in sorted(d, key=lambda a:a[0]):
            text_arr.append(add_a(v["name"], get_link(k)))
        return text_arr
    strarr = []
    d_arr = split_by_type(dic)

    for k, v in d_arr.items():
        text = k.upper()
        text += get_line()
        arr = arr_to_str(v)
        if len(arr) < max_num:
            text += "\n".join(arr)
            strarr.append(text)
        else:
            text += "\n".join(arr[:max_num])
            strarr.append(text)
            for i in range(len(arr)/max_num):
                text = "\n".join(arr[(i+1)*max_num:(i+2)*max_num])
                strarr.append(text)
    return strarr

def dic_sub(now_dic, priv_dic):
    return dict((k, v) for k, v in now_dic.items() if k not in priv_dic)

def filter_dic(dic, fl):
    if not fl:
        return dic
    return dict((k, v) for k, v in dic.items() if any(w in v["name"] for w in fl))






