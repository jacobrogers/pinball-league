'use strict';

angular.module('controllers')
.controller('TablesCtrl', ['$scope','$http', function($scope,$http) {
	$http.get('/api/tables').success(function(data) {
		$scope.tables = data;
	});
}]);