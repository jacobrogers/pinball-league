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
}])
.controller('FinishAccountSetupCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
    console.log('finishing account setup ' + $routeParams.token);

    $http.get('/api/lookupConfirmation/'+$routeParams.token)
        .success(function(data) {
            $scope.user = data;
        }).error(function(data,status,headers,config) {
            $scope.error = true;
        });

    $scope.submit = function(user) {
        if (user.password === user.confirmPassword) {
            $http.post('api/confirm_account/'+$routeParams.token, $scope.user)
                .success(function(data) {

                })
                .error(function(data, status, headers, config) {
                    $scope.error = true;
                });
        }
    };
}]);