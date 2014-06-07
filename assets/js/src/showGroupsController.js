'use strict';

angular.module('controllers')
.controller('ShowGroupsCtrl', ['$scope', '$http', function($scope, $http) {
	$http.get('/api/groups/1').success(function(data) {
		$scope.groups = data;
	});
}]);