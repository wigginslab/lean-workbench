/* Controllers */


function MyCtrl1(){
}

function MeasurementsController($scope, $http){
	$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
	$http.defaults.headers.common['Content-Type'] = 'application/json';
	$http.defaults.headers.common['Accept'] = 'application/json';

}

function DashboardController($scope) {
	$scope.hypothesis_submit = function(){
     $http.defaults.headers.common['X-CSRFToken'] = csrf_token;
      $http.defaults.headers.common['Content-Type'] = 'application/json'
      $http.defaults.headers.common['Accept'] = 'application/json'

      $http.post(
        '/api/v1/hypotheses',
        JSON.stringify({name: $scope.name, twitter: $scope.twitter})
        ).success(
        function(data){
          // if success
          if (data['response']['user']){
                 $location.path("/onboarding/stick");
          }

          else{
            // TODO: brevity
            var errors = data['response']['errors'];
           }
          }
     	).error(
        function(data){
          console.log('registration error')
          $scope.errorMsg = data.reason;
        }
      );
    }

	$scope.new_hypothesis = function(){
	
	}
}

function CarouselController($scope, $location, $anchorScroll){
  $scope.scroll_to = function(id) {
      $location.hash(id);
      $anchorScroll();
   }
}

function ErrorPageController(){
}

function OnboardingController(){
}


function StickController($scope, $http, GoogleAnalytics){
	var GAQuery = GoogleAnalytics.get();
	console.log(GAQuery);
	if (GAQuery.length > 0){
		$scope.GA = true;
	}
	$scope.has_GA = function(){
		if ($scope.GA){
			return true;
		}
	}
	$scope.GA_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
				'/connect/google-analytics'
				).success(
				function(data){
					var status = data['status'];
					if (status == 100){
						var redirect_url = data['redirect_url'];
						window.location(redirect_url);
					}
				}
			)
		}
}


function ViralityController($scope, $http, Facebook, Twitter){
	$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
	var FBQuery = Facebook.get();
	var TwitterQuery = Twitter.get();

	if (FBQuery.length > 0){
		$scope.FB = true;
	}

	$scope.has_FB = function(){
		if ($scope.FB){
			return true;
		}
	}

	$scope.fb_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
				'/connect/facebook'
		).success(
			function(data){
			var redirect_url = data['redirect_url'];
			if (redirect_url != null){
				open(redirect_url);
			}
				}
		).error(  
				function(data){
						console.log('error')
						$scope.FB_error = "Facebook authentication failed."
				})   
	}
	

	if (TwitterQuery['twitter_handle']){
		$scope.Twitter = true;
	}

	$scope.has_Twitter = function(){
		if ($scope.Twitter){
			return true;
		}
	}

	$scope.twitter_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
			'/connect/twitter'
			).success(
			function(data){
				var status = data['status'];
				if (status == 100){
					var redirect_url = data['redirect_url'];
					open(redirect_url);
				}
			}
		).error(  
			function(data){
				$scope.twitter_error = "Twitter authentication failed."
			}
		)
	}
}


function PayController($scope){

}


