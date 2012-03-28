# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil
echo "correct test" > vastatestrapport.txt
perl qa-test_vastas.pl regressiontests/vastas_corr.xml
grep -v ";" final_data.txt | grep "&" >> vastatestrapport.txt
echo " " >> vastatestrapport.txt
echo "error test" >> vastatestrapport.txt
perl qa-test_vastas.pl errortests/vastastest.xml
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> vastatestrapport.txt
less vastatestrapport.txt
