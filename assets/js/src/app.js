'use scrict';

angular.module('app', ['controllers','ngCookies', 'ngDragDrop'])
.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);