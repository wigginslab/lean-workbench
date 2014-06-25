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

function DashboardControllerTwo($scope, $http, Hypotheses, $resource, $location) {
  $scope.exampleData = [
                {
                    "key": "Series 1",
                    "values": [ [ 1025409600000 , 0] , [ 1028088000000 , -6.3382185140371] , [ 1030766400000 , -5.9507873460847] , [ 1033358400000 , -11.569146943813] , [ 1036040400000 , -5.4767332317425] , [ 1038632400000 , 0.50794682203014] , [ 1041310800000 , -5.5310285460542] , [ 1043989200000 , -5.7838296963382] , [ 1046408400000 , -7.3249341615649] , [ 1049086800000 , -6.7078630712489] , [ 1051675200000 , 0.44227126150934] , [ 1054353600000 , 7.2481659343222] , [ 1056945600000 , 9.2512381306992] , [ 1059624000000 , 11.341210982529] , [ 1062302400000 , 14.734820409020] , [ 1064894400000 , 12.387148007542] , [ 1067576400000 , 18.436471461827] , [ 1070168400000 , 19.830742266977] , [ 1072846800000 , 22.643205829887] , [ 1075525200000 , 26.743156781239] , [ 1078030800000 , 29.597478802228] , [ 1080709200000 , 30.831697585341] , [ 1083297600000 , 28.054068024708] , [ 1085976000000 , 29.294079423832] , [ 1088568000000 , 30.269264061274] , [ 1091246400000 , 24.934526898906] , [ 1093924800000 , 24.265982759406] , [ 1096516800000 , 27.217794897473] , [ 1099195200000 , 30.802601992077] , [ 1101790800000 , 36.331003758254] , [ 1104469200000 , 43.142498700060] , [ 1107147600000 , 40.558263931958] , [ 1109566800000 , 42.543622385800] , [ 1112245200000 , 41.683584710331] , [ 1114833600000 , 36.375367302328] , [ 1117512000000 , 40.719688980730] , [ 1120104000000 , 43.897963036919] , [ 1122782400000 , 49.797033975368] , [ 1125460800000 , 47.085993935989] , [ 1128052800000 , 46.601972859745] , [ 1130734800000 , 41.567784572762] , [ 1133326800000 , 47.296923737245] , [ 1136005200000 , 47.642969612080] , [ 1138683600000 , 50.781515820954] , [ 1141102800000 , 52.600229204305] , [ 1143781200000 , 55.599684490628] , [ 1146369600000 , 57.920388436633] , [ 1149048000000 , 53.503593218971] , [ 1151640000000 , 53.522973979964] , [ 1154318400000 , 49.846822298548] , [ 1156996800000 , 54.721341614650] , [ 1159588800000 , 58.186236223191] , [ 1162270800000 , 63.908065540997] , [ 1164862800000 , 69.767285129367] , [ 1167541200000 , 72.534013373592] , [ 1170219600000 , 77.991819436573] , [ 1172638800000 , 78.143584404990] , [ 1175313600000 , 83.702398665233] , [ 1177905600000 , 91.140859312418] , [ 1180584000000 , 98.590960607028] , [ 1183176000000 , 96.245634754228] , [ 1185854400000 , 92.326364432615] , [ 1188532800000 , 97.068765332230] , [ 1191124800000 , 105.81025556260] , [ 1193803200000 , 114.38348777791] , [ 1196398800000 , 103.59604949810] , [ 1199077200000 , 101.72488429307] , [ 1201755600000 , 89.840147735028] , [ 1204261200000 , 86.963597532664] , [ 1206936000000 , 84.075505208491] , [ 1209528000000 , 93.170105645831] , [ 1212206400000 , 103.62838083121] , [ 1214798400000 , 87.458241365091] , [ 1217476800000 , 85.808374141319] , [ 1220155200000 , 93.158054469193] , [ 1222747200000 , 65.973252382360] , [ 1225425600000 , 44.580686638224] , [ 1228021200000 , 36.418977140128] , [ 1230699600000 , 38.727678144761] , [ 1233378000000 , 36.692674173387] , [ 1235797200000 , 30.033022809480] , [ 1238472000000 , 36.707532162718] , [ 1241064000000 , 52.191457688389] , [ 1243742400000 , 56.357883979735] , [ 1246334400000 , 57.629002180305] , [ 1249012800000 , 66.650985790166] , [ 1251691200000 , 70.839243432186] , [ 1254283200000 , 78.731998491499] , [ 1256961600000 , 72.375528540349] , [ 1259557200000 , 81.738387881630] , [ 1262235600000 , 87.539792394232] , [ 1264914000000 , 84.320762662273] , [ 1267333200000 , 90.621278391889] , [ 1270008000000 , 102.47144881651] , [ 1272600000000 , 102.79320353429] , [ 1275278400000 , 90.529736050479] , [ 1277870400000 , 76.580859994531] , [ 1280548800000 , 86.548979376972] , [ 1283227200000 , 81.879653334089] , [ 1285819200000 , 101.72550015956] , [ 1288497600000 , 107.97964852260] , [ 1291093200000 , 106.16240630785] , [ 1293771600000 , 114.84268599533] , [ 1296450000000 , 121.60793322282] , [ 1298869200000 , 133.41437346605] , [ 1301544000000 , 125.46646042904] , [ 1304136000000 , 129.76784954301] , [ 1306814400000 , 128.15798861044] , [ 1309406400000 , 121.92388706072] , [ 1312084800000 , 116.70036100870] , [ 1314763200000 , 88.367701837033] , [ 1317355200000 , 59.159665765725] , [ 1320033600000 , 79.793568139753] , [ 1322629200000 , 75.903834028417] , [ 1325307600000 , 72.704218209157] , [ 1327986000000 , 84.936990804097] , [ 1330491600000 , 93.388148670744]]
                }
   ];

	  $scope.xAxisTickFormat = function(){
                return function(d){
                    return d3.time.format('%x')(new Date(d));  //uncomment for date format
                }
            }

	 $http.get(
        '/api/v1/twitter'
      ).success(
        function(data) {
          $scope.twitterData = data;
        }
      ).error(function(data){
	      	alert(data)
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
		$http.get(
				'/api/v1/twitter'
		).success(
			function(data){
				console.log(data)
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


function PayController($scope, $http, Quickbooks){
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
    .when('/dashboard2', {templateUrl: 'static/partials/dashboard2.html', controller: DashboardControllerTwo})
    .when('/dashboard', {templateUrl: 'static/partials/dashboard.html', controller: DashboardController})
    .when('/onboarding/stick', {templateUrl: '/static/partials/onboarding/stick.html', controller: StickController})
    .when('/onboarding/virality', {templateUrl: '/static/partials/onboarding/virality.html', controller: ViralityController})
    .when('/onboarding/pay', {templateUrl: '/static/partials/onboarding/pay.html', controller: PayController})
	.when('/signin', {templateUrl: 'static/partials/signin.html'})
	.when('/stats', {templateUrl: '/static/partials/measurements2.html', controller: MeasurementsController})
	.when('/stats/1', {templateUrl: '/static/partials/measurements.html', controller: MeasurementsController})
	.when('/export', {templateUrl: '/static/partials/export.html', controller: ExportController})
	.when('/connect/google-analytics/success', {templateUrl: '/static/partials/ga_success.html', controller: StickController})
    // enable push state
    $locationProvider.html5Mode(true);
}])
