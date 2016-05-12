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

# echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 
echo " "
echo "done"
echo "==================================================="

# ayaw

echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for translation"
$P install.py -g $META/grammar_defaults.xml -q $META/transl_questions.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for object agreement"
# $P install.py -g $META/grammar_defaults.xml -q $META/obj_agreement_questions.xml
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TA-PRS_PRT_FUTDEF_FUTINT.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TI - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TI-PRS_PRT_FUTDEF_FUTINT.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA CNJ - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TA-CNJ-PRS_PRT_FUTINT.xml
echo " "
echo "done"
echo "==================================================="

# TODO: +Prs missing

echo "==================================================="
echo "installing Morfa-C questions for V - II - Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/II-PRS.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for AI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TA-CNJ-PRS_PRT_FUTINT.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for TI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TI-CNJ-PRS_PRT_FUTINT.xml
echo " "
echo "done"
echo "==================================================="


# echo "stopped at: "
# date '+%T'
