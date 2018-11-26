P="python"
DATA=../smn
SMN="$DATA/src"
FIN="$DATA/finsmn"

for xfile in $(ls $SMN/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile  
  echo " "
  echo "done"
  echo "   "
done

for xfile in $(ls $FIN/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile
  echo " "
  echo "done"
  echo "   "
done

$P install.py --sem $DATA/meta-data/semantical_sets.xml

