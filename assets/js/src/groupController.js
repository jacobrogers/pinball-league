'use strict';

angular.module('controllers')
.controller('GroupCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.init = function(week, group) {
		$scope.groupNumber = group;
		$scope.week = week;
		$http.get('/api/group', {params: {'group': group, 'week': week}})
		.success(function(data) {
			$scope.group = data;
		});
	};

	$scope.saveTable = function(table) {
		var gamesToSave = $scope.group.games.filter(function(game) { return game.table.name === table.name });
		var scoresAreValid = true;
		_.each(gamesToSave, function(game) {
			if (!_.isNumber(game.score)) {
				scoresAreValid = false;
				game.status = 'invalidScore';
			}
		});

		if (scoresAreValid) {
			$http.post('/api/saveGames', {games: gamesToSave, week: $scope.week, group: $scope.groupNumber})
				.success(function(data) {
					for (var i in data) {
						var gamePoints = data[i];
						for (var j in gamesToSave) {
							var gameToSave = gamesToSave[j];
							if (gameToSave.id == gamePoints.id) {
								gameToSave.league_points = gamePoints.league_points;
								gameToSave.bonus_points = gamePoints.bonus_points;
								gameToSave.status = 'saved';
							}
						}
					}
				});
		}
	};
}]);