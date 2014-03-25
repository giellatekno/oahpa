from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from django.conf import settings

URL_PREFIX = settings.URL_PREFIX


def render_to_response(*args, **kwargs):
    """ Append an attribute onto the response so that we can grab the context
    from it in the track decorator. It has to be an attribute so that it
    doesn't depend on the function returning the response to be decorated by
    @trackGrade to get proper output. """

    from django.shortcuts import render_to_response

    response = render_to_response(*args, **kwargs)
    # response.response_args = args
    response.context = args[1]

    return response

from django.contrib.auth.decorators import login_required

from models import UserProfile, Course, UserGrade, Activity

def cookie_login(request, next_page=None, required=False, **kwargs):
    """ Check for existing site.uit.no cookie
    """
    from django.conf import settings
    from django.contrib import auth

    if not next_page:
        # TODO: change next url for deep links
        next_page = '/%s/courses/' % URL_PREFIX
    if request.user.is_authenticated():
        message = "You are logged in as %s." % request.user.username
        request.user.message_set.create(message=message)
        return HttpResponseRedirect(next_page)

    matching_cookies = [(c, v) for c, v in request.COOKIES.iteritems() 
                                if c.startswith(settings.COOKIE_NAME)]

    try:
        cookie_name, wp_cookie = matching_cookies[0]
        wp_username, session, session_hex = wp_cookie.split('%7C')
        cookie_uid = wp_username
    except:
        cookie_uid = False

    if cookie_uid:
        user = auth.authenticate(cookie_uid=cookie_uid)
        if user is not None:
            auth.login(request, user)
            name = user.username
            message = "Login succeeded. Welcome, %s." % name
            user.message_set.create(message=message)
            return HttpResponseRedirect(next_page)
        # elif settings.CAS_RETRY_LOGIN or required:
            # return HttpResponseRedirect(_login_url(service))
        else:
            error = "<h1>Forbidden</h1><p>Login failed.</p>"
            return HttpResponseForbidden(error)
    else:
        return HttpResponseRedirect('/%s/courses/standard_login/' % URL_PREFIX) 
        # TODO: check


def cookie_logout(request, next_page=None, **kwargs):
    """
    """

    from django.contrib.auth import logout

    logout(request)

    # TODO: redirect to kursa logout link

    # This can't redirect to cookie_logout, or else there are unlimited
    # redirects.

    if not next_page:
        next_page = '/%s/courses/logout/' % URL_PREFIX

    return HttpResponseRedirect(next_page)


def trackGrade(gamename, request, c):
    """ Takes a name of the game, request, and the context, and produces
        a course grade entry for the student.

        In the corresponding oahpa.drills.views, first import this function

            ex.)    from courses.views import trackGrade

        Then, insert the following into each view before the return render_to_response

            ex.)    trackGrade('Morfa', request, c)
                    return render_to_response( etc ... )

        The first value is the name of the game, but this function handles
        the rest of choosing specifics, so course grade entries will display:

                Morfa - N-ILL - Bisyllabic
                Morfa - PRS - Trisyllabic
    """
    try:
        SETTINGS = c['settingsform'].data
    except TypeError:
        print repr(c)
        return

    if c['show_correct'] == 1 or c['all_correct'] == 1:
        if request.user.is_authenticated() and not request.user.is_anonymous():
            game_type = ''
            if 'gamename_key' in c['settings']:
                game_type = c['settings']['gamename_key']

            gamename = gamename + ' - ' + game_type

            points, _, total = c['score'].partition('/')
            activity, _ = Activity.objects.get_or_create(name=gamename)
            new_grade = UserGrade.objects.create(user=request.user.get_profile(),
                                                game=activity,
                                                score=points,
                                                total=total)

@login_required
def courses_goal_construction(request):
    template = 'courses/courses_main_goals.html'
    c = {}
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

