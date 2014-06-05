'use scrict';

angular.module('app', ['ngCookies'])
.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}])
.config(['$httpProvider',function($httpProvider) {
	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
}])
.run(['$http', '$cookies', function( $http, $cookies ){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
}])
.controller('CreateGroupsCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.groups = [];
	$scope.week = 1;

	$http.get('/api/players').success(function(data) {
		$scope.players = data;
	});
	$http.get('/api/tables').success(function(data) {
		$scope.tables = data;
	});

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
			group.selectedTable = null;
		}
	};	

	$scope.removeTable = function(group, table) {
		remove(group.tables, table);
		$scope.tables.push(table);
	};

	$scope.addGroup = function() {
		$scope.groups.push({players: [], tables: []});
	};

	$scope.removeGroup = function(group) {
		for (var i in group.players) {
			$scope.players.push(group.players[i]);
		}
		remove($scope.groups, group);
	};

	$scope.saveGroups = function() {
		for (i in $scope.groups) {
			delete $scope.groups[i].selectedPlayer;
			delete $scope.groups[i].selectedTable;
		}
		$http.post('/api/saveGroups', {week: $scope.week, groups: $scope.groups})
			.success(function(data) {
				console.log('saved');
			});
	};
}]);;