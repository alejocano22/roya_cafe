date = historial[0]["time"].toString();
n =  Object.keys(historial).length;
google.charts.load('current', {packages: ['corechart', 'line']});
var funcionActual;
let chartGeneral = new Chart("Datos Generales","button-b","Gráfico de datos");
function drawChartGeneral() {
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
        data.setCell(i, 4, historial[i]["illuminance"].toString());
        data.setCell(i, 5, historial[i]["etapa"].toString());
    }
    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartGeneral.options);
    funcionActual = drawChartGeneral;
}
google.charts.setOnLoadCallback(drawChartGeneral);
chartGeneral.boton.onclick = drawChartGeneral;

let chartEtapa = new Chart("Etapa del hongo","button-c","Etapa vs Tiempo")
function drawChartEtapa() {
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
    funcionActual = drawChartEtapa;
}
chartEtapa.boton.onclick = drawChartEtapa;


let chartTemperatura= new Chart("Temperatura","button-d","Temperatura Vs tiempo")
function drawChartTemperatura() {
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
    funcionActual = drawChartTemperatura;
}
chartTemperatura.boton.onclick = drawChartTemperatura;


let chartHumedad= new Chart("Humedad","button-e","Humedad vs Tiempo")
function drawChartHumedad() {
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
    funcionActual = drawChartHumedad;
}
chartHumedad.boton.onclick = drawChartHumedad;


let chartPh= new Chart("Ph","button-f","Ph vs Tiempo")
function drawChartPh() {
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
    funcionActual = drawChartPh;
}
chartPh.boton.onclick = drawChartPh;


let chartLuminosidad= new Chart("Luminosidad","button-g","Luminosidad vs Tiempo")
function drawChartLuminosidad() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Día');
    data.addColumn('number','illuminance');

    data.addRows(n);
    for (var i = 0; i<n;i++){
        data.setCell(i, 0, historial[i]["time"].toString());
        data.setCell(i, 1, historial[i]["illuminance"].toString());
    }

    var chart = new google.visualization.LineChart(document.getElementById('container1'));
    chart.draw(data, chartLuminosidad.options);
    funcionActual = drawChartLuminosidad;
}
chartLuminosidad.boton.onclick = drawChartLuminosidad;


$(window).resize(function(){
  funcionActual();
});