@login_required
def courses_stats(request):
    """ This is the main view presented to users after login.
        Instructors will be shown a link to view grades and student progress,
        students will be shown their current progress in all of the games
        that they have records in.
    """

    template = 'courses/courses_stats.html'

    c = {}
    new_profile = None
    is_student = None

    try:
        profile = request.user.get_profile()
        new_profile = False
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        profile.save()
        new_profile = True

    summary = False

    if profile.is_instructor:
        if request.GET.get('student_view', False):
            is_student = True
        else:
            is_student = False
    else:
        is_student = True

    if is_student:
        summary = profile.usergradesummary_set.all()
        if summary.count() == 0:
            new_profile = True

    user_defined_goals = Goal.objects.filter(created_by=request.user, course=None)

    c = {
        'user':  request.user,
        'profile':  profile,
        'new_profile':  new_profile,
        'is_student':  is_student,
        'summaries':  summary,
        'courses': profile.studentships,
        'user_defined_goals': user_defined_goals
    }

    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

@login_required
def courses_main(request):
    """ This is the main view presented to users after login.
        Instructors will be shown a link to view grades and student progress,
        students will be shown their current progress in all of the games
        that they have records in.
    """

    template = 'courses/courses_main.html'

    c = {}
    new_profile = None
    is_student = None

    try:
        profile = request.user.get_profile()
        new_profile = False
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
        profile.save()
        new_profile = True

    summary = False

    if profile.is_instructor:
        if request.GET.get('student_view', False):
            template = 'courses/courses_main.html'
            is_student = True
        else:
            template = 'courses/courses_main_instructor.html'
            is_student = False
    else:
        template = 'courses/courses_main.html'
        is_student = True

    if is_student:
        summary = profile.usergradesummary_set.all()
        if summary.count() == 0:
            new_profile = True

    user_defined_goals = Goal.objects.filter(created_by=request.user, course=None)

    c = {
        'user':  request.user,
        'profile':  profile,
        'new_profile':  new_profile,
        'is_student':  is_student,
        'summaries':  summary,
        'courses': profile.studentships,
        'user_defined_goals': user_defined_goals
    }

    return render_to_response(template, 
                              c, 
                              context_instance=RequestContext(request))

from django.contrib.auth.decorators import user_passes_test

def instructor_group(user):
    if user.get_profile().is_instructor:
        return True
    else:
        return False

@user_passes_test(instructor_group)
def instructor_student_detail(request, uid):
    student = UserProfile.objects.get(user__id=uid)
    instructor = request.user.get_profile()

    instructor_courses = list([a.id for a in instructor.instructorships])
    student_courses = list([a.id for a in student.courses])

    intersection = list(set(instructor_courses) & set(student_courses))

    if len(intersection) == 0:
        error = 'Student not found.'
        return HttpResponseForbidden(error)

    template = 'courses/instructor_student_detail.html'
    c = {}
    c['student'] = UserProfile.objects.get(user__id=uid)
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))


from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserGoalInstance

class GetOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        if request.method == 'GET':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return False

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGoalInstance
        fields = ('progress', 'rounds', 'total_answered', 'correct', 'completed_date', 'grade', 'correct_first_try', 'is_complete')

class UserStatsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, GetOnly)
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

