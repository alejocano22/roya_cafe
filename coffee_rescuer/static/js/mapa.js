

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
        var x = informacion.coordenadas[pk].x;
        var w = informacion.coordenadas[pk].w;
        var y = informacion.coordenadas[pk].y;
        var h = informacion.coordenadas[pk].h;


        canva_mapa.ctx.fillStyle = canva_mapa.colores[informacion.etapas[pk]];
        canva_mapa.ctx.fillRect(x, y, w, h);
         //Para hacerle un borde
        canva_mapa.ctx.fillStyle = "#000000";
        canva_mapa.ctx.rect( x,y, w, h);

        canva_mapa.ctx.rect((x + 1),
                            (y + 1),
                            (w - 1),
                            (h - 1));

        canva_mapa.ctx.font = "20px Arial";

        if (informacion.lotes[i]["fields"]["nombre"] != null) {
            canva_mapa.ctx.fillText(informacion.lotes[i]["fields"]["nombre"], x + w/4 , y + 5 +h/2);
        } else {
            canva_mapa.ctx.fillText(pk, x + w/4 ,y + 5 + h/2    );
            canva_mapa.ctx.stroke();
        }
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
        if(posx <= x+w && posx >= x && posy <= y+h && posy >=y){

            f(i);
        }

    }
}

let canva_mapa = new Canvas("canva_mapa");
ancho_actual = document.getElementById('canva_mapa').offsetWidth;
alto_actual = document.getElementById('canva_mapa').offsetHeight;
canva_mapa.c.width = 1000;
canva_mapa.c.height = 1000;
let informacion =  new Informacion(jsonContextoCoordenadas,jsonContextoEtapas,jsonContextoLotes);
pintarMapa();

var posx;
var posy;
canva_mapa.c.addEventListener("click",handleClick);


let canva_finca = new Canvas('circle_finca');
pintarCanvaFinca();

