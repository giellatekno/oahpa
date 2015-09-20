#!/bin/sh

P="python2.7"

LANGDIR="hdn"
DATA=$GTHOME/ped/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/nobhdn"
DPF="$DATA/frahdn"
DPW="$DATA/enghdn"
DPE="$DATA/esthdn"
DPL="$DATA/lathdn"
DPR="$DATA/rushdn"
DPD="$DATA/smehdn"
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
##  hdn->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_hdn.xml"
 $P install.py --file $DPS/N_hdn.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/Ipc_hdn.xml"
 $P install.py --file $DPS/Ipc_hdn.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/Pron_hdn.xml"
 $P install.py --file $DPS/Pron_hdn.xml --tagfile $META/tags.txt --paradigmfile $META/pron_paradigms.txt 2>>error.log
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
# echo "feeding db with $DPS/prop_hdnnob.xml"
# $P install.py --file $DPS/prop_hdnnob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_hdnnob.xml"
# $P install.py --file $DPS/num_hdnnob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 #echo "==================================================="
 #echo "feeding db with $DPS/A_hdn2X.xml"
 #$P install.py --file $DPS/A_hdn2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_hdn.xml"
 $P install.py --file $DPS/V_hdn.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
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
# echo "feeding db with $DPS/adv_hdnnob.xml"
# $P install.py --file $DPS/adv_hdnnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_hdnnob.xml"
# $P install.py --file $DPS/multiword_hdnnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## nobhdn
# ##

#echo "==================================================="
#echo "feeding db with $DPN/N_nobhdn.xml"
#$P install.py --file $DPN/N_nobhdn.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_nobhdn.xml"
#$P install.py --file $DPN/num_nobhdn.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 #echo "==================================================="
 #echo "feeding db with $DPN/V_nobhdn.xml"
 #$P install.py --file $DPN/V_nobhdn.xml 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="
 
 #echo "==================================================="
 #echo "feeding db with $DPN/A_nobhdn.xml"
 #$P install.py --file $DPN/A_nobhdn.xml 2>>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/adv_nobhdn.xml"
# $P install.py --file $DPN/adv_nobhdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/mwe_nobhdn.xml"
# $P install.py --file $DPN/mwe_nobhdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_nobhdn.xml"
# $P install.py --file $DPN/prop_nobhdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## frahdn
# ##


echo "==================================================="
echo "feeding db with $DPF/N_frahdn.xml"
$P install.py --file $DPF/N_frahdn.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Ipc_frahdn.xml"
$P install.py --file $DPF/Ipc_frahdn.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_frahdn.xml"
# $P install.py --file $DPF/num_frahdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_frahdn.xml"
$P install.py --file $DPF/V_frahdn.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPF/A_frahdn.xml"
#$P install.py --file $DPF/A_frahdn.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPF/adv_frahdn.xml"
# $P install.py --file $DPF/adv_frahdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/mwe_frahdn.xml"
# $P install.py --file $DPF/mwe_frahdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_frahdn.xml"
# $P install.py --file $DPF/prop_frahdn.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## enghdn
##


echo "==================================================="
echo "feeding db with $DPW/N_enghdn.xml"
$P install.py --file $DPW/N_enghdn.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Ipc_enghdn.xml"
$P install.py --file $DPW/Ipc_enghdn.xml
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPW/V_enghdn.xml"
$P install.py --file $DPW/V_enghdn.xml
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPW/A_enghdn.xml"
#$P install.py --file $DPW/A_enghdn.xml
#echo " "
#echo "done"
#echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_swehdn.xml"
# $P install.py --file $DPW/adv_swehdn.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_swehdn.xml"
# $P install.py --file $DPW/multiword_swehdn.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_swehdn.xml"
# $P install.py --file $DPW/prop_swehdn.xml
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_hdnnob.xml"
# $P install.py --file $DPS/grammaticalwords_hdnnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_hdn.xml"
# $P install.py --file $DPS/pron_hdn.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_hdn.xml"
# $P install.py --file $DPS/derverb_hdn.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.hdn.xml 2>>error.log
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
# $P install.py --messagefile $META/messages_vasta.hdn.xml 2>>error.log
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
$P install.py -f $DPS/N_hdn.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "adding feedback to verbs"
# $P install.py -f $DPS/v_hdnnob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_hdnnob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_hdnnob.xml --feedbackfile $META/feedback_numerals.xml
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
