# 获得视频的 BV 号

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

params = {
    "mid": id_tyyh,
    "ps": "30",
    "tid": "0",
    "pn": "1",
    "keyword": search_keyword1,
    "order": "pubdate",
    "jsonp": "jsonp"
}

proxies = {
     "http": "115.221.246.148:9999"
}

response = requests.get(
    url=url,
    headers=headers,
    params=params,
    proxies=proxies
)

results = response.json()
total_page_num = int(results['data']['page']['count'] / results['data']['page']['ps'] + 1)
print(total_page_num)

bv_dict = {}
for bv_info in reversed(results['data']['list']['vlist']):

    video_bvid = str(bv_info['bvid'])                                       # bvid
    video_title = bv_info['title']                                          # 标题
    video_ep = video_title.split()[0].split('】')[1]                         # EP
    video_created_time = time.asctime(time.localtime(bv_info['created']))   # 投稿时间
    video_play = str(bv_info['play'])                                       # 播放数量
    video_comment = str(bv_info['comment'])                                 # 评论数量
    video_danmaku = str(bv_info['video_review'])                            # 弹幕数量

    # 例子：
    # {'BV1vt411k7At': ['EP187', '【乃木坂工事中】EP187 一期生四人联合毕业式【坂道之诗】', 'Mon Dec 24 07:54:13 2018', '96786', '684', '2578']}
    bv_dict[video_bvid] = [video_ep, video_title, video_created_time, video_play, video_comment, video_danmaku]


print(bv_dict)

with open('resources/bv_info.json', 'w') as bv_file:
    json.dump(bv_dict, bv_file, ensure_ascii=False, indent=2)

