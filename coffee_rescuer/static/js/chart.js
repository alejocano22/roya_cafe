class Chart {
    constructor(titlevAxis,id,title) {
        this.boton = document.getElementById(id);
        this.options = {'title' : title,
            hAxis: {
                title: 'Fecha de Toma'
            },
            vAxis: {
                title: titlevAxis
            },
            'width':1000,
            'height':400,
            curveType: 'function'
        };
    }
}