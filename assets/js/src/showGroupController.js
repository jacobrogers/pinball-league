'use strict';

angular.module('controllers')
.controller('ShowGroupCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
	$http.get('/api/group', {params: {'group': $routeParams.group, 'week': $routeParams.week}}).success(function(data) {
		$scope.group = data;
	});
}]);