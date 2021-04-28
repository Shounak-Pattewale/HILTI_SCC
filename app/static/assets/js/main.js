var df = [];
data.forEach(function (d) {
  df[0] = d["Air temp"];
  df[1] = d["Process temp"];
  df[2] = d["Rpm"];
  df[3] = d["Torque"];
  df[4] = d["Tool wear"];
  df[5] = d['time'];
});

am4core.ready(function () {
  // console.log("1")

  // Themes begin
  // am4core.useTheme(am4themes_dark);
  am4core.useTheme(am4themes_animated);
  // Themes end

  var chartMin = 1000;
  var chartMax = 3000;

  var data = {
    score: 1052.7,
    gradingData: [
      {
        title: "Low",
        color: "#f3eb0c",
        lowScore: 1000,
        highScore: 1350,
      },
      {
        title: "Better",
        color: "#fdae19",
        lowScore: 1350,
        highScore: 1500,
      },
      {
        title: "Good",
        color: "#54b947",
        lowScore: 1500,
        highScore: 2000,
      },
      {
        title: "Very High",
        color: "#ee1f25",
        lowScore: 2750,
        highScore: 3000,
      },
      {
        title: "High",
        color: "#f04922",
        lowScore: 2000,
        highScore: 2750,
      },
    ],
  };

  /**
    Grading Lookup
     */
  function lookUpGrade(lookupScore, grades) {
    // Only change code below this line
    for (var i = 0; i < grades.length; i++) {
      if (
        grades[i].lowScore < lookupScore &&
        grades[i].highScore >= lookupScore
      ) {
        return grades[i];
      }
    }
    return null;
  }

  // create chart
  var chart = am4core.create("myChart4", am4charts.GaugeChart);
  chart.hiddenState.properties.opacity = 0;
  chart.fontSize = 11;
  chart.innerRadius = am4core.percent(80);
  chart.resizable = true;

  /**
   * Normal axis
   */

  var axis = chart.xAxes.push(new am4charts.ValueAxis());
  axis.min = chartMin;
  axis.max = chartMax;
  axis.strictMinMax = true;
  axis.renderer.radius = am4core.percent(80);
  axis.renderer.inside = true;
  axis.renderer.line.strokeOpacity = 0.1;
  axis.renderer.ticks.template.disabled = false;
  axis.renderer.ticks.template.strokeOpacity = 1;
  axis.renderer.ticks.template.strokeWidth = 0.5;
  axis.renderer.ticks.template.length = 5;
  axis.renderer.grid.template.disabled = true;
  axis.renderer.labels.template.radius = am4core.percent(15);
  axis.renderer.labels.template.fontSize = "0.9em";

  /**
   * Axis for ranges
   */

  var axis2 = chart.xAxes.push(new am4charts.ValueAxis());
  axis2.min = chartMin;
  axis2.max = chartMax;
  axis2.strictMinMax = true;
  axis2.renderer.labels.template.disabled = true;
  axis2.renderer.ticks.template.disabled = true;
  axis2.renderer.grid.template.disabled = false;
  axis2.renderer.grid.template.opacity = 0.5;
  axis2.renderer.labels.template.bent = true;
  axis2.renderer.labels.template.fill = am4core.color("#000");
  axis2.renderer.labels.template.fontWeight = "bold";
  axis2.renderer.labels.template.fillOpacity = 0.3;

  /**
    Ranges
    */

  for (let grading of data.gradingData) {
    var range = axis2.axisRanges.create();
    range.axisFill.fill = am4core.color(grading.color);
    range.axisFill.fillOpacity = 0.8;
    range.axisFill.zIndex = -1;
    range.value = grading.lowScore > chartMin ? grading.lowScore : chartMin;
    range.endValue =
      grading.highScore < chartMax ? grading.highScore : chartMax;
    range.grid.strokeOpacity = 0;
    range.stroke = am4core.color(grading.color).lighten(-0.1);
    range.label.inside = true;
    range.label.text = grading.title.toUpperCase();
    range.label.inside = true;
    range.label.location = 0.5;
    range.label.inside = true;
    range.label.radius = am4core.percent(10);
    range.label.paddingBottom = -5; // ~half font size
    range.label.fontSize = "0.9em";
  }

  var matchingGrade = lookUpGrade(data.score, data.gradingData);

  /**
   * Label 1
   */

  var label = chart.radarContainer.createChild(am4core.Label);
  label.isMeasured = false;
  label.fontSize = "6em";
  label.x = am4core.percent(50);
  label.paddingBottom = 15;
  label.horizontalCenter = "middle";
  label.verticalCenter = "bottom";
  //label.dataItem = data;
  label.text = data.score.toFixed(1);
  //label.text = "{score}";
  label.fill = am4core.color(matchingGrade.color);

  /**
   * Label 2
   */

  var label2 = chart.radarContainer.createChild(am4core.Label);
  label2.isMeasured = false;
  label2.fontSize = "2em";
  label2.horizontalCenter = "middle";
  label2.verticalCenter = "bottom";
  label2.text = matchingGrade.title.toUpperCase();
  label2.fill = am4core.color(matchingGrade.color);

  /**
   * Hand
   */

  var hand = chart.hands.push(new am4charts.ClockHand());
  hand.axis = axis2;
  hand.innerRadius = am4core.percent(55);
  hand.startWidth = 8;
  hand.pin.disabled = true;
  hand.value = data.score;
  hand.fill = am4core.color("#444");
  hand.stroke = am4core.color("#000");

  hand.events.on("positionchanged", function () {
    label.text = axis2.positionToValue(hand.currentPosition).toFixed(1);
    var value2 = axis.positionToValue(hand.currentPosition);
    var matchingGrade = lookUpGrade(
      axis.positionToValue(hand.currentPosition),
      data.gradingData
    );
    label2.text = matchingGrade.title.toUpperCase();
    label2.fill = am4core.color(matchingGrade.color);
    label2.stroke = am4core.color(matchingGrade.color);
    label.fill = am4core.color(matchingGrade.color);
  });

  var chart = am4core.create("chartdiv", am4charts.XYChart);

  chart.data = [
    {
      country: "Air Temperature",
      visits: df[0][0],
    },
    {
      country: "Process Temperature",
      visits: df[1][0],
    },
    {
      country: "RPM",
      visits: df[2][0],
    },
    {
      country: "Torque",
      visits: df[3][0],
    },
    {
      country: "Tool Wear",
      visits: df[4][0],
    },
  ];

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
  series.tooltipText = "{valueY.value}";
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
    var socket = io.connect("http://127.0.0.1:5000");
    // console.log("Here : ", socket)
    socket.on("connect", function () {
      var r = 1;
      var i = 0;
      var l = 0;
      setInterval(function () {
        if (r > 10000) {
          r = 0;
        }
        var msg = [df[1][r], df[2][r], df[3][r], df[4][r], i];

        // ##### Main Barchart updation (amCharts) #####
        chart.data[0]["visits"] = df[0][r];
        chart.data[1]["visits"] = df[1][r];
        chart.data[2]["visits"] = df[2][r];
        chart.data[3]["visits"] = df[3][r];
        chart.data[4]["visits"] = df[4][r];
        chart.invalidateRawData();
        // End of Barchart

        // ##### Sending message for prediction #####
        socket.send(msg);

        //##### Linechart updation #####
        var rotation = [];
        var labels = [];
        for (let k = r + 1; k < r + 7; k++) {
          rotation.push(df[3][k]);
          labels.push(df[5][k]);
        }
        updateLineData(lineChart, rotation, labels);
        $("#rotational_speed").html(rotation[5] + " Nm");
        $("#rpm").html(rotation[5] + " Nm");
        // End of Linechart

        //##### Bar graph updation #####
        process_temp = [];
        air_temp = [];
        temp_labels = [];
        for (let j = r+1 ; j < r + 7; j++) {
          process_temp.push(df[0][j]);
          air_temp.push(df[1][j]);
          temp_labels.push(df[5][j]);
        }
        updateBarData(myChart, air_temp, process_temp, temp_labels);
        $("#temperature").html(air_temp[5] + " K");


        if (l < 10000) {
            hand.showValue(df[2][l], 1000, am4core.ease.cubicOut);
            $("#torque").html(df[2][l] + " rpm");
            $("#torque").html(df[2][l] + " rpm");
            l += 1;
          } else {
            l = 0;
          }

          i++;

        r += 1;
      }, 2000);
    });
  });

  categoryAxis.sortBySeries = series;
}); // end am4core.ready()

