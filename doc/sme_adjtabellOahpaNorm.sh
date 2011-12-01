# list of command making jspwiki document

# c. only oahpa adjectives
cat $GTHOME/ped/sme/univ_oahpa_data/data_sme/sme/a_smenob.xml | grep '<l ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over VD-adjektiv med Norm" > nudoc/gen/sme_adjOahpatabellNorm.jspwiki
echo "" >> nudoc/gen/sme_adjOahpatabellNorm.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_adjOahpatabellNorm.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Attr || Comp Sg Nom || Superl Sg Nom" >> nudoc/gen/sme_adjOahpatabellNorm.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr3

cat t3|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t3|sed 's/$/+A+Comp+Attr/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcompattr3

cat t3|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp3


cat t3|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl3

paste -d"|" t3 tattr3 tsgnom3 tcompattr3 tcomp3 tsuperl3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_adjOahpatabellNorm.jspwiki

rm -f tattr*  tsgnom*  tcomp*   tsuperl* 

