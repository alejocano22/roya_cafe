let canva_lote = new Canvas('canva_lote');
var X = canva_lote.c.width / 2;
var Y = canva_lote.c.height / 2;
var R = 45;
pintarCanvaLote();

function pintarCanvaLote(){
    canva_lote.ctx.beginPath();
    canva_lote.ctx.arc(X, Y, R, 0, 2 * Math.PI, false);
    canva_lote.ctx.fillStyle = canva_lote.colores[parseInt(etapa)];
    canva_lote.ctx.fill();
    canva_lote.ctx.lineWidth = 3;
    canva_lote.ctx.strokeStyle = '#000000';
    canva_lote.ctx.stroke();

}
