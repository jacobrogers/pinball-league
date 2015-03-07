'use strict';

angular.module('controllers')
.controller('GroupCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.init = function(week, group) {
		$scope.groupNumber = group;
		$scope.week = week;
		$http.get('/api/group', {params: {'group': group, 'week': week}})
		.success(function(data) {
			$scope.matches = data.matches;
			$scope.tables = data.tables;
			
			for (var i=0; i<$scope.matches.length; i++) {
				for (var j=0; j<$scope.tables.length; j++) {
					if ($scope.matches[i].table.id === $scope.tables[j].id) {
						$scope.matches[i].table = $scope.tables[j];
						break;
					}
				}
			}

			var matchesToCreate = 3-$scope.matches.length;
			for (var i=0; i<matchesToCreate; i++) {
				var games = [];
				for (var j=0; j<data.players.length; j++) {
					games.push({player: {id: data.players[j].id, name: data.players[j].name}});
				}
				$scope.matches.push({games: games});
			}
		});
	};

	$scope.saveGame = function(match) {
		var players = [];
		var scoresAreValid = true;
		for (var i=0; i < match.games.length; i++) {
			var game = match.games[i];
			var player = {id: game.player.id, name: game.player.name};
			if (isNaN(Number(game.score))) {
				scoresAreValid = false;
				player.status = 'invalidScore';
			} else {
				player.score = game.score;
				if (game.id) player.gameId = game.id;
				players.push(player);
			}
		};

		if (!scoresAreValid) return;

		var data = {players: players, week: $scope.week, group: $scope.groupNumber, table: match.table}
		$http.post('/api/saveGame', data)
			.success(function(data) {
				for (var i in data) {
					var game = data[i];
					for (var j in match.games) {
						var gameToSave = match.games[j];
						if (gameToSave.player.id == game.player) {
							gameToSave.league_points = game.league_points;
							gameToSave.status = 'saved';
						}
					}
				}
			});
	};
}])
.directive('formatScore', ['$filter', function ($filter) {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;

            ctrl.$formatters.unshift(function (a) {
                return $filter('number')(ctrl.$modelValue)
            });

            ctrl.$parsers.unshift(function (viewValue) {
                var plainNumber = viewValue.replace(/[^\d|\-+|\.+]/g, '');
                elem.val($filter('number')(plainNumber));
                return plainNumber;
            });
        }
    };
}]);
