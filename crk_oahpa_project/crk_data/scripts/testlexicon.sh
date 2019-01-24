# sh scripts/testlexicon.sh 

#The test gives and opens a dokument: testresult.txt with lemmas which are not generated and how the dependent nouns are generated for Px1Sg. 

grep '<l ' src/V_crk.xml | grep -v '"none"' |grep '"AI"' | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+V+AI+Ind+Prs+3Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst > generation_allverbs.txt
grep '<l ' src/V_crk.xml | grep -v '"none"' |grep '"II"' | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+V+II+Ind+Prs+3Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allverbs.txt
grep '<l ' src/V_crk.xml | grep -v '"none"' |grep '"TI"' | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+V+TI+Ind+Prs+3Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allverbs.txt
grep '<l ' src/V_crk.xml | grep -v '"none"' |grep '"TA"' | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+V+TA+Ind+Prs+3Sg+4Sg\/PlO/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allverbs.txt

cat generation_allverbs.txt | cut -f1 | cut -d '+' -f1 | sort -u > lemmas
cat generation_allverbs.txt | cut -f2 | sort -u > genlemmas
echo "Not generated verb lemma(s):"  
comm -23 lemmas genlemmas  
echo ""  

grep '<l ' src/N_crk.xml | grep -v '"none"' |grep AN | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+N+AN+Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst > generation_allnouns.txt

grep '<l ' src/N_crk.xml | grep -v '"none"' |grep IN | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+IN+Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allnouns.txt

grep '<l ' src/N_crk.xml | grep  '"Pl"' |grep IN | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+IN+Pl/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allnouns.txt

grep '<l ' src/N_crk.xml | grep  '"Pl"' |grep AN | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+AN+Pl/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> generation_allnouns.txt

cat generation_allnouns.txt | cut -f1 | cut -d '+' -f1 | sort -u > lemmas
cat generation_allnouns.txt | cut -f2 | sort -u > genlemmas
echo "Not generated noun lemma(s):" 
comm -23 lemmas genlemmas  
echo ""  

echo "Generating depented lemmas in a document for manual check, , opening now."  
echo "Generating depended lemmas for manual check" > testresult.txt
echo "" >> testresult.txt
grep '<l ' src/N_crk.xml | grep -v '"none"' |grep 'AN.*>-' | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+AN+Sg+Px1Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-norm.xfst >> testresult.txt


rm lemmas genlemmas generation_allverbs.txt generation_allnouns.txt


open testresult.txt

