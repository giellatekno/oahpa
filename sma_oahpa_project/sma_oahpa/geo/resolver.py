"""

TODO: access/error logs for univ_oahpa on gtlab

# Basic notes on Geo IP resolving

Additional changes have been made in univ_drill to ensure that user_country is
stored in Logs, if that setting is available in the session. This module handles
getting the country code data into the session, and requires the use of a Python
library, GeoIP2, and its relevant data files.

# Installation

## Table alterations for drill.log

See geo/sql_changes.sql but be careful on production servers.

## Install geoip2 Python library

The Python library is required for the geodjango GeoIP2 object to be able to perform lookups.
(ref. https://docs.djangoproject.com/en/1.11/ref/contrib/gis/geoip2/)

    pip install geoip2
    mkdir geo/data
    Download GeoLite2 City and Country db, unzip and mv them to geo/data

## settings.py

The paths to db and names are included in settings_not_in_svn.py.

## Install the libmaxminddb C library

Add the context processor to add country to user session info

	"LLL1_oahpa.geo.resolver.session_country"

## Potential problems

### request.META has no 'REMOTE_ADDR', or 'HTTP_X_REAL_IP'

Check that nginx is passing this in the fastcgi configuration, if not, add

	fastcgi_param REMOTE_ADDR $remote_addr;

### only IPs tracked are 127.0.0.1

Nginx proxy definitions need to have the following:

	proxy_set_header   X-Real-IP        $remote_addr;
	proxy_set_header   X-Forwarded-For  $remote_addr;

"""

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

        try:
            result = getCountryFromIP(_ip)
        except Exception:
            result = False
	if result:
		user_country = result.get('country_code')
		request.session['country'] = user_country
	else:
		user_country = request.session.get('country')
	return {'user_country': user_country}

def getCountryFromIP(ip_as_string):
	_geo = GeoIP2()
	return _geo.country(ip_as_string)
