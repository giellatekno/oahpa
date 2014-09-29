#!/bin/sh

P="python2.7"
GTHOME="/Users/mslm/main/ped"
LANGDIR="udm"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
INC="$DATA/inc"
META="$DATA/meta"
DPN="$DATA/nobudm"
DPF="$DATA/finudm"
DPW="$DATA/engudm"
DPE="$DATA/estudm"
DPL="$DATA/latudm"
DPR="$DATA/rusudm"
DPD="$DATA/smeudm"
#WORDS=$GTHOME/words/dicts/smenob/src

echo "==================================================="
echo "installing tags and paradigms for Morfa"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>error.log
echo " "
echo "done"
echo "==================================================="

##
## Trying to set up Udmurt


##
##  udm->X
##

 echo "==================================================="
 echo "feeding db with $DPS/N_udm2X.xml"
 $P install.py --file $DPS/n_udm2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
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
# echo "feeding db with $DPS/prop_udmnob.xml"
# $P install.py --file $DPS/prop_udmnob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/num_udmnob.xml"
# $P install.py --file $DPS/num_udmnob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/A_udm2X.xml"
 $P install.py --file $DPS/a_udm2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPS/V_udm2X.xml"
 $P install.py --file $DPS/v_udm2X.xml --tagfile $META/tags.txt --paradigmfile $META/V_paradigms.txt 2>>error.log
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
# echo "feeding db with $DPS/adv_udmnob.xml"
# $P install.py --file $DPS/adv_udmnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/multiword_udmnob.xml"
# $P install.py --file $DPS/multiword_udmnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## nobudm
# ##

echo "==================================================="
echo "feeding db with $DPN/N_nobudm.xml"
$P install.py --file $DPN/n_nobudm.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_nobudm.xml"
#$P install.py --file $DPN/num_nobudm.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPN/V_nobudm.xml"
 $P install.py --file $DPN/V_nobudm.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="
 
 echo "==================================================="
 echo "feeding db with $DPN/A_nobudm.xml"
 $P install.py --file $DPN/A_nobudm.xml 2>>error.log
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/adv_nobudm.xml"
# $P install.py --file $DPN/adv_nobudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/mwe_nobudm.xml"
# $P install.py --file $DPN/mwe_nobudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPN/prop_nobudm.xml"
# $P install.py --file $DPN/prop_nobudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# ##
# ## finudm
# ##


echo "==================================================="
echo "feeding db with $DPF/N_finudm.xml"
$P install.py --file $DPF/N_finudm.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/num_finudm.xml"
# $P install.py --file $DPF/num_finudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finudm.xml"
$P install.py --file $DPF/V_finudm.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/A_finudm.xml"
$P install.py --file $DPF/A_finudm.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPF/adv_finudm.xml"
# $P install.py --file $DPF/adv_finudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/mwe_finudm.xml"
# $P install.py --file $DPF/mwe_finudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPF/prop_finudm.xml"
# $P install.py --file $DPF/prop_finudm.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

##
## engudm
##


echo "==================================================="
echo "feeding db with $DPW/N_engudm.xml"
$P install.py --file $DPW/N_engudm.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/V_engudm.xml"
$P install.py --file $DPW/V_engudm.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/A_engudm.xml"
$P install.py --file $DPW/A_engudm.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_sweudm.xml"
# $P install.py --file $DPW/adv_sweudm.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_sweudm.xml"
# $P install.py --file $DPW/multiword_sweudm.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_sweudm.xml"
# $P install.py --file $DPW/prop_sweudm.xml
# echo " "
# echo "done"
# echo "==================================================="

##
## estudm
##

#echo "==================================================="
#echo "feeding db with $DPE/N_estudm.xml"
#$P install.py --file $DPE/N_estudm.xml
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPE/V_estudm.xml"
#$P install.py --file $DPE/V_estudm.xml
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPE/A_estudm.xml"
#$P install.py --file $DPE/A_estudm.xml
#echo " "
#echo "done"
#echo "==================================================="


##                                                                                
## rusudm                                                                        
##                                                                                                                                                           

echo "==================================================="
echo "feeding db with $DPR/N_rusudm.xml"
$P install.py --file $DPR/N_rusudm.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/V_rusudm.xml"
$P install.py --file $DPR/V_rusudm.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPR/A_rusudm.xml"
$P install.py --file $DPR/A_rusudm.xml
echo " "
echo "done"
echo "==================================================="


# echo "==================================================="
# echo "feeding db with $DPS/grammaticalwords_udmnob.xml"
# $P install.py --file $DPS/grammaticalwords_udmnob.xml 2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/pron_udm.xml"
# $P install.py --file $DPS/pron_udm.xml --tagfile $META/tags.txt  2>>error.log
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPS/derverb_udm.xml"
# $P install.py --file $DPS/derverb_udm.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
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
# $P install.py --messagefile $META/messages.udm.xml 2>>error.log
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
# $P install.py --messagefile $META/messages_vasta.udm.xml 2>>error.log
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
# $P install.py -f $DPS/v_udmnob.xml --feedbackfile $META/feedback_verbs.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to adjectives"
# $P install.py -f $DPS/a_udmnob.xml --feedbackfile $META/feedback_adjectives.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "adding feedback to numerals"
# $P install.py -f $DPS/num_udmnob.xml --feedbackfile $META/feedback_numerals.xml
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
