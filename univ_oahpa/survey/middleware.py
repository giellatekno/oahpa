""" Middleware for checking whether any surveys are available, and
notifying the user.
"""

from courses.models import create_activity_log_from_drill_logs
from django.contrib.auth.models import AnonymousUser

from .models import Survey

class SurveyCheckMiddleware(object):

    check_increment = 2

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ Mark view as counting for survey check purposes.
        """

        setattr(request, 'survey_check_view', False)

        admin_page = view_func.__module__.startswith('django.contrib.admin.')
        static_page = view_func.__module__ == 'django.views.static'
        json_request = 'application/json' in request.META['HTTP_ACCEPT']

        if any([admin_page, static_page, json_request]):
            setattr(request, 'survey_check_view', False)
        else:
            setattr(request, 'survey_check_view', True)

    def process_response(self, request, response):
        """ Here the goal is to process the grading that pertains to the
        user's current activity, which is marked on the session object,
        and store it in the courses activity log model. """

        # If there's no session, we can't do anything
        if not hasattr(request, 'session'):
            return response

        if hasattr(request, 'survey_check_view'):
            if request.survey_check_view == False:
                return response

        if 'ignored_surveys' not in request.session:
            ignored = request.session['ignored_surveys'] = []
        else:
            ignored = request.session['ignored_surveys']

        if 'survey_check' not in request.session:
            request.session['survey_check'] = 0
        else:
            request.session['survey_check'] += 1

        if request.session['survey_check'] % self.check_increment == 0:
            request.session['survey_check'] = 0
        else:
            try: del request.session['display_survey_notice']
            except: pass
            try: del request.session['survey_ids_available']
            except: pass

            return response

        # TODO: allow user to opt out of being alerted for individual
        # surveys (store in session)

        u = request.user

        # Assuming one response per survey
        responses = Survey.objects.exclude(id__in=ignored)\
                                  .filter(responses__user=u)

        unanswered = Survey.objects.exclude(id__in=ignored)\
                                   .exclude(responses__user=u)

        responses_count = responses.count()

        surveys = Survey.objects.all().count()
        survey_ids_available = ','.join(map(str, unanswered.values_list('id', flat=True)))

        if len(unanswered) > 0:
            # "User can fill out survey."
            print 'survey displayed'
            request.session['display_survey_notice'] = True
            request.session['survey_ids_available'] = survey_ids_available 
        else:
            # "User has no surveys"
            request.session['display_survey_notice'] = False

        return response

# vim: set ts=4 sw=4 tw=72 syntax=python :
