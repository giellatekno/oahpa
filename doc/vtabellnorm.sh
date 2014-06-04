# list of command making jspwiki document


# a. all verbs
cat $GTHOME/gt/sma/src/verb-sma-lex.txt |tr "\!" "£"|cut -d"£" -f1|grep ";"|grep -v 'Err/Sub'|tr '[+:]' ' '| cut -d" " -f1|tr -d '[#^]'|sort|uniq > t1

# b. dict verbs
cat $GTHOME/words/dicts/smanob/src/v_smanob.xml|grep '<l '|tr '<' '>'|cut -d">" -f3 > t2


# c. only oahpa verbs
cat $GTHOME/ped/sma/src/v_smanob.xml | grep '<l ' | tr "<" ">" | cut -d ">" -f3 | sort -u > t3

DATO=`date`

# Printing headers:

echo "!!!Tabell over alle verb - OBS! arbeidsliste for debugging " > smadoc/gen/verballetabellnorm.jspwiki
echo "" >> smadoc/gen/verballetabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verballetabellnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verballetabellnorm.jspwiki

echo "!!!Reversert tabell over alle verb - OBS! arbeidsliste for debugging" > smadoc/gen/verballetabellrevnorm.jspwiki
echo "" >> smadoc/gen/verballetabellrevnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verballetabellrevnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verballetabellrevnorm.jspwiki

echo "!!!Tabell over dict-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verbdicttabellnorm.jspwiki
echo "" >> smadoc/gen/verbdicttabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verbdicttabellnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verbdicttabellnorm.jspwiki

echo "!!!Reversert tabell over dict-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verbdicttabellrevnorm.jspwiki
echo "" >> smadoc/gen/verbdicttabellrevnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verbdicttabellrevnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verbdicttabellrevnorm.jspwiki

echo "!!!Tabell over oahpa-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verboahpatabellnorm.jspwiki
echo "" >> smadoc/gen/verboahpatabellnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verboahpatabellnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verboahpatabellnorm.jspwiki

echo "!!!Reversert tabell over oahpa-verb - OBS! arbeidsliste for debugging" > smadoc/gen/verboahpatabellrevnorm.jspwiki
echo "" >> smadoc/gen/verboahpatabellrevnorm.jspwiki
echo "Testdato: $DATO" >> smadoc/gen/verboahpatabellrevnorm.jspwiki
echo "||  lemma  ||  Inf  ||  Prs Sg1 || Prs Sg3 || Prs Du1 || Prs Du3 || Prs Pl3 || Prt Sg1  ||  PrfPrc || Ger || PrsPrc " >> smadoc/gen/verboahpatabellrevnorm.jspwiki

# Making the 7 columns
cat t1|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1inf
cat t2|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2inf
cat t3|sed 's/$/+V+Inf/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3inf

cat t1|sed 's/$/+V+Ind+Prs+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prssg1
cat t2|sed 's/$/+V+Ind+Prs+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prssg1
cat t3|sed 's/$/+V+Ind+Prs+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prssg1

cat t1|sed 's/$/+V+Ind+Prs+Sg3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prssg3
cat t2|sed 's/$/+V+Ind+Prs+Sg3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prssg3
cat t3|sed 's/$/+V+Ind+Prs+Sg3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prssg3

cat t1|sed 's/$/+V+Ind+Prs+Du1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prsdu1
cat t2|sed 's/$/+V+Ind+Prs+Du1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prsdu1
cat t3|sed 's/$/+V+Ind+Prs+Du1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsdu1

cat t1|sed 's/$/+V+Ind+Prs+Du3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prsdu3
cat t2|sed 's/$/+V+Ind+Prs+Du3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prsdu3
cat t3|sed 's/$/+V+Ind+Prs+Du3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsdu3

cat t1|sed 's/$/+V+Ind+Prs+Pl3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prspl3
cat t2|sed 's/$/+V+Ind+Prs+Pl3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prspl3
cat t3|sed 's/$/+V+Ind+Prs+Pl3/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prspl3

cat t1|sed 's/$/+V+Ind+Prt+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prtsg1
cat t2|sed 's/$/+V+Ind+Prt+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prtsg1
cat t3|sed 's/$/+V+Ind+Prt+Sg1/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prtsg1

cat t1|sed 's/$/+V+PrfPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prfprc
cat t2|sed 's/$/+V+PrfPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prfprc
cat t3|sed 's/$/+V+PrfPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prfprc


cat t1|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1ger
cat t2|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2ger
cat t3|sed 's/$/+V+Ger/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3ger

cat t1|sed 's/$/+V+PrsPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t1prsprc
cat t2|sed 's/$/+V+PrsPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t2prsprc
cat t3|sed 's/$/+V+PrsPrc/;'| lookup -q $GTHOME/gt/sma/bin/isma-norm.fst |tr '\n' '™'|sed 's/™™/£/g;'|tr '£' '\n'|tr '™' '\t'|cut -f2,4,6,8|sed 's/.*+V.*/-/'|tr '\t' ',' > t3prsprc

paste -d"|" t1 t1inf t1prssg1 t1prssg3 t1prsdu1 t1prsdu3 t1prspl3 t1prtsg1 t1prfprc t1ger t1prsprc | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tverbforms1
paste -d"|" t2 t2inf t2prssg1 t2prssg3 t2prsdu1 t2prsdu3 t2prspl3 t2prtsg1 t2prfprc t2ger t2prsprc | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tverbforms2
paste -d"|" t3 t3inf t3prssg1 t3prssg3 t3prsdu1 t3prsdu3 t3prspl3 t3prtsg1 t3prfprc t3ger t3prsprc | sed 's/|/ | /g;' | sed 's/^/| /'| sed 's/,/, /g;' | grep '[A-Za-z]' > tverbforms3

cat tverbforms1 >> smadoc/gen/verballetabellnorm.jspwiki
cat tverbforms2 >> smadoc/gen/verbdicttabellnorm.jspwiki
cat tverbforms3 >> smadoc/gen/verboahpatabellnorm.jspwiki

rm -f t?inf t?prssg1 t?prssg3 t?prsdu1 t?prsdu3 t?prspl3 t?prtsg1 t?prfprc t?ger t?prsprc

cat t1 | perl -nle 'print scalar reverse $_' > t1rev
cat t2 | perl -nle 'print scalar reverse $_' > t2rev
cat t3 | perl -nle 'print scalar reverse $_' > t3rev

paste t1rev tverbforms1 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/verballetabellrevnorm.jspwiki
paste t2rev tverbforms2 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/verbdicttabellrevnorm.jspwiki
paste t3rev tverbforms3 | sort | cut -f2 | grep '[A-Za-z]' >> smadoc/gen/verboahpatabellrevnorm.jspwiki

rm t1 t2 t3 t1rev t2rev t3rev tverbforms*
