var Courses = angular.module('Courses', []).
    config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
    });


// TODO: generalize API url
function GoalController($scope, $http) {
    $http.get('/davvi/courses/stats/')
         .success(function(data){
             $scope.results = data.results;
         });
}
