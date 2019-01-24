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
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for object agreement"
# $P install.py -g $META/grammar_defaults.xml -q $META/obj_agreement_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA - Prs, Prt, FutDef, FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-PRS.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-PRT.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-FUTDEF.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA - Prs, Prt, FutDef, FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-PRS.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-PRT.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-FUTDEF.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TI - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-PRS.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-PRT.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-FUTDEF.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - II - Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/II-PRS.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA CNJ - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-CNJ-PRS.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-CNJ-PRT.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-CNJ-FUTINT.xml  2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for TI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-CNJ-PRS.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-CNJ-PRT.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TI-CNJ-FUTINT.xml  2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for AI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-CNJ-PRS.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-CNJ-PRT.xml  2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-AI-CNJ-FUTINT.xml  2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "stopped at: "
# date '+%T'
