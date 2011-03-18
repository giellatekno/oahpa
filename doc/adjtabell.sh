# list of command making jspwiki document

# a. all adjectives
cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. dict adjs
# cat ../../words/dicts/smanob/src/a_smanob.xml|grep '<l '|tr '<' '>'|cut -d">" -f3 > t1


# c. only oahpa adjectives
# cat ../../words/dicts/smanob/src/a_smanob.xml |tr '\n' '™' | sed 's/<l /£/g;'| tr '£' '\n'|grep '"oahpa"'|tr '™' '\n' |grep '^pos'|tr '<' '>' | cut -d">" -f2|sort|uniq > t1


# Printing headers:

echo "!!!Tabell over adjektiv - OBS! arbeidsliste for debugging" > smadoc/adjalletabell.jspwiki
echo "" >> smadoc/adjalletabell.jspwiki
echo " ||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom " >> smadoc/adjalletabell.jspwiki

echo "!!!Reversert tabell over adjektiv - OBS! arbeidsliste for debugging" > smadoc/adjalletabellrev.jspwiki
echo "" >> smadoc/adjalletabellrev.jspwiki
echo " ||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom " >> smadoc/adjalletabellrev.jspwiki

# Making the 4 columns
cat t1|sed 's/$/+A+Attr/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr

cat t1|sed 's/$/+A+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom

cat t1|sed 's/$/+A+Comp+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp

cat t1|sed 's/$/+A+Superl+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl

paste -d"|" t1 tattr tsgnom tcomp tsuperl | sed 's/|/ | /g;' | sed 's/^/|/'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms

cat tadjforms >> smadoc/adjalletabell.jspwiki

rm tattr  tsgnom  tcomp   tsuperl 

cat t1 | perl -nle 'print scalar reverse $_' > t1rev

paste t1rev tadjforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/adjalletabellrev.jspwiki

rm t1rev tadjforms
