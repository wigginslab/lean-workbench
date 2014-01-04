'use strict';

angular.module('lwbAppApp', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ngRoute'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/static/lwb-app/views/main.html',
        controller: 'MainCtrl'
      })
      .when('/register', {
        templateUrl: '/static/lwb-app/views/register.html',
        controller: 'RegistrationController'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
