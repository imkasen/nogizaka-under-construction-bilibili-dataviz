#!/usr/bin/env python3

# 一个简单的爬虫，用于获得 “乃木板工事中” 的各个视频信息

import requests
import json
import time

id_tyyh = "2301165"  # 天翼羽魂 id
search_keyword1 = "乃木坂工事中 不够热"
search_keyword2 = "乃木坂工事中 坂道之诗"

id_qyyy = "19553445"  # 千葉幽羽 id
search_keyword3 = "乃木坂工事中 上行之坂"

# 请求 URL
url = "https://api.bilibili.com/x/space/arc/search"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36"
}

# 代理
proxies = {
    "http": "http://120.232.175.244:80"
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


def collect_bv_info(mid, keyword, ep_list):
    """
    refilter the information of each video and store it into the list.
    :param mid: user id
    :param keyword: search keyword
    :param ep_list: to store the information
    :return: None
    """
    for page_num in reversed(range(1, get_total_page_number(mid, keyword) + 1)):
        results = get_response(mid, page_num, keyword)

        for bv_info in reversed(results['data']['list']['vlist']):

            video_bvid = str(bv_info['bvid'])                                                             # BV 号
            video_title = bv_info['title']                                                                # 标题
            video_ep = video_title[int(video_title.find('EP')):int(video_title.find('EP')) + 5].rstrip()  # EP
            video_created_time = time.strftime("%Y %b %d, %a", time.localtime(bv_info['created']))        # 投稿时间
            video_play = bv_info['play']                                                                  # 播放数量
            video_comment = bv_info['comment']                                                            # 评论数量
            video_danmaku = bv_info['video_review']                                                       # 弹幕数量

            if video_ep == "":
                if video_bvid == "BV1Ts411D7bN":  # 跳过 "乃木坂在哪完结篇"
                    continue
                else:
                    video_ep = "EP86.5"  # 【乃木坂工事中SP】161229 乃木坂46&欅坂46共同大年会
            if video_ep == "EP04【":
                video_ep = video_ep[:4]  # EP04【乃木坂不够热】提取问题
            if video_play == "--":
                video_play = None    # 【乃木坂工事中】EP40 无播放数据

            video_index = float(video_ep[2:6])                                                            # 序号

            # 例子：
            # {
            #     {
            #         "Index": 1.0,
            #         "EP": "EP01",
            #         "BV": "BV1ss411D7X5",
            #         "Title": "【乃木坂】新番组！乃木坂工事中 EP01 成员提供的有关于西野七濑的情报",
            #         "Time": "2015 Apr 21, Tue",
            #         "Play": 106435,
            #         "Comment": 74,
            #         "Danmaku": 1607
            #     },
            #     ...
            # }
            ep_list.append({
                "Index": video_index,
                "EP": video_ep,
                "BV": video_bvid,
                "Title": video_title,
                "Time": video_created_time,
                "Play": video_play,
                "Comment": video_comment,
                "Danmaku": video_danmaku,
            })


bv_lists = []
bv_lists2 = []
# 天翼羽魂
# 获取关键词 "乃木坂工事中 不够热" 下的每个页面内容并整合
collect_bv_info(id_tyyh, search_keyword1, bv_lists)

# 手动删除
del bv_lists[93]  # "EP103"，下个关键词再添加

# 获取关键词 "乃木坂工事中 坂道之诗" 下的每个页面内容并整合
# 注意：缺少 EP154 生驹里奈毕业演唱会特集
collect_bv_info(id_tyyh, search_keyword2, bv_lists)
bv_lists.append({
    "Index": 154.0,
    "EP": "EP154",
    "BV": "",
    "Title": "【乃木坂工事中】EP154 生驹里奈毕业演唱会特集【坂道之诗】",
    "Time": None,
    "Play": None,
    "Comment": None,
    "Danmaku": None,
})

# 千葉幽羽
# 获取关键词 "乃木坂工事中 上行之坂" 下的每个页面内容并整合
# 注意：EP183 - EP187 重复，但仍然保留数据
collect_bv_info(id_qyyy, search_keyword3, bv_lists2)

# 按序号排序
bv_lists.sort(key=lambda k: k.get("Index"))
bv_lists2.sort(key=lambda k: k.get("Index"))

# 天翼羽魂部分写入 'bv_info.json'
with open('resources/bv_info.json', 'w') as bv_file:
    json.dump(bv_lists, bv_file, ensure_ascii=False, indent=4)

# 千葉幽羽部分写入 'bv_info2.json'
with open('resources/bv_info2.json', 'w') as bv_file2:
    json.dump(bv_lists2, bv_file2, ensure_ascii=False, indent=4)

