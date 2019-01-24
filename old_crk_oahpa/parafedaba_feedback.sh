#!/bin/sh

P="python2.7"

LANGDIR="crk"
if [ -n $INSTALL_SRC ] 
then
  DATA=$INSTALL_SRC
else
  DATA=/home/crk_oahpa/$LANGDIR
fi

DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/nobcrk"
DPF="$DATA/fracrk"
DPW="$DATA/engcrk"
DPE="$DATA/estcrk"
DPL="$DATA/latcrk"
DPR="$DATA/ruscrk"
DPD="$DATA/smecrk"
#WORDS=$PED_PATH/words/dicts/smenob/src

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.eng.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/N_crk.xml --feedbackfile $META/feedback_nouns.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $DPS/V_crk.xml --feedbackfile $META/feedback_verbs.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to pronouns"
$P install.py -f $DPS/Pron_crk.xml --feedbackfile $META/feedback_pronouns.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "stopped at: "
date '+%T'
