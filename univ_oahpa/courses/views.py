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
def courses_main(request):
    """ This is the main view presented to users after login.
        Instructors will be shown a link to view grades and student progress,
        students will be shown their current progress in all of the games
        that they have records in.
    """
    from .models import Goal

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

    def get_queryset(self):
        """
        This view should return a list of all the purchases
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
                    'params': ['case', 'book', 'vtype'],
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
                    'params': ['case', 'book'],
                    'label': 'Morfa-S Nouns',
                    'value': 'morfa_s_noun',
                    'path': '/morfas/s/',
                },
            ],
            'label': 'Morfa-S',
            'value': 'morfa_s'
        },
    }

    return GOAL_CHOICE_TREE, GOAL_PARAMETER_CHOICE_VALUES

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class GoalParametersView(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = ()

    def create(self, request):
        from .models import Goal

        EXERCISE_TYPE_URL_BASES = dict([
            (subtype.get('value'), subtype.get('path'))
            for k, v in prepare_goal_params()[0].iteritems()
            for subtype in v.get('subtypes', [])
        ])

        # TODO: must be authed, can't be anon
        response_parameters = {}
        new_obj = request.DATA
        params = new_obj.pop('params')

        main_type = new_obj.pop('main_type')
        sub_type = new_obj.pop('sub_type')

        # use main_type to get url path
        url_base = EXERCISE_TYPE_URL_BASES.get(sub_type)
        new_obj['exercise_type'] = url_base

        goal = Goal.objects.create(created_by=request.user, **new_obj)
        for p_k, p_v in params.iteritems():
            goal.goalparameter_set.create(parameter=p_k, value=p_v)

        response_parameters['success'] = True
        response_parameters['id'] = goal.id
        return Response(response_parameters)

    def metadata(self, request):
        # This returns all the parameters 
        data = super(GoalParametersView, self).metadata(request)
        choice_tree, parameter_values = prepare_goal_params(request)
        parameters = {'tree': choice_tree, 'values': parameter_values}
        data['parameters'] = parameters
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

    request.session['question_set_count'] = 1
    request.session['question_try_count'] = {}
    request.session['answered'] = {}
    request.session['previous_exercise_params'] = False

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

