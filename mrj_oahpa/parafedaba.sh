#!/bin/sh

P="python2.7"
GTHOME="/Users/mslm/main/ped"
LANGDIR="mrj"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/deumrj"
DPF="$DATA/finmrj"
DPW="$DATA/engmrj"
DPE="$DATA/estmrj"
DPL="$DATA/latmrj"
DPR="$DATA/rusmrj"
DPD="$DATA/smemrj"
#WORDS=$GTHOME/words/dicts/smedeu/src

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Filling the Hill Mari Oahpa database with data


##
##  mrj->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_mrj2X.xml"
 $P install.py --file $DPS/N_mrj2X.xml 
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
# echo "feeding db with $DPS/prop_mrjdeu.xml"
# $P install.py --file $DPS/prop_mrjdeu.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_mrjdeu.xml"
# $P install.py --file $DPS/num_mrjdeu.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/A_mrj2X.xml"
 $P install.py --file $DPS/A_mrj2X.xml 
 # --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_mrj2X.xml"
 $P install.py --file $DPS/V_mrj2X.xml 
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
echo "feeding db with $DPS/Adv_mrj2X.xml"
$P install.py --file $DPS/Adv_mrj2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Mwe_mrj2X.xml"
$P install.py --file $DPS/Mwe_mrj2X.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# ##
# ## deumrj
# ##

echo "==================================================="
echo "feeding db with $DPN/N_deumrj.xml"
$P install.py --file $DPN/N_deumrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_deumrj.xml"
#$P install.py --file $DPN/num_deumrj.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/V_deumrj.xml"
 $P install.py --file $DPN/V_deumrj.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPN/A_deumrj.xml"
 $P install.py --file $DPN/A_deumrj.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Adv_deumrj.xml"
$P install.py --file $DPN/Adv_deumrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Mwe_deumrj.xml"
$P install.py --file $DPN/Mwe_deumrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_deumrj.xml"
# $P install.py --file $DPN/prop_deumrj.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## finmrj
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finmrj.xml"
$P install.py --file $DPF/N_finmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_finmrj.xml"
# $P install.py --file $DPF/num_finmrj.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finmrj.xml"
$P install.py --file $DPF/V_finmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finmrj.xml"
$P install.py --file $DPF/A_finmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPF/Adv_finmrj.xml"
$P install.py --file $DPF/Adv_finmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Mwe_finmrj.xml"
$P install.py --file $DPF/Mwe_finmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_finmrj.xml"
# $P install.py --file $DPF/prop_finmrj.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engmrj
##


echo "==================================================="
echo "feeding db with $DPW/N_engmrj.xml"
$P install.py --file $DPW/N_engmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_engmrj.xml"
$P install.py --file $DPW/V_engmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_engmrj.xml"
$P install.py --file $DPW/A_engmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Adv_engmrj.xml"
$P install.py --file $DPW/Adv_engmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Mwe_engmrj.xml"
$P install.py --file $DPW/Mwe_engmrj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


##                                                                                
## rusmrj                                                                        
##                                                                                                                                                           

echo "==================================================="
echo "feeding db with $DPR/N_rusmrj.xml"
$P install.py --file $DPR/N_rusmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_rusmrj.xml"
$P install.py --file $DPR/V_rusmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_rusmrj.xml"
$P install.py --file $DPR/A_rusmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Adv_rusmrj.xml"
$P install.py --file $DPR/Adv_rusmrj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Mwe_rusmrj.xml"
$P install.py --file $DPR/Mwe_rusmrj.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_mrjdeu.xml"
# $P install.py --file $DPS/grammaticalwords_mrjdeu.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_mrj.xml"
# $P install.py --file $DPS/pron_mrj.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_mrj.xml"
# $P install.py --file $DPS/derverb_mrj.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.mrj.xml 2>>error.log
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

echo "==================================================="
#echo "installing Morfa-C questions for nouns"
#$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
#echo "installing Morfa-C questions for verbs"
#$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 2>>error.log
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
# $P install.py --messagefile $META/messages_vasta.mrj.xml 2>>error.log
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
# $P install.py -f $DPS/v_mrjdeu.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_mrjdeu.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_mrjdeu.xml --feedbackfile $META/feedback_numerals.xml
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
