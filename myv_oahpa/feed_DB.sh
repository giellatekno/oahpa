#!/bin/sh

file_dir=PATH/TO/DIR

for xfile in $(ls $file_dir/demo_*_sma.xml)
do
  #name=$(echo $xfile | cut -d"." -f1)
  echo "feeding db with: $xfile"
  python install.py -f $xfile
  echo " "
  echo "done"
  echo "   "
done


for xfile in $(ls $file_dir/eMerged/*)
do
  #name=$(echo $xfile | cut -d"." -f1)
  echo "feeding db with: $xfile"
  python install.py -f $xfile
  echo " "
  echo "done"
  echo "   "
done


