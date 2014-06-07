'use scrict';

angular.module('app', ['ngCookies','ngRoute','controllers', 'config', 'navMenu'], function($routeProvider) {
	var route = function(path, partial, controller) {
		$routeProvider.when(path, {templateUrl: '/static/partials/'+partial, controller: controller});		
	};

	route('/tables', 'tables.html', 'TablesCtrl');
	route('/players', 'players.html', 'PlayersCtrl');
	route('/createGroups', 'create_group.html', 'CreateGroupsCtrl');
	route('/', 'index.html', 'IndexCtrl');
	$routeProvider.otherwise({redirectTo: '/'});
})
.controller('IndexCtrl', ['$scope', function($scope) {
}]);

angular.module('controllers', []);