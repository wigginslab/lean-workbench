/* Controllers */


var LWBApp = angular.module('LWBApp', ['ngRoute','http-auth-interceptor'], 
  function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}).controller({
  RegistrationController: function($scope, $http, authService){
    $scope.submit = function(){
      $http.defaults.headers.post['X-CSRFToken'] = csrf_token;

      $http.post(
        '/registration',

        JSON.stringify({email: $scope.email, company: $scope.company, password: $scope.password, password_confirm: $scope.password_confirm})
        ).success(
        function(data){
          if data['user']{
            $scope.success = "Success! Check your email to confirm your registration."
          }
          else{
            var errors = data['response']['errors'];
            $scope.email_error = errors['email'][0];
            $scope.company_error = errors['company'][0];
            $scope.password_error = errors['password'][0];
            $scope.password_confirm_error = errors['password_confirm'][0];
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
      //debugger;
      $http.post(
        '/login/',
        JSON.stringify({ username: $scope.username, password: $scope.password })
      ).success(
        function(data) {
          alert('LoginController submit success');
          //debugger;
          $.cookie('username', data.username, { expires: 7 });
          $.cookie('key', data.key, { expires: 7 });
          $http.defaults.headers.common['Authorization'] = 'ApiKey ' +
            data.username + ':' + data.key;
          authService.loginConfirmed();
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
      $http.post('/logout/').success(function() {
        $scope.restrictedContent = [];
        $.cookie('key', null);
        $http.defaults.headers.common['Authorization'] = null;
      }).error(function() {
        // This should happen after the .post call either way.
        $.cookie('key', null);
        $http.defaults.headers.common['Authorization'] = null;
      });
    };
  }

});