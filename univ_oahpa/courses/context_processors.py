from django.conf import settings

def request_user(request):
    return {'rquser': request.user}

# vim: set ts=4 sw=4 tw=72 syntax=python :