def prepare_goal_params(rq=None):
    from univ_drill.forms import *

    # Here's a definition of all the choice possibilities that will be
    # available to users below.

    # TODO: will need to evaluate the values for each request, because
    # of localization.
    # TODO: use the same strings as localization provides
    # TODO: add the rest of the form choices.

    # TODO: bisyllabic, trisyllabic, contracted choices as checkboxes
    GOAL_PARAMETER_CHOICE_VALUES = {
        'source': {'options': dict(BOOK_CHOICES),
                   'name': 'Book'},
        'geography': {'options': dict(GEOGRAPHY_CHOICES),
                      'name': 'Geography'},
        'common': {'options': dict(FREQUENCY_CHOICES),
                   'name': 'Word frequency'},
        'semtype': {'options': dict(SEMTYPE_CHOICES),
                    'name': 'Semantic set'},
        'transtype': {'options': dict(TRANS_CHOICES),
                      'name': 'Translation'},

        'numgame': {'options': dict(NUMGAME_CHOICES),
                    'name': 'Game type'},
        'maxnum':  {'options': dict(NUM_CHOICES),
                    'name': 'Max number'},

        'gametype':  {'options': dict(KLOKKA_CHOICES),
                    'name': 'Difficulty'},

        'case':  {'options': dict(CASE_CHOICES),
                  'name': 'Case'},
        'vtype': {'options': dict(VTYPE_CHOICES),
                  'name': 'Verb type'},

        'pron_type': {'options': dict(PRONOUN_SUBCLASSES),
                  'name': 'Pronoun type'},
        'proncase': {'options': dict(CASE_CHOICES),
                  'name': 'Pronoun case'},

        'case_context':  {'options': dict(CASE_CONTEXT_CHOICES),
                  'name': 'Case'},
        'vtype_context': {'options': dict(VTYPE_CONTEXT_CHOICES),
                  'name': 'Verb type'},
        # TODO: test adj
        'adj_context': {'options': dict(ADJ_CONTEXT_CHOICES),
                  'name': 'Adjective type'},
        'pron_context': {'options': dict(PRON_CONTEXT_CHOICES),
                  'name': 'Pronoun type'},
        'num_context': {'options': dict(NUM_CONTEXT_CHOICES),
                  'name': 'Numeral case'},
        'derivation_type_context': {'options': dict(DERIVATION_CHOICES),
                  'name': 'Derivation type'},

        # TODO: adj grade choices in context?
    }

    # This is a definition of the form tree that wil be presented.  Each
    # key represents a main type, and this is a list of subtypes.  Each
    # subtype contains `params`, which are HTTP parameters that will be
    # set on the URL. If any need to be hidden and only displayed in
    # certain cases, these will be defined in 'conditional', which is a
    # list of objects, where the key is the parameter that the condition
    # relates to, and a value is defined with a list of parameters that
    # will be displayed if this condition is true.

    # Eventually this might be able to be automatically constructed from
    # something.

    GOAL_CHOICE_TREE = {
        'leksa': {
            'subtypes': [
                {
                    'path': '/leksa/',
                    'label': 'Words',
                    'value': 'leksa',
                    'params': ['source', 'semtype', 'transtype'],
                },
                {
                    'path': '/leksa/sted/',
                    'label': 'Placenames',
                    'value': 'leksa_place',
                    'params': ['geography', 'common', 'transtype'],
                }
            ],
            'label': 'Leksa',
            'value': 'leksa',
        },
        'numra': {
            'subtypes': [
                {
                    'path': '/numra/',
                    'label': 'Cardinal numbers',
                    'value': 'numra_number',
                    'params': ['numgame', 'maxnum'],
                },
                {
                    'path': '/numra/ord/',
                    'label': 'Ordinal numbers',
                    'value': 'numra_ordinal',
                    'params': ['numgame', 'maxnum'],
                },
                {
                    'path': '/numra/klokka/',
                    'label': 'Time',
                    'value': 'numra_klokka',
                    'params': ['gametype', 'numgame', 'maxnum'],
                },
                {
                    'path': '/numra/dato/',
                    'label': 'Time',
                    'value': 'numra_dato',
                    'params': ['numgame'],
                },
            ],
            'label': 'Numra',
            'value': 'numra',
        },
        'morfas': {
            'subtypes': [
                {
                    'params': ['case', 'book', 'stem_type'],
                    'label': 'Morfa-S Nouns',
                    'value': 'morfa_s_noun',
                    'path': '/morfas/s/',
                },
                {
                    'params': ['vtype', 'book', 'stem_type'],
                    'label': 'Morfa-S Verb',
                    'value': 'morfa_s_verb',
                    'path': '/morfas/v/',
                    'conditional': [
                        { 'key': 'vtype',
                          'value': 'PRS',
                          'params': ['something'],
                        },
                        { 'key': 'vtype',
                          'value': 'PRT',
                          'params': ['something_else'],
                        },
                    ],
                },
                {
                    'params': ['pron_type', 'proncase',],
                    'label': 'Morfa-S Pronouns',
                    'value': 'morfa_s_pron',
                    'path': '/morfas/p/',
                },
                # TODO: Morfa-S Adj
                # TODO: Morfa-S Pronouns
                # TODO: Morfa-S Numerals
                # TODO: Morfa-S Derivations
            ],
            'label': 'Morfa-S',
            'value': 'morfa_s'
        },
        'morfac': {
            'subtypes': [
                {
                    'params': ['case_context',],
                    'label': 'Morfa-C Nouns',
                    'value': 'morfa_c_noun',
                    'path': '/morfac/s/',
                },
                {
                    'params': ['vtype_context',],
                    'label': 'Morfa-C Verb',
                    'value': 'morfa_c_verb',
                    'path': '/morfac/v/',
                },
                {
                    'params': ['adj_context',],
                    'label': 'Morfa-C Adjectives',
                    'value': 'morfa_c_adj',
                    'path': '/morfac/a/',
                },
                {
                    'params': ['pron_context',],
                    'label': 'Morfa-C Pronouns',
                    'value': 'morfa_c_pron',
                    'path': '/morfac/p/',
                },
                {
                    'params': ['num_context',],
                    'label': 'Morfa-C Numerals',
                    'value': 'morfa_c_num',
                    'path': '/morfac/l/',
                },
                {
                    'params': ['derivation_type_context'],
                    'label': 'Morfa-C Derivations',
                    'value': 'morfa_c_der',
                    'path': '/morfac/der/',
                },
            ],
            'label': 'Morfa-C',
            'value': 'morfa_c'
        },
    }

    return GOAL_CHOICE_TREE, GOAL_PARAMETER_CHOICE_VALUES

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import mixins

