'''
## Install geoip2 Python library

The Python library is required for the geodjango GeoIP2 object to be able to perform lookups.
(ref. https://docs.djangoproject.com/en/1.11/ref/contrib/gis/geoip2/)

    pip install geoip2
    mkdir geo/data
    Download GeoLite2 City and Country db, unzip and mv them to geo/data
	(https://dev.maxmind.com/geoip/geoip2/geolite2/, download MaxMind DB binary, gzipped)



## settings.py

The paths to db and names are included in settings_not_in_svn.py.

## Install the libmaxminddb C library

Add the context processor to add country to user session info

	LLL1+"_oahpa.geo.resolver.session_country"

'''


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
