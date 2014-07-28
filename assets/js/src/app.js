'use scrict';

angular.module('app', ['ngCookies','ngRoute','controllers', 'config'], function($routeProvider) {
	var route = function(path, partial, controller) {
		$routeProvider.when(path, {templateUrl: '/static/partials/'+partial, controller: controller});
	};
	route('/tables', 'tables.html', 'TablesCtrl');
	route('/players', 'players.html', 'PlayersCtrl');
	route('/createWeek/:week', 'create_week.html', 'CreateWeekCtrl');
	route('/week/:week/group/:group', 'group.html', 'GroupCtrl');
	route('/week/:week', 'week.html', 'WeekCtrl');
	route('/', 'index.html', 'IndexCtrl');
	$routeProvider.otherwise({redirectTo: '/'});
})
.service('$weekService', function() {
    var _weeks = [];
    var _nextWeek = 0;
    var getWeeks = function() { return _weeks; };
    var addWeek = function(week) {
        _weeks.push(week);
        _nextWeek = parseInt(week)+1;
    };
    var getNextWeek = function() {
        return _weeks.length+1;
    };
    return { getWeeks: getWeeks, addWeek: addWeek, getNextWeek: getNextWeek };
})
.controller('IndexCtrl', ['$scope','$http', function($scope,$http) {
    $http.get('/api/overview')
        .success(function(data) {
            $scope.hasRankings = data.rankings.length > 0;
            $scope.rankings = data.rankings;
            $scope.week = data.week;
        });
}])
.controller('NavCtrl', ['$scope', '$location', '$weekService', function($scope, $location, $weekService) {
	$scope.navClass = function (page) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page === currentRoute ? 'active' : '';
    };
    $scope.weeks = $weekService.getWeeks();
    $scope.createNextWeek = function() {
        var nextWeek = $weekService.getNextWeek();
        $location.path('/createWeek/'+nextWeek);
    }
    $scope.init = function(weeks) {
        for (var i=1; i<=weeks; i++) 
            $weekService.addWeek(weeks[i]);
    };
}]);

angular.module('controllers', []);