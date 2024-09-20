# Dockerfile to run sme_oahpa

FROM docker.io/library/debian:bookworm

# build-essential
# compiler to build python2

# libaio1 libaio-dev
# required for mysql (which is required for mysql-python==1.2.5)

# ca-certificates
# unsure if I need ca-certificates or not, but it's no big deal either way

# libmariadb-dev libmariadb-dev-compat
# can't use them: using pre-built mysql from tarball directly instead

# gettext
# required for localization (e.g. django-admin compilemessages)

# mariadb-server
# the database

# also install nginx and supervisor

RUN set -eux && \
    apt-get update && \
    apt-get install -y curl xz-utils build-essential \
    zlib1g-dev libssl-dev libssl3 \
    libaio1 libaio-dev \
    ca-certificates \
    gettext \
    mariadb-server \
    libncurses5 \
    nginx supervisor

WORKDIR /tmp

# install python2 (from source)
RUN set -eux && \
    curl -O https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz && \
    tar -Jxf Python-2.7.18.tar.xz && \
    cd Python-2.7.18 && \
    ./configure && \
    make && \
    make install

# requirement for MySQL-Python 1.2.5:
# RUN apt-get install -y libmariadb-dev-compat libmariadb-dev
# MariaDB in Debian didn't work for us. Probably they
# are too changed from mysql version 5.6.51, which
# is around the version we need.
# This file is downloaded from oracle's mysql site. Note that Oracle has
# made it so unintuitive and difficult to find these old releases on their
# site, that it's better to just search-engine for "mysql 5.6" or such,
# to find the download site.
COPY containerized_deploy/mysql-5.6.51-linux-glibc2.12-x86_64.tar.gz /tmp
RUN tar -zxf mysql-5.6.51-linux-glibc2.12-x86_64.tar.gz && \
    cd mysql-5.6.51-linux-glibc2.12-x86_64 && \
    cp -r bin include lib share /usr/

# install pip
RUN python -m ensurepip

# install all pip packages. refer to commented out code below this for
# info about each package
RUN pip install uwsgi django==1.11.13 Fabric==1.9.0 Markdown==2.4 distribute==0.7.3 MySQL-python==1.2.5 South==1.0 Werkzeug==0.9.4 django-extensions==1.1.0 django-forms-bootstrap==3.0.0 django-messages==0.5.0 django-model-utils==2.0.3 django-modeltranslation==0.13b1 django-serializers==0.5.0 djangorestframework==3.9.0 ecdsa==0.11 flup==1.0.3.dev-20110405 ipython==1.2.1 itsdangerous==0.24 paramiko==1.14.0 pexpect==2.4 pycrypto==2.6.1 schematics==1.0-0 simplejson==3.4.0 six==1.8.0 wsgiref==0.1.2 django-notifications-hq==1.5.0

# deliberately uninstall previously installed newer package that was installed
# as a dependency or something of some other package, to be able to install
# an older version of jsonfield (which is required for django-extensions)
RUN pip uninstall --yes jsonfield
RUN pip install jsonfield==1.0.1

# more packages that we seem to need...:
RUN pip install django-extensions==2.1.4 odfpy==1.3.6 geoip2==2.9.0

# Install packages (this will be python2-compatible ones)
# "modeltranslation" due to crash on
# "ImportError: no module named modeltranslation"
# "djangorestframework" due to crash on
# ImportError: No module named rest_framework
# (hint from https://stackoverflow.com/questions/33308781/django-rest-framework-no-module-named-rest-framework)
# "python-openid" due to crash on
# ImportError: No module named openid_provider
#RUN pip install uwsgi

# Some requirement files said django==1.4.16 (released in 2014)
# But that ran into various problems...
# RUN pip install django==1.4.16
# 1.4.16 has the error:
# TypeError: can only concatenate tuple (not "list") to tuple
# in other words, the code in app doesn't work against it, so it _cannot_
# be that version.

# 1.11 first released in 2017, but 1.11.29 released in 2020
# update: running python => import django; django.__version__ revealed
# that what was on the server is actually 1.11.13
#RUN pip install django==1.11.13

#RUN pip install modeltranslation
#RUN pip install djangorestframework
#RUN pip install django-oidc-provider

#RUN pip install Fabric==1.9.0
#RUN pip install Markdown==2.4

# 0.6.28 failed for us, trying with 0.7.3
#RUN pip install distribute==0.6.28
#RUN pip install distribute==0.7.3

# originally, it was 1.2.4, but it didn't work, so
# trying 1.2.5 instead
#RUN pip install MySQL-python==1.2.4
#RUN pip install MySQL-python==1.2.5

