$('registration-button').click(function(){
	var serialized = $('#registration-form')
});

var getAPIs = {
	init: function(){
		this.get_google_analytics();
	},
	get_google_analytics: function(){
		/*$.ajax({
  			type: "GET",
			  url: "/api/v1/google-analytics/?username="+username,
			  success: function(data){
			  	console.log(data);
			var tmplMarkup = $('#ga-tmpl').html();
			// ...tell Underscore to render the template...
			var compiledTmpl = _.template(tmplMarkup, { profiles : data });
// ...and update part of your page:
$('.ga-accounts').html(compiledTmpl);
			  },
			  error: function(error){
			  	console.log(error);
			  }
		});*/

	}
}

$(document).ready(function() {
	username = $("#username").text();
	getAPIs.init(username);
	var router = new Router_View({el:'.api-sidebar'});
});

function line(){
	gaData = [
  		{
	 		"key": "Site visitors (total)",
			"values": [ [ 1374256623694 , 30], [ 1376798400000 , 500] ] 
		},
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
}

function funnel(){
	  var getRandomData = function (count) {
          var data = [],
            i=0,
            count = count || 6;

          for(i=0; i < count; i++) {
            data.push({amount: Math.floor(Math.random() * 10000) , title: 'Something-' + i});
          }
          return data;
        }

          var funnel = new Funnel({
            valueAttribute: 'amount',
            uniqueAttribute: 'title',
            height: 400,
            sortData: true,
            horizontalOrientation: true,
            axisSize: 40,
            data: [
              {amount: 9909 , title: 'Vistors' , color: '#FF0000'},
              {amount: 8999 , title: 'Unique Vistors' , color: '#FFFF00'},
              {amount: 3040 , title: 'Signups' , color: '#FF00FF'},
              {amount: 2903 , title: 'Confirmed Users'},
              {amount: 1333 , title: 'Active Users'},
            ],
            axisTemplate: _.template('<div class="title"><%= title %></div><div class="amount"><%= amount %></div>')
          });
          $('.funnel-container').append(funnel.el);
    //      $('#update').on('click' , function () {
        //    var items = Math.ceil(Math.random()*7)+1;
       //     funnel.update(getRandomData(items));
       //   });
			$("#update").remove();
			$("#empty").remove();
          $('#toggle-orientation').on('click' , function () {
            funnel.options.horizontalOrientation = !funnel.options.horizontalOrientation;
            funnel.options.axisSize = funnel.options.horizontalOrientation ? 40 : 200;
            funnel.options.gapBetweenSize = funnel.options.horizontalOrientation ? 20 : 10;
            funnel.update();
          });

      //    $('#empty').on('click' , function () {
         //   funnel.update([]);
        //  });
}


