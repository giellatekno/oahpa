cat task.txt | preprocess | $LOOKUP ../englexc/eng.fst | lookup2cg > engtest
cat answer.txt| preprocess | $LOOKUP $GTHOME/langs/crk/src/analyser-gt-desc.xfst | lookup2cg >  crktest
cat engtest delimiter.txt crktest | vislcg3 -g ../src/crk-ped.cg3