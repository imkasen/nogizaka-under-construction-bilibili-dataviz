"use strict";

// container1/2/3，drawChart1/2/3
// 这命名确实有点糟糕，
// 不过总共也就 3 个，那就懒得改了...
// 1 - 天翼羽魂
// 2 - 千葉幽羽
// 3 - 词云图

import {drawChart} from "./container.js";
import {drawChart2} from "./container2.js";
import {drawChart3} from "./container3.js";

let urls = [
    'resources/bv_info.json',
    'resources/bv_info2.json',
];

async function fetchURLs() {
    try {
        return await Promise.allSettled(
            urls.map(
                (url) => fetch(url)
                    .then((res) => res.json())
            )
        );
        // return await Promise.all([
        //     fetch('resources/bv_info.json')
        //         .then((res) => res.json()),
        //     fetch('resources/bv_info2.json')
        //         .then((res) => res.json()),
        // ]);
    } catch (error) {
        console.log(error);
    }
}

fetchURLs().then((bv_data) => {
    // Promise.all
    // drawChart(data[0]);
    // drawChart2(data[1]);

    // Promise.allSettled
    if (bv_data[0].status === "fulfilled") {
        drawChart(bv_data[0].value);
    } else {
        // rejected
        console.log(bv_data[0].reason);
    }
    if (bv_data[1].status === "fulfilled") {
        drawChart2(bv_data[1].value);
    } else {
        // rejected
        console.log(bv_data[1].reason);
    }

    // latest ep number
    return bv_data[0].value.length + bv_data[1].value.length - 6;
}).then((ep_num) => {
    // get danmaku data
    // return fetch(`resources/danmaku/EP${ep_num}.json`)
    //    .then(res => res.json());
    return fetch(`resources/danmaku.json`)
       .then(res => res.json());
}).then((danmaku_data) => {
    $('.wordcloud_title').html(danmaku_data[0]); // 插入标题
    drawChart3(danmaku_data[1]);
});
