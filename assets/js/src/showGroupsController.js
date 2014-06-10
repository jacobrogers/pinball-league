'use strict';

angular.module('controllers')
.controller('ShowGroupsCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
	$http.get('/api/week/1').success(function(data) {
		$scope.groups = data;
	});

	$scope.showGroup = function(group) {
		console.log('showing ' + group);
		var url = '/week/'+$scope.groups.week+'/group/'+group.group;
		console.log(url);
		$location.url(url);
	};
}]);