#RUN pip install South==1.0
#RUN pip install Werkzeug==0.9.4
#RUN pip install django-extensions==1.1.0
#RUN pip install django-forms-bootstrap==3.0.0
#RUN pip install django-messages==0.5.0
#RUN pip install django-model-utils==2.0.3

# this seemed to be trying to access something it couldn't find,
# maybe a different version will work..
# some requirements.txt file said this:
#RUN pip install django-modeltranslation==0.8b2
# But server says 0.13b1

#RUN pip install django-modeltranslation==0.13b1

#RUN pip install django-serializers==0.5.0

# 2.3.14 came from some requirements.txt file, but seems wrong
#RUN pip install djangorestframework==2.3.14
#RUN pip install djangorestframework==3.9.0


#RUN pip install ecdsa==0.11
##RUN pip install ## FIXME: could not find svn URL in dependency_links for this package:
#RUN pip install flup==1.0.3.dev-20110405
#RUN pip install ipython==1.2.1
#RUN pip install itsdangerous==0.24
#RUN pip install paramiko==1.14.0
#RUN pip install pexpect==2.4
#RUN pip install pycrypto==2.6.1
#RUN pip install schematics==1.0-0
#RUN pip install simplejson==3.4.0
#RUN pip install six==1.8.0
#RUN pip install wsgiref==0.1.2

# worked with django 1.4.16, but not with 1.11, which is what
# I'm trying to run now
#RUN pip install django-notifications-hq==0.7.0
# all 0.6.* fails with "NameError: name 'patterns' is not defined"
# on gtoahpa: python => import notifications; notifications.__version__ says
# 1.5.0
#RUN pip install django-notifications-hq==1.5.0

# django-notifications-hq==1.5.0 fails with
#  File "/usr/local/lib/python2.7/site-packages/jsonfield/fields.py", line 22
#    def __init__(self, *args, dump_kwargs=None, load_kwargs=None, **kwargs):
# so, try to install a lower version of jsonfield. on server it's 1.0.1
# update: apparently, the image currently has json==3.0.0 ??
# try to uninstall, and deliberately install an older version ..?
#RUN pip uninstall --yes jsonfield
#RUN pip install jsonfield==1.0.1

# more packages that we seem to need...:
#RUN pip install django-extensions==2.1.4
#RUN pip install odfpy==1.3.6
#RUN pip install geoip2==2.9.0

# Copy in configuration files
COPY containerized_deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY containerized_deploy/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY containerized_deploy/nginx.conf /etc/nginx/nginx.conf

WORKDIR /app/sme_oahpa_project

# Copy in the application itself
COPY . /app/sme_oahpa_project/

# a custom file that is apparently needed, but didn't exist in svn,
# copied directly from the server
COPY containerized_deploy/settings_not_in_svn.py /app/sme_oahpa_project/sme_oahpa/settings_not_in_svn.py

# "django-admin.py" and not "django-admin" for django==1.4.16
# this makes the .mo files from .po files in locale/
RUN django-admin.py compilemessages

# We need this file (scp'd from gtoahpa-01.uit.no:/opt/smi/sme/bin)
RUN mkdir -p /opt/smi/sme/bin
COPY ped-sme.fst /opt/smi/sme/bin/ped-sme.fst
COPY sme-num.fst /opt/smi/sme/bin/sme-num.fst

# copy in the /media directory to /var/www/html
COPY media /var/www/html/davvi/media

# the database
# this directory has to exist, mariadbd writes its pidfile there
RUN mkdir -p /run/mysqld
#COPY containerized_deploy/my.cnf /etc/mysql/my.cnf

# Copy the database sql file
COPY containerized_deploy/sme_oahpa.sql.gz /tmp/sme_oahpa.sql.gz
COPY containerized_deploy/init_db.sh /tmp/init_db.sh
RUN chmod +x /tmp/init_db.sh && /tmp/init_db.sh

COPY containerized_deploy/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# numra needs this
COPY lookup /usr/local/bin/lookup

# not using entrypoint, instead executing shell script inside builder
# to make the database
#ENTRYPOINT [ "entrypoint.sh" ]

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf" ]

# uwsgi --chdir=/path/to/your/project \
#     --module=mysite.wsgi:application \
#     --env DJANGO_SETTINGS_MODULE=mysite.settings \
#     --master --pidfile=/tmp/project-master.pid \
#     --socket=127.0.0.1:49152 \      # can also be a file
#     --processes=5 \                 # number of worker processes
#     --uid=1000 --gid=2000 \         # if root, uwsgi can drop privileges
#     --harakiri=20 \                 # respawn processes taking more than 20 seconds
#     --max-requests=5000 \           # respawn processes after serving 5000 requests
#     --vacuum \                      # clear environment on exit
#     --home=/path/to/virtual/env \   # optional path to a virtualenv
#     --daemonize=/var/log/uwsgi/yourproject.log      # background the process
