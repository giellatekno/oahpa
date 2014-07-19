from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status

from .models import Survey, UserSurvey
from .permissions import *
from .serializers import *

class SurveyView(viewsets.ModelViewSet):
    """ This view gets the survey meta data, and survey parameters.

    TODO: list un-surveyed surveys for non-admin users only, so no one
    will be able to see something they cannot take.
    """

    permission_classes = (IsAuthenticated, GetOnly)

    def get_queryset(self):
        """ If non-admin user, return unsurveyed surveys only as
        queryset.
        """
        user = self.request.user

        qs = self.queryset

        if not user.is_superuser:
            qs = self.queryset.exclude(usersurvey__user=user,
                                       usersurvey__completed__isnull=True)

        return qs

    def create(self, request):
        pass

class UserSurveyView(viewsets.ModelViewSet):
    """ This view only handles submission and creation of user survey
    instances.

    TODO:
    TODO: permissions - only one submission per user per session
    TODO: permissions - anonymous submissions not allowed
    """


