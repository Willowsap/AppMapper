anychart.data.loadJsonFile('https://student2.cs.appstate.edu/sapphirewe/AppMapper/scripts/data.json', function (data) {
  // create a chart from the loaded data
  var chart = anychart.graph(data);

  // set the title
  chart.title("Appstate.edu URL Map");

  // draw the chart
  chart.container("container").draw();
})
