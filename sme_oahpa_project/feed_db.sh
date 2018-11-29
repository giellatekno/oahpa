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
$P install.py -i $META/grammatikklinker.txt 2>>$log_file
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
    	 $P install.py --file $xfile --tagfile $META/tags.txt --append  2>>$log_file # TODO: test append with this
    elif [ "$fl" == "pron_sme.xml" ] ; then
    	 echo "... w tags but w/o paradime: pron_"
    	 $P install.py --file $xfile --tagfile $META/tags.txt 2>>$log_file
    fi
    echo "done"
    echo " "
done

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "appending forms from $DPS/n_px.xml"
$P install.py --file $META/n_px.xml --tagfile $META/tags.txt --paradigmfile $META/n_px_paradigms.txt --append 2>>$log_file
echo "done"
echo " "
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "appending forms from $DPS/v_pass.xml"
$P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>$log_file
echo "done"
echo " "
echo "==================================================="


##
## xxx2sme/*.xml
##

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py --file $xfile 2>>$log_file
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

MESSAGE_FILES="messages.xml
messages.sme.xml
messages.eng.xml
messages.swe.xml
messages.fin.xml"

for mf in $MESSAGE_FILES
do
    echo "==================================================="
    echo "messages to feedback: $META/$mf"
    $P install.py --messagefile $META/$mf 2>>$log_file
    echo " "
    echo "done"
    echo "==================================================="
done


#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now
echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms_all.txt --tagfile $META/tags.txt 2>>$log_file
echo " "
echo "done"
echo "==================================================="

$P manage.py mergetags
$P manage.py fixtagattributes


# installing question files for MorfaC, Vasta and VastaS
for q_file in $(ls $META/*_questions.xml)
do
  echo "installing questions: $q_file"
  $P install.py -g $META/grammar_defaults.xml -q $META/$q_file 2>>$log_file
  echo "done"
  echo "   "
done

### below this line no abstraction: TODO

echo "==================================================="
echo "Installing feedback messages for vasta"
$P install.py --messagefile $META/messages_vasta.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in English"
$P install.py --messagefile $META/messages_vasta.eng.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Finnish"
$P install.py --messagefile $META/messages_vasta.fin.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in North Sámi"
$P install.py --messagefile $META/messages_vasta.sme.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Swedish"
$P install.py --messagefile $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Checking for differences in feedback files"
$P check_feedback.py $META/messages_vasta.xml \
    $META/messages_vasta.fin.xml \
    $META/messages_vasta.sme.xml \
    $META/messages_vasta.eng.xml \
    $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

#####
# Sahka
#####

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting"
$P install.py -k $META/dialogue_firstmeeting.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - hello"
$P install.py -k $META/dialogue_hello.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - car"
$P install.py -k $META/dialogue_car.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - coffee break"
$P install.py -k $META/dialogue_coffee.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - grocery shop"
$P install.py -k $META/dialogue_grocery.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - adjectives in shop"
$P install.py -k $META/dialogue_shopadj.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - visit"
$P install.py -k $META/dialogue_visit.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="


# TODO: 
# fixtagattributes
# mergetags

$P manage.py fixattributes
$P manage.py mergetags
$P manage.py fixattributes

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/n_smenob.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $DPS/v_smenob.xml --feedbackfile $META/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to passive verbs"
$P install.py -f $DPS/v_smenob.xml --feedbackfile $META/feedback_passiveverbs.xml --append
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to adjectives"
$P install.py -f $DPS/a_smenob.xml --feedbackfile $META/feedback_adjectives.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
$P install.py -f $DPS/num_smenob.xml --feedbackfile $META/feedback_numerals.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to possessives"
$P install.py -f $META/n_px.xml --feedbackfile $META/feedback_n_px.xml --append
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "Optimizing tables"
#cat optimize_analyze_tables.sql | $P manage.py dbshell
#echo " "
#echo "done"
#echo "==================================================="

echo "stopped at: "
date '+%T'

