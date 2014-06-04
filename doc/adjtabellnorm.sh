# list of command making jspwiki document

# a. all adjectives
# cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1
cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|grep -v 'Err/Sub'|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1
# ikkje generering, for å få med feil. Vi fjernar sub med grep -v

# b. dict adjs
#cat $GTHOME/words/dicts/smanob/src/a_smanob.xml | grep '<l ' | tr '<' '>' | cut -d">" -f3 > t2
cat $GTHOME/words/dicts/smanob/src/a_smanob.xml | grep '<l ' | tr '<' '>' | cut -d">" -f3 | lookup -q $GTHOME/gt/sma/bin/sma-norm.fst | grep '+A+' | grep -v '+Ord' | cut -f1 | uniq > t2

# c. only oahpa adjectives
cat $GTHOME/ped/sma/src/a_smanob.xml | grep '<l ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

# a. all adjectives 
echo "!!!Tabell over alle adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjalletabellnorm.jspwiki
echo "" >> smadoc/gen/adjalletabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjalletabellnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc || Sg Ill" >> smadoc/gen/adjalletabellnorm.jspwiki

echo "!!!Reversert tabell over alle adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjalletabellrevnorm.jspwiki
echo "" >> smadoc/gen/adjalletabellrevnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjalletabellrevnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc || Sg Ill" >> smadoc/gen/adjalletabellrevnorm.jspwiki

# b. dict adj
echo "!!!Tabell over dict-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjdicttabellnorm.jspwiki
echo "" >> smadoc/gen/adjdicttabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjdicttabellnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc || Sg Ill" >> smadoc/gen/adjdicttabellnorm.jspwiki

echo "!!!Reversert tabell over dict-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjdicttabellrevnorm.jspwiki
echo "" >> smadoc/gen/adjdicttabellrevnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjdicttabellrevnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc || Sg Ill" >> smadoc/gen/adjdicttabellrevnorm.jspwiki

# c. oahpa adj
echo "!!!Tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabellnorm.jspwiki
echo "" >> smadoc/gen/adjoahpatabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjoahpatabellnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc || Sg Ill" >> smadoc/gen/adjoahpatabellnorm.jspwiki

echo "!!!Reversert tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabellrevnorm.jspwiki
echo "" >> smadoc/gen/adjoahpatabellrevnorm.jspwiki 
echo "Testdato: $DATO" >> smadoc/gen/adjoahpatabellrevnorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc || Sg Ill" >> smadoc/gen/adjoahpatabellrevnorm.jspwiki

# Making the 4 columns
cat t1|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr1
cat t2|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr2
cat t3|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr3

cat t1|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom1
cat t2|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom2
cat t3|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t1|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp1
cat t2|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp2
cat t3|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp3

cat t1|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl1
cat t2|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl2
cat t3|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl3

cat t1|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tAcc1
cat t2|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tAcc2
cat t3|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tAcc3

cat t1|sed 's/$/+A+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tIll1
cat t2|sed 's/$/+A+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tIll2
cat t3|sed 's/$/+A+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A+.*/-/'|tr '\t' ',' > tIll3


paste -d"|" t1 tattr1 tsgnom1 tcomp1 tsuperl1 tAcc1 tIll1 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms1
paste -d"|" t2 tattr2 tsgnom2 tcomp2 tsuperl2 tAcc2 tIll2 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms2
paste -d"|" t3 tattr3 tsgnom3 tcomp3 tsuperl3 tAcc3 tIll3 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms1 >> smadoc/gen/adjalletabellnorm.jspwiki
cat tadjforms2 >> smadoc/gen/adjdicttabellnorm.jspwiki
cat tadjforms3 >> smadoc/gen/adjoahpatabellnorm.jspwiki

rm -f tattr*  tsgnom*  tcomp*   tsuperl* tAcc* tIll*

cat t1 | perl -nle 'print scalar reverse $_' > t1rev
cat t2 | perl -nle 'print scalar reverse $_' > t2rev
cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t1rev tadjforms1 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjalletabellrevnorm.jspwiki
paste t2rev tadjforms2 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjdicttabellrevnorm.jspwiki
paste t3rev tadjforms3 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjoahpatabellrevnorm.jspwiki

rm -f t?rev* tadjforms* t1 t2 t3
