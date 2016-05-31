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
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Trying to set up Plains Cree Oahpa


##
##  crk->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_crk.xml"
 $P install.py --file $DPS/N_crk.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
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
echo "feeding db with $DPS/Ipc_crk.xml"
$P install.py --file $DPS/Ipc_crk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/MWE_crk.xml"
# $P install.py --file $DPS/MWE_crk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $META/names.xml"
# $P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/prop_crknob.xml"
# $P install.py --file $DPS/prop_crknob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_crknob.xml"
# $P install.py --file $DPS/num_crknob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 #echo "==================================================="
 #echo "feeding db with $DPS/A_crk2X.xml"
 #$P install.py --file $DPS/A_crk2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_crk.xml"
 $P install.py --file $DPS/V_crk.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
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


# echo "==================================================="
# echo "feeding db with $DPS/adv_crknob.xml"
# $P install.py --file $DPS/adv_crknob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_crknob.xml"
# $P install.py --file $DPS/multiword_crknob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## nobcrk
# ##

#echo "==================================================="
#echo "feeding db with $DPN/N_nobcrk.xml"
#$P install.py --file $DPN/N_nobcrk.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_nobcrk.xml"
#$P install.py --file $DPN/num_nobcrk.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 #echo "==================================================="
 #echo "feeding db with $DPN/V_nobcrk.xml"
 #$P install.py --file $DPN/V_nobcrk.xml 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="
 
 #echo "==================================================="
 #echo "feeding db with $DPN/A_nobcrk.xml"
 #$P install.py --file $DPN/A_nobcrk.xml 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/adv_nobcrk.xml"
# $P install.py --file $DPN/adv_nobcrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/mwe_nobcrk.xml"
# $P install.py --file $DPN/mwe_nobcrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_nobcrk.xml"
# $P install.py --file $DPN/prop_nobcrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## fracrk
# ##


echo "==================================================="
echo "feeding db with $DPF/N_fracrk.xml"
$P install.py --file $DPF/N_fracrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Ipc_fracrk.xml"
$P install.py --file $DPF/Ipc_fracrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/MWE_fracrk.xml"
# $P install.py --file $DPF/MWE_fracrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_fracrk.xml"
# $P install.py --file $DPF/num_fracrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_fracrk.xml"
$P install.py --file $DPF/V_fracrk.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPF/A_fracrk.xml"
#$P install.py --file $DPF/A_fracrk.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPF/adv_fracrk.xml"
# $P install.py --file $DPF/adv_fracrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/mwe_fracrk.xml"
# $P install.py --file $DPF/mwe_fracrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_fracrk.xml"
# $P install.py --file $DPF/prop_fracrk.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engcrk
##


echo "==================================================="
echo "feeding db with $DPW/N_engcrk.xml"
$P install.py --file $DPW/N_engcrk.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Ipc_engcrk.xml"
$P install.py --file $DPW/Ipc_engcrk.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/MWE_engcrk.xml"
# $P install.py --file $DPW/MWE_engcrk.xml
# echo " "
# echo "done"
# echo "==================================================="


echo "==================================================="
echo "feeding db with $DPW/V_engcrk.xml"
$P install.py --file $DPW/V_engcrk.xml
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPW/A_engcrk.xml"
#$P install.py --file $DPW/A_engcrk.xml
#echo " "
#echo "done"
#echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_swecrk.xml"
# $P install.py --file $DPW/adv_swecrk.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_swecrk.xml"
# $P install.py --file $DPW/multiword_swecrk.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_swecrk.xml"
# $P install.py --file $DPW/prop_swecrk.xml
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_crknob.xml"
# $P install.py --file $DPS/grammaticalwords_crknob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_crk.xml"
# $P install.py --file $DPS/pron_crk.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_crk.xml"
# $P install.py --file $DPS/derverb_crk.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
# echo " "
# echo "done"
# echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with messages to feedback"
# $P install.py --messagefile $META/messages.crk.xml 2>>error.log
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
# $P install.py --messagefile $META/messages.fra.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# #  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# # Morfa-C


echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# $P manage.py mergetags
# $P manage.py fixtagattributes

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
echo "installing Morfa-C questions for translation"
$P install.py -g $META/grammar_defaults.xml -q $META/transl_questions.xml 2>>error.log
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
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-PRS.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-PRT.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-FUTDEF.xml 2>>error.log
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/V-TA-FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TI - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TI-PRS_PRT_FUTDEF_FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for V - TA CNJ - Prs, Prt, FutDef FutInt"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TA-CNJ-PRS_PRT_FUTINT.xml 2>>error.log
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
echo "installing Morfa-C questions for AI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TA-CNJ-PRS_PRT_FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for TI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/TI-CNJ-PRS_PRT_FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for AI - CNJ - Prt, Prs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions/AI-CNJ-PRT_PRS_FUTINT.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "installing grammar links for norwegian"
# $P install.py -i $META/grammatikklinker.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ###################
# # Vasta and VastaS
# ###################

echo "==================================================="
echo "installing Vasta questions"
$P install.py -g $META/grammar_defaults.xml -q $META/eng_questions_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

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
# $P install.py --messagefile $META/messages_vasta.crk.xml 2>>error.log
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


$P manage.py fixtagattributes
$P manage.py mergetags

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

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_crknob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_crknob.xml --feedbackfile $META/feedback_numerals.xml
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
