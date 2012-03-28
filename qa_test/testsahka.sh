# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

perl qa-test_dialogue.pl regressiontests/grocery_corr.xml sahka
cp final_data.txt  sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/shopadj_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/visit_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/firstmeeting_all_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt
grep -v ";" sahkafinal_data.txt | grep "&" | grep -v dia > sahkatestrapport.txt
perl qa-test_dialogue.pl regressiontests/grocerytest.xml sahka
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> sahkatestrapport.txt
less sahkatestrapport.txt

