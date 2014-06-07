'use strict';

angular.module('controllers')
.controller('PlayersCtrl', ['$scope','$http', function($scope,$http) {
	$http.get('/api/players').success(function(data) {
		$scope.players = data;
	});
}]);