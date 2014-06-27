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
    // var feedback_url = $element.attr('ng-source') ;
    var feedback_url = "/davvi/errorapi/lookup/";

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    $element.find('ul.samples a').bind('click', function($event){
        var feedback_link = $($event.target).parents('a');
        var form = $(feedback_link).html()
        console.log(form);

    
        // JSON? 
        var feedback_data = {
            'lookup': form,
        }
        var config = {
            withCredentials: true,
        };

        $http.post(feedback_url, feedback_data, config)
         .success( function(data) {
             console.log(data);
         });

    });

    // $http.get(feedback_url).success(function(data){

    //     $scope.registerFeedback = function() {
    //         console.log('click');
    //     };

    // });

});
