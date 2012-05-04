#!/bin/sh
python2.7 manage.py runfcgi method=prefork host=127.0.0.1 port=3032
