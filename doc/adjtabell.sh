# list of command making jspwiki document

# a. all adjectives
cat $GTHOME/gt/sma/src/adj-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. only oahpa adjectives
# blabla

# Making the 4 columns
cat t1|sed 's/$/+A+Attr/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr

cat t1|sed 's/$/+A+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tpred

cat t1|sed 's/$/+A+Comp+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp

cat t1|sed 's/$/+A+Superl+Sg+Nom/;'| lookup $GTHOME/gt/sma/bin/isma.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl

paste -d"|" t1 tattr tpred tcomp tsuperl | sed 's/|/ | /g;' | sed 's/^/|/'| sed 's/,/, /g;'> ttabell

rm tattr tpred tcomp tsuperl

cat t1 | perl -nle 'print scalar reverse $_' > t1rev

paste t1rev ttabell | sort | cut -f2 > ttabellrev

rm t1rev
