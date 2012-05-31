# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

echo "correct test" > sahkatestrapport.txt
perl qa-test_dialogue.pl oahpalog/sahkacorr2012log.xml sahka
cp final_data.txt  sahkafinal_data.txt
grep -v ";" sahkafinal_data.txt | grep "&" | grep -v dia >> sahkatestrapport.txt
echo " " >> sahkatestrapport.txt
echo "error test" >> sahkatestrapport.txt
perl qa-test_dialogue.pl oahpalog/sahkaerror2012log.xml sahka
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | grep QDL | tr "€" "\n" >> sahkatestrapport.txt
less sahkatestrapport.txt

