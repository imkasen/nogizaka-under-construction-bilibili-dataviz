#!/usr/bin/env python3

# 视频弹幕爬虫
# 弹幕数据有限制，并非完整爬取全部数量

import requests
import json
from bs4 import BeautifulSoup
import re
import jieba
from collections import Counter

cid_url = "https://api.bilibili.com/x/player/pagelist"
danmaku_url = "https://comment.bilibili.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36"
}

# proxies = {
#     "http": ""
# }


def get_cid_response(bvid: str) -> json:
    """
    获取包含 cid 的 JSON 内容。
    :param bvid: 视频的 BVID
    :return: json
    """
    params = {
        "bvid": bvid,
        "jsonp": "jsonp"
    }

    response = requests.get(
        url=cid_url,
        headers=headers,
        params=params,
        # proxies=proxies,
        timeout=5,
    )

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        response.raise_for_status()


def get_danmaku(cid: int) -> dict:
    """
    根据 cid 获得弹幕，使用结巴分词并统计单词出现的频率。
    :param cid: 视频的 cid
    :return: dict
    """
    # 弹幕文件格式
    # .../<cid>.xml
    # ...
    # <d p="...">xxx</d>
    # ...
    # 请求并提取弹幕
    total_url = danmaku_url + str(cid) + ".xml"
    response = requests.get(total_url)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('d')
    barrages = [barrage.text for barrage in results]
    # 格式化
    barrages = [barrage.upper().replace(' ', '') for barrage in barrages]  # 大写，删除弹幕中的空格
    reg_str = '([\\W]+)|([0-9]+)|(哈{2,})|(字幕组)|(字幕)|(感谢)|(W{2,})|(H{2,})|(啊{2,})'
    barrages = [re.sub(reg_str, '', barrage).replace('_', '') for barrage in barrages]  # 删除标点、数字、下划线等
    barrages = [barrage for barrage in barrages if len(barrage) > 1]  # 删除空元素
    # 结巴分词
    jieba.load_userdict('resources/nogi46_names.txt')
    barrages_list = []
    for barrage in barrages:
        barrages_list.extend(jieba.lcut(barrage))
    barrages_list = [barrage for barrage in barrages_list if len(barrage) > 1]  # 删除单个汉字
    # 统计词频
    danmaku_dict = dict(Counter(barrages_list).most_common(len(barrages_list)))
    danmaku_dict = {k: v for k, v in danmaku_dict.items() if v > 2}  # 控制频率：删除只出现两次及以下的单词
    return danmaku_dict


def main() -> None:
    # 只获取最近一次 EP 的弹幕
    with open('resources/bv_info2.json', 'r') as read_file:
        bv_data = json.load(read_file)
        last_bv = bv_data[-1]['BV']
        # last_ep = bv_data[-1]['EP']
        last_title = bv_data[-1]['Title']
        cid_data = get_cid_response(last_bv)
        last_cid = cid_data['data'][0]['cid']
        danmaku = get_danmaku(last_cid)
        # with open(f'resources/danmaku/{last_ep}.json', 'w') as write_file:
        #     json.dump([last_title, danmaku], write_file, ensure_ascii=False, indent=4)
        with open(f'resources/danmaku.json', 'w') as write_file:
            json.dump([last_title, danmaku], write_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
