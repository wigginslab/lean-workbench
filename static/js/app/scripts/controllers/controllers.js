'use strict';

/* Controllers */

angular.module('LWBApp', [])
 .controller('RegistrationController',['$scope', function($scope){	

 	var show_reg_button = False;

	$scope.click_reg_button = function(){
		show_reg_button = True;
	}
}


$scope.processRegistration = function() {
	$http({
        method  : 'POST',
        url     : '/registration',
        data    : $.param($scope.formData),  // pass in data as strings
        headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the headers so angular passing info as form data (not request payload)
    })
        .success(function(data) {
            console.log(data);

            if (!data.success) {
            	// if not successful, bind errors to error variables
                $scope.errorName = data.errors.name;
                $scope.errorSuperhero = data.errors.superheroAlias;
            } else {
            	// if successful, bind success message to message
                $scope.message = data.message;
                console.log($scope.message)
            }
        });
};

function AboutController($scope) {
	
}

function RegistrationController($scope, $http){
	
}

function PostListController($scope, Post) {
	var postsQuery = Post.get({}, function(posts) {
		$scope.posts = posts.objects;
	});
}

function PostDetailController($scope, $routeParams, Post) {
	var postQuery = Post.get({ postId: $routeParams.postId }, function(post) {
		$scope.post = post;
	});
}



