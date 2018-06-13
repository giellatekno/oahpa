#!/bin/sh

P="python2.7"
GTHOME="/home/sms_oahpa"
LANGDIR="sms"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
META="$DATA/meta"
DPN="$DATA/nobsms"
DPF="$DATA/finsms"
DPR="$DATA/russms"
DPE="$DATA/engsms"
#WORDS=$GTHOME/words/dicts/smsnob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
##  sms->X
##

#U    src/det_sms2X.xml
#U    src/pro_sms2X.xml
#U    src/pcle_sms2X.xml

echo "==================================================="
echo "feeding db with $DPS/N_sms2X.xml"
$P install.py --file $DPS/N_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $META/N_Prop_sms2X.xml"
$P install.py --file $DPS/N_Prop_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/num_sms2X.xml"
$P install.py --file $DPS/Num_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/Num_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/a_sms2X.xml"
$P install.py --file $DPS/A_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/v_sms2X.xml"
$P install.py --file $DPS/V_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/V_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.


echo "==================================================="
echo "feeding db with $DPS/Adv_sms2X.xml"
$P install.py --file $DPS/Adv_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Adp_sms2X.xml"
$P install.py --file $DPS/Adp_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/CC_sms2X.xml"
$P install.py --file $DPS/CC_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/CS_sms2X.xml"
$P install.py --file $DPS/CS_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Interj_sms2X.xml"
$P install.py --file $DPS/Interj_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Det_sms2X.xml"
$P install.py --file $DPS/Det_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Pron_sms2X.xml"
$P install.py --file $DPS/Pron_sms2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Pcle_sms2X.xml"
$P install.py --file $DPS/Pcle_sms2X.xml 2>>error.log
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
echo "feeding db with $DPN/adp_nobsms.xml"
$P install.py --file $DPN/adp_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/prop_nobsms.xml"
$P install.py --file $DPN/prop_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/cs_nobsms.xml"
$P install.py --file $DPS/cs_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/i_nobsms.xml"
$P install.py --file $DPS/i_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/det_nobsms.xml"
$P install.py --file $DPS/det_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pro_nobsms.xml"
$P install.py --file $DPS/pro_nobsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pcle_nobsms.xml"
$P install.py --file $DPS/pcle_nobsms.xml 2>>error.log
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
echo "feeding db with $DPF/adp_finsms.xml"
$P install.py --file $DPF/adp_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/prop_finsms.xml"
$P install.py --file $DPF/prop_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/cs_finsms.xml"
$P install.py --file $DPF/cs_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/i_finsms.xml"
$P install.py --file $DPF/i_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/det_finsms.xml"
$P install.py --file $DPF/det_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/pro_finsms.xml"
$P install.py --file $DPF/pro_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/pcle_finsms.xml"
$P install.py --file $DPF/pcle_finsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## engsms
##

echo "==================================================="
echo "feeding db with $DPE/a_engsms.xml"
$P install.py --file $DPE/a_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/n_engsms.xml"
$P install.py --file $DPE/n_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/v_engsms.xml"
$P install.py --file $DPE/v_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/adv_engsms.xml"
$P install.py --file $DPE/adv_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/adp_engsms.xml"
$P install.py --file $DPE/adp_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/prop_engsms.xml"
$P install.py --file $DPE/prop_engsms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/cs_engsms.xml"
$P install.py --file $DPE/cs_engsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/i_engsms.xml"
$P install.py --file $DPE/i_engsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/det_engsms.xml"
$P install.py --file $DPE/det_engsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/pro_engsms.xml"
$P install.py --file $DPE/pro_engsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/pcle_engsms.xml"
$P install.py --file $DPE/pcle_engsms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## russms
##

echo "==================================================="
echo "feeding db with $DPR/a_russms.xml"
$P install.py --file $DPR/a_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/n_russms.xml"
$P install.py --file $DPR/n_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/v_russms.xml"
$P install.py --file $DPR/v_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/adv_russms.xml"
$P install.py --file $DPR/adv_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/adp_russms.xml"
$P install.py --file $DPR/adp_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/prop_russms.xml"
$P install.py --file $DPR/prop_russms.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/cs_russms.xml"
$P install.py --file $DPR/cs_russms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/i_russms.xml"
$P install.py --file $DPR/i_russms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/det_russms.xml"
$P install.py --file $DPR/det_russms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/pro_russms.xml"
$P install.py --file $DPR/pro_russms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/pcle_russms.xml"
$P install.py --file $DPR/pcle_russms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


#echo "==================================================="
#echo "feeding db with $DPS/grammaticalwords_smsnob.xml"
#$P install.py --file $DPS/grammaticalwords_smsnob.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/pron_sms.xml"
#$P install.py --file $DPS/pron_sms.xml --tagfile $META/tags.txt  2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/derverb_sms.xml"
#$P install.py --file $DPS/derverb_sms.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
#echo " "
#echo "done"
#echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.sms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# Morfa-C 


echo "==================================================="
echo "installing Morfa-C word fillings"
#$P install.py -f $META/fillings_smsnob.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>error.log
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
#$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for pronoun"
#$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
#$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for numerals"
#$P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for derivation"
#$P install.py -g $META/grammar_defaults.xml -q $META/derivation_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
#$P install.py -i $META/grammatikklinker.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

###################
# Vasta and VastaS
###################
echo "==================================================="
echo "installing Vasta questions"
#$P install.py -g $META/grammar_defaults.xml -q $META/questions_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Vasta-S questions"
#$P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "Installing feedback messages for vasta"
#$P install.py --messagefile $META/messages_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in English"
#$P install.py --messagefile $META/messages_vasta.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Finnish"
#$P install.py --messagefile $META/messages_vasta.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in North Sámi"
#$P install.py --messagefile $META/messages_vasta.sms.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in engdish"
#$P install.py --messagefile $META/messages_vasta.eng.xml
echo " "
echo "done"
echo "==================================================="

#####
# Sahka
#####
echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting"
#$P install.py -k $META/dialogue_firstmeeting.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - boy"
#$P install.py -k $META/dialogue_firstmeeting_boy.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - girl"
#$P install.py -k $META/dialogue_firstmeeting_girl.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - man"
#$P install.py -k $META/dialogue_firstmeeting_man.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - grocery shop"
#$P install.py -k $META/dialogue_grocery.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - adjectives in shop"
#$P install.py -k $META/dialogue_shopadj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - visit"
#$P install.py -k $META/dialogue_visit.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# TODO: 
# fixtagattributes
# mergetags

$P manage.py fixtagattributes
$P manage.py mergetags
$P manage.py fixtagattributes

echo "==================================================="
echo "adding feedback to nouns"
#$P install.py -f $DPS/n_smsnob.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
#$P install.py -f $DPS/v_smsnob.xml --feedbackfile $META/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to adjectives"
#$P install.py -f $DPS/a_smsnob.xml --feedbackfile $META/feedback_adjectives.xml 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
#$P install.py -f $DPS/num_smsnob.xml --feedbackfile $META/feedback_numerals.xml 
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

