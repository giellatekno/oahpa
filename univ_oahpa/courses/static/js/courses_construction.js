/* jshint strict: false */
/* jshint camelcase: false */

function listContainsObject(_list, _obj, field) {
    for (var i = 0; i < _list.length; i++) {
        if(_list[i][field] === _obj[field]) {
            return i;
        }
    }
    return -1;
}

// TODO: http://stackoverflow.com/questions/20181323/passing-data-between-controllers-in-angular-js
//   when a task is created, need to broadcast it to the
//   CourseGoalController for inclusion in the list.

var CoursesConstruction = angular.module('CoursesConstruction', ['ngCookies', 'ui.sortable', 'ngDialog']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

function applyHeaderToken($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.delete = {};
    $http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;
    return $http;
}

function CourseGoalConstructorController($scope, $http, $element, $cookies, ngDialog) {
    'use strict';

    var coursegoal_url = $element.attr('ng-source-coursegoal') ;
    var goal_url = $element.attr('ng-source-goal') ;

    $scope.course_goal = {};
    $scope.orderable_goals = [];
    $scope.sorting = [];
    $scope.not_in_use = [];
    $scope.edit = false;
    $scope.intermediate = false;
    $scope.adding_sub_goal = false;

    $scope.sortableOptions = {
        placeholder: "sortable-placeholder",
        connectWith: ".connected-sorting",
    };

    $scope.newTaskPopup = function(e) {
        
        ngDialog.open({
            template: "add/goal/?dialog=True",
            preCloseCallback: function(value) {
                // Refresh task list with the new item
                $http.get(goal_url).success(function(data){
                    $scope.not_in_use = [];
                    for (var i = 0; i < data.goals.length; i++) {
                        var goal = data.goals[i];
                    
                        $scope.not_in_use.push({
                            text: goal.short_name,
                            assigned: goal.assigned,
                            id: goal.id,
                            value: i+1
                        });
                    }
                });
            }
        });
        
    };

    // $http = applyHeaderToken($http, $cookies);
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.delete = {};
    $http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;

    // This is the ng-change function for the existing course goal selector.
    $scope.populateGoal = function() {

        // If this is null, clear things and return
        if ($scope.edit_goal_id === null) {
           $scope.course_goal = {};
           $scope.intermediate = false;
           $scope.edit = false;

            // Re-add all the goals that we grabbed while
            // initializing
            for (var i = 0; i < $scope.goals.length; i++) {
                var goal = $scope.goals[i];
                console.log(goal);

                $scope.not_in_use.push({
                    text: goal.short_name,
                    assigned: goal.assigned,
                    id: goal.id,
                    value: i+1
                });
            }

           return false;
        }

        var get_url = coursegoal_url + $scope.edit_goal_id + '/' ;

        if ($scope.edit_goal_id !== undefined) {
            $http.get(get_url).success( function(data){

                // TODO: allow user to restore this
                $scope.course_goal_create = $scope.user_goal ;
                $scope.course_goal = data ;
                $scope.intermediate = true;
                $scope.edit = true;

                $scope.sorting = [];
                $scope.not_in_use = [];

                // Re-add all the goals that we grabbed while
                // initializing
                for (var i = 0; i < $scope.goals.length; i++) {
                    var goal = $scope.goals[i];

                    $scope.not_in_use.push({
                        text: goal.short_name,
                        assigned: goal.assigned,
                        id: goal.id,
                        value: i+1
                    });
                }

                // Now iterate through the response goals, if they're
                // assigned already, remove from $scope.not_in_use
                for (var i = 0; i < data.goals.length; i++) {

                    var goal = data.goals[i];

                    var item = {
                        text: goal.short_name,
                        assigned: goal.assigned,
                        id: goal.id,
                        value: i+1
                    };
                    console.log(item);

                    var ind_of = listContainsObject($scope.not_in_use, item, 'id');

                    if (ind_of >= -1) {
                      $scope.not_in_use.pop(ind_of);
                    }

                    $scope.sorting.push(item);
                }

            });
        }
    };

    $scope.submitForm = function() {
        var config = {
            withCredentials: true,
        };

        $http.post(coursegoal_url, $scope.course_goal, config)
         .success( function(data) {
            if (!data.success) {
                // TODO: add some error spans to form
                $scope.errorName = data.errors.name;
                // other errors go here.

            } else {
                $scope.created = true;
                $scope.edit = true;
                $scope.message = data.message;
                $scope.created_goal = data.goal;
                $scope.course_goal.id = data.id;
            }
        });
    };

    $scope.refresh = function() {
        location.reload();
    };

    $scope.deleteCourseGoal = function() {
        var config = {
            withCredentials: true,
        };

        var delete_url = coursegoal_url + $scope.course_goal.id + '/' ;

        $http.delete(delete_url, config).success( function(data) {
            $scope.deleted = true;
            $scope.goal_deleted = true;
            $scope.edit = false;
            $scope.finalized = true;
        });
    };

    $scope.saveSorting = function() {
        $scope.course_goal.goals  = [];

        for (var i = 0; i < $scope.sorting.length; i++) {
            var obj = $scope.sorting[i];
            $scope.course_goal.goals.push(obj.id);
        }
        
        var config = {
            withCredentials: true,
        };

        var update_url = coursegoal_url + $scope.course_goal.id + '/' ;
        $http.put(update_url, $scope.course_goal, config).success( function(data) {
            if (!data.success) {
                $scope.errorName = data.errors;
            } else {
                $scope.finalized = true;
            }
        });
    };

    // Get existing course goals that user has access to.
    $http.get(coursegoal_url).success(function(data){
        $scope.coursegoals = data.results;

    });

    // Get available courses and other options
    $http({method: 'OPTIONS', url: coursegoal_url}).success(function(data){
        $scope.courses = data.courses;
    });

    // Push the Tasks that the user has access to into the not in use box.
    $http.get(goal_url).success(function(data){
        $scope.goals = data.goals;
        for (var i = 0; i < data.goals.length; i++) {
            var goal = data.goals[i];
        
            $scope.not_in_use.push({
                text: goal.short_name,
                assigned: goal.assigned,
                id: goal.id,
                value: i+1
            });
        }
    });

}

function TaskConstructorController($scope, $http, $element, $cookies) {
    var params_url = $element.attr('ng-source') ;

    var default_new_goal = {
        threshold: 80,
        minimum_sets_attempted: 5,
    };

    $scope.main_type = 'numra';
    $scope.user_goal = default_new_goal;
    $scope.form_submitted = false;
    $scope.form_success = false;
    $scope.editing_existing = false;

    $scope.goal_created = false;
    $scope.goal_edited = false;
    $scope.goal_deleted = false;

    $scope.reset = function() {
        $scope.user_goal.params = {};
    };

    $scope.beginGoal = function() {
        window.location = window.location.origin + $scope.goal.begin_url ;
    };

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.delete = {};
    $http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;

    // Get user's goals
    $http.get(params_url)
         .success(function(data){
             $scope.existing_goals = data.goals;
             $scope.goal_deleted = false;
         });

    // Get all the parameters for the form
    $http({method: 'OPTIONS', url: params_url})
         .success(function(data){
             $scope.results = data.parameters;

             $scope.main_types = (function() {
               var _results;
               _results = [];
               for (var k in data.parameters.tree) {
                 _results.push({'label': data.parameters.tree[k].label, 'value': k});
               }
               return _results;
             })();

             $scope.tree = data.parameters.tree;
             $scope.option_values = data.parameters.values;
             $scope.instructor_courses = data.courses;
         });

    // Delete a goal
    $scope.deleteGoal = function() {
       var config = {
           withCredentials: true,
       };
       var delete_url = params_url + $scope.edit_goal_id + '/' ;
       $http.delete(delete_url, config)
            .success(function() {
                $scope.goal_deleted = true;
                $scope.goal_edited = false;
                $scope.goal_created = false;
                $scope.form_success = true;
            });
    };

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
        //
        var p, v;
        var cleaned_params = {};

        var params = $scope.user_goal.params;
        console.log(params);

        for (p in params) {
          v = params[p];
          if (v === false) {
            continue;
          } else {
            cleaned_params[p] = v;
          }
        }

        $scope.user_goal.params = cleaned_params;

        if ($scope.editing_existing) {
           var update_url = params_url + $scope.edit_goal_id + '/' ;
           console.log($scope.user_goal);
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
                        $scope.goal_edited = true;
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
                    $scope.goal_created = true;
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
             });

    };


}
