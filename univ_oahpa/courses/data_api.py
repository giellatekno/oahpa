from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import ( UserGoalInstance
                    , CourseGoal
                    , Goal
                    , GoalParameter
                    , UserFeedbackLog
                    , CourseGoalGoal
                    )

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
        rq.data['current_set_count'] = request.session.get('question_set_count', 0)
        rq.data['max_rounds'] = request.session.get('max_rounds', False)
        rq.data['correct_threshold'] = request.session.get('correct_threshold', False)
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
            user_goal_instance = UserGoalInstance.objects.filter( user=user
                                                                , id=goal_id
                                                                , opened=True
                                                                )\
                                                         .order_by('-last_attempt')
            return user_goal_instance
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

    def create(self, request):
        data = request.DATA

        with_ids = []

        for d in data:
            _d = d.copy()
            _d['user'] = request.user.id
            with_ids.append(_d)

        fb_texts = list(set([a.get('feedback_texts') for a in with_ids if a.get('feedback_texts', False)]))

        if len(fb_texts) > 0:
            print UserFeedbackLog.levels.get_user_level(request.user, fb_texts)

        serialized = self.serializer_class(data=with_ids, many=True)

        if serialized.is_valid():
            serialized.save()
            headers = self.get_success_headers(serialized.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)

class CourseGoalView(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (CanCreateAndUpdateCourseGoal, )
    queryset = CourseGoal.objects.all()

    serializer_class = CourseGoalSerializer

    def get_queryset(self):
        user = self.request.user
        # TODO: also return coursegoals for users instructorships
        return self.queryset.filter(created_by=user)

    def update(self, request, pk=None, partial=False):
        response_params = {}
        errors = []

        success = True
        data = request.DATA

        try: data.pop('id')
        except: pass

        goals = data.pop('goals')

        try:
            obj = self.queryset.filter(pk=pk).update(**data)
        except Exception, e:
            success = False
            errors.append(repr(e))

        obj = self.queryset.get(pk=pk)

        goal_objs = Goal.objects.filter(id__in=goals)

        try:
            CourseGoalGoal.objects.filter(coursegoal=obj).delete()
            for g in goal_objs:
                CourseGoalGoal.objects.create(coursegoal=obj, goal=g)
        except Exception, e:
            errors.append(repr(e))

        success = True
        if not success:
            response_params['errors'] = errors

        response_params['success'] = success

        return Response(response_params)

    def create(self, request):
        # TODO: this can probably be generalized with the serializer now

        # TODO: doublecheck that course_id within
        # request.user.get_profile().instructorships if course is
        # specified?

        success = True
        response_parameters = {}

        new_obj = request.DATA
        new_obj['created_by'] = request.user
        new_obj['course_id'] = new_obj.pop('course')
        new_goal = CourseGoal.objects.create(**new_obj)

        response_parameters = {
            'success': success,
        }

        if success:
            response_parameters['id'] = new_goal.id
            response_parameters['goal'] = self.serializer_class(data=new_goal).data

        return Response(response_parameters)

    def metadata(self, request):
        """ This returns stuff when the OPTIONS verb is used,
        but we're coopting it slightly to include the parameters for the
        form, which need to be automatically constructed for each
        installation.

        If the user is an instructor in any courses, these are included
        and rendered in the form.
        """

        data = super(CourseGoalView, self).metadata(request)

        data['courses'] = [
            {'value': c.id, 'label': c.name}
            for c in request.user.get_profile().instructorships
        ]

        return data

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

        errors = []

        # use main_type to get url path
        url_base = self.exercise_type_url_bases.get(new_obj.get('sub_type'))
        new_obj['url_base'] = url_base

        success = True

        goal = Goal.objects.create(created_by=request.user, **new_obj)

        if success:
            for p_k, p_v in params.iteritems():
                goal.params.create(parameter=p_k, value=p_v)

        from django.core.urlresolvers import reverse

        if success:
            response_parameters['goal'] = {}
            response_parameters['goal']['id'] = goal.id
            response_parameters['goal']['short_name'] = goal.short_name
            response_parameters['goal']['begin_url'] = goal.begin_url
        else:
            response_parameters['error'] = "Could not create the goal."
            response_parameters['errors'] = errors

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
        # data['courses'] = [(c.id, c.name) for c in request.user.get_profile().instructorships]
        return data

from notifications.models import Notification

# TODO: test permissions
# -  allows to delete also ?
class NotificationsView(viewsets.ModelViewSet):

    model = Notification()
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (CanCreateAndUpdateNotification, )

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user).unread()

    def create(self, request):
        from notifications import notify

        notify.send(request.user,
                    recipient=request.user,
                    description=request.DATA.get('description'),
                    verb=u'tested notifications',)

        return Response({'success': True})
