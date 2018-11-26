from rest_framework import viewsets, mixins

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Survey, UserSurvey

from .permissions import *
from .serializers import *

from django.conf import settings
URL_PREFIX = settings.URL_PREFIX

class Auth(object):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

class AnswerView(Auth, viewsets.GenericViewSet, mixins.CreateModelMixin):

    model = UserSurvey
    serializer_class = UserSurveySerializer
    permission_classes = (IsAuthenticated, PostOnly, CanCreateSurvey)

    def pre_save(self, obj):
        obj.user = self.request.user

class SurveyView(Auth, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ This view gets the survey meta data, and survey parameters.
    """

    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, )

    queryset = Survey.objects.all()

    def get_queryset(self):
        """ If non-admin user, return unsurveyed surveys only as
        queryset. """

        from django.db.models import Q

        user = self.request.user

        if user.is_anonymous():
            return []

        qs = self.queryset

        # if not user.is_superuser:
        qs = self.queryset.exclude(responses__user=user,
                                   responses__completed__isnull=False)

        qs = qs.filter(Q(target_course__isnull=True) |
                       Q(target_course__in=user.get_profile().courses))

        # visibility field? 

        return qs

def render_to_response(*args, **kwargs):
    """ Append an attribute onto the response so that we can grab the context
    from it in the track decorator. It has to be an attribute so that it
    doesn't depend on the function returning the response to be decorated by
    @trackGrade to get proper output. """

    from django.shortcuts import render_to_response

    response = render_to_response(*args, **kwargs)
    response.context = args[1]

    return response

from django.template import Context, RequestContext, loader
from django.http import HttpResponse

def answer(request):

    context = {}

    if 'courses_survey_redirect' in request.session:
        redir = '/%s/courses/' % URL_PREFIX
        context['redirect'] = redir
    else:
        context['redirect'] = False

    return render_to_response('survey.html', context,
                           context_instance=RequestContext(request))

def dismiss(request):
    """ Add ignored surveys to the session so that user is not notified.
    """
    if request.method == 'POST':
        if 'ignored_surveys' not in request.session:
            request.session['ignored_surveys'] = []

        new_ids = request.POST.get('ids').split(',')
        request.session['ignored_surveys'].extend(new_ids)

        request.session['ignored_surveys'] = list(set(request.session['ignored_surveys']))

    okay = HttpResponse("Ok", content_type="application/json")
    okay.status_code = 200
    return okay

