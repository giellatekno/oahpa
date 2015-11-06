#!/bin/sh

P="python2.7"
#PEDHOME="/Users/mslm/main/ped"
OAHPAHOME="/home/vro_oahpa"
LANGDIR="vro"
DATA=$OAHPAHOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/nobvro"
DPF="$DATA/finvro"
DPW="$DATA/engvro"
DPE="$DATA/estvro"
DPL="$DATA/swevro"
DPR="$DATA/deuvro"
DPD="$DATA/smevro"

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Installing the source files into Võro Oahpa database.
##

##
##  vro->X
##

echo "==================================================="
 echo "feeding db with $INC/n_tyypsonad.xml"
 $P install.py --file $INC/n_tyypsonad.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPS/oahpa_lexicon.xml"
 $P install.py --file $DPS/oahpa_lexicon.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt --append 2>error.log
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
# echo "feeding db with $DPS/prop_vronob.xml"
# $P install.py --file $DPS/prop_vronob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_vronob.xml"
# $P install.py --file $DPS/num_vronob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/A_vro2X.xml"
# $P install.py --file $DPS/A_vro2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/oahpa_lexicon.xml"
 $P install.py --file $DPS/oahpa_lexicon.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt --append 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/morfac_verbs.xml"
 $P install.py --file $DPS/morfac_verbs.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt --append 2>>\
    error.log
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
# echo "feeding db with $DPS/adv_vronob.xml"
# $P install.py --file $DPS/adv_vronob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_vronob.xml"
# $P install.py --file $DPS/multiword_vronob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## nobvro
# ##

echo "==================================================="
echo "feeding db with $DPN/N_nobvro.xml"
$P install.py --file $DPN/N_nobvro.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Num_nobvro.xml"
$P install.py --file $DPN/Num_nobvro.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/V_nobvro.xml"
 $P install.py --file $DPN/V_nobvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPN/A_nobvro.xml"
 $P install.py --file $DPN/A_nobvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/Adv_nobvro.xml"
 $P install.py --file $DPN/Adv_nobvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/Mwe_nobvro.xml"
 $P install.py --file $DPN/Mwe_nobvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_nobvro.xml"
# $P install.py --file $DPN/prop_nobvro.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## finvro
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finvro.xml"
$P install.py --file $DPF/N_finvro.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPF/Num_finvro.xml"
 $P install.py --file $DPF/Num_finvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finvro.xml"
$P install.py --file $DPF/V_finvro.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finvro.xml"
$P install.py --file $DPF/A_finvro.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


 echo "==================================================="
 echo "feeding db with $DPF/Adv_finvro.xml"
 $P install.py --file $DPF/Adv_finvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPF/Mwe_finvro.xml"
 $P install.py --file $DPF/Mwe_finvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_finvro.xml"
# $P install.py --file $DPF/prop_finvro.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engvro
##


echo "==================================================="
echo "feeding db with $DPW/N_engvro.xml"
$P install.py --file $DPW/N_engvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_engvro.xml"
$P install.py --file $DPW/V_engvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_engvro.xml"
$P install.py --file $DPW/A_engvro.xml
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPW/Adv_engvro.xml"
 $P install.py --file $DPW/Adv_engvro.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPW/Mwe_engvro.xml"
 $P install.py --file $DPW/Mwe_engvro.xml
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
 echo "feeding db with $DPW/Num_engvro.xml"
 $P install.py --file $DPW/Num_engvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
# echo "==================================================="
# echo "feeding db with $DPW/prop_swevro.xml"
# $P install.py --file $DPW/prop_swevro.xml
# echo " "
# echo "done"
# echo "==================================================="

##
## estvro
##

echo "==================================================="
echo "feeding db with $DPE/N_estvro.xml"
$P install.py --file $DPE/N_estvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/V_estvro.xml"
$P install.py --file $DPE/V_estvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/A_estvro.xml"
$P install.py --file $DPE/A_estvro.xml
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPE/Adv_estvro.xml"
 $P install.py --file $DPE/Adv_estvro.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPE/Mwe_estvro.xml"
 $P install.py --file $DPE/Mwe_estvro.xml
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
 echo "feeding db with $DPE/Num_estvro.xml"
 $P install.py --file $DPE/Num_estvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

##       
## swevro                                                                         
##                                                                                     

echo "==================================================="
echo "feeding db with $DPL/N_swevro.xml"
$P install.py --file $DPL/N_swevro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPL/V_swevro.xml"
$P install.py --file $DPL/V_swevro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPL/A_swevro.xml"
$P install.py --file $DPL/A_swevro.xml
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPL/Adv_estvro.xml"
 $P install.py --file $DPL/Adv_estvro.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPL/Mwe_estvro.xml"
 $P install.py --file $DPL/Mwe_estvro.xml
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
 echo "feeding db with $DPL/Num_estvro.xml"
 $P install.py --file $DPL/Num_estvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

##                                                                                
## deuvro                                                                        
##                                                                                                                                                           

echo "==================================================="
echo "feeding db with $DPR/N_deuvro.xml"
$P install.py --file $DPR/N_deuvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_deuvro.xml"
$P install.py --file $DPR/V_deuvro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_deuvro.xml"
$P install.py --file $DPR/A_deuvro.xml
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPR/Adv_deuvro.xml"
 $P install.py --file $DPR/Adv_deuvro.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPR/Mwe_deuvro.xml"
 $P install.py --file $DPR/Mwe_deuvro.xml
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
 echo "feeding db with $DPR/Num_deuvro.xml"
 $P install.py --file $DPR/Num_deuvro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

##                                                                                
## smevro                                                                         
##                                                                                
                                                                                   

echo "==================================================="
echo "feeding db with $DPD/N_smevro.xml"
$P install.py --file $DPD/N_smevro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPD/V_smevro.xml"
$P install.py --file $DPD/V_smevro.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPD/A_smevro.xml"
$P install.py --file $DPD/A_smevro.xml
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPD/Adv_smevro.xml"
 $P install.py --file $DPD/Adv_smevro.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPD/Mwe_smevro.xml"
 $P install.py --file $DPD/Mwe_smevro.xml
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
 echo "feeding db with $DPD/Num_smevro.xml"
 $P install.py --file $DPD/Num_smevro.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_vronob.xml"
# $P install.py --file $DPS/grammaticalwords_vronob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_vro.xml"
# $P install.py --file $DPS/pron_vro.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_vro.xml"
# $P install.py --file $DPS/derverb_vro.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.vro.xml 2>>error.log
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
# $P install.py --messagefile $META/messages_vasta.vro.xml 2>>error.log
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
 $P manage.py fixtagattributes

# echo "==================================================="
# echo "adding feedback to verbs"
# $P install.py -f $DPS/v_vronob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_vronob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_vronob.xml --feedbackfile $META/feedback_numerals.xml
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
