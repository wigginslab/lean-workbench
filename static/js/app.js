$('registration-button').click(function(){
	var serialized = $('#registration-form')
});

var getAPIs = {
	init: function(){
		this.get_google_analytics();
	},
	get_google_analytics: function(){
		$.ajax({
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
		});

	}
}

$(document).ready(function() {
	username = $("#username").text();
	getAPIs.init(username);
	var router = new Router_View({el:'.api-sidebar'});
});
