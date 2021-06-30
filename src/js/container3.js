// 最近一次 EP 的弹幕词语图可视化
"use strict";

let myChart = echarts.init(document.getElementById('container3'));
myChart.showLoading();

export function drawChart3(data) {
    myChart.hideLoading();

    let keywords_data = [];
    for (let name in data) {
        keywords_data.push({
            name: name,
            value: data[name],
        });
    }

    let maskImage = new Image();

    let option = {
        series: [{
            type: 'wordCloud',
            shape: 'circle',
            // left: 'center',
            // top: 'center',
            width: '100%',
            height: '100%',
            // right: null,
            // bottom: null,
            sizeRange: [10, 150],
            rotationRange: [-45, 45],
            rotationStep: 45,
            gridSize: 5,
            drawOutOfBound: false,
            layoutAnimation: true,
            textStyle: {
                // fontFamily: 'Noto Sans SC',
                // fontWeight: 'bold',
                color: function () {
                    // Random color
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                focus: 'self',
                textStyle: {
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            data: keywords_data.sort(function (a, b) {
                return b.value - a.value;
            })
        }],
    };

    myChart.setOption(option);

    window.addEventListener('resize', function () {
        myChart.resize();
    })
}
