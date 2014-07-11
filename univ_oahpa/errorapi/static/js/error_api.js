/* jshint strict: false */
/* jshint camelcase: false */

var ErrorAPI = angular.module('ErrorAPI', ['ngCookies', 'angular-loading-bar']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });



ErrorAPI.controller('ErrorRequester', function($scope, $http, $element, $cookies) {
    function handle_api_response (data) {
        $scope.response = data;
        if(data.messages.length > 0) {
            $scope.messages = data.messages;
            $scope.analyzer = data.fst[0];
            $scope.no_errors = false;
        } else {
            $scope.messages = false;
            $scope.analyzer = false
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

    $element.find("form").bind('submit', function($event){

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

    $element.find(css_selector).bind('click', function($event){

        $event.preventDefault();

        var feedback_link = $($event.target);

        // Prepare request
        var form  = $(feedback_link).html();
        var task  = $(feedback_link).attr('data-task');
        var lemma = $(feedback_link).attr('data-lemma');

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

        console.log([form, task, lemma]);
    
        var config = {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        };

        feedback_data = JSON.stringify(feedback_data);

        $http.post(feedback_url, feedback_data, config)
             .success(handle_api_response);

    });

});
