#!/bin/sh
PROJDIR="/home/neahtta/kursadict/"
ENVDIR="/home/neahtta/neahtta_env/"
PIDFILE="/home/neahtta/kursadict/pidfile.pid"

. $ENVDIR/bin/activate

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  # python manage.py runfcgi method=prefork host=127.0.0.1 port=$PORT pidfile=$PIDFILE
  python manage.py runfcgi --method=fork --host=127.0.0.1 --port=2323 --pidfile=$PIDFILE --daemonize

# python manage.py runfcgi --method=fork --host=127.0.0.1 --port=2323 --pidfile=pidfile.pid --daemonize

