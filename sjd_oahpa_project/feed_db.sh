#!/bin/sh

P="python"
LLL1="sjd"
DATA="${LLL1}_data"
META="$DATA/meta_data"
SRC="$DATA/src"
XXX="$DATA/*2${LLL1}"

rm -fv error.log

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NB:
#sms_oahpa>export DJANGO_SETTINGS_MODULE=sms_oahpa.settings

for xfile in $(ls $SRC/*.xml)
do
    fl=$(basename $xfile)
    POS=${fl%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"


    echo "feeding db with: $xfile"


    if [ -e "$PARA_FILE" ]; then
	echo "File exists $PARA_FILE"

	$P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>error.log

    else
	echo "File does not exist $PARA_FILE"

	$P install.py --file $xfile 2>>error.log

    fi
    echo " "
    echo "done"
done

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>error.log
  echo " "
  echo "done"
  echo "   "
done

echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="



#$P manage.py mergetags
#$P manage.py fixtagattributes



echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "stopped at: "
date '+%T'
