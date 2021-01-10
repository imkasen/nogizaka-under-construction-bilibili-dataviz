// 千葉幽羽部分可视化
"use strict";

let myChart = echarts.init(document.getElementById('container2'));
myChart.showLoading();

export function drawChart2(data) {
  myChart.hideLoading();

  let option = {
    title: {
      text: "【乃木坂工事中】数据",
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    toolbox: {
      right: '7%',
      feature: {
        dataView: {
          readOnly: true,
        },
        magicType: {
          type: ['line', 'bar'],
        },
        saveAsImage: {},
        restore: {},
      },
    },
    grid: {
      right: '10%',
      // containLabel: true,
    },
    legend: {
      right: '20%',
      data: ["播放次数", "弹幕数量", "评论数量"],
    },
    dataset: {
      source: data,
    },
    xAxis: {
      // name: "期数",
      type: 'category',
      axisTick: {
        alignWithLabel: true,
      },
      axisPointer: {
        type: 'shadow',
      },
    },
    yAxis: [
      {
        name: "播放数",
        type: 'value',
        min: 0,
        max: 200000,
        interval: 40000,
        position: 'left',
        axisLine: {
          show: true,
        },
        axisLabel: {
          formatter: function (value) {
            value = +value;
            return isFinite(value) ? echarts.format.addCommas(+value / 1000) + 'K' : '';
          },
        },
      },
      {
        name: "弹幕数",
        type: 'value',
        min: 0,
        max: 6000,
        interval: 1200,
        position: 'right',
        axisLine: {
          show: true,
        },
      },
      {
        name: "评论数",
        type: 'value',
        min: 0,
        max: 1000,
        interval: 200,
        position: 'right',
        offset: 70,
        axisLine: {
          show: true,
        },
      },
    ],
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: 0,
        end: 25,
      },
      {
        type: 'inside',
        show: true,
        start: 0,
        end: 25,
      }
    ],
    series: [
      {
        name: '播放次数',
        type: 'line',
        yAxisIndex: 0,
        encode: {
          x: "EP",
          y: "Play",
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
      },
      {
        name: '评论数量',
        type: 'bar',
        yAxisIndex: 2,
        encode: {
          x: "EP",
          y: "Comment",
        },
      },
    ],
  };

  myChart.setOption(option);
}

