from rest_framework import viewsets, mixins

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Survey, UserSurvey

from .permissions import *
from .serializers import *

class Auth(object):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

# TODO: PostOnly permission, remove list mixins
class AnswerView(Auth, viewsets.GenericViewSet, mixins.CreateModelMixin):

    model = UserSurvey
    serializer_class = UserSurveySerializer
    permission_classes = (IsAuthenticated, CanCreateSurvey, PostOnly)

    def pre_save(self, obj):
        obj.user = self.request.user

class SurveyView(Auth, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ This view gets the survey meta data, and survey parameters.

    TODO: list un-surveyed surveys for non-admin users only, so no one
    will be able to see something they cannot take.
    """

    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, )

    queryset = Survey.objects.all()

    def get_queryset(self):
        """ If non-admin user, return unsurveyed surveys only as
        queryset. """

        user = self.request.user

        if user.is_anonymous():
            return []

        qs = self.queryset

        if not user.is_superuser:
            qs = self.queryset.exclude(usersurvey__user=user,
                                       usersurvey__completed__isnull=True)

        return qs

class UserSurveyView(viewsets.ModelViewSet):
    """ This view only handles submission and creation of user survey
    instances.

    TODO:
    TODO: permissions - only one submission per user per session
    TODO: permissions - anonymous submissions not allowed
    """

    pass

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

def answer(request):

    context = {}

    return render_to_response('survey.html', context,
                           context_instance=RequestContext(request))
