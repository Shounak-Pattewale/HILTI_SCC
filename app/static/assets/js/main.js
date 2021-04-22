var df = []
data.forEach(function(d) {
    df[0] = d['Air temp']
    df[1] = d['Process temp']
    df[2] = d['Rpm']
    df[3] = d['Torque']
    df[4] = d['Tool wear']
});

am4core.ready(function () {
    console.log("1")

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chartdiv", am4charts.XYChart);

    chart.data = [{
        "country": "Air Temperature",
        "visits": df[0]
    }, {
        "country": "Process Temperature",
        "visits": df[1]
    }, {
        "country": "RPM",
        "visits": df[2]
    }, {
        "country": "Torque",
        "visits": df[3]
    }, {
        "country": "Tool Wear",
        "visits": df[4]
    }];

    console.log(2)


chart.padding(40, 40, 40, 40);

var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.dataFields.category = "country";
categoryAxis.renderer.minGridDistance = 60;
categoryAxis.renderer.inversed = true;
categoryAxis.renderer.grid.template.disabled = true;

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.min = 0;
valueAxis.extraMax = 0.1;
//valueAxis.rangeChangeEasing = am4core.ease.linear;
//valueAxis.rangeChangeDuration = 1500;

var series = chart.series.push(new am4charts.ColumnSeries());
series.dataFields.categoryX = "country";
series.dataFields.valueY = "visits";
series.tooltipText = "{valueY.value}"
series.columns.template.strokeOpacity = 0;
series.columns.template.column.cornerRadiusTopRight = 10;
series.columns.template.column.cornerRadiusTopLeft = 10;
//series.interpolationDuration = 1500;
//series.interpolationEasing = am4core.ease.linear;
var labelBullet = series.bullets.push(new am4charts.LabelBullet());
labelBullet.label.verticalCenter = "bottom";
labelBullet.label.dy = -10;
labelBullet.label.text = "{values.valueY.workingValue.formatNumber('#.')}";

chart.zoomOutButton.disabled = true;

// as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
series.columns.template.adapter.add("fill", function (fill, target) {
    return chart.colors.getIndex(target.dataItem.index);
});
console.log(3)

$(document).ready(function () {
        var socket = io.connect('http://127.0.0.1:5000');
        console.log("Here : ", socket)
        socket.on('connect', function () {
            var r = 0
            setInterval(function () {
                var msg = [df[1][r++], df[2][r++], df[3][r++], df[4][r++]];

                chart.data[0]['visits'] = df[0][r++]
                chart.data[1]['visits'] = df[1][r++]
                chart.data[2]['visits'] = df[2][r++]
                chart.data[3]['visits'] = df[3][r++]
                chart.data[4]['visits'] = df[4][r++]

                chart.invalidateRawData();
                console.log('before socket call')
                socket.send(msg);
            }, 2000)
        });
    });

categoryAxis.sortBySeries = series;

}); // end am4core.ready()