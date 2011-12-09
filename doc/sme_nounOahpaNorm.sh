# list of command making jspwiki document

# c. only oahpa nouns
cat $GTHOME/ped/sme/src/n_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-GG' | egrep -v '(g3|actor)' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3
cat $GTHOME/ped/sme/src/n_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-GG' | grep  g3 | tr "<" ">" | cut -d ">" -f3 | sort -u > g3t3
cat $GTHOME/ped/sme/src/n_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-GG' | grep actor | tr "<" ">" | cut -d ">" -f3 | sort -u > actort3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-substantiv med Norm" > nudoc/gen/sme_nounOahpaNorm.jspwiki
echo "" >> nudoc/gen/sme_nounOahpaNorm.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_nounOahpaNorm.jspwiki
echo "||  lemma  ||  Sg Nom  ||  Pl Nom || Sg Ill || Pl Acc " >> nudoc/gen/sme_nounOahpaNorm.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' > tsgnom3

cat t3|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' > tplnom3

cat t3|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' > tsgill3

cat t3|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' > tplacc3

cat g3t3|sed 's/$/+G3+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgnom3

cat g3t3|sed 's/$/+G3+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplnom3

cat g3t3|sed 's/$/+G3+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgill3

cat g3t3|sed 's/$/+G3+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplacc3

cat actort3|sed 's/$/+N+Actor+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgnom3

cat actort3|sed 's/$/+N+Actor+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplnom3

cat actort3|sed 's/$/+N+Actor+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgill3

cat actort3|sed 's/$/+N+Actor+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplacc3

echo '- ' >> t3

cat g3t3 >> t3

echo '- ' >> t3

cat actort3 >> t3


paste -d"|" t3 tsgnom3 tplnom3 tsgill3 tplacc3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_nounOahpaNorm.jspwiki

rm -f tsg*  tpl*   

