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

        # Increment the session variable for attempts on the whole set
        if 'question_set_count' in request.session:
            request.session['question_set_count'] += 1
        else:
            request.session['question_set_count'] = 1

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
        if request.session.get('set_completed', False):
            request.session['question_try_count'] = {}
            request.session['question_set_count'] = 1
            request.session['answered'] = {}

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        if not hasattr(request, 'graded_view'):
            return response

        user_isnt_anon = request.user.is_authenticated()
        request_logs_exist = hasattr(request, 'user_logs_generated')

        # TODO: need to actually set this on the session somewhere
        current_user_goal = request.session.get('current_user_goal', False)

        if request_logs_exist and user_isnt_anon and current_user_goal:
            self.increment_session_answer_counts(request)

            create_activity_log_from_drill_logs(request, request.user,
                                                request.user_logs_generated,
                                                current_user_goal=current_user_goal)

            self.reset_increments(request)

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
