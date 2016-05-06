The Vasta demo
==============

You can test different translations.

echo 'This is a shoe' | preprocess | $LOOKUP ../englexc/eng.fst | lookup2cg > engtest

echo 'maskisin ôma' | preprocess | $LOOKUP $GTHOME/langs/crk/src/analyser-gt-desc.xfst | lookup2cg >  crktest

sh cg3_check.sh

Sentence patters (no punctuation!):
* This/that is a shoe
* These/those are cats
* This/that shoe
* These/those cats


The nouns which are included in the demo:

shoe
knife
spoon
bread
sugar
carrot
dog
man
woman
cat
fish
bacon
milk
store
egg
chair
potato


