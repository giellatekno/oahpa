"""

TODO: access/error logs for univ_oahpa on gtlab
TODO: request IP test
TODO: extract information and include in Log object creation. Include caching of
      lookups in user session to save time for users who are using the system
      a lot.

Basic notes on Geo IP resolving

# Installation

## Table alterations for univ_drill.log

See geo/sql_changes.sql but be careful on production servers.

## Install geoip C library

The C library is required for the geodjango GeoIP object to be able to perform lookups, and what we need out of this is the path of libGeoIP.so

    wget http://www.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
    tar zxvf GeoIP.dat.gz
    cd into directory
    mkdir /home/univ_oahpa/univ_oahpa/geo/geoip
    ./configure --prefix=/home/univ_oahpa/univ_oahpa/geo/geoip
    make
    make install

Then find the path to that file, which should be: 

	/home/univ_oahpa/univ_oahpa/geo/geoip/lib/libGeoIP.so


## fetch data files

Here we need two .dat files.

    wget http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    wget http://www.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
    
    gzip -d GeoLiteCity.dat.gz
    gzip -d GeoIP.dat.gz
    
    cp *.dat /home/univ_oahpa/univ_oahpa/geo/data/


## settings.py

Include the following settings in settings.py, change the directories if you
have installed them to another path.

	GEOIP_PATH = '/home/univ_oahpa/univ_oahpa/geo/data/'
	GEOIP_LIBRARY_PATH = '/home/univ_oahpa/univ_oahpa/geo/geoip/lib/libGeoIP.so'
	GEOIP_COUNTRY = 'GeoIP.dat'
	GEOIP_CITY = 'GeoLiteCity.dat'

"""

from django.contrib.gis.utils import GeoIP

def getCountryFromIP(ip_as_string):
	_geo = GeoIP()
	return _geo.country(ip_as_string)

def getCityFromIP(ip_as_string):
	_geo = GeoIP()
	return _geo.city(ip_as_string)

