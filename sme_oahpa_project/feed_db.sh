#!/bin/sh

# run the script:
# sh feed_db.sh sme (= LLL1)

P="python"
LLL1=$1
log_file="db_install_error.log"
DATA="${LLL1}_data"
META="$DATA/meta_data"
SRC="$DATA/src"
XXX="$DATA/*2${LLL1}"

rm -fv $log_file

echo "==================================================="
echo "fixing collation to utf-8"
cat fix_collation.sql | $P manage.py dbshell
echo "==================================================="
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
##  sme->X
##

for xfile in $(ls $SRC/*.xml)
do
    fl=$(basename $xfile)
    # the first substring before the first '_' in the xml file name is the POS ('prop' for both pers and geo)
    POS=${fl%%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"
    echo "feeding db with $xfile: pos $POS"
    if [ "$fl" != "derverb_sme.xml" ] && [ "$fl" != "pron_sme.xml" ] ; then
	
	if [ -e "$PARA_FILE" ]; then
	    echo "... both w paradime and w tags"
	    $P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>$log_file
	else
	    echo "... both w/o paradime and w/o tags"
	    $P install.py --file $xfile 2>>$log_file
	fi
    # special treatment
    elif [ "$fl" == "derverb_sme.xml" ] ; then
    	 echo "... w tags but w/o paradime: append derverb_"
    	 $P install.py --file $xfile --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
    elif [ "$fl" == "pron_sme.xml" ] ; then
    	 echo "... w tags but w/o paradime: pron_"
    	 $P install.py --file $xfile --tagfile $META/tags.txt 2>>error.log
    fi
    echo "done"
    echo " "
done


# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "appending forms from $DPS/n_px.xml"
$P install.py --file $META/n_px.xml --tagfile $META/tags.txt --paradigmfile $META/n_px_paradigms.txt --append 2>>error.log
echo "done"
echo " "
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "appending forms from $DPS/v_pass.xml"
$P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>error.log
echo "done"
echo " "
echo "==================================================="



=======
=======
=======
=======
=======
=======
=======
=======

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>$log_file
echo " "
echo "done"
echo "==================================================="

# NB:
#sms_oahpa>export DJANGO_SETTINGS_MODULE=sms_oahpa.settings

for xfile in $(ls $SRC/*.xml)
do
    fl=$(basename $xfile)
    POS=${fl%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"


    echo "feeding db with: $xfile"


    if [ -e "$PARA_FILE" ]; then
	echo "File exists $PARA_FILE"

	$P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>$log_file

    else
	echo "File does not exist $PARA_FILE"

	$P install.py --file $xfile 2>>$log_file

    fi
    echo " "
    echo "done"
done

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>$log_file
  echo " "
  echo "done"
  echo "   "
done

echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="



$P manage.py mergetags
$P manage.py fixtagattributes



echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "stopped at: "
date '+%T'
