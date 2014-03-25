from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import UserGoalInstance, Goal, GoalParameter, UserFeedbackLog

from .data_permissions import *
from .data_serializers import *
from .data_utils import *

class UserStatsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, GetOnly)
    model = UserGoalInstance
    serializer_class = StatusSerializer

    def list(self, request):
        rq = super(UserStatsViewSet, self).list(request)
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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (CanCreateAndUpdateGoal, )
    queryset = Goal.objects.all()

    serializer_class = GoalSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user)

    def list(self, request):
        """
        This view should return a list of all the goals
        for the currently authenticated user.
        """

        goals = Goal.objects.filter(created_by=request.user)

        response_parameters = {}
        response_parameters['success'] = True
        response_parameters['goals'] = GoalSerializer(goals).data

        return Response(response_parameters)

    @property
    def exercise_type_url_bases(self):
        return dict([
            (subtype.get('value'), subtype.get('path'))
            for k, v in prepare_goal_params()[0].iteritems()
            for subtype in v.get('subtypes', [])
        ])

    def update(self, request, pk=None):
        success = True

        response_parameters = {}
        new_obj = request.DATA
        new_obj.pop('id')
        new_obj.pop('begin_url')
        url_base = self.exercise_type_url_bases.get(new_obj.get('sub_type'))
        new_obj['url_base'] = url_base
        params = new_obj.pop('params')

        # TODO: check user has permissions to update
        try:
            goal = self.queryset.filter(pk=pk)
            goal.update(**new_obj)
        except Exception, e:
            success = False

        goal = goal[0]

        if success:
            GoalParameter.objects.filter(goal=goal).delete()
            for p_k, p_v in params.iteritems():
                goal.params.create(parameter=p_k, value=p_v)

            # TODO: Reset user instance

        response_parameters = {}

        if success:
            response_parameters['goal'] = GoalSerializer(goal).data
        else:
            response_parameters['error'] = "Could not update the goal."

        response_parameters['success'] = success


        return Response(response_parameters)

    def create(self, request):
        # TODO: this can probably be generalized with the serializer now

        # TODO: must be authed, can't be anon
        # TODO: course_id within
        # request.user.get_profile().instructorships?

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
        # TODO: include user's courses if they are an instructor in any
        # This returns all the parameters 
        data = super(GoalParametersView, self).metadata(request)
        choice_tree, parameter_values = prepare_goal_params(request)
        parameters = {'tree': choice_tree, 'values': parameter_values}
        data['parameters'] = parameters
        data['courses'] = [(c.id, c.name) for c in request.user.get_profile().instructorships]
        return data

