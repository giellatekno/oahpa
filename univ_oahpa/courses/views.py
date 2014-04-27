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
    template = 'courses_main_goals.html'
    c = {'coursegoal': False}
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

@login_required
def courses_coursegoal_construction(request):
    template = 'courses_main_goals.html'
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

    template = 'courses_stats.html'

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
def personal_goals(request):
    """ This is the main view presented to users after login.
        Instructors will be shown a link to view grades and student progress,
        students will be shown their current progress in all of the games
        that they have records in.
    """

    template = 'personal_goals.html'

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

    user_defined_goals = Goal.objects.filter(created_by=request.user, course=None)

    c = {
        'user':  request.user,
        'profile':  profile,
        'new_profile':  new_profile,
        'is_student':  is_student,
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

    template = 'courses_main.html'

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
            template = 'courses_main.html'
            is_student = True
        else:
            template = 'courses_main_instructor.html'
            is_student = False
    else:
        template = 'courses_main.html'
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

def instructor_can_see_student(instructor, student):
    # Instructor's course IDs
    instructor_p = instructor.get_profile()
    instructor_courses = list([a.id for a in instructor_p.instructorships])

    # Student's ... 
    student_p = student.get_profile()
    student_courses = list([a.id for a in student_p.courses])
    intersection = list(set(instructor_courses) & set(student_courses))

    if len(intersection) == 0:
        return False
    else:
        return True

@user_passes_test(instructor_group)
def instructor_student_detail(request, uid, cid):
    student = UserProfile.objects.get(user__id=uid)
    instructor = request.user.get_profile()

    instructor_courses = list([a.id for a in instructor.instructorships])
    course_for_inst = [a for a in instructor_courses if a == long(cid)]

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

    template = 'instructor_student_detail.html'
    c = {}
    c['student'] = UserProfile.objects.get(user__id=uid)
    c['course'] = course
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

def goal_history(request, goal_id, user_id=None):
    from django.contrib.auth.models import User
    from .models import UserActivityLog
    from .models import incorrects_by_frequency

    if user_id is None:
        u = request.user
    else:
        requested_user = User.objects.get(id=user_id)
        if request.user.id == user_id:
            u = request.user
        else:
            # Likely an instructor is requesting this user_id, so we
            # need to make sure they have access
            if instructor_can_see_student(request.user, requested_user):
                u = requested_user
            else:
                u = request.user

    goal = Goal.objects.get(id=goal_id)
    instances = UserGoalInstance.objects.filter(user=u, goal=goal_id)\
                                        .order_by('-last_attempt')
    instances_rev = UserGoalInstance.objects.filter(user=u, goal=goal_id)\
                                        .order_by('last_attempt')
    template = 'goal_history.html'
    c = {}
    c['student'] = u.get_profile()
    c['goal'] = goal
    c['goal_instances'] = instances
    c['incorrects'] = incorrects_by_frequency(u, goal=goal)
    c['spark_data'] = ','.join(map(str, instances_rev.values_list('correct', flat=True)))

    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

def begin_course_task(request, task_id):
    """ Mark the session with the goal ID, and redirect the user to the
    goal's start page.
    """
    from .models import Goal, UserActivityLog

    task_id = int(task_id)

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

    try: del request.session['current_user_goal']
    except: pass

    try: del request.session['max_rounds']
    except: pass

    try: del request.session['correct_threshold']
    except: pass

    request.session['prev_new_game'] = False

    # Check that the user has the goal
    user_courses = request.user.get_profile().courses
    user_own_goals = list(Goal.objects.filter(created_by=request.user,
                                              course=None))

    user_course_goals = [coursegoalgoal.goal for course in user_courses
                              for coursegoal in course.coursegoal_set.all()
                              for coursegoalgoal in coursegoal.goals.all()
                        ] + user_own_goals

    goal_ids = list(set([int(g.id) for g in user_course_goals]))

    if not task_id in goal_ids:
        return HttpResponseForbidden("This is missing, or you do not have access.")

    # TODO: redirect to beginning of course goal

    goal = Goal.objects.get(id=task_id)

    # Reset goal progress
    # TODO: will this need to be connected to a usergoalinstance? 
    # UserActivityLog.objects.filter(user=request.user, goal=goal)

    UserGoalInstance.objects.filter(user=request.user, goal=goal).update(opened=False)
    ugi = UserGoalInstance.objects.create(user=request.user, goal=goal)
    request.session['current_user_goal'] = int(ugi.id)
    request.session['max_rounds'] = goal.minimum_sets_attempted
    request.session['correct_threshold'] = goal.threshold

    return HttpResponseRedirect(goal.start_url())


@user_passes_test(instructor_group)
def course_invite(request):
    c = {}
    profile = request.user.get_profile()
    c['profile'] = profile
    template = 'invite_students.html'
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

def course_enroll(request):
    from django.core.urlresolvers import reverse

    # invite stored in 'key' parameter.
    # http://oahpa.no/davvi/courses/enroll/?key=NDg.BioJAg.E2-Y6uBwr6_35Qhk03uBamTTnHc


    # TODO: if user isn't logged in, store the invite key in the session
    # before redirecting them to log in (we assume they already have a
    # user account because of cookie auth).

    # TODO: when user lands on this page, pop the stored key if it
    # exists, and key isn't set.

    # TODO: enroll user in course

    # TODO: notify instructors of enrollment changes (post-save signal
    # instead?)
    enrollment_key = request.GET.get('key', False)
    session_key = False

    if request.user.is_anonymous():
        request.session['enrollment_key'] = enrollment_key
        next_page = '/%s/courses/enroll/' % URL_PREFIX
        return HttpResponseRedirect(reverse('courses_login') + '?next=' + next_page)

    if not enrollment_key:
        try:
            enrollment_key = request.session.get('enrollment_key')
            session_key = True
        except:
            pass

    if enrollment_key:
        course = Course.objects.get(token=enrollment_key)
    else:
        course = False

    enrolled = False

    # notify these when the enrollment works
    enrolled, error = course.add_student(request.user)

    c = {
        'enrollment_key': enrollment_key,
        'session_key': session_key,
        'target_course': course,
        'incoming_user': request.user,
    }

    if enrolled:
        try:
            enrollment_key = request.session.get('enrollment_key')
            session_key = True
        except:
            pass
    else:
        c['error'] = error


    return render_to_response('course_enroll.html',
                              c,
                              context_instance=RequestContext(request))

@login_required
def recipient_search(request):
	# https://github.com/philippWassibauer/django-threaded-messages
    from django.contrib.auth.models import User
    from django.db.models import Q

    from django.core.urlresolvers import reverse
    from django.http import HttpResponse
    import simplejson

    # TODO: filter by user's fellow students/instructors/etc.
    term = request.GET.get("term")
    users = User.objects.filter(Q(first_name__icontains=term)|
                                Q(last_name__icontains=term)|
                                Q(username__icontains=term)|
                                Q(email__icontains=term))
    if request.GET.get("format") == "json":
        data = []
        for user in users:
            # avatar_img_url = avatar_url(user, size=50)
            data.append({"id": user.username,
                         # "url": reverse("profile_detail",args=(user.username,)),
                         "name": "%s %s"%(user.first_name, user.last_name),
                         # "img": avatar_img_url
                        })

        return HttpResponse(simplejson.dumps(data),
                            mimetype='application/json')
