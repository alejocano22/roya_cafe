date = historial[0]["time"].toString();
n =  Object.keys(historial).length;

let chartGeneral = new Chart("Datos Generales","button-b","Gráfico de datos")
chartGeneral.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Día');
    data.addColumn('number', 'Temperatura');
    data.addColumn('number','Humedad');
    data.addColumn('number','Ph');
    data.addColumn('number','iluminance');
    data.addColumn('number','Etapa roya');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["env_temperature"].toString());
        data.setCell(i, 2, historial[i]["env_humidity"].toString());
        data.setCell(i, 3, historial[i]["ph"].toString());
        data.setCell(i, 4, historial[i]["iluminance"].toString());
        data.setCell(i, 5, historial[i]["etapa"].toString());
    }
    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartGeneral.options);
}
let chartEtapa = new Chart("Etapa del hongo","button-c","Etapa vs Tiempo")
chartEtapa.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Día');
    data.addColumn('number','Etapa roya');

    data.addRows(n);
    for (var i = 0; i<n;i++) {
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["etapa"].toString());
    }
    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartEtapa.options);
}

let chartTemperatura= new Chart("Temperatura","button-d","Temperatura Vs tiempo")
chartTemperatura.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();

    data.addColumn('string', 'Día');
    data.addColumn('number', 'Temperatura');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["env_temperature"].toString());
    }
    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartTemperatura.options);
}

let chartHumedad= new Chart("Humedad","button-e","Humedad vs Tiempo")
chartHumedad.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Día');
    data.addColumn('number','Humedad');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["env_humidity"].toString());
    }
    // Instantiate and draw the chart.
    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartHumedad.options);
}

let chartPh= new Chart("Ph","button-f","Ph vs Tiempo")
chartPh.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Día');
    data.addColumn('number','ph');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["ph"].toString());
    }

    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartPh.options);
}

let chartLuminosidad= new Chart("Luminosidad","button-g","Luminosidad vs Tiempo")
chartLuminosidad.boton.onclick = function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Día');
    data.addColumn('number','iluminance');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["iluminance"].toString());
    }

    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartLuminosidad.options);
}

