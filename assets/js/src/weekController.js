'use strict';

angular.module('controllers')
.controller('WeekCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
	$http.get('/api/week/1').success(function(data) {
		$scope.week = data.week;
		$scope.groups = data.groups;
	});

	$scope.showGroup = function(group) {
		var url = '/week/'+$scope.week+'/group/'+group.group;
		$location.url(url);
	};
}]);