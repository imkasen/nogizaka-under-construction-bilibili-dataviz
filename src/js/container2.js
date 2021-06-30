// 千葉幽羽部分可视化
"use strict";

import {getWaterMark} from "./watermark.js";

// 纵坐标分割线设置
let div_num = 5;
// 播放数
let max_play = 200000;
let interval_play = max_play / div_num;
// 弹幕数
let max_danmaku = 6000;
let interval_danmaku = max_danmaku / div_num;
// 评论数
let max_comment = 1000;
let interval_comment = max_comment / div_num;

// 初始化 ECharts
let myChart = echarts.init(document.getElementById('container2'));
myChart.showLoading();

// 配置 ECharts
export function drawChart2(data) {
    myChart.hideLoading();

    let option = {
        aria: { // 无障碍访问
            enabled: true,
        },
        title: { // 标题
            text: "「乃木坂工事中」千葉幽羽部分视频数据（上行之坂）",
            subtext: "2018 年 12 月 ~ 至今",
            left: 'center',
        },
        tooltip: { // 提示框
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
            },
            formatter: function (params) { // 自定义
                /*
                * 注意：
                * params[0] 对应 series[0]，以此类推。
                * 因为 series[0] 用了 data，
                * 而 series[1|2] 用了 encode，
                * 所以 params[0].value 返回 number，
                * 而 params[1|2].value 返回 object。
                */

                let htmlStr = '';

                htmlStr += params[1].name + "</br>"; // EP 数，与 X 轴相同
                htmlStr += params[1].value['Title'] + "</br>"; // 标题
                // htmlStr += params[1].value['Time'] + "</br>"; // 投稿时间

                params.forEach((param) => {
                    htmlStr += param.marker + " " + param.seriesName + " : ";
                    if (param.value.constructor === Object) {
                        let param_key = Object.keys(param.value)[param.encode['y'][0]];
                        htmlStr += param.value[param_key];
                    }
                    else {
                        htmlStr += param.value;
                    }
                    htmlStr += "</br>";
                });

                return htmlStr;
            }
        },
        toolbox: { // 工具栏
            right: '11%',
            feature: {
                dataView: {
                    readOnly: true,
                },
                magicType: {
                    type: ['line', 'bar'],
                },
                saveAsImage: {
                    // name: "「乃木坂工事中」千葉幽羽部分视频数据（上行之坂）",
                    pixelRatio: 1,
                    backgroundColor: { // 下载水印
                        type: 'pattern',
                        image: getWaterMark(),
                        repeat: 'repeat',
                    },
                },
                restore: {},
            },
        },
        grid: { // 直角坐标系
            right: '10%',
            // containLabel: true,
        },
        legend: { // 图例
            left: '10%',
            data: ["播放次数", "弹幕数量", "评论数量"],
        },
        dataset: { // 数据集
            source: data,
        },
        calculable: true,
        xAxis: { // X 轴设置
            // name: "期数",
            type: 'category',
            axisTick: {
                alignWithLabel: true, // 刻度线与标签对齐
            },
            axisPointer: {
                type: 'shadow',
            },
        },
        yAxis: [ // Y 轴设置
            {
                name: "播放数",
                type: 'value',
                min: 0,
                max: max_play,
                interval: interval_play,
                position: 'left',
                axisLine: {
                    show: true, // 显示轴线
                },
                axisLabel: {
                    formatter: function (value) {
                        value = +value;
                        return isFinite(value) ? echarts.format.addCommas(+value / 1000) + 'K' : '';
                    }
                },
            },
            {
                name: "弹幕数",
                type: 'value',
                min: 0,
                max: max_danmaku,
                interval: interval_danmaku,
                position: 'right',
                axisLine: {
                    show: true,
                },
            },
            {
                name: "评论数",
                type: 'value',
                min: 0,
                max: max_comment,
                interval: interval_comment,
                position: 'right',
                offset: 70,
                axisLine: {
                    show: true,
                },
            },
        ],
        dataZoom: [ // 缩放
            {
                type: 'slider',
                show: true,
                start: 85,
                end: 100,
            },
            // {
            //     type: 'inside',
            //     show: true,
            //     start: 0,
            //     end: 25,
            // }
        ],
        series: [
            {
                name: '播放次数',
                type: 'line',
                yAxisIndex: 0,
                // encode: {
                //   x: "EP",
                //   y: "Play",
                // },
                data: data.map(function (item) {
                    return item["Play"];
                }),
                itemStyle: {  // 折线拐点样式
                    color: '#BA55D3',
                },
                lineStyle: { // 折线样式
                    color: { // 渐变色
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            {
                                offset: 0, color: '#8700b3', // 顶部颜色
                            },
                            {
                                offset: 0.5, color: '#BA55D3',
                            },
                            {
                                offset: 1, color: '#fbccff', // 底部颜色
                            }
                        ],
                        global: false,
                    },
                },
                markLine: {
                    data: [
                        { // 中位数标线
                            type: 'median',
                            name: "中位数",
                            label: {
                                position: 'start',
                                formatter: "中位播放数",
                            },
                            lineStyle: {
                                color: '#00B2EE',
                            },
                        },
                        [ // 最大值标线
                            { // 起点
                                symbol: 'circle',
                                x: '10%',
                                yAxis: 'max',
                                label: {
                                    position: 'start',
                                    formatter: "最多播放",
                                },
                            },
                            { // 终点
                                type: 'max',
                                name: "最高点",
                                symbol: 'none',
                                lineStyle: {
                                    color: '#00B2EE',
                                },
                            },
                        ],
                    ],
                },
            },
            {
                name: '弹幕数量',
                type: 'bar',
                yAxisIndex: 1,
                encode: {
                    x: "EP",
                    y: "Danmaku",
                },
                itemStyle: {
                    color: '#66CD00',
                },
                markPoint: { // 最大值标点
                    symbolSize: 35,
                    data: [
                        {
                            type: 'max',
                            name: '最多弹幕数',
                        },
                    ],
                },
            },
            {
                name: '评论数量',
                type: 'bar',
                yAxisIndex: 2,
                encode: {
                    x: "EP",
                    y: "Comment",
                },
                itemStyle: {
                    color: '#EEC900',
                },
                markPoint: { // 最大值标点
                    symbolSize: 35,
                    data: [
                        {
                            type: 'max',
                            name: '最多评论数',
                        },
                    ],
                },
            },
        ],
    };

    // 显示图表
    myChart.setOption(option);

    // 图表形状随浏览器窗口变化而变化
    window.addEventListener('resize', function () {
        myChart.resize();
    })

    // 点击事件
    myChart.on('click', function (params) {
        // 点击折线拐点，柱状图跳转至相关网页
        let url = "https://www.bilibili.com/video/";
        if (params.componentType === "series"){
            if (params.seriesType === "bar") {
                let bv_id = params.data["BV"];
                window.open(url + bv_id);
            }
            else if (params.seriesType === "line") {
                let index = params.dataIndex;
                let bv_id = data.map((item) => {return item["BV"];})[index];
                window.open(url + bv_id);
            }
        }
    });
}

