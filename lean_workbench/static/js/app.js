// Declare app level module which depends on filters, and services
angular.module(
    'LWBApp', [
         'LWBAppServices',
        'http-auth-interceptor', 'ngCookies', 'ngRoute'
    ]
)
.config(function($httpProvider) {
  $http.defaults.headers.common['Authentication-Token'] = $.cookie('auth_token');
})
.run( function run( $http, $cookies ){
    $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
})
