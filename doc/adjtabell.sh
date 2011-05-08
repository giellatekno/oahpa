# list of command making jspwiki document

# a. all adjectives
cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. dict adjs
 cat ../../words/dicts/smanob/src/a_smanob.xml|grep '<l '|tr '<' '>'|cut -d">" -f3 > t2


# c. only oahpa adjectives
 cat ../../words/dicts/smanob/src/a_smanob.xml |tr '\n' '™' | sed 's/<l /£/g;'| tr '£' '\n'|grep '"oahpa"'|tr '™' '\n' |grep '^pos'|tr '<' '>' | cut -d">" -f2|sort|uniq > t3


# Printing headers:

echo "!!!Tabell over alle adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjalletabell.jspwiki
echo "" >> smadoc/gen/adjalletabell.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjalletabell.jspwiki
echo "!!!Reversert tabell over alle adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjalletabellrev.jspwiki
echo "" >> smadoc/gen/adjalletabellrev.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjalletabellrev.jspwiki

echo "!!!Tabell over dict-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjdicttabell.jspwiki
echo "" >> smadoc/gen/adjdicttabell.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjdicttabell.jspwiki
echo "!!!Reversert tabell over dict-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjdicttabellrev.jspwiki
echo "" >> smadoc/gen/adjdicttabellrev.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjdicttabellrev.jspwiki

echo "!!!Tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabell.jspwiki
echo "" >> smadoc/gen/adjoahpatabell.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjoahpatabell.jspwiki

echo "!!!Reversert tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabellrev.jspwiki
echo "" >> smadoc/gen/adjoahpatabellrev.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom || Sg Acc " >> smadoc/gen/adjoahpatabellrev.jspwiki

# Making the 4 columns
cat t1|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr1
cat t2|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr2
cat t3|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr3

cat t1|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom1
cat t2|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom2
cat t3|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t1|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp1
cat t2|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp2
cat t3|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp3

cat t1|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl1
cat t2|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl2
cat t3|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl3

cat t1|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tAcc1
cat t2|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tAcc2
cat t3|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tAcc3

paste -d"|" t1 tattr1 tsgnom1 tcomp1 tsuperl1 tAcc1 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms1
paste -d"|" t2 tattr2 tsgnom2 tcomp2 tsuperl2 tAcc2 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms2
paste -d"|" t3 tattr3 tsgnom3 tcomp3 tsuperl3 tAcc3 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms1 >> smadoc/gen/adjalletabell.jspwiki
cat tadjforms2 >> smadoc/gen/adjdicttabell.jspwiki
cat tadjforms3 >> smadoc/gen/adjoahpatabell.jspwiki

rm -f tattr*  tsgnom*  tcomp*   tsuperl* tAcc*

cat t1 | perl -nle 'print scalar reverse $_' > t1rev
cat t2 | perl -nle 'print scalar reverse $_' > t2rev
cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t1rev tadjforms1 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjalletabellrev.jspwiki
paste t2rev tadjforms2 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjdicttabellrev.jspwiki
paste t3rev tadjforms3 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjoahpatabellrev.jspwiki

rm -f t?rev* tadjforms*
