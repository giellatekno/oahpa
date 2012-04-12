# list of command making jspwiki document

# c. only oahpa adjectives
cat $GTHOME/ped/sme/src/a_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | egrep -v '(Ord|none|NOT-KJ)' | tr "<" ">" | cut -d ">" -f3 | sort -u  > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-adjektiv med KJ-dialekt" > nudoc/gen/sme_adjOahpatabellKJ.jspwiki
echo "" >> nudoc/gen/sme_adjOahpatabellKJ.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_adjOahpatabellKJ.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom ||  Sg Acc ||  Sg Loc || Sg Ill || Comp Attr || Comp Sg Nom || Superl Sg Nom" >> nudoc/gen/sme_adjOahpatabellKJ.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr3

cat t3|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t3|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgacc3

cat t3|sed 's/$/+A+Sg+Loc/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgloc3

cat t3|sed 's/$/+A+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgill3

cat t3|sed 's/$/+A+Comp+Attr/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcompattr3

cat t3|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp3

cat t3|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl3

paste -d"|" t3 tattr3 tsgnom3  tsgacc3 tsgloc3 tsgill3 tcompattr3 tcomp3 tsuperl3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_adjOahpatabellKJ.jspwiki

rm -f tattr*  tsg*  tcomp*  tsuperl* 

