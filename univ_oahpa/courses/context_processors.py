from django.conf import settings

def request_user(request):
    return {'rquser': request.user}

def courses_user(request):
    if request.user.is_authenticated():
        return {'courses_user': request.user}
    else:
        return {'courses_user': False}

# vim: set ts=4 sw=4 tw=72 syntax=python :
