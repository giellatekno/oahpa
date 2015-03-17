grep '<l ' src/N_crk.xml | grep -v '"none"' |grep AN | tr '<' '>' | cut -d '>' -f3 | grep -v '^-' |sed 's/$/+N+AN+Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-desc.xfst > gennouns.txt

grep '<l ' src/N_crk.xml | grep -v '"none"' |grep IN | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+IN+Sg/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-desc.xfst >> gennouns.txt

grep '<l ' src/N_crk.xml | grep -v '"none"' |grep 'AN.*>-' | tr '<' '>' | cut -d '>' -f3 |sed 's/$/+N+AN+Sg+PxSg1/' |$LOOKUP $GTHOME/langs/crk/src/generator-gt-desc.xfst >> gennouns.txt

cat gennouns.txt | cut -f1 | cut -d '+' -f1 | sort -u > lemmas
cat gennouns.txt | cut -f2 | sort -u > generated
comm -23 lemmas generated | see
