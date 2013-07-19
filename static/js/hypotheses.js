 nv.addGraph(function() {  
   var chart = nv.models.lineChart();
  
    chart.xAxis
        .axisLabel('Time (Days)')
        .tickFormat(d3.format(',r'));
  
    chart.yAxis
       .axisLabel('Views')
       .tickFormat(d3.format('.02f'));
 
   d3.select('#chart svg')
       .datum(sinAndCos())
     .transition().duration(500)
       .call(chart);
 
   nv.utils.windowResize(function() { d3.select('#chart svg').call(chart) });
 
   return chart;
 });
 
 function sinAndCos() {
   var sin = [],
       cos = [];
 
   for (var i = 0; i < 100; i++) {
     sin.push({x: i, y: Math.sin(i/10)});
     cos.push({x: i, y: .5 * Math.cos(i/10)});
   }
 
   return [
     {
       values: sin,
       key: 'New Visitors',
       color: '#ff7f0e'
     },
     {
       values: cos,
      key: 'Returning Visitors',
       color: '#2ca02c'
     }
   ];
 }

