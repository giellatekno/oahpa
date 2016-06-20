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
ENG="$DATA/engsrc"
DPE="$DATA/estcrk"
DPL="$DATA/latcrk"
DPR="$DATA/ruscrk"
DPD="$DATA/smecrk"
#WORDS=$PED_PATH/words/dicts/smenob/src

## vasta_eng_words

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/eng_paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

$P manage.py fixtagattributes


echo "==================================================="
echo "feeding db with $DPS/N_crk.xml"
$P install.py --file $ENG/N_eng.xml --tagfile $META/tags.txt --paradigmfile $META/eng_n_paradigms.txt --language eng
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/N_crk.xml"
$P install.py --file $ENG/N_Prop_eng.xml --tagfile $META/tags.txt --paradigmfile $META/eng_n_prop_paradigms.txt --language eng
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/A_crk.xml"
$P install.py --file $ENG/A_eng.xml --tagfile $META/tags.txt --paradigmfile $META/eng_a_paradigms.txt --language eng
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Pron_crk.xml"
$P install.py --file $ENG/Pron_eng.xml --tagfile $META/tags.txt --paradigmfile $META/eng_pron_paradigms.txt --language eng
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/V_crk.xml"
$P install.py --file $ENG/V_eng.xml --tagfile $META/tags.txt --paradigmfile $META/eng_v_paradigms.txt --language eng
echo " "
echo "done"
echo "==================================================="

## /vasta_eng_words


# vasta_questions

echo "==================================================="
echo "installing Vasta questions"
$P install.py -g $META/grammar_defaults.xml -q $META/eng_questions_vasta.xml 
echo " "
echo "done"
echo "==================================================="

### echo "Installing feedback messages for vasta"
### $P install.py --messagefile $META/messages_vasta.eng.xml 
### echo " "
### echo "done"
### echo "==================================================="
### 
### echo "==================================================="
### echo "Installing feedback messages for vasta - in English"
### $P install.py --messagefile $META/messages_vasta.eng.xml 
### echo " "
### echo "done"
### echo "==================================================="

## /vasta_questions

echo "stopped at: "
date '+%T'
