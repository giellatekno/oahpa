# list of command making jspwiki document

# c. only oahpa nouns
 cat $GTHOME/ped/sma/src/n_smanob.xml |tr '\n' '™' | sed 's/<l /£/g;'| tr '£' '\n'|tr '™' '\n' |grep '^pos'|tr '<' '>' | cut -d">" -f2|sort|uniq > t3


# Printing headers:


echo "!!!Tabell over oahpa-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounoahpatabellL.jspwiki
echo "" >> smadoc/gen/nounoahpatabellL.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounoahpatabellL.jspwiki
echo "!!!Reversert tabell over oahpa-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounoahpatabellrevL.jspwiki
echo "" >> smadoc/gen/nounoahpatabellrevL.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounoahpatabellrevL.jspwiki

# Making the 7 columns
cat t3|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgnom

cat t3|sed 's/$/+N+Sg+Gen/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sggen

cat t3|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgill

cat t3|sed 's/$/+N+Sg+Ine/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgine

cat t3|sed 's/$/+N+Ess/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3ess

cat t3|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3plnom

cat t3|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3placc

cat t3|sed 's/$/+N+Pl+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-L.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3plill



paste -d"|" t3 t3sggen t3sgill t3sgine t3ess t3plnom t3placc t3plill | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > t3nounforms

cat t3nounforms >> smadoc/gen/nounoahpatabellL.jspwiki

rm -f  t?sggen t?sgill t?sgine t?ess t?plnom t?placc t?plill 

cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t3rev t3nounforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/nounoahpatabellrevL.jspwiki

rm t3 t3rev t?nounforms
