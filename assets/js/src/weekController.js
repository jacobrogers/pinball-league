'use strict';

angular.module('controllers')
.controller('WeekCtrl', ['$scope', '$http', '$location', '$routeParams', function($scope, $http, $location, $routeParams) {
	$scope.week = $routeParams.week;

    $http.get('/api/week/'+$routeParams.week).success(function(data) {
		$scope.groups = data.groups;
	});

	$scope.showGroup = function(group) {
		var url = '/week/'+$scope.week+'/group/'+group.group;
		$location.url(url);
	};
}]);