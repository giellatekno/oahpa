#!/bin/sh

#
# It's my hope that this will work to configure things quick. If not, it's at least a log of the things I've done to get things running.
#

P27="/usr/bin/env python2.7"

rm test.db && 
echo "Waiting for manage.py ... "

EXP=$(<<EOL expect -c "
	spawn $P27 manage.py syncdb
	expect \"Would you like to create one now? (yes/no): \"
	send \"yes\\r\"
	
	expect \"Username (Leave blank to use 'pyry'): \" 
	send \"asdf\\r\"
	
	expect \"E-mail address: \"
	send "asdf@asdf.com\\r"
	
	expect \"Password: \"
	send \"asdf\\r\"

	expect \"Password (again): \"
	send \"asdf\\r\"
	
	expect EOF"
EOL
)
echo "$EXP" &&
echo "Waiting to make sure test DB is created ... " &&
sleep 3 && 
$P27 install.py --file nouns_explanation_test.xml --tagfile $GTHOME/ped/rus/src/tags.txt --paradigmfile $GTHOME/ped/rus/src/paradigms.txt

# TODO: need to start using paradigm generation
# -r $GTHOME/ped/sma/src/tags.txt
# gtsvn/ped/sma/xml
# gtsvn/ped/sma/paradigm.txt
