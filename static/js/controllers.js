/* Controllers */


var LWBApp = angular.module('LWBApp', ['ngRoute','http-auth-interceptor'], 
  function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}).controller({
  RegistrationController: function($scope, $http, authService){
    $scope.submit = function(){
      $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
      $http.defaults.headers.post['Content-Type'] = 'application/json'
      $http.defaults.headers.post['Accept'] = 'application/json'

      $http.post(
        '/registration',

        JSON.stringify({email: $scope.email, company: $scope.company, password: $scope.password, password_confirm: $scope.password_confirm})
        ).success(
        function(data){
          // if success
          if (data['response']['user']){
            // login
             $http.post('/logout').success(
               $http.post(
                  '/login',
                  JSON.stringify({ email: $scope.email, password: $scope.password })
                ).success(
                  function(data) {
                    alert('LoginController submit success');
                    alert(data);
                    //debugger;
                    $.cookie('email', data.email, { expires: 7 });
                    $.cookie('auth_token', data.auth_token, { expires: 7 });
                    $http.defaults.headers.common['Authentication-Token'] = data.auth_token;
                    authService.loginConfirmed();
                }
              )
            )
          }

          else{
            // TODO: brevity
            var errors = data['response']['errors'];
            if (errors.hasOwnProperty('email')){
              $scope.email_error = errors['email'][0];
            }
            if (errors.hasOwnProperty('company')){
              $scope.company_error = errors['company'][0];
            }
            if (errors.hasOwnProperty('password')){
              $scope.password_error = errors['password'][0];
            }            
            if (errors.hasOwnProperty('password_confirm')){
              $scope.password_confirm_error = errors['password_confirm'][0];
            }
          }
        }
      ).error(
        function(data){
          console.log('registration error')
          alert(data)
          $scope.errorMsg = data.reason;
        }
      );
    };
  }

}).controller({
  LoginController: function ($scope, $http, authService) {
    $scope.submit = function() {
      alert('LoginController inside 3');
      $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
      $http.defaults.headers.common['Content-Type'] = 'application/json'
      //debugger;
      $http.post(
        '/login',
          JSON.stringify({ email: $scope.email, password: $scope.password })
      ).success(
        function(data) {
          //debugger;
          $.cookie('email', $scope.email, { expires: 7 });
          $.cookie('auth_token', data.authentication_token, { expires: 7 });
          $http.defaults.headers.common['Authentication-Token'] = data.authentication_token;
          authService.loginConfirmed();

          // test
          $http.post(
            '/dashboard',
           JSON.stringify({authentication_token: $.cookie('auth_token')})
          ).success(
            function(data) {
              console.log(data);
            }
          )
        }
        ).error(
        function(data) {
          alert('LoginController submit error');
          $scope.errorMsg = data.reason;
          //debugger;
        }
      );
    };
  }

}).controller({
  ContentController: function ($scope, $http) {

    $scope.publicContent = [];
    $scope.restrictedContent = [];

    $scope.publicAction = function() {

      $http.post(
        '/api/myproperty/paymenttype/',
        JSON.stringify({ name: $scope.publicData })
      ).success(
        function(response) {
          $scope.publicContent.push(response);
        }
      ).error(
        function(response) {
          alert('error 99');
        }
      );
    };

    $scope.restrictedAction = function() {
      alert('restrictedAction');

      $http.post(
        'http://localhost:8001/api/myproperty/paymenttype/',
        JSON.stringify({ name: $scope.restrictedData }), {
          //transformResponse: function(data),
          timeout: 5000
        }
      ).success(
        function(response) {
          alert('restrictedAction inside');
          // this piece of code will not be executed until user is authenticated
          $scope.restrictedContent.push(response);
        }
      );
    };

    $scope.logout = function() {
      $http.post('/logout').success(function() {
        $scope.restrictedContent = [];
        $.cookie('auth_token', null);
        $http.defaults.headers.common['Authorization'] = null;
      }).error(function() {
        // This should happen after the .post call either way.
        $.cookie('auth_token', null);
        $http.defaults.headers.common['Authorization'] = null;
      });
    };
  }

});