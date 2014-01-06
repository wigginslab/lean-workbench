'use strict';

/* Services */

'use strict';

angular.module('LWBServices', ['ngResource'])
	.factory('Hypotheses', function($resource) {
		return $resource('/api/v1/hypotheses', {}, {
			query: {
				method: 'GET',
				isArray: true
			}
		});
	})
;
