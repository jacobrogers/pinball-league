'use strict';

angular.module('controllers')
.controller('GroupCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
	$http.get('/api/group', {params: {'group': $routeParams.group, 'week': $routeParams.week}}).success(function(data) {
		$scope.group = data;
	});

	$scope.saveTable = function(table) {
		var gamesToSave = $scope.group.games.filter(function(game) { return game.table.name === table.name });
		$http.post('/api/saveGames', {games: gamesToSave})
			.success(function(data) {
				console.log('saved');
			});
	};
}]);