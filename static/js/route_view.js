var Router_View = Backbone.View.extend({

	events: {
		'click li.connect': 'redirect_connect',
		'click li.view': 'redirect_view'
	},

	initialize: function(){
		console.log('router init');
	},
	redirect_connect: function(e){
		console.log(e);
		elementId = e.currentTarget.id;	
		$('#body-content').load('/connect/'+elementId);
	},

	redirect_view: function(e){
		console.log(e);
		elementId = e.currentTarget.id;	
		$('#body-content').load('/view/'+elementId);
	}
});
