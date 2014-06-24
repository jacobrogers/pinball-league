'use strict';

angular.module('controllers')
.controller('GroupCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
	$http.get('/api/group', {params: {'group': $routeParams.group, 'week': $routeParams.week}})
		.success(function(data) {
			$scope.group = data;
		});

	$scope.saveTable = function(table) {
		var gamesToSave = $scope.group.games.filter(function(game) { return game.table.name === table.name });
		$http.post('/api/saveGames', {games: gamesToSave})
			.success(function(data) {
				for (var i in data) {
					var gamePoints = data[i];
					for (var j in gamesToSave) {
						var gameToSave = gamesToSave[j];
						if (gameToSave.id == gamePoints.id) {
							gameToSave.league_points = gamePoints.league_points;
							gameToSave.bonus_points = gamePoints.bonus_points;
						}
					}
				}
			});
	};
}]);