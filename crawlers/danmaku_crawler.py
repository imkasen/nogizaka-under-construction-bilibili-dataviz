#!/usr/bin/env python3

# 视频弹幕爬虫
# 弹幕数据有限制，并非完整爬取全部数量

import requests
import json
from bs4 import BeautifulSoup

cid_url = "https://api.bilibili.com/x/player/pagelist"
danmaku_url = "https://comment.bilibili.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/70.0.3538.110 Safari/537.36"
}

proxies = {
    "http": ""
}


def get_cid_response(bvid):
    """
    get json response content which contains the cid.
    :param bvid: BV id
    :return: json format
    """
    params = {
        "bvid": bvid,
        "jsonp": "jsonp"
    }

    response = requests.get(
        url=cid_url,
        headers=headers,
        params=params,
        proxies=proxies,
        timeout=5,
    )

    return response.json()


def get_danmaku(cid):
    total_url = danmaku_url + str(cid) + ".xml"
    response = requests.get(total_url)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, 'lxml')
    # .../<cid>.xml
    # ...
    # <d p="...">xxx</d>
    # ...
    results = soup.find_all('d')
    barrages = [barrage.text for barrage in results]  # list
    barrages = [barrage.upper() for barrage in barrages]
    barrages = [barrage.replace(' ', '') for barrage in barrages]  # remove blank
    return barrages


# get danmaku of the last video
with open('../resources/bv_info2.json', 'r') as read_file:
    bv_data = json.load(read_file)
    last_bv = bv_data[-1]['BV']
    last_ep = bv_data[-1]['EP']
    cid_data = get_cid_response(last_bv)
    last_cid = cid_data['data'][0]['cid']  # p=1
    danmaku = get_danmaku(last_cid)
    with open(f'../resources/danmaku/{last_ep}.json', 'w') as write_file:
        json.dump(danmaku, write_file, ensure_ascii=False, indent=4)
