﻿from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import UserGoalInstance, Goal, GoalParameter, UserFeedbackLog

from .data_permissions import *
from .data_serializers import *
from .data_utils import *

class UserStatsViewSet(viewsets.ModelViewSet):
    """ This view powers the display of goal progress when the user is
    submitting answers for a course goal.
    """
    permission_classes = (IsAuthenticated, GetOnly)
    model = UserGoalInstance
    serializer_class = StatusSerializer

    def list(self, request):
        rq = super(UserStatsViewSet, self).list(request)

        # Insert some things for easier display
        rq.data['current_set_count'] = request.session['question_set_count']
        rq.data['navigated_away'] = request.session.get('navigated_away', 0)
        return rq

    def get_queryset(self):
        """
        This view should return a list of all the goals
        for the currently authenticated user.
        """
        user = self.request.user
        goal_id = self.request.session.get('current_user_goal', False)
        if goal_id:
            return UserGoalInstance.objects.filter(user=user, goal__id=goal_id)
        else:
            return []

class FeedbackLogView(viewsets.ModelViewSet):
    """ These views are for adding feedback logs when the user clicks on
    a feedback link.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (CanCreateAndUpdateFeedbackLog, )
    model = UserFeedbackLog
    serializer_class = FeedbackLogSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)

class GoalParametersView(viewsets.ModelViewSet):
    """ These views are for creating, editing and deleting users'
    personal goals, as well as goals connected to courses.

    Django admin wasn't really enough to manage this kind of thing.
    OPTIONS provides a set of possible parameters, and POST and PUT are
    available for creating and editing. DELETE is also possible, and
    permissions are checked.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (CanCreateAndUpdateGoal, )
    queryset = Goal.objects.all()

    serializer_class = GoalSerializer

    def get_queryset(self):
        """ Always filter by user, because this only concerns
        creating/editing goals, not exhaustively listing all goals
        available to the user via classes.
        """
        user = self.request.user
        return self.queryset.filter(created_by=user)

    def list(self, request):
        """
        This view should return a list of all the goals
        for the currently authenticated user.
        """

        goals = self.get_queryset()

        response_parameters = {}
        response_parameters['success'] = True
        response_parameters['goals'] = self.serializer_class(goals).data

        return Response(response_parameters)

    @property
    def exercise_type_url_bases(self):
        return dict([
            (subtype.get('value'), subtype.get('path'))
            for k, v in prepare_goal_params()[0].iteritems()
            for subtype in v.get('subtypes', [])
        ])

    def update(self, request, pk=None):
        """ When the PUT verb is used, this is called.
        """
        success = True

        response_parameters = {}

        new_obj = request.DATA

        # Pop some kwargs not available in the model
        new_obj.pop('id')
        new_obj.pop('begin_url')

        # grab the URL base of the exercise
        url_base = self.exercise_type_url_bases.get(new_obj.get('sub_type'))
        new_obj['url_base'] = url_base

        # Pop params, because we iterate later.
        params = new_obj.pop('params')

        # NB: queryset already filtered for user

        # Actually update the main object, easier to do as a queryset.
        try:
            goal = self.queryset.filter(pk=pk)
            goal.update(**new_obj)
        except Exception, e:
            success = False

        goal = goal[0]

        # If the update worked, remove the GoalParameters and re-add
        # them.
        if success:
            GoalParameter.objects.filter(goal=goal).delete()
            for p_k, p_v in params.iteritems():
                goal.params.create(parameter=p_k, value=p_v)

            # Reset user progress.
            goal.usergoalinstance_set.all().delete()

        if success:
            # re-serialize the created goal for return.
            response_parameters['goal'] = self.serializer_class(goal).data
        else:
            response_parameters['error'] = "Could not update the goal."

        response_parameters['success'] = success

        return Response(response_parameters)

    def create(self, request):
        # TODO: this can probably be generalized with the serializer now

        # TODO: doublecheck that course_id within
        # request.user.get_profile().instructorships if course is
        # specified?

        response_parameters = {}
        new_obj = request.DATA
        params = new_obj.pop('params')

        # use main_type to get url path
        url_base = self.exercise_type_url_bases.get(new_obj.get('sub_type'))
        new_obj['url_base'] = url_base

        success = True
        try:
            goal = Goal.objects.create(created_by=request.user, **new_obj)
        except Exception, e:
            success = False

        if success:
            for p_k, p_v in params.iteritems():
                goal.params.create(parameter=p_k, value=p_v)

        from django.core.urlresolvers import reverse

        if success:
            response_parameters['goal'] = {}
            response_parameters['goal']['id'] = goal.id
            response_parameters['goal']['short_name'] = goal.short_name
            response_parameters['goal']['description'] = goal.description
            response_parameters['goal']['begin_url'] = goal.begin_url
        else:
            response_parameters['error'] = "Could not create the goal."

        response_parameters['success'] = success

        return Response(response_parameters)

    def metadata(self, request):
        """ This returns stuff when the OPTIONS verb is used,
        but we're coopting it slightly to include the parameters for the
        form, which need to be automatically constructed for each
        installation.

        If the user is an instructor in any courses, these are included
        and rendered in the form.
        """

        data = super(GoalParametersView, self).metadata(request)
        choice_tree, parameter_values = prepare_goal_params(request)
        parameters = {'tree': choice_tree, 'values': parameter_values}
        data['parameters'] = parameters
        data['courses'] = [(c.id, c.name) for c in request.user.get_profile().instructorships]
        return data
