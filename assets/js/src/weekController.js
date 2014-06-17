'use strict';

angular.module('controllers')
.controller('WeekCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
	$http.get('/api/week/1').success(function(data) {
		$scope.groups = data;
	});

	$scope.showGroup = function(group) {
		var url = '/week/'+$scope.groups.week+'/group/'+group.group;
		$location.url(url);
	};
}]);