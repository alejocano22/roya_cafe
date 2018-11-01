class Chart {
    constructor(titlevAxis,id,title) {
        this.boton = document.getElementById(id);
        this.options = {title : title,
            hAxis: {
                title: 'Fecha de Toma'
            },
            vAxis: {
                title: titlevAxis
            },
            curveType: 'function'
        };
    }
}