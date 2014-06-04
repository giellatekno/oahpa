/* jshint strict: false */
/* jshint camelcase: false */

var Courses = angular.module('Courses', ['ngCookies']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

// Feedback
// idea:
// http://stackoverflow.com/questions/14574365/angularjs-dropdown-directive-hide-when-clicking-outside
//
Courses.controller('TooltipController', function($scope, $http, $element, $cookies) {
    var feedback_url = $element.attr('ng-source') ;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.delete = {};
    $http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;

    $element.find('.feedback_link').bind('click', function($event){
        var feedback_link = $($event.target).parents('.feedback_link');

        var feedback_count = feedback_link.attr('id').split('_')[1].split('-')[1];

        var feedback_id = '#feedback-' + feedback_count;
        var feedback_div = $(document).find(feedback_id);
        var feedback_msg_ids = $(feedback_div).attr('data-feedback-msgids');

        var answer_id = feedback_count + '-answer';

        var user_input = $(document).find('input[name=' + answer_id + ']').val();
        var correct_answer = $(document).find('a#link_tooltip-' + feedback_count).html();

        // msg_ids, question id in set, question lemma, current user input.

        var feedback_data = []
          , feedback_names = feedback_msg_ids.split(',');
    
        for (i = 0, _len = feedback_names.length; i < _len; i++) {
            var msg = feedback_names[i];
            feedback_data.push({
                feedback_texts: msg, 
                user_input: user_input, 
                correct_answer: correct_answer
            });
        };

        var config = {
            withCredentials: true,
        };

        $http.post(feedback_url, feedback_data, config)
         .success( function(data) {
            console.log("logged feedback");
         });

    });

    $http.get(feedback_url).success(function(data){

        $scope.registerFeedback = function() {
            console.log('click');
        };

    });

    $scope.model = {};

});

Courses.controller('GoalController', function($scope, $http, $element, $cookies) {
    var stats_url = $element.attr('ng-source') ;

    $http.get(stats_url).success(function(data){
         $scope.success = data.results;
         if (data.results.length == 0) {
             return false;
         }
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
             $scope.progress_percent = ($scope.current_set_count / $scope.max_rounds) * 100;
             if ($scope.progress_percent > 100) {
                $scope.progress_percent = 100;
             }
             if ($scope.current_set_count < $scope.max_rounds) {
                 $scope.progress_class = 'progress-bar-warning';
             }
             if ($scope.current_set_count === $scope.max_rounds) {
                 $scope.progress_class = 'progress-bar-success';
             }
         }
     });
});
