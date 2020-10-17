# -*- coding: utf-8 -*-
# @Time    : 2020/8/27 20:53
# @Author  : Can Zhang
# @FileName: Crawing_main_kth.py
# @Software: PyCharm
import requests
from requests.exceptions import RequestException
import re
import pymongo
from config import *
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'class="text-xs-small padding-left-xs pos-title"> <a href="(.*?)">(.*?)<.*?class="text-xs-small padding-right-xs pos-ends">.*?>(.*?)</a>',re.S)
    return re.findall(pattern,html)

def main():
    url = 'https://www.kth.se/en/om/work-at-kth/lediga-jobb'
    html = get_one_page(url)

    results = parse_one_page(html)
    for result in results:
        result_dict = {
            'title':result[1],
            'address time':'',
            'link': 'https://www.kth.se' + result[0],
            'application deadline':result[2]
        }

        save_to_mongo(result_dict)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

if __name__ == '__main__':
    main()
