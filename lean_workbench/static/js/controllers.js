/* Controllers */


function MyCtrl1(){
}

function MeasurementsController($scope, $http, Hypotheses, GoogleAnalytics, Twitter){
	// Hypotheses query
	var hyp = Hypotheses.get();
	//GA query
	var ga = GoogleAnalytics.get();
	// Twitter Query
	var twitter = Twitter.get();
	// Quickbooks Query
	//Wufoo Query

 
}



function DashboardController($scope, $http, Hypotheses, $resource) {

	$( ".datepicker" ).datepicker({ minDate: 0 });
  	/*$scope.hypotheses = Hypotheses.get(function(hypotheses){
  		console.log(hypotheses.hypotheses)
  		console.log(hypotheses.hypotheses[0])
  		$scope.hypotheses = hypotheses.hypotheses;
  	});*/
	var hypotheses=  $http.get(
			'/api/v1/hypotheses'
			).success(
			function(data){
				console.log(data)
				console.log(data.hypotheses)
				$scope.hypotheses = data.hypotheses;
			}
		).error(function(data){
				console.log(data)
			}
		)

	$scope.show_form = false;
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

    $scope.formData = {};


    $scope.create_hypothesis = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.defaults.headers.common['Content-Type'] = 'application/json';
		$http.defaults.headers.common['Accept'] = 'application/json';
		$http({
			method: "POST",
			url: '/api/v1/hypotheses',
			data: $scope.formData,
			headers : { 'Content-Type': 'application/json' }

			}).success(
				function(data){
				
					// TODO: brevity
					var errors = data['response']['errors'];
					if (typeof errors != "undefined")
					{

						$scope.hypotheses = Hypotheses.get();

					}
					else{
						if (errors.hasOwnProperty('end_date')){
							$scope.end_date_error = true;
							$scope.errorMsg = "Improper end date.";
						}
						if (errors.hasOwnProperty('start_date')){
							$scope.start_date = true;
							$scope.errorMsg = "Improper start date";
						}
						if (errors.hasOwnProperty('google_analytics.')) {
							$scope.google_analytics = true;
							$scope.errorMsg = "Improper endpoint";
						}            
						if (errors.hasOwnProperty('title')){
							$scope.title = true;
							$scope.errorMsg = "Improper title.";
						}
					}
				}

			).error(
				function(data){
					console.log('hypothesis error')
					$scope.errorMsg = data.reason;
				}
			);
	};

    

	$scope.new_hypothesis = function(){

		$scope.show_form = true;
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
	$scope.has_GA = false;

	$scope.GA_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		console.log('ga auth');
		$http.post(
				'/connect/google-analytics'
				).success(
				function(data){
					var status = data['status'];
					console.log(data);
					console.log(status);
					if (status == 100){
						var redirect_url = data['redirect_url'];
						window.location = redirect_url;
					}
				}
			)
	}

	var profiles =  $http.get(
			'/api/v1/google-analytics'
			).success(
			function(data){
				$scope.GA_profiles = data;
				$scope.has_GA = true;	
			}
		).error(function(data){
				console.log(data)
			}
		)
	
	$scope.submit_prof = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
			'/api/v1/google-analytics',
			JSON.stringify({metric:'profile-id', profile_id:$scope.user_profile})
		).success(
			function(data){
				if (data.status == 200){
					window.location = '/onboarding/virality';
				}
			}
		)
	}	
}

function ViralityController($scope, $http, Facebook, Twitter){
	$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
	var FBQuery = Facebook.get();

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
	
	$scope.has_twitter = false;
		$http.get(
				'/api/v1/twitter'
		).success(
			function(data){
				if (data['twitter_authed']){
					$scope.has_twitter = true;
				}
			}
		)

		$scope.has_fb = false;
		$http.get(
				'/api/v1/facebook'
		).success(
			function(data){
				if (data['fb_authed']){
					$scope.has_fb = true;
				}
			}
		)

   
	
	$scope.twitter_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
			'/connect/twitter'
			).success(
			function(data){
				var status = data['status'];
				if (status == 100){
					var redirect_url = data['redirect_url'];
					window.location = redirect_url;
				}
			}
		).error(  
			function(data){
				$scope.twitter_error = "Twitter authentication failed."
			}
		)
	}

	$scope.done_onboarding = function(){
		$http.defaults.headers.common['X-CSRFToken'] = csrf_token;
		$http.post(
			'/api/v1/users',
			JSON.stringify({'onboarded':true})
		).success(
			function(data){
				window.location = '/dashboard';
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
										$scope.company_error = true;
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

      $http.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
      console.log( $("#csrf").val())
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
		$location.path('/signin');  
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
    .when('/dashboard', {templateUrl: 'static/partials/dashboard.html', controller: DashboardController})
    .when('/onboarding/stick', {templateUrl: '/static/partials/onboarding/stick.html', controller: StickController})
    .when('/onboarding/virality', {templateUrl: '/static/partials/onboarding/virality.html', controller: ViralityController})
    .when('/onboarding/pay', {templateUrl: '/static/partials/onboarding/pay.html', controller: PayController})
	.when('/signin', {templateUrl: 'static/partials/signin.html'})
	.when('/stats', {templateUrl: '/static/partials/measurements.html', controller: MeasurementsController})
	.when('/stats/1', {templateUrl: '/static/partials/measurements.html', controller: MeasurementsController})
	
	.when('/connect/google-analytics/success', {templateUrl: '/static/partials/ga_success.html', controller: StickController})
    // enable push state
    $locationProvider.html5Mode(true);
}])