from .models import Goal, GoalParameter, UserFeedbackLog

class FeedbackLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedbackLog
        fields = ('feedback_texts', 'user_input', 'correct_answer', 'datetime')

class GoalParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalParameter
        fields = ('parameter', 'value')

# TODO: edit/put
class GoalSerializer(serializers.ModelSerializer):
    begin_url = serializers.CharField(source='begin_url', read_only=True)
    params = GoalParamSerializer(many=True)

    def transform_params(self, obj, value):
        """ Need to switch all these to dictionaries
        """
        if value is not None:
            return dict([(p.get('parameter'), p.get('value')) for p in value])
        return None

    class Meta:
        model = Goal
        fields = ('id', 'short_name', 'description', 'begin_url',
                  'course', 'params', 'main_type', 'sub_type',
                  'threshold', 'minimum_sets_attempted',
                  'correct_first_try')

from django.shortcuts import get_object_or_404

class CanCreateAndUpdateFeedbackLog(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class CanCreateAndUpdateGoal(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # If there's a course, only the instructors can edit
        if obj.course:
            return obj.course in request.user.get_profile().instructorships
        # Otherwise, this is the user's personal goal.
        else:
            return obj.created_by == request.user
        return False

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


def begin_course_goal(request, goal_id):
    """ Mark the session with the goal ID, and redirect the user to the
    goal's start page.
    """
    from .models import Goal, UserActivityLog

    goal_id = int(goal_id)

    # Reset any session variables for tracking progress
    if 'all_correct' in request.session:
        del request.session['all_correct']
    if 'set_completed' in request.session:
        del request.session['set_completed']
    if 'new_game' in request.session:
        del request.session['new_game']
    if 'prev_new_game' in request.session:
        del request.session['prev_new_game']

    request.session['question_set_count'] = 0
    request.session['question_try_count'] = {}
    request.session['answered'] = {}
    request.session['previous_exercise_params'] = False
    request.session['prev_new_game'] = False

    # Check that the user has the goal
    user_courses = request.user.get_profile().courses
    user_course_goals = [goal for course in user_courses
                              for goal in course.goal_set.all()
                        ] + list(Goal.objects.filter(created_by=request.user,
                                                course=None))

    goal_ids = list(set([int(g.id) for g in user_course_goals]))

    if not goal_id in goal_ids:
        return HttpResponseForbidden("This is missing, or you do not have access.")

    # TODO: redirect to beginning of course goal

    goal = Goal.objects.get(id=goal_id)
    request.session['current_user_goal'] = int(goal_id)

    # Reset goal progress
    # TODO: confirm first if there is progress, then reset.
    # TODO: maybe don't delete, but preserve somehow, create a new
    # usergoalinstance to relate logs to?
    UserActivityLog.objects.filter(user=request.user, goal=goal).delete()

    UserGoalInstance.objects.filter(user=request.user, goal=goal).delete()
    UserGoalInstance.objects.create(user=request.user, goal=goal)

    return HttpResponseRedirect(goal.start_url())

