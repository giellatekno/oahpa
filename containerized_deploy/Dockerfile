# Python2 builder image (this compiles from source)
FROM docker.io/library/debian:bookworm AS python2

WORKDIR /tmp

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates gettext \
    autoconf automake bzip2 dpkg-dev file g++ gcc \
    imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev \
    libdb-dev libevent-dev libffi-dev libgdbm-dev libglib2.0-dev \
    libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev \
    libmagickwand-dev libmaxminddb-dev libncurses5-dev \
    libncursesw5-dev libpng-dev libpq-dev libreadline-dev libsqlite3-dev \
    libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev \
    libyaml-dev make patch unzip xz-utils zlib1g-dev \
    libmariadb-dev-compat libmariadb-dev

RUN set -eux && \
    curl -O https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz && \
    tar -Jxf Python-2.7.18.tar.xz

WORKDIR /tmp/Python-2.7.18

RUN set -ex && \
    ./configure \
    --prefix=/tmp/installed \
    --enable-optimizations \
    --with-lto \
    --enable-option-checking=fatal \
    --enable-shared \
    --enable-unicode=ucs4 && \
    make -j PROFILE_TASK='-m test.regrtest --pgo test_array test_base64 test_binascii test_binhex test_binop test_bytes test_c_locale_coercion test_class test_cmath test_codecs test_compile test_complex test_csv test_decimal test_dict test_float test_fstring test_hashlib test_io test_iter test_json test_long test_math test_memoryview test_pickle test_re test_set test_slice test_struct test_threading test_time test_traceback test_unicode ' && \
    make install



# Mysql image. The tarball contains pre-compiled files.
# Is just copied in and extracted
# TODO this may not save that much time. probably not needed to have a builder
# image just for this
FROM docker.io/library/debian:bookworm AS mysql

COPY containerized_deploy/mysql-5.6.51-linux-glibc2.12-x86_64.tar.gz /tmp
RUN cd /tmp && tar -zxf mysql-5.6.51-linux-glibc2.12-x86_64.tar.gz



FROM docker.io/library/debian:bookworm

WORKDIR /tmp/python2
COPY --from=python2 /tmp/installed /tmp/python2
RUN cp -r bin include lib share /usr/

WORKDIR /tmp/mysql
COPY --from=mysql /tmp/mysql-5.6.51-linux-glibc2.12-x86_64 /tmp/mysql
RUN cp -r bin include lib share /usr

# need ssl (libssl3) to download pip packages
# need a c compiler to build c extensions for python
# also install packages we need: uwsgi, supervisord, nginx, and mariadb-server
# also gettext, to compile translation messages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libssl-dev libssl3 build-essential \
    gettext \
    uwsgi supervisor nginx mariadb-server

RUN curl https://apertium.projectjj.com/apt/install-nightly.sh | bash

RUN apt-get update && apt-get install -y --no-install-recommends hfst

RUN python -m ensurepip

# Install dependencies
# This list of specific versions was tediously determined through trial and
# error...
# voro needs kitchen==1.1.1
RUN pip install django==1.11.13 Fabric==1.9.0 Markdown==2.4 jsonfield==1.0.1 distribute==0.7.3 MySQL-python==1.2.5 South==1.0 Werkzeug==0.9.4 django-extensions==2.1.4 django-forms-bootstrap==3.0.0 django-messages==0.5.0 django-model-utils==2.0.3 django-modeltranslation==0.13b1 django-serializers==0.5.0 djangorestframework==3.9.0 ecdsa==0.11 flup==1.0.3.dev-20110405 ipython==1.2.1 itsdangerous==0.24 paramiko==1.14.0 pexpect==2.4 pycrypto==2.6.1 schematics==1.0-0 simplejson==3.4.0 six==1.8.0 wsgiref==0.1.2 django-notifications-hq==1.5.0 odfpy==1.3.6 geoip2==2.9.0 kitchen==1.1.1

# This plugin is not available anymore in bookworm (version 12, released 2023)
# So it was downloaded from the archives for buster (10, released 2019, eol 2024)
# to make dpkg install it, we must --force-all our way through the dependency
# problems.. This also means that apt will be in an "unresolved dependencies"
# state after this, and so, this must be the last `apt` command that we run.
COPY containerized_deploy/uwsgi-plugin-python_2.0.18-1_amd64.deb /tmp/
RUN dpkg --install --force-all /tmp/uwsgi-plugin-python_2.0.18-1_amd64.deb

# this directory has to exist, mariadbd writes its pidfile there
RUN mkdir -p /run/mysqld

