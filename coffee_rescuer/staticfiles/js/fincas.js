function pintarCanvaFinca(canva_finca,prom) {
    var X = canva_finca.c.width / 2;
    var Y = canva_finca.c.height / 2;
    var R = 40;
    canva_finca.ctx.beginPath();
    canva_finca.ctx.arc(X, Y+6, R, 0, 2 * Math.PI, false);

    canva_finca.ctx.fillStyle = canva_finca.colores[parseInt(prom)];
    canva_finca.ctx.fill();
    canva_finca.ctx.lineWidth = 3;
    canva_finca.ctx.strokeStyle = '#000000';
    canva_finca.ctx.stroke();
}

fincas = JSON.parse(jsonContextoFincas);

for (var i = 0; i < Object.keys(fincas).length; i++) {
    var id = fincas[i]["pk"];

    var prom = fincas[i]["fields"]["promedio_estado_lotes"];
    let canva_finca = new Canvas('circle_finca_' + id);
    pintarCanvaFinca(canva_finca,prom)
}