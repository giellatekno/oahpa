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
        if request.session.get('set_completed', False):
            request.session['question_try_count'] = {}
            request.session['question_set_count'] += 1
            request.session['answered'] = {}

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        from .models import Goal, UserGoalInstance

        if not hasattr(request, 'graded_view'):
            return response

        user_isnt_anon = request.user.is_authenticated()
        request_logs_exist = hasattr(request, 'user_logs_generated')

        # TODO: need to actually set this on the session somewhere
        current_user_goal = request.session.get('current_user_goal', False)

        if request_logs_exist and user_isnt_anon and current_user_goal:
            current = request.session.get('current_exercise_params', False)
            previous = request.session.get('previous_exercise_params', False)
            print (current, previous)
            # This test is sometimes wrong when switching in and out of
            # a goal.
            if current and previous:
                if current != previous:
                    print " -- user navigated to new page, stop tracking --"
                    request.session['previous_exercise_params'] = current
                    del request.session['current_user_goal']
                    del request.session['current_exercise_params']
                    del request.session['previous_exercise_params']
                    return response

            self.increment_session_answer_counts(request)

            create_activity_log_from_drill_logs(request, request.user,
                                                request.user_logs_generated,
                                                current_user_goal=current_user_goal)

            self.reset_increments(request)

            goal = Goal.objects.get(id=current_user_goal)
            # TODO: this is for debug only.
            result = goal.evaluate_for_student(request.user)

            user_goal_instance = UserGoalInstance.objects.filter(user=request.user, goal=goal)
            if not user_goal_instance:
                UserGoalInstance.objects.create(user=request.user,
                                                goal=goal, **result)
            else:
                user_goal_instance.update(**result)

            print user_goal_instance

        request.session['previous_exercise_params'] = \
                request.session.get('current_exercise_params', False)

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