# Import database
COPY containerized_deploy/sme_oahpa.sql.gz /tmp/sme_oahpa.sql.gz
COPY containerized_deploy/sma_oahpa.sql.gz /tmp/sma_oahpa.sql.gz
COPY containerized_deploy/sms_oahpa.sql.gz /tmp/sms_oahpa.sql.gz
COPY containerized_deploy/smn_oahpa.sql.gz /tmp/smn_oahpa.sql.gz
COPY containerized_deploy/myv_oahpa.sql.gz /tmp/myv_oahpa.sql.gz
COPY containerized_deploy/vro_oahpa.sql.gz /tmp/vro_oahpa.sql.gz
COPY containerized_deploy/fkv_oahpa.sql.gz /tmp/fkv_oahpa.sql.gz
COPY containerized_deploy/crk_oahpa.sql.gz /tmp/crk_oahpa.sql.gz
COPY containerized_deploy/est_oahpa.sql.gz /tmp/est_oahpa.sql.gz
COPY containerized_deploy/init_db.sh /tmp/init_db.sh
RUN chmod +x /tmp/init_db.sh && /tmp/init_db.sh

# Configuration files
COPY containerized_deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY containerized_deploy/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY containerized_deploy/nginx.conf /etc/nginx/nginx.conf
COPY containerized_deploy/my.cnf /etc/mysql/my.cnf

# numra needs this
COPY containerized_deploy/lookup /usr/local/bin/lookup

# media is served statically directly from the root by nginx
# TODO I believe this is the same folder for every instance, but unsure
COPY media /var/www/html

# fsts are expected to be in a certain directory
#COPY containerized_deploy/ped-sme.fst /opt/smi/sme/bin/ped-sme.fst
#COPY containerized_deploy/sme-num.fst /opt/smi/sme/bin/sme-num.fst

COPY containerized_deploy/uwsgi_vassals /etc/uwsgi/vassals

# TODO anders: there are many paths in various config files that
# defines /home/oahpa/ as the root directory for the application.
# However, further down, these paths should all be rewritten, but
# there could still be things that doesnt work because of wrong paths...
# (it's hard to know what it may affect) -- so it's maybe better
# and easier to use /home/oahpa instead of /app inside the image.
# besides, inside the image, the path really doesn't matter anyway.
# IF CHANGING THIS, MAKE SURE TO FIND ALL PLACES WHERE /app IS USED!
WORKDIR /app

# Copy in files we need to run the project vessels
COPY crk_oahpa_project /app/crk_oahpa_project
COPY est_oahpa_project /app/est_oahpa_project
COPY fkv_oahpa_project /app/fkv_oahpa_project
COPY myv_oahpa_project /app/myv_oahpa_project
COPY sma_oahpa_project /app/sma_oahpa_project
COPY sme_oahpa_project /app/sme_oahpa_project
COPY smn_oahpa_project /app/smn_oahpa_project
COPY sms_oahpa_project /app/sms_oahpa_project
COPY vro_oahpa_project /app/vro_oahpa_project

# Copy settings_not_in_svn.py to where it needs to be.
RUN cp /app/crk_oahpa_project/settings_not_in_svn.py /app/crk_oahpa_project/crk_oahpa/settings_not_in_svn.py
RUN cp /app/est_oahpa_project/settings_not_in_svn.py /app/est_oahpa_project/est_oahpa/settings_not_in_svn.py
RUN cp /app/fkv_oahpa_project/settings_not_in_svn.py /app/fkv_oahpa_project/fkv_oahpa/settings_not_in_svn.py
RUN cp /app/myv_oahpa_project/settings_not_in_svn.py /app/myv_oahpa_project/myv_oahpa/settings_not_in_svn.py
RUN cp /app/sma_oahpa_project/settings_not_in_svn.py /app/sma_oahpa_project/sma_oahpa/settings_not_in_svn.py
RUN cp /app/sme_oahpa_project/settings_not_in_svn.py /app/sme_oahpa_project/sme_oahpa/settings_not_in_svn.py
RUN cp /app/smn_oahpa_project/settings_not_in_svn.py /app/smn_oahpa_project/smn_oahpa/settings_not_in_svn.py
RUN cp /app/sms_oahpa_project/settings_not_in_svn.py /app/sms_oahpa_project/sms_oahpa/settings_not_in_svn.py
RUN cp /app/vro_oahpa_project/settings_not_in_svn.py /app/vro_oahpa_project/vro_oahpa/settings_not_in_svn.py

# Update the paths in these settings_not_in_svn.py files
RUN find . -name settings_not_in_svn.py -exec sed --in-place -e 's,/home/oahpa/,/app/,g' {} \;

# This replaces the SECRET_KEY = '...' with a new secret key for each lang
COPY containerized_deploy/roll_keys.sh /tmp/roll_keys.sh
RUN /tmp/roll_keys.sh

# vro: crashes on no attribute in settings, so just add this
RUN echo "MEDIA_DIR = '/app/oahpa/media/'" >> /app/vro_oahpa_project/vro_oahpa/settings_not_in_svn.py
# TODO: what even is this directory?

# vro complained "template liv_oahpa.html not found", so lets try to install it
COPY liv_oahpa /app/liv_oahpa

# Compile translations for all instances
RUN cd /app && django-admin compilemessages

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf" ]

