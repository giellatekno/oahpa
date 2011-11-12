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
sleep 5 && 
$P27 install.py --file data_sma/sma/n_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt && 
$P27 install.py --file data_sma/sma/a_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt &&
$P27 install.py --file data_sma/sma/v_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt &&
$P27 install.py --file data_sma/sma/adv_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt &&
$P27 install.py --file data_sma/sma/multiword_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt &&
$P27 install.py --pronoun $GTHOME/words/dicts/smanob/src/pronPers_smanob.xml --tagfile $GTHOME/ped/sma/src/tags.txt --paradigmfile $GTHOME/ped/sma/src/paradigms.txt &&
$P27 install.py --sem data_sma/meta/semantical_sets.xml &&
$P27 install.py --file data_sma/nob/n_nobsme.xml &&
$P27 install.py --file data_sma/nob/a_nobsme.xml &&
$P27 install.py --file data_sma/nob/v_nobsme.xml &&

# feedback

$P27 install.py -m data_sma/meta/messages.xml &&
$P27 install.py -f data_sma/sma/n_smanob.xml  -e data_sma/meta/feedback_nouns.xml &&
$P27 install.py -f data_sma/sma/v_smanob.xml  -e data_sma/meta/feedback_verbs.xml


# TODO: need to start using paradigm generation
# -r $GTHOME/ped/sma/src/tags.txt
# gtsvn/ped/sma/xml
# gtsvn/ped/sma/paradigm.txt
