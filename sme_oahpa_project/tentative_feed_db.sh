#!/bin/sh

P="python"
LLL1=$1
log_file="db_install_error.log"
DATA="${LLL1}_data"
META="$DATA/meta_data"
SRC="$DATA/src"
XXX="$DATA/*2${LLL1}"

rm -fv $log_file

# NB:
#sme_oahpa>export DJANGO_SETTINGS_MODULE=sme_oahpa.settings

echo "==================================================="
echo "fixing collation to utf-8"
cat fix_collation.sql | $P manage.py dbshell
echo "==================================================="
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>$log_file
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>log_file
echo " "
echo "done"
echo "==================================================="



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

# TODO
# NB: the above for does not install correctly all files in parafedaba.sh
# due to inconsistency in naming it will install the following files without paradigms
echo "==================================================="
echo "installing remaining files in SRC"

  $P install.py --file $SRC/prop_pers_names_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>log_file
  $P install.py --file $SRC/prop_geo_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log

echo " "
echo "done"
echo "==================================================="

# These also are not included in the above for, since these are in $META
echo "==================================================="
echo "installing files in $META with paradigm"

  $P install.py --file $META/n_px.xml --tagfile $META/tags.txt --paradigmfile $META/n_px_paradigms.txt --append 2>>log_file
  $P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>log_file
  $P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms_all.txt --tagfile $META/tags.txt 2>>log_file

echo " "
echo "done"
echo "==================================================="


# Installing files in xxx2xxx
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


# NB: the following for install messages files not in parafedaba.sh:
#   noun_messages_level_test.xml
#   messages.sme.level_test.xml
#   morfaerrorfstmessages.xml
# a solution could be to mv them to folder disabled or delete them
for xfile in $(ls $META/*messages*.xml)
do

    echo "feeding db with: $xfile"

	  $P install.py --messagefile $xfile 2>>$log_file

    echo " "
    echo "done"
done


$P manage.py mergetags
$P manage.py fixtagattributes


# NB: the following for install questions files not in parafedaba.sh:
#   pron_questions_reflexive.xml
# a solution could be to mv them to folder disabled or delete them
for xfile in $(ls $META/*questions*.xml)
do

    echo "feeding db with: $xfile"

    $P install.py -g $META/grammar_defaults.xml -q $xfile 2>>log_file

    echo " "
    echo "done"
done



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



# NB: the following for install dialogue files not in parafedaba.sh:
#   dialogue_firstmeeting_boy.xml
#   dialogue_firstmeeting_girl.xml
#   dialogue_firstmeeting_man.xml
# a solution could be to mv them to folder disabled or delete them
for xfile in $(ls $META/*dialogue*.xml)
do

    echo "feeding db with: $xfile"

    $P install.py -k $xfile 2>>log_file

    echo " "
    echo "done"
done


$P manage.py fixattributes
$P manage.py mergetags
$P manage.py fixattributes


# TODO
# This could be done in a for as well, but the file-naming should be consistent (see sma_oahpa)
#   n_smenob --> n_feedback
#   v_smenob --> v_feedback
#   v_smenob --> passive ??
#   a_smenob --> a_feedback
#   num_smenob --> num_feedback
#   n_px_smenob --> ?

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $SRC/n_smenob.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $SRC/v_smenob.xml --feedbackfile $META/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to passive verbs"
$P install.py -f $SRC/v_smenob.xml --feedbackfile $META/feedback_passiveverbs.xml --append
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to adjectives"
$P install.py -f $SRC/a_smenob.xml --feedbackfile $META/feedback_adjectives.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
$P install.py -f $SRC/num_smenob.xml --feedbackfile $META/feedback_numerals.xml
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
