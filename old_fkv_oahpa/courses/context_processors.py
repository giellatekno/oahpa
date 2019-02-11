from django.conf import settings

def request_user(request):
	return {'rquser': request.user}
