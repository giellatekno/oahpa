#!/bin/sh

# run the script:
# sh feed_db.sh smn (= LLL1)

P="python"
LLL1=$1
log_file="db_install_error.log"
DATA="${LLL1}_data"
META="$DATA/meta_data"
SRC="$DATA/src"
XXX="$DATA/*2${LLL1}"

rm -fv $log_file

'''
echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>$log_file
echo " "
echo "done"
echo "==================================================="
'''

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

	$P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>$log_file

    else
	echo "File does not exist $PARA_FILE"

	$P install.py --file $xfile 2>>$log_file

    fi
    echo " "
    echo "done"
done

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>$log_file
  echo " "
  echo "done"
  echo "   "
done

echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="



$P manage.py mergetags
$P manage.py fixtagattributes
