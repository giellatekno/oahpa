#!/bin/bash

PROJDIR="/home/univ_oahpa/univ_oahpa/"
PIDFILE="/home/univ_oahpa/univ_oahpa/fastcgi.pid"
P="python2.7"
PORT=3032

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  $P manage.py runfcgi method=prefork host=127.0.0.1 port=$PORT pidfile=$PIDFILE

