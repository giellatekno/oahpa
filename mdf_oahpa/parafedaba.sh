#!/bin/sh

P="python2.7"
GTHOME="/home/heli/main/ped"
LANGDIR="liv"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/nobliv"
DPF="$DATA/finliv"
DPW="$DATA/engliv"
DPE="$DATA/estliv"
DPL="$DATA/latliv"
DPR="$DATA/rusliv"
DPD="$DATA/smeliv"
#WORDS=$GTHOME/words/dicts/smenob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Trying to set up Livonian


##
##  liv->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_liv2X.xml"
 $P install.py --file $DPS/N_liv2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
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
# echo "feeding db with $DPS/prop_livnob.xml"
# $P install.py --file $DPS/prop_livnob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_livnob.xml"
# $P install.py --file $DPS/num_livnob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/A_liv2X.xml"
 $P install.py --file $DPS/A_liv2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_liv2X.xml"
 $P install.py --file $DPS/V_liv2X.xml --tagfile $META/tags.txt --paradigmfile $META/V_paradigms.txt 2>>error.log
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
# echo "feeding db with $DPS/adv_livnob.xml"
# $P install.py --file $DPS/adv_livnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_livnob.xml"
# $P install.py --file $DPS/multiword_livnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## nobliv
# ##

echo "==================================================="
echo "feeding db with $DPN/N_nobliv.xml"
$P install.py --file $DPN/N_nobliv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_nobliv.xml"
#$P install.py --file $DPN/num_nobliv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/V_nobliv.xml"
 $P install.py --file $DPN/V_nobliv.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPN/A_nobliv.xml"
 $P install.py --file $DPN/A_nobliv.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/adv_nobliv.xml"
# $P install.py --file $DPN/adv_nobliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/mwe_nobliv.xml"
# $P install.py --file $DPN/mwe_nobliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_nobliv.xml"
# $P install.py --file $DPN/prop_nobliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## finliv
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finliv.xml"
$P install.py --file $DPF/N_finliv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_finliv.xml"
# $P install.py --file $DPF/num_finliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finliv.xml"
$P install.py --file $DPF/V_finliv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finliv.xml"
$P install.py --file $DPF/A_finliv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPF/adv_finliv.xml"
# $P install.py --file $DPF/adv_finliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/mwe_finliv.xml"
# $P install.py --file $DPF/mwe_finliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_finliv.xml"
# $P install.py --file $DPF/prop_finliv.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engliv
##


echo "==================================================="
echo "feeding db with $DPW/N_engliv.xml"
$P install.py --file $DPW/N_engliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_engliv.xml"
$P install.py --file $DPW/V_engliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_engliv.xml"
$P install.py --file $DPW/A_engliv.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_sweliv.xml"
# $P install.py --file $DPW/adv_sweliv.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_sweliv.xml"
# $P install.py --file $DPW/multiword_sweliv.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_sweliv.xml"
# $P install.py --file $DPW/prop_sweliv.xml
# echo " "
# echo "done"
# echo "==================================================="

##
## estliv
##

echo "==================================================="
echo "feeding db with $DPE/N_estliv.xml"
$P install.py --file $DPE/N_estliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/V_estliv.xml"
$P install.py --file $DPE/V_estliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/A_estliv.xml"
$P install.py --file $DPE/A_estliv.xml
echo " "
echo "done"
echo "==================================================="

##       
## latliv                                                                         
##                                                                                     

echo "==================================================="
echo "feeding db with $DPL/N_latliv.xml"
$P install.py --file $DPL/N_latliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPL/V_latliv.xml"
$P install.py --file $DPL/V_latliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPL/A_latliv.xml"
$P install.py --file $DPL/A_latliv.xml
echo " "
echo "done"
echo "==================================================="

##                                                                                
## rusliv                                                                        
##                                                                                                                                                           

echo "==================================================="
echo "feeding db with $DPR/N_rusliv.xml"
$P install.py --file $DPR/N_rusliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_rusliv.xml"
$P install.py --file $DPR/V_rusliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_rusliv.xml"
$P install.py --file $DPR/A_rusliv.xml
echo " "
echo "done"
echo "==================================================="

##                                                                                
## smeliv                                                                         
##                                                                                
                                                                                   

echo "==================================================="
echo "feeding db with $DPD/N_smeliv.xml"
$P install.py --file $DPD/N_smeliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPD/V_smeliv.xml"
$P install.py --file $DPD/V_smeliv.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPD/A_smeliv.xml"
$P install.py --file $DPD/A_smeliv.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_livnob.xml"
# $P install.py --file $DPS/grammaticalwords_livnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_liv.xml"
# $P install.py --file $DPS/pron_liv.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_liv.xml"
# $P install.py --file $DPS/derverb_liv.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.liv.xml 2>>error.log
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
# $P install.py --messagefile $META/messages_vasta.liv.xml 2>>error.log
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
# $P install.py -f $DPS/v_livnob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_livnob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_livnob.xml --feedbackfile $META/feedback_numerals.xml
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
