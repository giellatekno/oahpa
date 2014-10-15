for n in xml-out/*.xml
do
   mv $n $(echo $n | sed -e 's/nob_fin_eng/fin/')
done
