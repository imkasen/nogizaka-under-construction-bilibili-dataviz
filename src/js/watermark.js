export function getWaterMark() {
    let waterMarkText = 'github.com/imkasen';
    let watermark_canvas = document.createElement('canvas');
    let ctx = watermark_canvas.getContext('2d');
    watermark_canvas.width = 100;
    watermark_canvas.height = 100;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.globalAlpha = 0.1;
    ctx.font = '12px Microsoft Yahei';
    ctx.translate(50, 50);
    ctx.rotate(-Math.PI / 4);
    ctx.fillText(waterMarkText, 0, 0);

    return watermark_canvas;
}

