'use scrict';

angular.module('app', ['ngCookies','controllers'])
.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}])
.config(['$httpProvider',function($httpProvider) {
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
}])
.run(['$http', '$cookies', function( $http, $cookies ){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
}]);;

angular.module('controllers', []);