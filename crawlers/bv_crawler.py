#!/usr/bin/env python3

# 一个简单的爬虫，用于获得 “乃木板工事中” 的各个视频信息

import requests
import json
import time
import math
import re

id_tyyh = "2301165"  # 天翼羽魂 id
search_keyword1 = "乃木坂工事中 EP 不够热"
search_keyword2 = "乃木坂工事中 坂道之诗"

id_qyyy = "19553445"  # 千葉幽羽 id
search_keyword3 = "乃木坂工事中 EP 上行之坂"

# 请求 URL
url = "https://api.bilibili.com/x/space/arc/search"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36"
}

# 代理
# proxies = {
#     "http": ""
# }


def get_response(mid: str, page_number: int, keyword: str) -> json:
    """
    获得相应内容。
    :param mid: 用户 ID
    :param page_number: 当前页面号
    :param keyword: 搜索关键词
    :return: json
    """
    params = {
        "mid": mid,              # 用户 ID
        "ps": "30",              # 每一页显示的视频数量
        "tid": "0",              # 视频分区
        "pn": str(page_number),  # 第几页
        "keyword": keyword,      # 搜索关键词
        "order": "pubdate",      # 按发布日期排序
        "jsonp": "jsonp"
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        # proxies=proxies,
        timeout=5
    )

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        response.raise_for_status()


def get_total_page_number(mid: str, keyword: str) -> int:
    """
    获得关键词所对应的搜索结果页面总数。
    :param mid: 用户 ID
    :param keyword: 搜索关键词
    :return: int
    """
    page_result = get_response(mid, 1, keyword)
    return math.ceil(page_result['data']['page']['count'] / page_result['data']['page']['ps'])


def collect_bv_info(mid: str, keyword: str, ep_list: list) -> None:
    """
    过滤整理每个视频的信息并保存在列表中。
    :param mid: 用户 ID
    :param keyword: 搜索关键词
    :param ep_list: 用于保存信息
    :return: None
    """
    for page_num in reversed(range(1, get_total_page_number(mid, keyword) + 1)):  # 用 reversed() 是因为最新的 ep 出现在最前，所以使用倒序，即从 ep1 开始，下面同理
        results = get_response(mid, page_num, keyword)
        
        # 尝试解决 KeyError: 'data' 错误：
        # 原因应该是请求太快引发的，
        # response status code 应该还是 200，得到的也还是 json
        if not 'data' in results:
            time.sleep(30)  # 人为等待 30s
            results = get_response(mid, page_num, keyword)  # 再次请求

        for bv_info in reversed(results['data']['list']['vlist']):

            video_bvid = str(bv_info['bvid'])                                                             # BV 号
            video_title = bv_info['title']                                                                # 标题
            video_ep = video_title[int(video_title.find('EP')):int(video_title.find('EP')) + 5].rstrip()  # EP
            video_created_time = time.strftime("%Y %b %d, %a", time.localtime(bv_info['created']))        # 投稿时间
            video_play = bv_info['play']                                                                  # 播放数量
            video_comment = bv_info['comment']                                                            # 评论数量
            video_danmaku = bv_info['video_review']                                                       # 弹幕数量

            # 跳过 "NOGIROOM"，"NOGIBINGO"，"乃木坂在哪儿"
            excluded_title_list = ["NOGI", "在哪"]
            if any([title in video_title for title in excluded_title_list]):
                continue

            # 精简标题
            reg_str = '(【.*?】)|(EP[0-9]+[ ]?)|([，]?乃木坂工事中[ ]?)|([，]?[0-9]{6})'
            video_title = re.sub(reg_str, '', video_title).strip()

            if video_ep == "":
                video_ep = "EP86.5"      # 【乃木坂工事中SP】161229 乃木坂46&欅坂46共同大年会
            if video_ep == "EP04【":
                video_ep = video_ep[:4]  # EP04【乃木坂不够热】提取问题
            if video_play == "--":
                video_play = None        # 【乃木坂工事中】EP40 无播放数据

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


def main() -> None:
    bv_lists = []
    bv_lists2 = []
    # 天翼羽魂
    # 获取关键词 "乃木坂工事中 EP 不够热" 下的每个页面内容并整合
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
        "Title": "生驹里奈毕业演唱会特集",
        "Time": None,
        "Play": None,
        "Comment": None,
        "Danmaku": None,
    })

    # 千葉幽羽
    # 获取关键词 "乃木坂工事中 EP 上行之坂" 下的每个页面内容并整合
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


if __name__ == '__main__':
    main()
