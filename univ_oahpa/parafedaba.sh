#!/bin/sh

P="python2.6"
DATA="data_sma/"
DPS="data_sma/sma"
META="data_sma/meta"
DPN="data_sma/nob"
DPF="data_sma/fin"
DPW="data_sma/swe"
SRC="ped/sma/src"
SP=$GTHOME/$SRC
WORDS=$GTHOME/words/dicts/smanob/src

##
##  sma->X
##

echo "==================================================="
echo "feeding db with $DPS/n_smanob.xml"
$P install.py --file $DPS/n_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $META/names.xml"
$P install.py --file $META/names.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smanob.xml"
$P install.py --file $DPS/prop_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smanob.xml"
$P install.py --file $DPS/propPl_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/num_smanob.xml"
$P install.py --file $META/num_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/a_smanob.xml"
$P install.py --file $DPS/a_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/a_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/v_smanob.xml"
$P install.py --file $DPS/v_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/adv_smanob.xml"
$P install.py --file $DPS/adv_smanob.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/multiword_smanob.xml"
$P install.py --file $DPS/multiword_smanob.xml
echo " "
echo "done"
echo "==================================================="

##
## nobsma
##

echo "==================================================="
echo "feeding db with $DPN/a_nobsma.xml"
$P install.py --file $DPN/a_nobsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/n_nobsma.xml"
$P install.py --file $DPN/n_nobsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/v_nobsma.xml"
$P install.py --file $DPN/v_nobsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/adv_nobsma.xml"
$P install.py --file $DPN/adv_nobsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/multiword_nobsma.xml"
$P install.py --file $DPN/multiword_nobsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/prop_nobsma.xml"
$P install.py --file $DPN/prop_nobsma.xml
echo " "
echo "done"
echo "==================================================="

##
## finsma
##

echo "==================================================="
echo "feeding db with $DPF/a_finsma.xml"
$P install.py --file $DPF/a_finsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/n_finsma.xml"
$P install.py --file $DPF/n_finsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/v_finsma.xml"
$P install.py --file $DPF/v_finsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/adv_finsma.xml"
$P install.py --file $DPF/adv_finsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/multiword_finsma.xml"
$P install.py --file $DPF/multiword_finsma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/prop_finsma.xml"
$P install.py --file $DPF/prop_finsma.xml
echo " "
echo "done"
echo "==================================================="

##
## swesma
##



echo "==================================================="
echo "feeding db with $DPW/a_swesma.xml"
$P install.py --file $DPW/a_swesma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/n_swesma.xml"
$P install.py --file $DPW/n_swesma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/v_swesma.xml"
$P install.py --file $DPW/v_swesma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/adv_swesma.xml"
$P install.py --file $DPW/adv_swesma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/multiword_swesma.xml"
$P install.py --file $DPW/multiword_swesma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/prop_swesma.xml"
$P install.py --file $DPW/prop_swesma.xml
echo " "
echo "done"
echo "==================================================="




echo "==================================================="
echo "feeding db with data_sma/sma/pronPers_smanob.xml"
$P install.py --file $DPS/pronPers_smanob.xml --tagfile $META/tags.txt --paradigmfile $META/pron_paradigms.txt 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with data_sma/meta/semantical_sets.xml"
$P install.py --sem data_sma/meta/semantical_sets.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile data_sma/meta/messages.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile data_sma/meta/messages.sma.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile data_sma/meta/messages.eng.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile data_sma/meta/messages.swe.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile data_sma/meta/messages.fin.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f data_sma/sma/n_smanob.xml --feedbackfile data_sma/meta/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f data_sma/sma/v_smanob.xml --feedbackfile data_sma/meta/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="

#  ... and then repeat for adjectives.

# Morfa-C 

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r data_sma/meta/paradigms.txt -t data_sma/meta/tags.txt -b
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smanob.xml --paradigmfile data_sma/meta/paradigms.txt --tagfile data_sma/meta/tags.txt
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q data_sma/meta/noun_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q data_sma/meta/verb_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q data_sma/meta/verb_problems.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for verbs"
# $P install.py -g $META/grammar_defaults.xml -q data_sma/meta/more_verb_questions.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for verbs"
# $P install.py -g $META/grammar_defaults.xml -q data_sma/meta/imprt_questions.xml
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q data_sma/meta/adjective_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for pronoun"
$P install.py -g $META/grammar_defaults.xml -q data_sma/meta/pron_questions.xml
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Optimizing tables"
cat optimize_analyze_tables.sql | $P manage.py dbshell
echo " "
echo "done"
echo "==================================================="

