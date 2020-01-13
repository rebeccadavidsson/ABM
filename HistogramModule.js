var HistogramModule = function(bins, canvas_width, canvas_height, data) {

    // Create the tag:
    var canvas_tag = "<canvas id='canvas' width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "style='position:absolute'></canvas>";
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("body").append(canvas);

    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");

    console.log(data);
    // Prep the chart properties and series:
    var datasets = [{
        label: "Data",
        fillColor: "rgba(151,187,205,0.5)",
        strokeColor: "rgba(151,187,205,0.8)",
        highlightFill: "rgba(151,187,205,0.75)",
        highlightStroke: "rgba(151,187,205,1)",
        data: data
    }];

    // Add a zero value for each bin
    // for (var i in data)
    // console.log(datasets[0].data);
    //     datasets[0].data.push(data[i]);

    var data = {
        labels: bins,
        datasets: datasets
    };

    var options = {
        scaleBeginsAtZero: true
    };

    // Create the chart object
    var chart = new Chart(context, {
        type: "bar",
        data: data
      },
      options);

    // chart.data.datasets[0].data[i] = data[i];

    this.render = function(data) {
      console.log(data, "DATA");
        for (var i in data)
            chart.data.datasets[0].data[i] = data[i];
            console.log(chart.data);
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        // Create the chart object
        var chart = new Chart(context, {
            type: "bar",
            data: data
          },
          options);
    };
};
