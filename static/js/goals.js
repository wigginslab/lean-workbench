
gaData = [

 
  {
	      "key": "Site visitors (total)",
		      "values": [ [ 1374256623694 , 30], [ 1376798400000 , 500] ] },
			    {
					    "key": "Hypothesis visitors",
						    "values": [  [ 1374256623694 , 20], [ 1376798400000 , 100]]
								  }
];
nv.addGraph(function() {
	  var chart = nv.models.cumulativeLineChart()
	                .x(function(d) { return d[0] })
	                .y(function(d) { return d[1] }) //adjusting, 100% is 1.00, not 100 as it is in the data
	                .color(d3.scale.category10().range());

  chart.xAxis
	      .tickFormat(function(d) {
					          return d3.time.format('%x')(new Date(d))
			        });

  chart.yAxis
	      .tickFormat(d3.format(',.1'));

  d3.select('#char svg')
	      .datum(gaData)
	    .transition().duration(500)
	      .call(chart);

  nv.utils.windowResize(chart.update);
chart.height = "600px";
    return chart;
});

