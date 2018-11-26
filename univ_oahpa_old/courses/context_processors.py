from django.conf import settings

def request_user(request):
    return {'rquser': request.user}

def courses_user(request):
    from survey.models import Survey
    from django.db.models import Q

    user_has_surveys = False

    # Assuming one response per survey
    # We only check for this every few times context is called

    if request.user.is_authenticated():
        interval = 8
        check_count = request.session.get('check_count', 0)
        print check_count

        if 'user_has_surveys' in request.session and (check_count != interval):
            user_has_surveys = request.session['user_has_surveys']
        else:
            print 'checking'
            if check_count == 0 or check_count == interval:
                u = request.user
                responses = Survey.objects.filter(responses__user=u)

                unanswered = Survey.objects.exclude(responses__user=u)

                unanswered = unanswered.filter(Q(target_course__isnull=True) |
                                               Q(target_course__in=u.get_profile().courses))

                responses_count = responses.count()

                survey_ids_available = ','.join(map(str, unanswered.values_list('id', flat=True)))

                if len(unanswered) > 0:
                    user_has_surveys = True

                request.session['user_has_surveys'] = user_has_surveys
                check_count = 0

        check_count += 1
        request.session['check_count'] = check_count


    if request.user.is_authenticated():
        return {'courses_user': request.user, 'courses_user_profile': request.user.get_profile(), 'user_has_surveys': user_has_surveys}
    else:
        return {'courses_user': False, 'courses_user_profile': False}

# vim: set ts=4 sw=4 tw=72 syntax=python :
