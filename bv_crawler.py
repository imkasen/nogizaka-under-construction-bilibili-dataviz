#!/usr/bin/env python3

# 一个简单的爬虫，用于获得 “乃木板工事中” 的各个视频信息

import requests
import json
import time

id_tyyh = "2301165"  # 天翼羽魂 id
search_keyword1 = "乃木坂工事中 坂道之诗"
search_keyword2 = "乃木坂工事中 不够热"

# 请求 URL
url = "https://api.bilibili.com/x/space/arc/search"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36"
}

# 代理
proxies = {
    "http": "http://27.206.72.206:9000"
}


def get_response(mid, page_number, keyword):
    """
    get response content.
    :param mid: user id number
    :param page_number: current page number
    :param keyword: search keyword
    :return: json format
    """
    params = {
        "mid": mid,
        "ps": "30",
        "tid": "0",
        "pn": str(page_number),
        "keyword": keyword,
        "order": "pubdate",
        "jsonp": "jsonp"
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        proxies=proxies,
        timeout=5
    )

    return response.json()


def get_total_page_number(mid, keyword):
    """
    obtain total page numbers for each keyword.
    :param mid: user id number
    :param keyword: search keyword
    :return: int
    """
    page_result = get_response(mid, "1", keyword)
    return int(page_result['data']['page']['count'] / page_result['data']['page']['ps'] + 1)


# 获取关键词 "乃木坂工事中 坂道之诗" 下的每个页面内容并整合
# 注意：缺少 EP154 生驹里奈毕业演唱会特集
bv_dict = {}
for page_num in reversed(range(1, get_total_page_number(id_tyyh, search_keyword1) + 1)):
    results = get_response(id_tyyh, page_num, search_keyword1)

    for bv_info in reversed(results['data']['list']['vlist']):

        video_bvid = str(bv_info['bvid'])                                                             # BV 号
        video_title = bv_info['title']                                                                # 标题
        video_ep = video_title[int(video_title.find('EP')):int(video_title.find('EP')) + 5].rstrip()  # EP
        video_created_time = time.asctime(time.localtime(bv_info['created']))                         # 投稿时间
        video_play = str(bv_info['play'])                                                             # 播放数量
        video_comment = str(bv_info['comment'])                                                       # 评论数量
        video_danmaku = str(bv_info['video_review'])                                                  # 弹幕数量

        # 例子：
        # {
        #     'BV1vt411k7At': [
        #         'EP187',
        #         '【乃木坂工事中】EP187 一期生四人联合毕业式【坂道之诗】',
        #         'Mon Dec 24 07:54:13 2018',
        #         '96786',
        #         '684',
        #         '2578'
        #     ]
        # }
        bv_dict[video_bvid] = [video_ep, video_title, video_created_time, video_play, video_comment, video_danmaku]

with open('resources/bv_info.json', 'w') as bv_file:
    json.dump(bv_dict, bv_file, ensure_ascii=False, indent=4)

