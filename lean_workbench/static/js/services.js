'use strict';

/* Services */
angular.module('LWBServices', ['ngResource'])
	.factory('Hypotheses', function($resource) {
		return $resource('/api/v1/hypotheses', {}, {
			query: {
				method: 'GET',
				isArray: true
			}
		});
	})
	.factory('GoogleAnalytics', function($resource){
		return $resource('/api/v1/googleanalytics',{}, {
			query:{
				method: 'POST',
				isArray: true
			}
		})
	})
	.factory('Facebook', function($resource){
		return $resource('/api/v1/facebook', {}, {
			query:{
				method: 'POST',
				isArray: true
			}
		})
	})
	.factory('Twitter', function($resource){
		return $resource('/api/v1/twitter', {},{
			query:{
				method:'POST',
				isArray: true
			}
		})
	})