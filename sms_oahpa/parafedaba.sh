#!/bin/sh

P="python2.7"
GTHOME="/Users/mslm/main/ped"
LANGDIR="sms"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
META="$DATA/meta"
DPN="$DATA/nobsms"
DPF="$DATA/finsms"
#DPW="$DATA/swesms"
#WORDS=$GTHOME/words/dicts/smsnob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
##  sms->X
##

echo "==================================================="
echo "feeding db with $DPS/n_sms2X.xml"
$P install.py --file $DPS/n_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $META/names.xml"
$P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smsnob.xml"
$P install.py --file $DPS/prop_smsnob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/num_smsnob.xml"
$P install.py --file $DPS/num_smsnob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/a_smsnob.xml"
$P install.py --file $DPS/a_smsnob.xml --tagfile $META/tags.txt --paradigmfile $META/a_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/v_smsnob.xml"
$P install.py --file $DPS/v_smsnob.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "feeding db with $DPS/v_pass.xml"
$P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/adv_smsnob.xml"
$P install.py --file $DPS/adv_smsnob.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/multiword_smsnob.xml"
$P install.py --file $DPS/multiword_smsnob.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## nobsms
##

echo "==================================================="
echo "feeding db with $DPN/a_nobsms.xml"
$P install.py --file $DPN/a_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/n_nobsms.xml"
$P install.py --file $DPN/n_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/num_nobsms.xml"
$P install.py --file $DPN/num_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/v_nobsms.xml"
$P install.py --file $DPN/v_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/adv_nobsms.xml"
$P install.py --file $DPN/adv_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/mwe_nobsms.xml"
$P install.py --file $DPN/mwe_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/prop_nobsms.xml"
$P install.py --file $DPN/prop_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## finsms
##

echo "==================================================="
echo "feeding db with $DPF/a_finsms.xml"
$P install.py --file $DPF/a_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/n_finsms.xml"
$P install.py --file $DPF/n_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/num_finsms.xml"
$P install.py --file $DPF/num_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/v_finsms.xml"
$P install.py --file $DPF/v_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/adv_finsms.xml"
$P install.py --file $DPF/adv_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/mwe_finsms.xml"
$P install.py --file $DPF/mwe_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/prop_finsms.xml"
$P install.py --file $DPF/prop_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## swesms - has not been created for the new format yet
##

# echo "==================================================="
# echo "feeding db with $DPW/a_swesms.xml"
# $P install.py --file $DPW/a_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/n_swesms.xml"
# $P install.py --file $DPW/n_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/v_swesms.xml"
# $P install.py --file $DPW/v_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_swesms.xml"
# $P install.py --file $DPW/adv_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_swesms.xml"
# $P install.py --file $DPW/multiword_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_swesms.xml"
# $P install.py --file $DPW/prop_swesms.xml
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/grammaticalwords_smsnob.xml"
$P install.py --file $DPS/grammaticalwords_smsnob.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pron_sms.xml"
$P install.py --file $DPS/pron_sms.xml --tagfile $META/tags.txt  2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/derverb_sms.xml"
$P install.py --file $DPS/derverb_sms.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantical_sets.xml"
$P install.py --sem $META/semantical_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.sms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.swe.xml 2>>error.log
echo " "
echo "done"
cho "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# Morfa-C 


echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smsnob.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

$P manage.py mergetags
$P manage.py fixtagattributes

echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for pronoun"
$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for numerals"
$P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for derivation"
$P install.py -g $META/grammar_defaults.xml -q $META/derivation_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

###################
# Vasta and VastaS
###################
echo "==================================================="
echo "installing Vasta questions"
$P install.py -g $META/grammar_defaults.xml -q $META/questions_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Vasta-S questions"
$P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "Installing feedback messages for vasta"
$P install.py --messagefile $META/messages_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in English"
$P install.py --messagefile $META/messages_vasta.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Finnish"
$P install.py --messagefile $META/messages_vasta.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in North Sámi"
$P install.py --messagefile $META/messages_vasta.sms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Swedish"
$P install.py --messagefile $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

#####
# Sahka
#####
echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting"
$P install.py -k $META/dialogue_firstmeeting.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - boy"
$P install.py -k $META/dialogue_firstmeeting_boy.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - girl"
$P install.py -k $META/dialogue_firstmeeting_girl.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - man"
$P install.py -k $META/dialogue_firstmeeting_man.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - grocery shop"
$P install.py -k $META/dialogue_grocery.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - adjectives in shop"
$P install.py -k $META/dialogue_shopadj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - visit"
$P install.py -k $META/dialogue_visit.xml 2>>error.log
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
$P install.py -f $DPS/n_smsnob.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $DPS/v_smsnob.xml --feedbackfile $META/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to adjectives"
$P install.py -f $DPS/a_smsnob.xml --feedbackfile $META/feedback_adjectives.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
$P install.py -f $DPS/num_smsnob.xml --feedbackfile $META/feedback_numerals.xml 
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

