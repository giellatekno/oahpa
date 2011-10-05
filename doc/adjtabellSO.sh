# list of command making jspwiki document

# c. only oahpa adjectives
cat $GTHOME/ped/sma/src/a_smanob.xml | grep '<l ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabellSO.jspwiki
echo "" >> smadoc/gen/adjoahpatabellSO.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/adjoahpatabellSO.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc" >> smadoc/gen/adjoahpatabellSO.jspwiki

echo "!!!Reversert tabell over oahpa-adjektiv - OBS! arbeidsliste for debugging" > smadoc/gen/adjoahpatabellrevSO.jspwiki
echo "" >> smadoc/gen/adjoahpatabellrevSO.jspwiki 
echo "Testdato: $DATO" >> smadoc/gen/adjoahpatabellrevSO.jspwiki
echo "||  lemma  ||  Attr  ||  Sg Nom || Comp Sg Nom || Superl Sg Nom  || Sg Acc" >> smadoc/gen/adjoahpatabellrevSO.jspwiki

# Making the 4 columns
cat t3|sed 's/$/+A+Attr/;'| lookup -q $GTHOME/gt/sma/bin/isma-SO.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tattr3

cat t3|sed 's/$/+A+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-SO.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t3|sed 's/$/+A+Comp+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-SO.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tcomp3

cat t3|sed 's/$/+A+Superl+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-SO.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A.*/-/'|tr '\t' ',' > tsuperl3

cat t3|sed 's/$/+A+Sg+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-SO.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+A+.*/-/'|tr '\t' ',' > tAcc3

paste -d"|" t3 tattr3 tsgnom3 tcomp3 tsuperl3 tAcc3 | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> smadoc/gen/adjoahpatabellSO.jspwiki

rm -f tattr*  tsgnom*  tcomp*   tsuperl* tAcc*

cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t3rev tadjforms3 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/adjoahpatabellrevSO.jspwiki

rm -f t?rev* tadjforms* t3
