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

function ExportController(){

}

function ViewScaleController($scope, $http){
	 $http.get(
        '/api/v1/scale'
      ).success(
        function(data) {
            if (data.hasOwnProperty('scale_authed')){
            } 
            else{
              $scope.startup_data = data;

            }
        }
      ).error(function(data){
	     }
      )


}

function ScaleController($scope, $http){
    $http.get(
                  '/api/v1/scale'
            ).success(
                function(data){
                    console.log(data);
                    if (data.hasOwnProperty('scale_authed')){
                    }
                    else{
                       $scope.description = data.description;
                       $scope.angellist_url = data.angellist_url;
                       $scope.crunchbase_url = data.crunchbase_url;
                    }
                }
            ).error(
                function(data){
                    console.log('error')
                    console.log(data)
            });
           
	$scope.add_startup_data = function(){
            $http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
            $http.defaults.headers.common['Content-Type'] = 'application/json'
            $http.defaults.headers.common['Accept'] = 'application/json'

           
          $http.post(
            '/api/v1/scale',
            JSON.stringify({crunchbase_url: $scope.crunchbase_url, angellist_url: $scope.angellist_url, description: $scope.description})
            ).success(
            function(data){
                $scope.request_sent = true;
                $scope.help_msg = data.msg;
              }
            ).error(
            function(data){
              $scope.request_sent = true;
              $scope.help_msg = data.msg;
            }
          );
    }

    $scope.done_onboarding = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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


function WufooController($scope, $http){
	$scope.add_survey = function(){
        $http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
        $http.defaults.headers.common['Content-Type'] = 'application/json'
        $http.defaults.headers.common['Accept'] = 'application/json'

      $http.post(
        '/api/v1/wufoo',
        JSON.stringify({url: $scope.url, handshake: $scope.handshake, create:true})
        ).success(
        function(data){

          }
     	).error(
        function(data){
          $scope.survey_url_error = data.error;
        }
      );
    }

    $scope.done_onboarding = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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

function DashboardControllerTwo($scope, $http, Hypotheses, $resource, $location) {
	  $scope.xAxisTickFormat = function(){
                return function(d){
                    return d3.time.format('%x')(new Date(d));  //uncomment for date format
                }
            }

	 $http.get(
        '/api/v1/twitter'
      ).success(
        function(data) {
          if (data.hasOwnProperty('twitter_authed')){
             $scope.has_twitterData = false; 
        }
          $scope.twitterData = data;        
          $scope.has_twitterData = true;
        }
      ).error(function(data){
	     }
      )

       $http.get(
        '/api/v1/google-analytics?metric=visits'
      ).success(
        function(data) {
          $scope.googleData = data;
          $scope.has_ga_data = true;
        }
      ).error(function(data){
          $scope.has_ga_data = false;

	     }
      )

        $http.get(
        '/api/v1/facebook'
      ).success(
        function(data) {
          if (data.hasOwnProperty('fb_authed')){
              $scope.has_fb_data = false;
          }
          else{
            $scope.has_fb_data = true;
            $scope.facebookData = data;
          }
        }
      ).error(function(data){
	     }
      )
}

function DashboardController($scope, $http, Hypotheses, $resource, $location) {
	$("#login").hide();
   	$("#logout").show();


	$( ".datepicker" ).datepicker({ minDate: 0 });

	var hypotheses=  $http.get(
			'/api/v1/hypotheses'
			).success(
			function(data){
				$scope.hypotheses = data.hypotheses;
			}
		).error(function(data){
				console.log(data)
			}
		)

	$scope.show_form = false;
	$scope.hypothesis_submit = function(){
        $http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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

		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
					if (data.hasOwnProperty('response')){
						if (data['response'].hasOwnProperty('errors')){
							var errors = data['response']['errors'];
							if (typeof errors == "undefined")
							{

								$location.path = "/dashboard";

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
						else{
						
						$scope.show_form = false;
						window.location = '/dashboard';
					}
				}
					else{
						
						$scope.show_form = false;
						window.location = '/dashboard';
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
	$("#login").hide();
   	$("#logout").show();
	$scope.has_GA = false;

	$scope.GA_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
		$http.post(
				'/connect/google-analytics'
				).success(
				function(data){
					var status = data['status'];
					if (data.hasOwnProperty('redirect_url')){

								var redirect_url = data['redirect_url'];
								window.location = redirect_url;
						}
					if (status == 200){
						$scope.has_GA = true;
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
			}
		)
	
	$scope.submit_prof = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
	$("#login").hide();
    $("#logout").show();
	$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
		$http.post('/api/v1/twitter?metric=authed'
		).success(
			function(data){
				console.log(data)
                                console.log(data[0])
				if (data[0]['twitter_authed']){
					$scope.has_twitter = true;
				}
			}
		)

		$scope.has_fb = false;
		$http.post(
				'/api/v1/facebook?metric=authed'
		).success(
			function(data){
				if (data[0]['fb_authed']){
					$scope.has_fb = true;
				}
			}
		)

   
	
	$scope.twitter_auth = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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

function PayController($scope, $http){
    $scope.ghosting_clicked = false;

	$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
	$http.get(
		'/api/v1/quickbooks'
		).success(
			function(data){
				if (data['qb_authed']){
					$scope.has_qb = true;
				}
			}
		)

    $scope.qb_ghost = function(){
        $http.post(
	    '/api/v1/ghosting',
	    JSON.stringify({'feature':"quickbooks"})
	).success(
	    function(data){
                $scope.ghosting_clicked = true;
	    }
	)
    }

    $scope.done_onboarding = function(){
		$http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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


var LWBApp = angular.module('LWBApp', ['ngRoute','http-auth-interceptor', 'LWBServices', 'nvd3ChartDirectives'], 
	function($interpolateProvider) {
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');
}).controller({
 	RegistrationController: function($scope, $http, authService, $location) {
 				$("#login").show();
 				$('#logout').hide();

                $scope.showModal = false;
                $scope.toggleModal = function() {
                        $scope.showModal = !$scope.showModal;
                };

                $scope.submit = function() {
                        $http.defaults.headers.common['X-CSRFToken'] = $("#csrf").val();
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
                                        $("#login").hide();
                                        $("#logout").show();
                                        $http.post(
                                                '/api/v1/users',
                                                JSON.stringify({'cohort':$scope.cohort})
                                         ).success(
                                               function(data){
                                                        console.log(data);
                                                }
                                        )
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
					        $scope.company_error = true;
									}
					if (errors.hasOwnProperty('password')) {
						$scope.password_error = true;
				        }            
				        if (errors.hasOwnProperty('password_confirm')){
					        $scope.password_confirm_error = true;
				        }
				    }
				}
                                    ).error(
                                            function(data){
                                                    console.log('registration error')
                                    
                                                    $scope.errorMsg = data.reason;
                                            }
                                    );
				};
		}

}).controller({
  LoginController: function ($scope, $http, authService, $location) {
  	     $("#logout").hide();
    	$("#login").show();

    $scope.submit = function() {
   
      $http.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
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
            $("#login").hide();
    		$("#logout").show();
            window.location = "/dashboard";
          }
          else{
          	if (data.hasOwnProperty('response')){
	            var errors = data['response']['errors'];
	            if (errors.hasOwnProperty('email')){
	              $scope.email_error = errors['email'][0];
	            }
	            if (errors.hasOwnProperty('password')){
	              $scope.password_error = errors['password'][0];
	            }            
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
    	$("#logout").hide();
    	$("#login").show();
	      $http.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
	      $scope.logged_in = false;
	      $http.get('/logout').success(function() {
	        $scope.restrictedContent = [];
	        $.cookie('auth_token', null);
	        $.cookie('email',null);
	        $http.defaults.headers.common['Authorization'] = null;
	        $http.defaults.headers.common['Authentication-Token'] = null;
	        window.location = "/";
	      }).error(function() {
	        // This should happen after the .post call either way.
	        $.cookie('auth_token', null);
	        $http.defaults.headers.common['Authorization'] = null;
	        window.location = "/";
	      }); 
	    };

	    $scope.scroll_to = function(id) {
	      $location.hash(id);
	      $anchorScroll();
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
    .when('/results', {templateUrl: 'static/partials/dashboard2.html', controller: DashboardControllerTwo})
    .when('/dashboard', {templateUrl: 'static/partials/dashboard.html', controller: DashboardController})
    .when('/onboarding/stick', {templateUrl: '/static/partials/onboarding/stick.html', controller: StickController})
    .when('/onboarding/virality', {templateUrl: '/static/partials/onboarding/virality.html', controller: ViralityController})
    .when('/onboarding/pay', {templateUrl: '/static/partials/onboarding/pay.html', controller: PayController})
	.when('/signin', {templateUrl: 'static/partials/signin.html'})
	.when('/stats', {templateUrl: '/static/partials/measurements2.html', controller: MeasurementsController})
	.when('/stats/1', {templateUrl: '/static/partials/measurements.html', controller: MeasurementsController})
	.when('/export', {templateUrl: '/static/partials/export.html', controller: ExportController})
	.when('/connect/google-analytics/success', {templateUrl: '/static/partials/ga_success.html', controller: StickController})
        .when('/onboarding/empathy', { templateUrl: '/static/partials/onboarding/wufoo.html', controller: WufooController})
         .when('/onboarding/scale', { templateUrl: '/static/partials/onboarding/scale.html', controller: ScaleController})
          .when('/scale', { templateUrl: '/static/partials/scale.html', controller: ViewScaleController})
    
    // enable push state
    $locationProvider.html5Mode(true);
}])
