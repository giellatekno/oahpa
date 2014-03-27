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

function GoalConstructorController($scope, $http, $element, $cookies) {
    var params_url = $element.attr('ng-source') ;

    $scope.main_type = 'numra';
    $scope.user_goal = {};
    $scope.form_submitted = false;
    $scope.form_success = false;
    $scope.editing_existing = false;

    $scope.reset = function() {
        $scope.user_goal.params = {};
    }

    $scope.beginGoal = function() {
        window.location = window.location.origin + $scope.goal.begin_url ;
    }

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;

    $http.get(params_url)
         .success(function(data){
             $scope.existing_goals = data.goals;
         });

    $http({method: 'OPTIONS', url: params_url})
         .success(function(data){
             $scope.results = data.parameters;
             var k, list, v;

             $scope.main_types = (function() {
               var _results;
               _results = [];
               for (k in data.parameters.tree) {
                 v = data.parameters.tree[k];
                 _results.push({'label': data.parameters.tree[k].label, 'value': k});
               }
               return _results;
             })();

             $scope.tree = data.parameters.tree;
             $scope.option_values = data.parameters.values;
             $scope.instructor_courses = data.courses;
         });

    $scope.deleteGoal = function() {
       var config = {
           withCredentials: true,
       };
       var delete_url = params_url + $scope.edit_goal_id + '/' ;
       $http.delete(delete_url, config)
            .success( function(data) {
                console.log(data);
            });
    }

    // TODO: fail behavior
    $scope.submitForm = function() {
        // disable form while submit happens
        // show loading thing
        // provide user link to begin their newly created event (return
        // ID)
        var config = {
            withCredentials: true,
        };
        $scope.form_submitted = true;
        // TODO: what do for edit existing?
        // $scope.editing_existing;

        if ($scope.editing_existing) {
           var update_url = params_url + $scope.edit_goal_id + '/' ;
           $http.put(update_url, $scope.user_goal, config)
                .success( function(data) {
                    $scope.form_success = true;
                    if (!data.success) {
                        // TODO: add some error spans to form
                        $scope.errorName = data.errors.name;
                        // other errors go here.

                    } else {
                        $scope.message = data.message;
                        $scope.goal = data.goal;
                    }
                });

        } else {
            $http.post(params_url, $scope.user_goal, config)
             .success( function(data) {
                $scope.form_success = true;
                if (!data.success) {
                    // TODO: add some error spans to form
                    $scope.errorName = data.errors.name;
                    // other errors go here.

                } else {
                    $scope.message = data.message;
                    $scope.goal = data.goal;
                }
            });
       }
    };

    $scope.populateGoal = function() {
        // TODO: need params returned
       var get_url = params_url + $scope.edit_goal_id + '/' ;
        
        $http.get(get_url)
             .success( function(data){
                 // TODO: allow user to restore this
                 $scope.user_goal_create = $scope.user_goal ;
                 $scope.user_goal = data ;
                 $scope.editing_existing = true;
             })

    }

}
