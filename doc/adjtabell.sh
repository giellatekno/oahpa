# list of command making jspwiki document

# a. all adjectives
#cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. dict adjs
cat ../../words/dicts/smanob/src/a_smanob.xml|grep '<l '|tr '<' '>'|cut -d">" -f3 > t1
doc$

# b. only oahpa adjectives
# blabla

# Printing headers:

echo "!!!Tabell over adjektiv" > smadoc/adjdicttabell.jspwiki
echo "" >> smadoc/adjdicttabell.jspwiki
echo " ||  lemma  ||  Attr  ||  Pred  ||  Comp  ||  Superl " >> smadoc/adjdicttabell.jspwiki

echo "!!!Reversert tabell over adjektiv" > smadoc/adjdicttabellrev.jspwiki
echo "" >> smadoc/adjdicttabellrev.jspwiki
echo " ||  lemma  ||  Attr  ||  Pred  ||  Comp  ||  Superl " >> smadoc/adjdicttabellrev.jspwiki

# Making the 4 columns
cat t1|sed 's/$/+A+Attr/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr

cat t1|sed 's/$/+A+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tpred

cat t1|sed 's/$/+A+Comp+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp

cat t1|sed 's/$/+A+Superl+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl

paste -d"|" t1 tattr tpred tcomp tsuperl | sed 's/|/ | /g;' | sed 's/^/|/'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms

cat tadjforms >> smadoc/adjdicttabell.jspwiki

#rm tattr tpred tcomp tsuperl 

cat t1 | perl -nle 'print scalar reverse $_' > t1rev

paste t1rev tadjforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/adjdicttabellrev.jspwiki

#rm t1rev tadjforms
