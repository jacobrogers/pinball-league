'use strict';

angular.module('controllers')
.controller('SetupWeekCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.groups = $scope.players = [];

	$scope.init = function(week) {
		$scope.week = week;
		$http.get('/api/setupWeek/'+week).success(function(data) {
			$scope.tables = data.tables;
			if ($scope.week == 1) {
				$scope.players = data.players;
			} else {
				for (var i in data.groups) {
					var group = data.groups[i];
					$scope.groups.push({players: group.players, tables: group.tables, availableTables: group.availableTables});
				}
				$scope.players = data.players;
			}
		});
	};

	var tablesCopy = function() {
		var availableTables = [];
		for (var i in $scope.tables)
			availableTables.push($scope.tables[i]);
		return availableTables;

	}
	var remove = function(array, value) {
		var i = array.indexOf(value);
		if(i != -1) array.splice(i, 1);
	};

	$scope.addPlayer = function(group) {
		group.players.push(group.selectedPlayer);
		remove($scope.players, group.selectedPlayer);
		group.selectedPlayer = null;
	};	

	$scope.removePlayer = function(group, player) {
		remove(group.players, player);
		$scope.players.push(player);
	};

	$scope.addTable = function(group) {
		if (group.tables.indexOf(group.selectedTable) < 0) {
			group.tables.push(group.selectedTable);
			remove(group.availableTables, group.selectedTable);
			group.selectedTable = null;
		}
	};	

	$scope.removeTable = function(group, table) {
		remove(group.tables, table);
		group.availableTables.push(table);
	};

	$scope.addGroup = function() {
		$scope.groups.push({players: [], tables: [], availableTables: tablesCopy()});
	};

	$scope.removeGroup = function(group) {
		for (var i in group.players) {
			$scope.players.push(group.players[i]);
		}
		remove($scope.groups, group);
	};

	var findRank = function(group, player) {
		var rank = 0, groupIndex = $scope.groups.indexOf(group);
		for (var i=0; i<=groupIndex; i++) {
			var players = $scope.groups[i].players;
			if (i!==groupIndex) {
				rank += players.length;
			} else {
				rank += players.indexOf(player) + 1;
			}
		}
		return rank;
	};

	$scope.allTablesAssigned = true;
	$scope.noGroups = false;

	$scope.saveGroups = function() {

		if ($scope.groups.length === 0) {
			$scope.noGroups = true;
			return;
		}
		for (var i in $scope.groups) {
			var group = $scope.groups[i];
			if (group.tables.length === 0) {
				$scope.allTablesAssigned = false;
				return;
			}
		}

		for (var i in $scope.groups) {
			delete group.selectedPlayer;
			delete group.selectedTable;
			delete group.availableTables;

			var group = $scope.groups[i];
			for (var j in group.players) {
				var player = group.players[j];
				player.rank = findRank(group, player);
			}
		}
		$http.post('/api/setupWeek/'+$scope.week, {groups: $scope.groups})
			.success(function(data) {
				$scope.weekSetup = true;
			})
			.error(function(data, status, headers, config) {
				$scope.error = true;
			});
	};
}])