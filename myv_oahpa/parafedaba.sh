#!/bin/sh

P="python2.7"
DATA="/home/heli/main/ped/myv"
DPS="$DATA/src"
META="$DATA/meta"
DPN="$DATA/nobmyv"
DPF="$DATA/finmyv"
DPW="$DATA/engmyv"
DPR="$DATA/rusmyv"
DPD="$DATA/smemyv"
#WORDS=$GTHOME/words/dicts/smenob/src

#echo "==================================================="
#echo "fixing collation to utf-8"
#cat fix_collation.sql | $P manage.py dbshell
#echo "==================================================="
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "installing grammar links for norwegian"
#$P install.py -i $META/grammatikklinker.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

##
##  myv->X
##

echo "==================================================="
echo "feeding db with $DPS/N_myv2X.xml"
$P install.py --file $DPS/N_myv2X.xml --tagfile $META/tags.txt --paradigmfile $META/N_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $META/names.xml"
#$P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/NProp_myv2X.xml"
$P install.py --file $DPS/NProp_myv2X.xml --tagfile $META/tags.txt --paradigmfile $META/NProp_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
#echo "==================================================="
#echo "feeding db with $DPS/n_px.xml"
#$P install.py --file $META/n_px.xml --tagfile $META/tags.txt --paradigmfile $META/n_px_paradigms.txt --append 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/num_smenob.xml"
#$P install.py --file $DPS/num_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/A_myv2X.xml"
$P install.py --file $DPS/A_myv2X.xml --tagfile $META/tags.txt --paradigmfile $META/A_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/V_myv2X.xml"
$P install.py --file $DPS/V_myv2X.xml --tagfile $META/tags.txt --paradigmfile $META/V_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
#echo "==================================================="
#echo "feeding db with $DPS/v_pass.xml"
#$P install.py --file $META/v_pass.xml --tagfile $META/tags.txt --paradigmfile $META/v_pass_paradigms.txt --append 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


#echo "==================================================="
#echo "feeding db with $DPS/adv_myvnob.xml"
#$P install.py --file $DPS/adv_myvnob.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/multiword_myvnob.xml"
#$P install.py --file $DPS/multiword_myvnob.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

##
## nobmyv
##

echo "==================================================="
echo "feeding db with $DPN/A_nobmyv.xml"
$P install.py --file $DPN/A_nobmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/N_nobmyv.xml"
$P install.py --file $DPN/N_nobmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/num_nobmyv.xml"
#$P install.py --file $DPN/num_nobmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/V_nobmyv.xml"
$P install.py --file $DPN/V_nobmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/adv_nobmyv.xml"
#$P install.py --file $DPN/adv_nobmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPN/mwe_nobmyv.xml"
#$P install.py --file $DPN/mwe_nobmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/NProp_nobmyv.xml"
$P install.py --file $DPN/NProp_nobmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## finmyv
##

echo "==================================================="
echo "feeding db with $DPF/A_finmyv.xml"
$P install.py --file $DPF/A_finmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/N_finmyv.xml"
$P install.py --file $DPF/N_finmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPF/num_finmyv.xml"
#$P install.py --file $DPF/num_finmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/V_finmyv.xml"
$P install.py --file $DPF/V_finmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPF/adv_finmyv.xml"
#$P install.py --file $DPF/adv_finmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPF/mwe_finmyv.xml"
#$P install.py --file $DPF/mwe_finmyv.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/NProp_finmyv.xml"
$P install.py --file $DPF/NProp_finmyv.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## engmyv 
##

 echo "==================================================="
 echo "feeding db with $DPW/A_engmyv.xml"
 $P install.py --file $DPW/A_engmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPW/N_engmyv.xml"
 $P install.py --file $DPW/N_engmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPW/V_engmyv.xml"
 $P install.py --file $DPW/V_engmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_engmyv.xml"
# $P install.py --file $DPW/adv_engmyv.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_engmyv.xml"
# $P install.py --file $DPW/multiword_engmyv.xml
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPW/NProp_engmyv.xml"
 $P install.py --file $DPW/NProp_engmyv.xml
 echo " "
 echo "done"
 echo "==================================================="
 
 ##
## rusmyv 
##

 echo "==================================================="
 echo "feeding db with $DPR/A_rusmyv.xml"
 $P install.py --file $DPR/A_rusmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPR/N_rusmyv.xml"
 $P install.py --file $DPR/N_rusmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPR/V_rusmyv.xml"
 $P install.py --file $DPR/V_rusmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPR/adv_rusmyv.xml"