var LWBApp = angular.module('LWBApp', ['ngRoute','http-auth-interceptor', 'LWBServices'], 
	function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
}).controller({
 	RegistrationController: function($scope, $http, authService, $location) {

                $scope.showModal = false;
                $scope.toggleModal = function() {
                        $scope.showModal = !$scope.showModal;
                };

                $scope.submit = function() {
                	$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
					console.log(csrf_token);
					$http.defaults.headers.common['Content-Type'] = 'application/json';
					$http.defaults.headers.common['Accept'] = 'application/json';

					$http.post(
						'/registration',

						JSON.stringify({email: $scope.email, company: $scope.company, password: $scope.password, password_confirm: $scope.password_confirm})
						).success(
							function(data){
								console.log(data);
								// if success
								console.log(data['response']['user']);
								if (data['response']['user']){
										$location.path("/onboarding/stick");
								}

								else{
									// TODO: brevity
									var errors = data['response']['errors'];
									if (errors.hasOwnProperty('email')){
										// $scope.email_error = errors['email'][0];
										$scope.email_error = true;
									}
									if (errors.hasOwnProperty('company')){
										// $scope.company_error = errors['company'][0];
										$scope.comapany_error = true;
									}
									if (errors.hasOwnProperty('password')) {
										$scope.password_error = true;
										// $scope.password_error = errors['password'][0];
									}            
									if (errors.hasOwnProperty('password_confirm')){
										$scope.password_confirm_error = true;
										// $scope.password_confirm_error = errors['password_confirm'][0];
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
  LoginController: function ($scope, $http, authService, $location) {
    $scope.submit = function() {
      console.log('in logincontroller')
      $http.defaults.headers.post['X-CSRFToken'] = csrf_token;
      $http.defaults.headers.common['Content-Type'] = 'application/json'
      $http.defaults.headers.common['Accept'] = 'application/json'

      //debugger;
      $http.post(
        '/login',
          JSON.stringify({ email: $scope.email, password: $scope.password })
      ).success(
        function(data) {
          if (data.meta){
            var status_code = data.meta.code;
          }
          else{
            var status_code = data.status;
          }
          if (status_code == 200 || status_code == 302 || status_code == 301){        
            $.cookie('email', $scope.email, { expires: 7 });
            $.cookie('auth_token', data.authentication_token, { expires: 7 });
            $http.defaults.headers.common['Authentication-Token'] = data.authentication_token;
            authService.loginConfirmed();
            $location.path("/dashboard");
          }
          else{
            var errors = data['response']['errors'];
            if (errors.hasOwnProperty('email')){
              $scope.email_error = errors['email'][0];
            }
            if (errors.hasOwnProperty('password')){
              $scope.password_error = errors['password'][0];
            }            
          }
        }
        ).error(
        function(data) {
          $scope.errorMsg = data.reason;
          //debugger;
        }
      );
    };
  }

})
.controller({
  NavController: function ($scope, $http, authService, $location) {
      $scope.click_login = function(){
        var main = $('#content');
        var login = $('#login-holder');
          login.slideDown('slow', function() {
          main.hide();
        });
      }
    
     $scope.click_logout = function() {
      $http.defaults.headers.post['X-CSRFToken'] = csrf_token;

      $http.get('/logout').success(function() {
        $scope.restrictedContent = [];
        $.cookie('auth_token', null);
        $.cookie('email', null);
        $http.defaults.headers.common['Authorization'] = null;
        $http.defaults.headers.common['Authentication-Token'] = null;

      }).error(function() {
        // This should happen after the .post call either way.
        $.cookie('auth_token', null);
        $http.defaults.headers.common['Authorization'] = null;
          $location.path("/");
      }); 
    };

    $scope.logged_in = function(){
      if ($.cookie('auth_token')){
        return True;
      }

      else{
        return False;
      }
    }

  }

})
.controller({
	HypothesesListController: function ($scope, $http, Hypotheses) {
		var hypothesesQuery = Hypotheses.get({}, function(hypotheses) {
			$scope.hypotheses = hypotheses.objects;
		});
	}
})
.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider
    .when('/', {templateUrl: 'static/partials/public.html', controller: MyCtrl1})
  //  .when('/dashboard', {templateUrl: 'static/partials/dashboard.html', controller: DashboardController})
    .when('/onboarding/stick', {templateUrl: '/static/partials/onboarding/stick.html', controller: StickController})
    .when('/onboarding/virality', {templateUrl: '/static/partials/onboarding/virality.html', controller: ViralityController})
    .when('/onboarding/pay', {templateUrl: '/static/partials/onboarding/pay.html', controller: PayController})
	.when('/dashboard', {templateUrl: '/static/partials/dashboard.html', controller: MeasurementsController})
    // enable push state
    $locationProvider.html5Mode(true);
}])
