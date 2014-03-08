from courses.models import create_activity_log_from_drill_logs
from django.contrib.auth.models import AnonymousUser

class GradingMiddleware(object):

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        user_isnt_anon = request.user.is_authenticated()
        request_logs_exist = hasattr(request, 'user_logs_generated')

        # TODO: need to actually set this on the session somewhere
        current_user_goal = request.session.get('current_user_goal', False)

        if request_logs_exist and user_isnt_anon and current_user_goal:
            create_activity_log_from_drill_logs(request.user,
                                                request.user_logs_generated,
                                                current_user_goal=current_user_goal)

        return response

