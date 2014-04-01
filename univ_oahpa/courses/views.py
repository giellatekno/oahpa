from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from django.conf import settings
from .models import Goal, UserGoalInstance

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
    c = {'coursegoal': False}
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

@login_required
def courses_coursegoal_construction(request):
    template = 'courses/courses_main_goals.html'
    c = {'coursegoal': True}
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
def instructor_student_detail(request, uid, cid):
    student = UserProfile.objects.get(user__id=uid)
    instructor = request.user.get_profile()

    instructor_courses = list([a.id for a in instructor.instructorships])
    print instructor_courses
    course_for_inst = [a for a in instructor_courses if a == long(cid)]
    print course_for_inst

    if len(course_for_inst) > 0:
        course = course_for_inst[0]
        course = Course.objects.get(id=course)
    else:
        course = False

    student_courses = list([a.id for a in student.courses])

    intersection = list(set(instructor_courses) & set(student_courses))

    if len(intersection) == 0 or not course:
        error = 'Student not found.'
        return HttpResponseForbidden(error)

    template = 'courses/instructor_student_detail.html'
    c = {}
    c['student'] = UserProfile.objects.get(user__id=uid)
    c['course'] = course
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

def goal_history(request, goal_id):
    u = request.user

    instances = UserGoalInstance.objects.filter(user=u, goal=goal_id)\
                                        .order_by('-last_attempt')
    template = 'courses/goal_history.html'
    c = {}
    c['student'] = UserProfile.objects.get(user__id=request.user.id)
    c['goal_instances'] = instances
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

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

    request.session['question_set_count'] = 1
    request.session['question_try_count'] = {}
    request.session['answered'] = {}

    try: del request.session['previous_exercise_params']
    except: pass

    try: del request.session['current_exercise_params']
    except: pass

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

    # Reset goal progress
    # TODO: will this need to be connected to a usergoalinstance? 
    # UserActivityLog.objects.filter(user=request.user, goal=goal)

    UserGoalInstance.objects.filter(user=request.user, goal=goal).update(opened=False)
    ugi = UserGoalInstance.objects.create(user=request.user, goal=goal)
    request.session['current_user_goal'] = int(ugi.id)

    return HttpResponseRedirect(goal.start_url())

