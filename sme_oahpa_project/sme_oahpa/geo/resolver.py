from django.contrib.gis.geoip2 import GeoIP2


def session_country(request):
	""" Add 'user_country' to context and 'country' to request.session, only
	perform lookup once per session.  """

	user_country = False
	if not request.session.get('country'):
		try:
			_ip = request.META['HTTP_X_REAL_IP']
		except KeyError:
			_ip = request.META['REMOTE_ADDR']

		result = getCountryFromIP(_ip)
		if result:
			user_country = result.get('country_code')
			request.session['country'] = user_country
	else:
		user_country = request.session.get('country')
	return {'user_country': user_country}

def getCountryFromIP(ip_as_string):
	_geo = GeoIP2()
	return _geo.country(ip_as_string)
