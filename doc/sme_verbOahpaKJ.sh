# list of command making jspwiki document

# c. only oahpa verbs
cat $GTHOME/ped/sme/src/v_smenob.xml | sed 's/<l /$<l /' | sed 's/<mg>/$<mg>/' | tr "\n" " " | tr "$" "\n" | grep '<l ' | grep -v 'NOT-KJ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

# c. oahpa adj
echo "!!!Tabell over Oahpa-verb med KJ" > nudoc/gen/sme_verbOahpaKJ.jspwiki
echo "" >> nudoc/gen/sme_verbOahpaKJ.jspwiki
echo "Testdato: $DATO" >> nudoc/gen/sme_verbOahpaKJ.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Pl1 || Pot Prs Sg3 || Cond Prs Sg1 || Imprt Pl1 || Imprt Pl2 || Ger " >> nudoc/gen/sme_verbOahpaKJ.jspwiki


# Making the 4 columns
cat t3|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > tinf3

cat t3|sed 's/$/+V+Ind+Prs+Pl1/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > tprspl13

cat t3|sed 's/$/+V+Pot+Prs+Sg3/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > tpotsg3

cat t3|sed 's/$/+V+Cond+Prs+Sg1/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > tcondsg13

cat t3|sed 's/$/+V+Imprt+Pl1/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > timppl13

cat t3|sed 's/$/+V+Imprt+Pl2/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > timppl23


cat t3|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sme/bin/isme-KJ.restr.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8,10,12,14,16|sed 's/.*+V.*/-/'|tr '\t' ',' > tger3


paste -d"|" t3 tinf3 tprspl13 tpotsg3 tcondsg13 timppl13 timppl23 tger3  | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tadjforms3

cat tadjforms3 >> nudoc/gen/sme_verbOahpaKJ.jspwiki

rm -f tinf*  tpr* tpot*  tcond* timp* tger*  

