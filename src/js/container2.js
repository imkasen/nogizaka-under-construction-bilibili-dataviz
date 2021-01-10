// 千葉幽羽部分可视化
"use strict";

let myChart = echarts.init(document.getElementById('container2'));
myChart.showLoading();

export function drawChart2(data) {
  myChart.hideLoading();

  let option = {
    title: { // 标题组件
      text: "【乃木坂工事中】千葉幽羽部分数据",
      subtext: "2018 年底 ~ 现在",
      left: 'center',
    },
    tooltip: { // 提示框
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    toolbox: { // 工具栏
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
    grid: { // 直角坐标系
      right: '10%',
      // containLabel: true,
    },
    legend: { // 图例
      right: '20%',
      data: ["播放次数", "弹幕数量", "评论数量"],
    },
    dataset: { // 数据集
      source: data,
    },
    calculable: true,
    xAxis: { // X 轴
      // name: "期数",
      type: 'category',
      axisTick: {
        alignWithLabel: true, // 刻度线与标签对齐
      },
      axisPointer: {
        type: 'shadow',
      },
    },
    yAxis: [ // Y 轴
      {
        name: "播放数",
        type: 'value',
        min: 0,
        max: 200000,
        interval: 40000, // (max - min) / interval = 5
        position: 'left',
        axisLine: {
          show: true, // 显示轴线
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
    dataZoom: [ // 缩放
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
        markLine: {
          data: [
            { // 中位数标线
              type: 'median',
              name: "中位数",
              label: {
                position: 'start',
                formatter: "中位数",
              },
            },
            [ // 最大值标线
              { // 起点
                symbol: 'none',
                x: '10%',
                yAxis: 'max',
              },
              { // 终点
                type: 'max',
                name: "最高点",
                symbol: 'circle',
                label: {
                  position: 'end',
                  formatter: "最大值",
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

  myChart.setOption(option);
}

