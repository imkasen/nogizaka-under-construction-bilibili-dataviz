// 最近一次 EP 的弹幕词语图可视化
"use strict";

let myChart = echarts.init(document.getElementById('container3'));
myChart.showLoading();

export function drawChart3(data) {
    myChart.hideLoading();

    console.log(data);

    let option = {};

    myChart.setOption(option);
}
