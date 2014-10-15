for n in xml-out/*.xml
do
   mv $n $(echo $n | sed -e 's/fin/eng/')
done
