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
			
			if (0 == $scope.matches.length) {
				$scope.matches = []
				for (var i=0; i<3; i++) {
					var games = [];
					for (var j=0; j<data.players.length; j++) {
						games.push({player: {id: data.players[j].id, name: data.players[j].name}});
					}
					$scope.matches.push(games);
				}
			}
		});
	};

	$scope.saveGame = function(match) {
		var players = [];
		var scoresAreValid = true;
		for (var i=0; i < match.games.length; i++) {
			var player = match.games[i].player;
			if (isNaN(Number(player.score))) {
				scoresAreValid = false;
				player.status = 'invalidScore';
			} else {
				players.push(player);
			}
		};

		if (!scoresAreValid) return;

		var data = {players: players, week: $scope.week, group: $scope.groupNumber, table: match.table}
		$http.post('/api/saveGame', data)
			.success(function(data) {
				for (var i in data) {
					var gamePoints = data[i];
					for (var j in match.games) {
						var gameToSave = match.games[j];
						// fix returned data
						if (gameToSave.player.id == gamePoints.id) {
							gameToSave.league_points = gamePoints.league_points;
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
