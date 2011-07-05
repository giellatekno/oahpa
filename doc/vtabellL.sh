# list of command making jspwiki document


# c. only oahpa verbs
cat $GTHOME/ped/sma/src/v_smanob.xml |tr '\n' '™' | sed 's/<l /£/g;'| tr '£' '\n'|tr '™' '\n' |grep '^pos'|tr '<' '>' | cut -d">" -f2|sort|uniq > t3

DATO=`date`

# Printing headers:

echo "!!!Tabell over oahpa-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verboahpatabellL.jspwiki
echo "" >> smadoc/gen/verboahpatabellL.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verboahpatabellL.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1 || Ger || PrsPrc " >> smadoc/gen/verboahpatabellL.jspwiki

echo "!!!Reversert tabell over oahpa-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verboahpatabellrevL.jspwiki
echo "" >> smadoc/gen/verboahpatabellrevL.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verboahpatabellrevL.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1 || Ger || PrsPrc " >> smadoc/gen/verboahpatabellrevL.jspwiki

# Making the 7 columns
cat t3|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3inf

cat t3|sed 's/$/+V+Ind+Prs+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prssg1

cat t3|sed 's/$/+V+Ind+Prs+Sg3/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prssg3

cat t3|sed 's/$/+V+Ind+Prs+Du1/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsdu1

cat t3|sed 's/$/+V+Ind+Prs+Du3/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsdu3

cat t3|sed 's/$/+V+Ind+Prs+Pl3/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prspl3

cat t3|sed 's/$/+V+Ind+Prt+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prtsg1

cat t3|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3ger

cat t3|sed 's/$/+V+PrsPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsprc

paste -d"|" t3 t3inf t3prssg1 t3prssg3 t3prsdu1 t3prsdu3 t3prspl3 t3prtsg1 t3ger t3prsprc | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tverbforms3

cat tverbforms3 >> smadoc/gen/verboahpatabellL.jspwiki

rm -f t?inf t?prssg1 t?prssg3 t?prsdu1 t?prsdu3 t?prspl3 t?prtsg1 t?ger t?prsprc

cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t3rev tverbforms3 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/verboahpatabellrevL.jspwiki

rm t3 t3rev tverbforms*
