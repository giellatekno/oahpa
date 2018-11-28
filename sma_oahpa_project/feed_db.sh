#!/bin/sh

# run the script:
# sh feed_db.sh sma (= LLL1)

P="python"
LLL1=$1
log_file="db_install_error.log"
META="${LLL1}_data/meta_data"
SRC="${LLL1}_data/src"
NOB="${LLL1}_data/nob"
FIN="${LLL1}_data/fin"
SWE="${LLL1}_data/swe"

rm -fv $log_file

##
##  sma->X
##

for xfile in $(ls $SRC/*.xml)
do
    fl=$(basename $xfile)
    POS=${fl%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"
    FEEDBACK_FILE="${META}/${POS}_feedback.xml"

    if [ -e "$PARA_FILE" ]; then
	    echo "File exists $PARA_FILE"
	    $P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>$log_file
    else
	    echo "File does not exist $PARA_FILE"
      $P install.py --file $xfile 2>>$log_file
    fi

    if [ -e "$FEEDBACK_FILE" ]; then
      $P install.py -f $xfile --feedbackfile $FEEDBACK_FILE 2>>$log_file
    fi

    echo " "
    echo "done"
    echo " "
done

##
## nobsma
##

for xfile in $(ls $NOB/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>$log_file

  echo " "
  echo "done"
  echo " "
done

##
## finsma
##

for xfile in $(ls $FIN/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>$log_file

  echo " "
  echo "done"
  echo "   "
done

##
## swesma
##

for xfile in $(ls $SWE/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>$log_file

  echo " "
  echo "done"
  echo "   "
done

echo "feeding db with $META/semantical_sets.xml"
$P install.py --sem $META/semantical_sets.xml 2>>$log_file
echo " "
echo "done"
echo "   "


for xfile in $(ls $META/messages*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py --messagefile $xfile 2>>$log_file

  echo " "
  echo "done"
  echo "   "
done


#  ... and then repeat for adjectives.

# Morfa-C

echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>$log_file
echo " "
echo "done"
echo " "

# LLL1="sma"
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smanob.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt 2>>$log_file
echo " "
echo "done"
echo " "

for xfile in $(ls $META/*_questions.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -g $META/grammar_defaults.xml -q $xfile 2>>$log_file

  echo " "
  echo "done"
  echo "   "
done


'''
#The file verb_problems.xml dows not exist!
echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_problems.xml
echo " "
echo "done"
echo "==================================================="
'''

echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>$log_file
echo " "
echo "done"
echo " "

echo "Optimizing tables"
cat optimize_analyze_tables.sql | $P manage.py dbshell
echo " "
echo "done"
echo " "
