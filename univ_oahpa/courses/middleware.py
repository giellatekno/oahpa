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

        print "all_correct: " + repr(request.session.get('all_correct', False))
        print "set_completed: " + repr(request.session.get('set_completed', False))

        if request_logs_exist and user_isnt_anon and current_user_goal:
            create_activity_log_from_drill_logs(request.user,
                                                request.user_logs_generated,
                                                current_user_goal=current_user_goal)

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
