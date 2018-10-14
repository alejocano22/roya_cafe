

class Informacion{
    constructor(jsonContextoCoordenadas,jsonContextoEtapas,jsonContextoLotes){
        this.coordenadas = JSON.parse(jsonContextoCoordenadas);
        this.etapas = JSON.parse(jsonContextoEtapas);
        this.lotes = JSON.parse(jsonContextoLotes);

    }
}



function pintarMapa() {
    for (var i = 0; i < Object.keys(informacion.coordenadas).length; i++) {
        var pk = informacion.lotes[i]["pk"];
        canva_mapa.ctx.fillStyle = canva_mapa.colores[informacion.etapas[pk]];
        canva_mapa.ctx.fillRect(informacion.coordenadas[pk].x, informacion.coordenadas[pk].y, informacion.coordenadas[pk].w, informacion.coordenadas[pk].h);
        canva_mapa.ctx.fillStyle = "#000000";
        canva_mapa.ctx.rect(informacion.coordenadas[pk].x, informacion.coordenadas[pk].y, informacion.coordenadas[pk].w, informacion.coordenadas[pk].h);
        canva_mapa.ctx.rect(informacion.coordenadas[pk].x + 1, informacion.coordenadas[pk].y + 1, informacion.coordenadas[pk].w - 1, informacion.coordenadas[pk].h - 1);
        canva_mapa.ctx.font = "20px Arial";
        if (informacion.lotes[i]["fields"]["nombre"] != null) {
            canva_mapa.ctx.fillText(informacion.lotes[i]["fields"]["nombre"], informacion.coordenadas[pk].x + 10, informacion.coordenadas[pk].y +50);
        } else {
            canva_mapa.ctx.fillText(pk, informacion.coordenadas[pk].x +10, informacion.coordenadas[pk].y + 50);
        }

        canva_mapa.ctx.stroke();
    }
}

function pintarCanvaFinca() {
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

function getMousePos(c,evt){

    var rect = c.getBoundingClientRect();
    return {
        x: evt.clientX,
        y: evt.clientY
    }
}

function handleClick(e){

    var pos = getMousePos(canva_mapa.c,e);
    var canva = canva_mapa.c.getBoundingClientRect();
    posx = pos.x - canva.left;
    posy = pos.y - canva.top;

    for (var i in informacion.coordenadas){
        var x = informacion.coordenadas[i].x;
        var y = informacion.coordenadas[i].y;
        var w = informacion.coordenadas[i].w;
        var h = informacion.coordenadas[i].h;
        if(posx<=x+w&&posx>=x&&posy<=y+h&&posy>=y){

            var win = window.open("http://127.0.0.1:8000/lote/"+i);
            win.focus();

        }

    }
}

let canva_mapa = new Canvas("canva_mapa");
canva_mapa.c.width = 1000;
canva_mapa.c.height = 500;

let informacion =  new Informacion(jsonContextoCoordenadas,jsonContextoEtapas,jsonContextoLotes);
pintarMapa();

var posx;
var posy;
canva_mapa.c.addEventListener("click",handleClick);


let canva_finca = new Canvas('circle_finca');
pintarCanvaFinca();

