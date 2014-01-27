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
		var GoogleAnalytics = {};
		GoogleAnalytics.get_profiles = function(){
			$http.get('/api/v1/google-analytics/?metric=profiles'

			).success(					
				function(data) {
				
					callback(data);
							
				}
			)
		}

		GoogleAnalytics.get = function(){
			$http.get('/api/v1/google-analytics/'
			).success(
				function(data) {
					callback(data);
				}
			)

		}

		return GoogleAnalytics;

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
