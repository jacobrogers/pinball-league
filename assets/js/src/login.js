'use strict';

angular.module('authentication', ['ngResource'])
.factory('api', function($resource) {
	function add_auth_header(data, headersGetter) {
		var headers = headersGetter();
		headers['Authorization'] = ('Basic ' + btoa(data.username+':'+data.password));
	}
	return {
		auth: $resource('/api/auth\\/', {}, { 
			login: {method: 'POST', transformRequest: add_auth_header},
			logout: {method: 'DELETE'}
		}),
		users: $resource('/api/users\\/', {}, {
			create: {method: 'POST'}
		})
	};
})
.controller('LoginCtrl', ['$scope','$http','api', function($scope,$http,api) {	
	// $('#username').checkAndTriggerAutoFillEvent();

	$scope.getCredentials = function() {
		return {username: $scope.username, password: $scope.password};
	};

	$scope.login = function() {
		api.auth.login($scope.getCredentials())
			.$promise.then(function(data) {
				$scope.user = data.username;
			}).catch(function(data) {
				alert(data.data.detail);
			});
	};

	$scope.logout = function() {
		$event.preventDefault();
		api.users.create($scope.getCredentials())
			.promise.then($scope.login)
			.catch(function(data) {
				alert(data.data.username);
			});
	};
}]);
