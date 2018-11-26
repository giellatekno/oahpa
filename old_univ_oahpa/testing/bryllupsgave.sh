#!/bin/sh

#
# It's my hope that this will work to configure things quick. If not, it's at least a log of the things I've done to get things running.
#

P27="/usr/bin/env python2.7"
export TAGFILE=/Users/pyry/gtsvn/ped/sma/src/tags.txt
export PARADIGMFILE=/Users/pyry/gtsvn/ped/sma/src/paradigms.txt
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
sleep 5 && 
python2.7 install.py --file testing/bryllupsgave_smanob.xml --tagfile $TAGFILE --paradigmfile $PARADIGMFILE && 
$P27 install.py --sem data_sma/meta/semantical_sets.xml &&
python2.7 install.py --file testing/bryllupsgave_nobsma.xml 
sleep 2


# TODO: need to start using paradigm generation
# -r $GTHOME/ped/sma/src/tags.txt
# gtsvn/ped/sma/xml
# gtsvn/ped/sma/paradigm.txt
