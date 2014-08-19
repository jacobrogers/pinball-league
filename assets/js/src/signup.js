'use strict';

angular.module('controllers')
.controller('SignupCtrl', ['$scope','$http', function($scope,$http) {
    $scope.user = {};

    $scope.submit = function(user) {
        $http.post('/api/signup', $scope.user)
            .success(function(data) {
                $scope.created = true;
                $scope.error = false;
            })
            .error(function(data, status, headers, config) {
                $scope.error = true;
            });
    };
}]);