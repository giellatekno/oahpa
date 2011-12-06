# list of command making jspwiki document

# c. only oahpa verbs
cat $GTHOME/ped/sme/univ_oahpa_data/data_sme/sme/v_smenob.xml | tr "\n" " " | tr "<" "\n" | grep '^l ' | cut -d ">" -f2 | sort -u > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-verb med GG" > nudoc/gen/sme_verbOahpaGG.jspwiki
echo "" >> nudoc/gen/sme_verbOahpaGG.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_verbOahpaGG.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Pl1 || Pot Prs Sg3 || Cond Prs Sg1 || Imprt Pl1 || Imprt Pl2 || Ger " >> nudoc/gen/sme_verbOahpaGG.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tinf3

cat t3|sed 's/$/+V+Ind+Prs+Pl1/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tprspl13

cat t3|sed 's/$/+V+Pot+Prs+Sg3/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tpotsg3

cat t3|sed 's/$/+V+Cond+Prs+Sg1/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tcondsg13

cat t3|sed 's/$/+V+Imprt+Pl1/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > timppl13

cat t3|sed 's/$/+V+Imprt+Pl2/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > timppl23


cat t3|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sme/bin/isme-GG.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+A.*/-/'|tr '\t' ',' > tger3


paste -d"|" t3 tinf3 tprspl13 tpotsg3 tcondsg13 timppl13 timppl23 tger3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_verbOahpaGG.jspwiki

rm -f tinf*  tpr* tpot*  tcond* timp* tger*  

