# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

echo "correct test" > sahkatestrapport.txt

# vuoje grammarchecking korpusiiguin main eai leat feaillat:
perl qa-test_dialogue.pl regressiontests/grocery_corr.xml sahka

# kopiere output sierra fiilii:
cp final_data.txt  sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/shopadj_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/visit_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt
perl qa-test_dialogue.pl regressiontests/firstmeeting_all_corr.xml sahka
cat final_data.txt >> sahkafinal_data.txt

# kopiere testrapportii buot sániid+errortag (earret dia-tagg mii lea juoga eará):
grep -v ";" sahkafinal_data.txt | grep "&" | grep -v dia >> sahkatestrapport.txt
echo " " >> sahkatestrapport.txt
echo "error test" >> sahkatestrapport.txt

# vuoje grammarchecking korpusiin mas leat feaillat:
perl qa-test_dialogue.pl errortests/grocerytest.xml sahka

# bija ¥ linnjáide main ii leat sisdoallu, ja juoge nu ahte olles cealkka lea ovtta linnjás. Kopiere testrapportii cealkagiid main ii leat errortag, muhto bija cealkagiid vuos ruovttoluotta álgoformáhtii:
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> sahkatestrapport.txt
perl qa-test_dialogue.pl errortests/sahkatest.xml sahka
grep -v "^;" final_data.txt | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" >> sahkatestrapport.txt

less sahkatestrapport.txt

#OUTPUT - example (čájeha ahte correct test manai bures, muhto ovtta error-cealkagis prográmma ii gávdnan feailla:
#
#correct test
# 
#error test
#
#"<Mii>"
#        "mii" Pron Interr Sg Nom
#"<heivešii>"
#        "heivet" V IV Cond Prs Sg3
#"<dutnje>"
#        "don" Pron Pers Sg2 Ill
#"<^sahka>"
#        "^sahka" QDL hálbiduvvon_galvvut
#"<Munnje>"
#        "mun" Pron Pers Sg1 Ill
#"<heivešii>"
#        "heivet" V IV Cond Prs Sg3
#"<sihke>"
#        "sihke" CC
#"<gintalat>"
#        "ginttal" N Pl Nom &dia-target
#"<gohput>"
#        "gohppu" N Pl Nom &dia-target
#"<rátnu>"
#        "rátnu" N Sg Nom &dia-target
#"<speadjala>"
#        "speajal" N Sg Acc
#        "speajal" N Sg Gen
#"<ruskalihtti>"
#        "ruskalihtti" N Sg Nom &dia-target
#"<ja>"
#        "ja" CC
#"<čáppa>"
#        "čáppat" A Attr
#"<govva>"
#        "govva" N Sg Nom &dia-target
#"<.>"
#        "." CLB



