# Basic notes on Geo IP resolving

Additional changes have been made in `univ_drill` to ensure that
`user_country` is stored in Logs, if that setting is available in the
session. This module handles getting the country code data into the
session, and requires the use of a C library, GeoIP, and its relevant
data files. Compilation is easy.

# Installation

## Table alterations for univ_drill.log

See `geo/sql_changes.sql` but be careful on production servers.

## Install geoip C library

The C library is required for the geodjango `GeoIP` object to be able to
perform lookups, and what we need out of this is the path of `libGeoIP.so`

    wget http://www.maxmind.com/download/geoip/api/c/GeoIP.tar.gz
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

Include the following settings in `settings.py`, change the directories if you
have installed them to another path.

	GEOIP_PATH = '/home/univ_oahpa/univ_oahpa/geo/data/'
	GEOIP_LIBRARY_PATH = '/home/univ_oahpa/univ_oahpa/geo/geoip/lib/libGeoIP.so'
	GEOIP_COUNTRY = 'GeoIP.dat'
	GEOIP_CITY = 'GeoLiteCity.dat'

Add the context processor to add country to user session info

	"univ_oahpa.geo.resolver.session_country"

## Potential problems

### request.META has no 'REMOTE_ADDR', or 'HTTP_X_REAL_IP'

Check that nginx is passing this in the fastcgi configuration, if not, add

	fastcgi_param REMOTE_ADDR $remote_addr;

### only IPs tracked are 127.0.0.1

Nginx proxy definitions need to have the following: 

	proxy_set_header   X-Real-IP        $remote_addr;
	proxy_set_header   X-Forwarded-For  $remote_addr;

## Additional django docs

https://docs.djangoproject.com/en/dev/ref/contrib/gis/geoip/#example
