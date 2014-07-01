/* jshint strict: false */
/* jshint camelcase: false */

var ErrorAPI = angular.module('ErrorAPI', ['ngCookies']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });


ErrorAPI.controller('ErrorRequester', function($scope, $http, $element, $cookies) {
    var feedback_url = $element.attr('data-lookup-url') ;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    if ($element.attr('data-error-watch')) {
        var css_selector = $element.attr('data-error-watch');
    } else {
        var css_selector = "a[data-error-fst]";
    }

    // $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    console.log(css_selector);
    console.log("watching:");
    console.log($element.find(css_selector)) ;

    $element.find(css_selector).bind('click', function($event){

        $event.preventDefault();

        console.log($event);
        console.log($event.target);

        var feedback_link = $($event.target).parents('a');

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
            feedback_data['lemma'] = lemma;
        }

        console.log([form, task, lemma]);
    
        var config = {
            withCredentials: true,
        };

        $http.post(feedback_url, feedback_data, config)
             .success( function(data) {
                 console.log(data);
             });

    });

});
