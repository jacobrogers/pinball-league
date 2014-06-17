'use scrict';

angular.module('app', ['ngCookies','ngRoute','controllers', 'config'], function($routeProvider) {
	var route = function(path, partial, controller) {
		$routeProvider.when(path, {templateUrl: '/static/partials/'+partial, controller: controller});
	};

	route('/tables', 'tables.html', 'TablesCtrl');
	route('/players', 'players.html', 'PlayersCtrl');
	route('/createGroups', 'create_week.html', 'CreateWeekCtrl');
	route('/week/:week/group/:group', 'group.html', 'GroupCtrl');
	route('/week/:week', 'week.html', 'WeekCtrl');
	route('/', 'index.html', 'IndexCtrl');
	$routeProvider.otherwise({redirectTo: '/'});
})
.controller('IndexCtrl', ['$scope', function($scope) {
}])
.controller('NavCtrl', ['$scope', '$location', function($scope, $location) {
	$scope.navClass = function (page) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page === currentRoute ? 'active' : '';
    };        
}]);

angular.module('controllers', []);