var app = angular.module('main', ['ngTable']).

controller('DemoCtrl', function($scope, $http) {

    $http.get('/issues').
        success(function(data, status, headers, config) {
            $scope.users = data;
        }).
        error(function(data, status, headers, config) {
            console.log(status);
        });
});