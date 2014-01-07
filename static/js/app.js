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

/*.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: '/static/partials/public.html', controller: MyCtrl1});
    $routeProvider.when('/dashboard', {templateUrl: '/static/partials/dashboard.html', controller: MyCtrl2});
    $routeProvider.otherwise({redirectTo: '/view1'});
}])*/

.run( function run( $http, $cookies ){
    $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
})