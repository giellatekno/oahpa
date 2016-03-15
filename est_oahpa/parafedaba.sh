#!/bin/sh

P="python2.7"
#EST_HOME="/home/est_oahpa"
EST_HOME="/Users/mslm/main/ped"
LANGDIR="est"
DATA=$EST_HOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/deuest"
DPF="$DATA/finest"
DPE="$DATA/engest"
DPW="$DATA/sweest"
DPR="$DATA/rusest"
#WORDS=$GTHOME/words/dicts/smenob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Trying to set up Estonian Oahpa


##
##  est->X
##

#echo "==================================================="
 #echo "feeding db with $DPS/E_nagu_Eesti.xml"
 #$P install.py --file $DPS/E_nagu_Eesti.xml 
 #--tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
 #echo " "
 #echo "done"
 #echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPS/N_est.xml"
 $P install.py --file $DPS/N_est.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $META/names.xml"
# $P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Prop_est.xml (place names)"
$P install.py --file $DPS/Prop_est.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/Firstnames.xml (a number of common male and female first names that can be used in Morfa-C sentences)"
$P install.py --file $DPS/Firstnames.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"

echo "==================================================="
echo "feeding db with $DPS/Pron_est.xml"
$P install.py --file $DPS/Pron_est.xml --tagfile $META/tags.txt --paradigmfile $META/pron_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/num_estnob.xml"
# $P install.py --file $DPS/num_estnob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/A_est.xml"
$P install.py --file $DPS/A_est.xml --tagfile $META/tags.txt --paradigmfile $META/a_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_est.xml"
 $P install.py --file $DPS/V_est.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
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
 echo "feeding db with $DPS/Adv_est.xml"
 $P install.py --file $DPS/Adv_est.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
  echo "==================================================="
 echo "feeding db with $DPS/X_est.xml"
 $P install.py --file $DPS/X_est.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_estnob.xml"
# $P install.py --file $DPS/multiword_estnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## deuest
# ##

echo "==================================================="
echo "feeding db with $DPN/N_deuest.xml"
$P install.py --file $DPN/N_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_deuest.xml"
#$P install.py --file $DPN/num_deuest.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/V_deuest.xml"
 $P install.py --file $DPN/V_deuest.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPN/A_deuest.xml"
 $P install.py --file $DPN/A_deuest.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Adv_deuest.xml"
$P install.py --file $DPN/Adv_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/MWE_deuest.xml"
$P install.py --file $DPN/MWE_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Prop_deuest.xml"
$P install.py --file $DPN/Prop_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Pron_deuest.xml"
$P install.py --file $DPN/Pron_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/X_deuest.xml"
$P install.py --file $DPN/X_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Interj_deuest.xml"
$P install.py --file $DPN/Interj_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/Adp_deuest.xml"
$P install.py --file $DPN/Adp_deuest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# ##
# ## finest
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finest.xml"
$P install.py --file $DPF/N_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_finest.xml"
# $P install.py --file $DPF/num_finest.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finest.xml"
$P install.py --file $DPF/V_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finest.xml"
$P install.py --file $DPF/A_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPF/Adv_finest.xml"
$P install.py --file $DPF/Adv_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/MWE_finest.xml"
$P install.py --file $DPF/MWE_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Pron_finest.xml"
$P install.py --file $DPF/Pron_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/X_finest.xml"
$P install.py --file $DPF/X_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Interj_finest.xml"
$P install.py --file $DPF/Interj_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/Adp_finest.xml"
$P install.py --file $DPF/Adp_finest.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## engest
##


echo "==================================================="
echo "feeding db with $DPE/N_engest.xml"
$P install.py --file $DPE/N_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/V_engest.xml"
$P install.py --file $DPE/V_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/A_engest.xml"
$P install.py --file $DPE/A_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/Adv_engest.xml"
$P install.py --file $DPE/Adv_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/MWE_engest.xml"
$P install.py --file $DPE/MWE_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/Pron_engest.xml"
$P install.py --file $DPE/pron_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/X_engest.xml"
$P install.py --file $DPE/X_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/Interj_engest.xml"
$P install.py --file $DPE/Interj_engest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/Adp_engest.xml"
$P install.py --file $DPE/Adp_engest.xml
echo " "
echo "done"
echo "==================================================="

##       
## latest                                                                         
##                                                                                     

#echo "==================================================="
#echo "feeding db with $DPL/N_latest.xml"
#$P install.py --file $DPL/N_latest.xml
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPL/V_latest.xml"
#$P install.py --file $DPL/V_latest.xml
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPL/A_latest.xml"
#$P install.py --file $DPL/A_latest.xml
#echo " "
#echo "done"
#echo "==================================================="

##                                                                                
## rusest                                                                        
##                                                                                                                                                           

echo "==================================================="
echo "feeding db with $DPR/N_rusest.xml"
$P install.py --file $DPR/N_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_rusest.xml"
$P install.py --file $DPR/V_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_rusest.xml"
$P install.py --file $DPR/A_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Adv_rusest.xml"
$P install.py --file $DPR/Adv_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/MWE_rusest.xml"
$P install.py --file $DPR/MWE_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Pron_rusest.xml"
$P install.py --file $DPR/Pron_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/X_rusest.xml"
$P install.py --file $DPR/X_rusest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/Interj_rusest.xml"
$P install.py --file $DPR/Interj_rusest.xml
echo " "
echo "done"
echo "==================================================="

##                                                                                
## sweest                                                                         
##                                                                                
                                                                                   

echo "==================================================="
echo "feeding db with $DPW/N_sweest.xml"
$P install.py --file $DPW/N_sweest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_sweest.xml"
$P install.py --file $DPW/V_sweest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_sweest.xml"
$P install.py --file $DPW/A_sweest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Adv_sweest.xml"
$P install.py --file $DPW/Adv_sweest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Adp_sweest.xml"
$P install.py --file $DPW/Adp_sweest.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/Pron_sweest.xml"
$P install.py --file $DPW/Pron_sweest.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_estnob.xml"
# $P install.py --file $DPS/grammaticalwords_estnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_est.xml"
# $P install.py --file $DPS/pron_est.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_est.xml"
# $P install.py --file $DPS/derverb_est.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.est.xml 2>>error.log
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
$P install.py --messagefile $META/messages_vasta.est.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Swedish"
$P install.py --messagefile $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

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
# $P install.py -f $DPS/v_estnob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_estnob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_estnob.xml --feedbackfile $META/feedback_numerals.xml
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
