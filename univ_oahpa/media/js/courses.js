var Courses = angular.module('Courses', ['ngCookies']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

function TooltipController($scope, $http, $element, $cookies) {
    console.log("tracking feedback");
    $scope.model = {};
    $scope.visible_elements = 0;
    $scope.feedbacks = $element.find('.feedback:visible');
    setInterval(function(){
        $scope.feedbacks = $element.find('.feedback:visible');
        console.log("poll");
    }, 1500);

    $scope.$watchCollection('feedbacks', function(n, o) {
        console.log("listening");
        console.log([n, o]);
        console.log($scope.feedbacks);
        $scope.feedbacks = $element.find('.feedback:visible');
    });


}

function GoalController($scope, $http, $element, $cookies) {
    var stats_url = $element.attr('ng-source') ;
    $http.get(stats_url)
         .success(function(data){
             $scope.results = data.results;
             $scope.current_set_count = data.current_set_count;
             $scope.navigated_away = data.navigated_away;
         });
}

