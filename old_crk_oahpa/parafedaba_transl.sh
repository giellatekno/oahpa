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

echo "==================================================="
echo "feeding db with $META/eng_fillings.xml"
$P install.py --file $META/eng_fillings.xml --tagfile $META/tags.txt --paradigmfile $META/eng_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Pron_crk.xml"
$P install.py --file $DPS/Pron_crk.xml --tagfile $META/tags.txt --paradigmfile $META/pron_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for translation"
$P install.py -g $META/grammar_defaults.xml -q $META/transl_questions_examples.xml
echo " "
echo "done"
echo "==================================================="

