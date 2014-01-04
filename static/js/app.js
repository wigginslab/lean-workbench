// Declare app level module which depends on filters, and services
angular.module(
    'LWBApp', [
        'LWBApp.filters', 'LWBApp.services', 'LWBApp.directives',
        'http-auth-interceptor', 'ngCookies'
    ]
)



.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
})


.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['Authorization'] = 'ApiKey ' +
    $.cookie('username') + ':' + $.cookie('key');

})

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: MyCtrl1});
    $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: MyCtrl2});
    $routeProvider.otherwise({redirectTo: '/view1'});
}])


.directive('authDemoApplication', function() {
    return {
      restrict: 'C',
      link: function(scope, elem, attrs) {
        //once Angular is started, remove class:
        elem.removeClass('waiting-for-angular');

        var login = elem.find('#login-holder');
        var main = elem.find('#content');

        login.hide();

        scope.$on('event:auth-loginRequired', function() {
          login.slideDown('slow', function() {
            main.hide();
          });
        });
        scope.$on('event:auth-loginConfirmed', function() {
          main.show();
          login.slideUp();
        });
      }
    };
  }).
run( function run( $http, $cookies ){

    // For CSRF token compatibility with Django
    console.log(csrf_token)
    $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
})