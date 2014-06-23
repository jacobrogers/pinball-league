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
.controller('IndexCtrl', ['$scope','$http', function($scope,$http) {
    $http.get('/api/overview')
        .success(function(data) {
            $scope.hasRankings = data.rankings.length > 0;
            $scope.rankings = data.rankings;
            $scope.week = data.week;
        });
}])
.controller('NavCtrl', ['$scope', '$location', function($scope, $location) {
	$scope.navClass = function (page) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page === currentRoute ? 'active' : '';
    };        
}]);

angular.module('controllers', []);