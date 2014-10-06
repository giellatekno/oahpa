/* jshint strict: false */
/* jshint camelcase: false */

var Courses = angular.module('Courses', ['ngCookies', 'angular-loading-bar']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });


Courses.controller('ErrorRequester', function($scope, $http, $element, $cookies) {

    function handle_api_response (data) {

        $scope.response = data;

        if(data.messages.length > 0) {
            $scope.messages = data.messages;
            $scope.analyzer = data.fst[0];
            $scope.no_errors = false;
        } else {
            $scope.messages = false;
            $scope.analyzer = false;
            $scope.no_errors = true;
        }

    }

    var feedback_url = $element.attr('data-lookup-url') ;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    if ($element.attr('data-error-watch')) {
        var css_selector = $element.attr('data-error-watch');
    } else {
        var css_selector = "a[data-error-fst]";
    }

    $element.find("form").bind('submit', function ($event) {

        var feedback_data = {
            'lookup': $scope.text_input,
        }
        $scope.no_errors = false;

        if ($scope.task) {
            feedback_data['task'] = $scope.task;
        }

        if ($scope.lemma) {
            feedback_data['intended_lemma'] = $scope.lemma;
        }

        var config = {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        };

        feedback_data = JSON.stringify(feedback_data);

        $http.post(feedback_url, feedback_data, config)
             .success(handle_api_response);
        
    });

    $element.find(css_selector).bind('click', function ($event) {

        // $event.preventDefault();

        var feedback_link = $($event.target);

        function handle_api_feedback_popover (data) {
            handle_api_response(data);

            if (window.last_feedback) {
                last_feedback.popover('destroy');
            }

            var displayed_strings = [];

            if ($scope.analyzer) {
                console.log("fst input: " + $scope.analyzer[0]);
                analyses = $scope.analyzer[1];

                if (analyses) {
                    console.log("fst results:");
                    for (_j = 0, _lenj = analyses.length; _j < _lenj; _j++) {
                        analysis = analyses[_j];
                        lemma = analysis[0];
                        tags = analysis[1];
                        console.log(lemma + "\t" + tags.join('+'));
                    }
                } else {
                    console.log("No analyses from FST.");
                }

            } else {
                console.log("No analyses from FST.");
            }

            if ($scope.messages) {

                // Collect feedback messages.
                // Attempted to do this by injecting an angular template, but
                // it was too tricky.
                var message_body_snippet = "<ul class='errorapi_messages'>";


                for (_i = 0, _len = $scope.messages.length; _i < _len; _i++) {
                    msg = $scope.messages[_i];

                    for (_j = 0, _lenz = msg.message.length; _j < _lenz; _j++) {
                        m = msg.message[_j];
                        message_body_snippet += "<li>" ;
                        if (m.title) {
                            message_body_snippet += m.title + ": " + m.description;
                        }
                        if (m.article) {
                            message_body_snippet += "<br /><a href='" + m.article + ">Klikk for å lese mer</a>";
                        }
                        message_body_snippet += "</li>" ;
                    }

                }
                message_body_snippet += "</ul>";

            } else {
                // TODO: localize
                message_body_snippet = "<p>No feedback available.</p>";
            }

            feedback_link.popover({
                title: 'Feedback',
                content: message_body_snippet,
                html: true,
                trigger: 'click focus',
            });
            feedback_link.popover('show');
            window.last_feedback = feedback_link;
        }

        // Prepare request
        var form  = $(feedback_link).attr('data-input-form') || $(feedback_link).html();
        var task  = $(feedback_link).attr('data-task');
        var lemma = $(feedback_link).attr('data-lemma');

        console.log("sending <task: " + task + "; intended lemma: " + lemma + "; user input: " + form + '>');

        // JSON? 
        var feedback_data = {
            'lookup': form,
        }

        if (task) {
            feedback_data['task'] = task;
        }

        if (lemma) {
            feedback_data['intended_lemma'] = lemma;
        }

        var config = {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        };

        feedback_data = JSON.stringify(feedback_data);

        $http.post(feedback_url, feedback_data, config)
             .success(handle_api_feedback_popover);

        return true;

    }); // click event

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
