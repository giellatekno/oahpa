# list of command making jspwiki document

# c. only oahpa nouns
cat $GTHOME/ped/sme/univ_oahpa_data/data_sme/sme/n_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-GG' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-substantiv med GG" > nudoc/gen/sme_nounOahpaGG.jspwiki
echo "" >> nudoc/gen/sme_nounOahpaGG.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_nounOahpaGG.jspwiki
echo "||  lemma  ||  Sg Nom  ||  Pl Nom || Sg Ill || Pl Acc " >> nudoc/gen/sme_nounOahpaGG.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgnom3

cat t3|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tplnom3

cat t3|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tsgill3

cat t3|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tplacc3


paste -d"|" t3 tsgnom3 tplnom3 tsgill3 tplacc3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_nounOahpaGG.jspwiki

rm -f tsg*  tpl*   

