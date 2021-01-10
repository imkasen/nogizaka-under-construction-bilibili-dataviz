// 千葉幽羽部分可视化
"use strict";

let myChart = echarts.init(document.getElementById('container2'));
myChart.showLoading();

export function drawChart2(data) {
  myChart.hideLoading();
  console.log(data);

  let option = {
    title: {
      text: "【乃木坂工事中】数据",
      left: 'center',
    },
    tooltip: {},
    toolbox: {
      right: '10%',
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
    legend: {},
    dataset: {
      source: data,
    },
    xAxis: {
      name: "期数",
      type: 'category',
    },
    yAxis: {
      name: "播放量",
      type: 'value',
    },
    series: [
      {
        type: 'line',
        encode: {
          x: "EP",
          y: "Play",
        },
      },
    ],
  };

  myChart.setOption(option);
}