var dtx = document.getElementById("lineChart").getContext("2d");
var lineChart = new Chart(dtx, {
  type: "line",
  data: {
    labels: [df[5][0],df[5][1],df[5][2],df[5][3],df[5][4],df[5][5]],
    datasets: [
      {
        label: "Torque",
        data: [df[3][0],df[3][1],df[3][2],df[3][3],df[3][4],df[3][5]],
        fill: false,
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

function updateLineData(chart, x, labels) {
  chart.data.datasets[0].data = x;
  chart.data.labels = labels;
  chart.update();
}

// BAR GRAPH

var ctx = document.getElementById("barChart").getContext("2d");
var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [df[5][0],df[5][1],df[5][2],df[5][3],df[5][4],df[5][5]],
    datasets: [
      {
        label: "Process Temp",
        data: [df[1][0],df[1][1],df[1][2],df[1][3],df[1][4],df[1][5]],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 99, 132, 1)",
        ],
        borderWidth: 1,
      },
      {
        label: "Air Temp",
        data: [df[0][0],df[0][1],df[0][2],df[0][3],df[0][4],df[0][5]],
        backgroundColor: [
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(54, 162, 235, 0.2)",
        ],
        borderColor: [
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(54, 162, 235, 1)",
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

function updateBarData(chart, x, y, labels) {
  chart.data.datasets[0].data = x;
  chart.data.datasets[1].data = y;
  chart.data.labels = labels;
  chart.update();
}


new Chart(document.getElementById("doughnutChart"), {
  type: 'doughnut',
  data: {
    labels: ["L", "M", "H"],
    datasets: [
      {
        label: "Machine Failures",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
        data: [15, 11, 9]
      }
    ]
  },
  options: {
    title: {
      display: false,
      text: ''
    }
  }
});