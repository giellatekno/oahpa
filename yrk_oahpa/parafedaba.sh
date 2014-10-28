#!/bin/sh
# Script for installing the database of Nenets Oahpa.

P="python2.7"
GTHOME="/Users/mslm/main/ped"
LANGDIR="yrk"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta-data"
DPN="$DATA/nobyrk"
DPF="$DATA/finyrk"
DPW="$DATA/engyrk"
DPE="$DATA/estyrk"
DPL="$DATA/latyrk"
DPR="$DATA/rusyrk"
DPG="$DATA/deuyrk"
#WORDS=$GTHOME/words/dicts/smenob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="



##
##  yrk->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_yrk2X.xml"
 $P install.py --file $DPS/N_yrk2X.xml 
 # --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $META/names.xml"
# $P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/prop_yrknob.xml"
# $P install.py --file $DPS/prop_yrknob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_yrknob.xml"
# $P install.py --file $DPS/num_yrknob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/A_yrk2X.xml"
 $P install.py --file $DPS/A_yrk2X.xml 
 # --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_yrk2X.xml"
 $P install.py --file $DPS/V_yrk2X.xml 
 # --tagfile $META/tags.txt --paradigmfile $META/V_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# # NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
# echo "==================================================="
# echo "feeding db with $DPS/v_pass.xml"
# $P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/Adv_yrk2X.xml"
$P install.py --file $DPS/Adv_yrk2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/MWE_yrk2X.xml"
$P install.py --file $DPS/MWE_yrk2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Num_yrk2X.xml"
$P install.py --file $DPS/Num_yrk2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="



# ##
# ## finyrk
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finyrk.xml"
$P install.py --file $DPF/N_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Num_finyrk.xml"
$P install.py --file $DPF/Num_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finyrk.xml"
$P install.py --file $DPF/V_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finyrk.xml"
$P install.py --file $DPF/A_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPF/Adv_finyrk.xml"
$P install.py --file $DPF/Adv_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/MWE_finyrk.xml"
$P install.py --file $DPF/MWE_finyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_finyrk.xml"
# $P install.py --file $DPF/prop_finyrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engyrk
##


echo "==================================================="
echo "feeding db with $DPW/N_engyrk.xml"
$P install.py --file $DPW/N_engyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_engyrk.xml"
$P install.py --file $DPW/V_engyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_engyrk.xml"
$P install.py --file $DPW/A_engyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Adv_engyrk.xml"
$P install.py --file $DPW/Adv_engyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/MWE_engyrk.xml"
$P install.py --file $DPW/MWE_engyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Num_engyrk.xml"
$P install.py --file $DPW/Num_engyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## rusyrk
##


echo "==================================================="
echo "feeding db with $DPR/N_rusyrk.xml"
$P install.py --file $DPR/N_rusyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_rusyrk.xml"
$P install.py --file $DPR/V_rusyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_rusyrk.xml"
$P install.py --file $DPR/A_rusyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Adv_rusyrk.xml"
$P install.py --file $DPR/Adv_rusyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/MWE_rusyrk.xml"
$P install.py --file $DPR/MWE_rusyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Num_rusyrk.xml"
$P install.py --file $DPR/Num_rusyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## deuyrk
##


echo "==================================================="
echo "feeding db with $DPG/N_deuyrk.xml"
$P install.py --file $DPG/N_deuyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPG/V_deuyrk.xml"
$P install.py --file $DPG/V_deuyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPG/A_deuyrk.xml"
$P install.py --file $DPG/A_deuyrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPG/Adv_deuyrk.xml"
$P install.py --file $DPG/Adv_deuyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPG/MWE_deuyrk.xml"
$P install.py --file $DPG/MWE_deuyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPG/Num_deuyrk.xml"
$P install.py --file $DPG/Num_deuyrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_yrknob.xml"
# $P install.py --file $DPS/grammaticalwords_yrknob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_yrk.xml"
# $P install.py --file $DPS/pron_yrk.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_yrk.xml"
# $P install.py --file $DPS/derverb_yrk.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
# echo " "
# echo "done"
# echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.yrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.eng.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.swe.xml 2>>error.log
# echo " "
# echo "done"
# cho "==================================================="

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.fin.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# #  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# # Morfa-C


#echo "==================================================="
#echo "installing Morfa-C word fillings"
#$P install.py -f $META/fillings.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

# $P manage.py mergetags
# $P manage.py fixtagattributes

#echo "==================================================="
#echo "installing Morfa-C questions for nouns"
#$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "installing Morfa-C questions for verbs"
#$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for pronoun"
# $P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for adjectives"
# $P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for numerals"
# $P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for derivation"
# $P install.py -g $META/grammar_defaults.xml -q $META/derivation_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing grammar links for norwegian"
# $P install.py -i $META/grammatikklinker.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ###################
# # Vasta and VastaS
# ###################
# echo "==================================================="
# echo "installing Vasta questions"
# $P install.py -g $META/grammar_defaults.xml -q $META/questions_vasta.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Vasta-S questions"
# $P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "Installing feedback messages for vasta"
# $P install.py --messagefile $META/messages_vasta.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing feedback messages for vasta - in English"
# $P install.py --messagefile $META/messages_vasta.eng.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing feedback messages for vasta - in Finnish"
# $P install.py --messagefile $META/messages_vasta.fin.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing feedback messages for vasta - in North Sámi"
# $P install.py --messagefile $META/messages_vasta.yrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing feedback messages for vasta - in Swedish"
# $P install.py --messagefile $META/messages_vasta.swe.xml
# echo " "
# echo "done"
# echo "==================================================="

# #####
# # Sahka
# #####
# echo "==================================================="
# echo "Installing dialogues for Sahka - firstmeeting"
# $P install.py -k $META/dialogue_firstmeeting.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - firstmeeting - boy"
# $P install.py -k $META/dialogue_firstmeeting_boy.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - firstmeeting - girl"
# $P install.py -k $META/dialogue_firstmeeting_girl.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - firstmeeting - man"
# $P install.py -k $META/dialogue_firstmeeting_man.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - grocery shop"
# $P install.py -k $META/dialogue_grocery.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - adjectives in shop"
# $P install.py -k $META/dialogue_shopadj.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "Installing dialogues for Sahka - visit"
# $P install.py -k $META/dialogue_visit.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# # TODO:
# # fixtagattributes
# # mergetags

# $P manage.py fixattributes
# $P manage.py mergetags
# $P manage.py fixattributes

# echo "==================================================="
# echo "adding feedback to verbs"
# $P install.py -f $DPS/v_yrknob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_yrknob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_yrknob.xml --feedbackfile $META/feedback_numerals.xml
# echo " "
# echo "done"
# echo "==================================================="

# #echo "==================================================="
# #echo "Optimizing tables"
# #cat optimize_analyze_tables.sql | $P manage.py dbshell
# #echo " "
# #echo "done"
# #echo "==================================================="

echo "stopped at: "
date '+%T'
