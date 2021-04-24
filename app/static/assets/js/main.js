var df = []
data.forEach(function(d) {
    df[0] = d['Air temp']
    df[1] = d['Process temp']
    df[2] = d['Rpm']
    df[3] = d['Torque']
    df[4] = d['Tool wear']
});

am4core.ready(function () {
    // console.log("1")

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chartdiv", am4charts.XYChart);

    chart.data = [{
        "country": "Air Temperature",
        "visits": df[0][0]
    }, {
        "country": "Process Temperature",
        "visits": df[1][0]
    }, {
        "country": "RPM",
        "visits": df[2][0]
    }, {
        "country": "Torque",
        "visits": df[3][0]
    }, {
        "country": "Tool Wear",
        "visits": df[4][0]
    }];

    // console.log(2)


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
// console.log(3)

$(document).ready(function () {
        var socket = io.connect('http://127.0.0.1:5000');
        // console.log("Here : ", socket)
        socket.on('connect', function () {
            var r = 1
            setInterval(function () {
                if(r>10000) {
                    r = 0
                }
                var msg = [df[1][r], df[2][r], df[3][r], df[4][r]];

        // ##### Main Barchart updation (amCharts) #####
                chart.data[0]['visits'] = df[0][r]
                chart.data[1]['visits'] = df[1][r]
                chart.data[2]['visits'] = df[2][r]
                chart.data[3]['visits'] = df[3][r]
                chart.data[4]['visits'] = df[4][r]
                chart.invalidateRawData();
                // End of Barchart

        // ##### Sending message for prediction #####
                socket.send(msg);

        //##### Linechart updation #####
                var current = []
                for (let i=r; i<r+7; i++){
                        current.push(df[2][i]);
                }
                updateData(lineChart, current)
                // End of Linechart

                r+=1
            }, 10000)
        });
    });

categoryAxis.sortBySeries = series;

}); // end am4core.ready()


var dtx = document.getElementById('lineChart').getContext('2d');
var lineChart = new Chart(dtx, {
    type: 'line',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function updateData(chart,x) {
    chart.data.datasets[0].data=x
    chart.update()
}


// BAR GRAPH


var ctx = document.getElementById('barChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [
            {
            label: 'Process Temp',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        },
        {
            label: 'Air Temp',
            data: [26, 29, 34, 51, 27, 23],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }
    ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function updateData2(chart,x, y) {
    console.log(chart.data.datasets[0].data)
    chart.data.datasets[0].data=x
    console.log(chart.data.datasets[0].data)
    chart.data.datasets[1].data=y
    chart.update()
}

// inserting the new dataset after 3 seconds
setTimeout(function () {
  updateData2(barChart, [16, 14, 8, 34, 56], [16, 14, 18, 34, 56]);
}, 3000);