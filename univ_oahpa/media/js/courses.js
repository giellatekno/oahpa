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
             $scope.success = data.results;
             $scope.goal = data.results[0];
             $scope.current_set_count = data.current_set_count;
             $scope.navigated_away = data.navigated_away;
             $scope.max_rounds = data.max_rounds;
             $scope.goal.rounded = Math.round($scope.goal.progress);
             $scope.correct_threshold = data.correct_threshold;
             $scope.progress_class = 'progress-bar-info';
             if ($scope.goal.progress >= $scope.correct_threshold) {
                 $scope.above = true;
             } else {
                 $scope.above = false;
             }
             if ($scope.max_rounds) {
                 $scope.progress_percent = ($scope.current_set_count - 1 / $scope.max_rounds) * 100;
                 if ($scope.progress_percent > 100) {
                    $scope.progress_percent = 100;
                 }
                 if ($scope.current_set_count < $scope.max_rounds) {
                     $scope.progress_class = 'progress-bar-warning';
                 }
                 if ($scope.current_set_count == $scope.max_rounds) {
                     $scope.progress_class = 'progress-bar-success';
                 }
             }
         });
}

