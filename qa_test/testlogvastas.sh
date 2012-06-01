# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil
echo "correct test" > vastastestrapport.txt
perl qa-test_vastas.pl oahpalog/vastascorr2012log.xml
cp final_data.txt  testdata/corrVS_data.txt
grep -v ";" testdata/corrVS_data.txt | grep "&" >> vastastestrapport.txt
echo " " >> vastastestrapport.txt
echo "error test" >> vastastestrapport.txt
perl qa-test_vastas.pl oahpalog/vastaserror2012log.xml
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> vastastestrapport.txt
cp final_data.txt  testdata/errVS_data.txt
less vastastestrapport.txt
