# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

echo "correct test" > vastaftestrapport.txt
perl qa-test_dialogue.pl oahpalog/vastafcorr2012.xml vastaf
cp final_data.txt  vastaffinal_data.txt
grep -v ";" vastaffinal_data.txt | grep "&" | grep -v dia >> vastaftestrapport.txt
echo " " >> vastaftestrapport.txt
echo "error test" >> vastaftestrapport.txt
perl qa-test_dialogue.pl oahpalog/vastaferror2012.xml vastaf
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> vastaftestrapport.txt
less vastaftestrapport.txt
