"use strict";

// bv_info2.json
// 千葉幽羽部分可视化

export function drawChart2(data) {

  const { Line } = G2Plot;

  const line = new Line('container2', {
    data: data,
    padding: 'auto',
    xField: 'EP',
    yField: 'Play',
    connectNulls: false,
    point: {
      size: 3,
      style: {
        fill: 'white',
        stroke: 'purple',
        lineWidth: 2,
      },
    },
    slider: {
      start: 0.0,
      end: 0.5,
    },
  });

  line.render();
}

