from courses.models import create_activity_log_from_drill_logs
from django.contrib.auth.models import AnonymousUser

class GradingMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ Mark view as being able to be graded or not.
        """

        setattr(request, 'graded_view', False)

        if view_func.__module__.startswith('django.contrib.admin.'):
            setattr(request, 'graded_view', False)
        else:
            setattr(request, 'graded_view', True)

    def increment_session_answer_counts(self, request):
        # If all_correct or all_complete

        # NB: Incrementing the session variable for set tried happens in
        # reset_increments
        # if 'question_set_count' in request.session:
        #     request.session['question_set_count'] += 1
        # else:
        #     request.session['question_set_count'] = 1

        # Increment individual question/answer tries
        for log in request.user_logs_generated:
            if log.correct in request.session['question_try_count']:
                # Increment and add to answered, thus count stops
                # incrementing after this round.
                if not request.session['answered'].get(log.correct,
                                                       False):
                    request.session['question_try_count'][log.correct] += 1
                    request.session['answered'][log.correct] = True
                else:
                    pass
            else:
                request.session['question_try_count'][log.correct] = 1

        request.session.modified = True
        return request

    def reset_increments(self, request):
        # If 'set_completed' is in the session variable, 
        # then need to clear variables for the next go around.
        # TODO: also increment on 'new set'
        new_set = request.session.get('new_game')
        prev_new_set = request.session['prev_new_game']
        new_sets = new_set and prev_new_set
        print 'new sets: ' + repr(new_sets)

        if request.session.get('set_completed', False) or new_sets:
            request.session['question_try_count'] = {}
            request.session['question_set_count'] += 1
            request.session['answered'] = {}

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        from .models import Goal, UserGoalInstance

        if not hasattr(request, 'session'):
            return response

        if request.session.get('navigated_away', False):
            if request.session['navigated_away'] > 0:
                request.session['navigated_away'] += 1
            if request.session['navigated_away'] > 2:
                request.session['navigated_away'] = 0

        if not hasattr(request, 'graded_view'):
            return response

        user_isnt_anon = request.user.is_authenticated()
        request_logs_exist = hasattr(request, 'user_logs_generated')

        # TODO: need to actually set this on the session somewhere
        current_user_goal = request.session.get('current_user_goal', False)

        if request_logs_exist and user_isnt_anon and current_user_goal:
            current = request.session.get('current_exercise_params', False)
            previous = request.session.get('previous_exercise_params', False)
            # This test is sometimes wrong when switching in and out of
            # a goal.
            if current and previous:
                if current != previous:
                    print " -- user navigated to new page, stop tracking --"

                    user_goal_instance = UserGoalInstance.objects.filter( user=request.user
                                                                        , id=current_user_goal
                                                                        , opened=True
                                                                        )\
                                                                 .order_by('-last_attempt')

                    # Mark this instance as no longer being active.
                    if user_goal_instance is not None:
                        user_goal_instance[0].opened = False
                        user_goal_instance[0].save()

                    request.session['previous_exercise_params'] = current
                    del request.session['current_user_goal']
                    del request.session['current_exercise_params']
                    del request.session['previous_exercise_params']
                    if request.session.get('navigated_away', False):
                        request.session['navigated_away'] += 1
                    return response

            self.increment_session_answer_counts(request)

            create_activity_log_from_drill_logs(request, request.user,
                                                request.user_logs_generated,
                                                current_user_goal=current_user_goal)

            self.reset_increments(request)

            ugi = UserGoalInstance.objects.get(id=current_user_goal)
            goal = ugi.goal

            # TODO: this is for debug only.
            result = ugi.evaluate_instance()

            if result is not None:
                user_goal_instance = UserGoalInstance.objects.filter(user=request.user, goal=goal, opened=True)
                if not user_goal_instance:
                    UserGoalInstance.objects.create(user=request.user,
                                                    goal=goal, **result)
                else:
                    user_goal_instance.update(**result)

                complete = goal.is_complete(user_goal_instance[0])
                print 'completed? ' + repr(complete)
                print 'new-game? ' + repr(request.session['new_game'])

        request.session['previous_exercise_params'] = \
                request.session.get('current_exercise_params', False)

        request.session['prev_new_game'] = \
                request.session.get('new_game', False)

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