# $P install.py --file $DPR/adv_rusmyv.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPR/multiword_rusmyv.xml"
# $P install.py --file $DPR/multiword_rusmyv.xml
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPR/NProp_rusmyv.xml"
 $P install.py --file $DPR/NProp_rusmyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 ##
## smemyv 
##

 echo "==================================================="
 echo "feeding db with $DPD/A_smemyv.xml"
 $P install.py --file $DPD/A_smemyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPD/N_smemyv.xml"
 $P install.py --file $DPD/N_smemyv.xml
 echo " "
 echo "done"
 echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPD/V_smemyv.xml"
 $P install.py --file $DPD/V_smemyv.xml
 echo " "
 echo "done"
 echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPR/adv_smemyv.xml"
# $P install.py --file $DPR/adv_smemyv.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPR/multiword_smemyv.xml"
# $P install.py --file $DPR/multiword_smemyv.xml
# echo " "
# echo "done"
# echo "==================================================="

 echo "==================================================="
 echo "feeding db with $DPD/NProp_smemyv.xml"
 $P install.py --file $DPD/NProp_smemyv.xml
 echo " "
 echo "done"
 echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/grammaticalwords_smenob.xml"
#$P install.py --file $DPS/grammaticalwords_smenob.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/pron_sme.xml"
#$P install.py --file $DPS/pron_sme.xml --tagfile $META/tags.txt  2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with $DPS/derverb_sme.xml"
#$P install.py --file $DPS/derverb_sme.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
#echo " "
#echo "done"
#echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.sme.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.eng.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.swe.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.fin.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# Morfa-C 


#echo "==================================================="
#echo "installing Morfa-C word fillings"
#$P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#$P manage.py mergetags
#$P manage.py fixtagattributes

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

#echo "==================================================="
#echo "installing Morfa-C questions for pronoun"
#$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "installing Morfa-C questions for numerals"
#$P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "installing Morfa-C questions for derivation"
#$P install.py -g $META/grammar_defaults.xml -q $META/derivation_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "installing Morfa-C questions for noun possessive suffixes"
#$P install.py -g $META/grammar_defaults.xml -q $META/px_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

###################
# Vasta and VastaS
###################
#echo "==================================================="
#echo "installing Vasta questions"
#$P install.py -g $META/grammar_defaults.xml -q $META/questions_vasta.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "installing Vasta-S questions"
#$P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


#echo "==================================================="
#echo "Installing feedback messages for vasta"
#$P install.py --messagefile $META/messages_vasta.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "Installing feedback messages for vasta - in English"
#$P install.py --messagefile $META/messages_vasta.eng.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "Installing feedback messages for vasta - in Finnish"
#$P install.py --messagefile $META/messages_vasta.fin.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

# echo "==================================================="
#echo "Installing feedback messages for vasta - in North Sámi"
#$P install.py --messagefile $META/messages_vasta.sme.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "Installing feedback messages for vasta - in Swedish"
#$P install.py --messagefile $META/messages_vasta.swe.xml
#echo " "
#echo "done"
#echo "==================================================="

#echo "==================================================="
#echo "Checking for differences in feedback files"
#$P check_feedback.py $META/messages_vasta.xml \
 #   $META/messages_vasta.fin.xml \
  #  $META/messages_vasta.sme.xml \
   # $META/messages_vasta.eng.xml \
    #$META/messages_vasta.swe.xml
#echo " "
#echo "done"
#echo "==================================================="

#####
# Sahka
#####
#echo "==================================================="
#echo "Installing dialogues for Sahka - firstmeeting"
#$P install.py -k $META/dialogue_firstmeeting.xml 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="


# TODO: 
# fixtagattributes
# mergetags

#$P manage.py fixattributes
#$P manage.py mergetags
#$P manage.py fixattributes

#echo "==================================================="
#echo "adding feedback to nouns"
#$P install.py -f $DPS/n_smenob.xml --feedbackfile $META/feedback_nouns.xml
#echo " "
#echo "done"
#echo "==================================================="



#echo "==================================================="
#echo "Optimizing tables"
#cat optimize_analyze_tables.sql | $P manage.py dbshell
#echo " "
#echo "done"
#echo "==================================================="

echo "stopped at: "
date '+%T'

