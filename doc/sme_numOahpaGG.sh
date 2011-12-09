# list of command making jspwiki document


# c. only oahpa numerals
cat $GTHOME/ped/sme/src/num_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-KJ' | tr "<" ">" | cut -d ">" -f3 | sort -u | egrep -v '(t|s|š|nubbi)$' > t3
cat $GTHOME/ped/sme/src/num_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-KJ'| tr "<" ">" | cut -d ">" -f3 | sort -u | egrep 's$' > collt3
cat $GTHOME/ped/sme/src/num_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-KJ'| tr "<" ">" | cut -d ">" -f3 | sort -u | egrep '(t|š|nubbi)$' > ordt3



DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-numeraler med GG" > nudoc/gen/sme_numOahpaGG.jspwiki
echo "" >> nudoc/gen/sme_numOahpaGG.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_numOahpaGG.jspwiki
echo "||  lemma  ||  Sg Nom  ||  Pl Nom || Sg Ill || Pl Acc " >> nudoc/gen/sme_numOahpaGG.jspwiki


# Making the columns
cat t3|sed 's/$/+Num+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+Num.*/-/'|tr '\t' ',' > tsgnom3

cat collt3|sed 's/$/+N+Coll+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgnom3

cat ordt3|sed 's/$/+A+Ord+Sg+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' >> tsgnom3


cat t3|sed 's/$/+Num+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+Num.*/-/'|tr '\t' ',' > tplnom3

cat collt3|sed 's/$/+N+Coll+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplnom3

cat ordt3|sed 's/$/+A+Ord+Pl+Nom/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' >> tplnom3


cat t3|sed 's/$/+Num+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+Num.*/-/'|tr '\t' ',' > tsgill3

cat collt3|sed 's/$/+N+Coll+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tsgill3

cat ordt3|sed 's/$/+A+Ord+Sg+Ill/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' >> tsgill3

cat t3|sed 's/$/+Num+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' > tplacc3

cat collt3|sed 's/$/+N+Coll+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplacc3

cat ordt3|sed 's/$/+A+Ord+Pl+Acc/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+N.*/-/'|tr '\t' ',' >> tplacc3

echo '- ' >> t3

cat collt3 >> t3

echo '- ' >> t3

cat ordt3 >> t3

paste -d"|" t3 tsgnom3 tplnom3 tsgill3 tplacc3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tnumforms3

cat tnumforms3 >> nudoc/gen/sme_numOahpaGG.jspwiki

rm -f tsg*  tpl*   


