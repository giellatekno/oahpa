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

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/eng_paradigms.txt -t $META/tags.txt -b 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/eng_fillings.xml --paradigmfile $META/eng_paradigms.txt --tagfile $META/tags.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "installing Vasta questions"
# $P install.py -g $META/grammar_defaults.xml -q $META/eng_questions_vasta.xml
# echo " "
# echo "done"
# echo "==================================================="


# echo "stopped at: "
# date '+%T'
