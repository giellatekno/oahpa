# list of command making jspwiki document

# a. all nouns
cat $GTHOME/gt/sma/src/noun-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|grep -v 'Err/Sub'|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. dict nouns
cat $GTHOME/words/dicts/smanob/src/n_smanob.xml|grep '<l '|tr '<' '>'|cut -d">" -f3 > t2


# c. only oahpa nouns
cat $GTHOME/ped/sma/src/n_smanob.xml | grep '<l ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3


# Printing headers:

echo "!!!Tabell over alle substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounalletabellnorm.jspwiki
echo "" >> smadoc/gen/nounalletabellnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounalletabellnorm.jspwiki
echo "!!!Reversert tabell over alle substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounalletabellrevnorm.jspwiki
echo "" >> smadoc/gen/nounalletabellrevnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounalletabellrevnorm.jspwiki

echo "!!!Tabell over dict-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/noundicttabellnorm.jspwiki
echo "" >> smadoc/gen/noundicttabellnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/noundicttabellnorm.jspwiki
echo "!!!Reversert tabell over dict-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/noundicttabellrevnorm.jspwiki
echo "" >> smadoc/gen/noundicttabellrevnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/noundicttabellrevnorm.jspwiki

echo "!!!Tabell over oahpa-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounoahpatabellnorm.jspwiki
echo "" >> smadoc/gen/nounoahpatabellnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounoahpatabellnorm.jspwiki
echo "!!!Reversert tabell over oahpa-substantiv - OBS! arbeidsliste for debugging" > smadoc/gen/nounoahpatabellrevnorm.jspwiki
echo "" >> smadoc/gen/nounoahpatabellrevnorm.jspwiki
echo "||  lemma  ||  Nom Sg  ||  Gen Sg || Ill Sg || Ine Sg || Ess || Nom Pl || Acc Pl || Ill Pl " >> smadoc/gen/nounoahpatabellrevnorm.jspwiki

# Making the 7 columns
cat t1|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1sgnom
cat t2|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2sgnom
cat t3|sed 's/$/+N+Sg+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgnom

cat t1|sed 's/$/+N+Sg+Gen/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1sggen
cat t2|sed 's/$/+N+Sg+Gen/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2sggen
cat t3|sed 's/$/+N+Sg+Gen/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sggen

cat t1|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1sgill
cat t2|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2sgill
cat t3|sed 's/$/+N+Sg+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgill

cat t1|sed 's/$/+N+Sg+Ine/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1sgine
cat t2|sed 's/$/+N+Sg+Ine/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2sgine
cat t3|sed 's/$/+N+Sg+Ine/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3sgine

cat t1|sed 's/$/+N+Ess/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1ess
cat t2|sed 's/$/+N+Ess/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2ess
cat t3|sed 's/$/+N+Ess/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3ess

cat t1|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1plnom
cat t2|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2plnom
cat t3|sed 's/$/+N+Pl+Nom/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3plnom

cat t1|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1placc
cat t2|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2placc
cat t3|sed 's/$/+N+Pl+Acc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3placc

cat t1|sed 's/$/+N+Pl+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t1plill
cat t2|sed 's/$/+N+Pl+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t2plill
cat t3|sed 's/$/+N+Pl+Ill/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+N.*/-/'|tr '\t' ',' > t3plill



paste -d"|" t1 t1sggen t1sgill t1sgine t1ess t1plnom t1placc t1plill | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > t1nounforms
paste -d"|" t2 t2sggen t2sgill t2sgine t2ess t2plnom t2placc t2plill | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > t2nounforms
paste -d"|" t3 t3sggen t3sgill t3sgine t3ess t3plnom t3placc t3plill | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > t3nounforms

cat t1nounforms >> smadoc/gen/nounalletabellnorm.jspwiki
cat t2nounforms >> smadoc/gen/noundicttabellnorm.jspwiki
cat t3nounforms >> smadoc/gen/nounoahpatabellnorm.jspwiki

rm -f  t?sggen t?sgill t?sgine t?ess t?plnom t?placc t?plill 

cat t1 | perl -nle 'print scalar reverse $_' > t1rev
cat t2 | perl -nle 'print scalar reverse $_' > t2rev
cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t1rev t1nounforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/nounalletabellrevnorm.jspwiki
paste t2rev t2nounforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/noundicttabellrevnorm.jspwiki
paste t3rev t3nounforms | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/nounoahpatabellrevnorm.jspwiki

rm t1 t2 t3 t1rev t2rev t3rev t?nounforms
