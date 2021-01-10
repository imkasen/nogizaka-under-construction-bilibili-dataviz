// 天翼羽魂部分可视化
"use strict";

let myChart = echarts.init(document.getElementById('container'));
myChart.showLoading();

export function drawChart(data) {
  myChart.hideLoading();
  console.log(data);

  let option = {
    title: {
      text: 'EChart 入门示例',
    },
    tooltip: {},
    legend: {
      data: ['销量'],
    },
    xAxis: {
      data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],
    },
    yAxis: {},
    series: [{
      name: '销量',
      type: 'bar',
      data: [5, 20, 36, 10, 10, 20],
    }],
  };

  myChart.setOption(option);
}
