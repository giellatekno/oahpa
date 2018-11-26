/* jshint strict: false */
/* jshint camelcase: false */

var CoursePage = angular.module('CoursePage', ['ngCookies']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

CoursePage.controller('NotificationController', function($scope, $http, $element, $cookies) {
    var notification_url = $element.attr('ng-source') ;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.delete = {};
    $http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;

    $scope.dismissNotification = function(note) {
        var config = {
            withCredentials: true,
        };
        var delete_url = notification_url + note.id + '/';
        $http.delete(delete_url, config).success(function(data) {
            note.deleted = true;
        });
    };

    $http.get(notification_url).success(function(data){
        $scope.notifications = data.results; 
    });

});
