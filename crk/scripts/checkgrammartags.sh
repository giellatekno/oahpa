# sh scripts/checkgrammartags.sh
# the output will be tags which are not in paradigm-files in meta
# and tags in task, but missing in tags.txt


grep grammar meta/verb_questions/* meta/noun_questions.xml meta/transl_questions.xml |cut -d '"' -f2  | sed 's/Animacy/AN/g' |sort -u > tasktags
cat meta/v_paradigms.txt meta/n_paradigms.txt meta/pron_paradigms.txt |sort > paradigmtags
echo "Problematic tag string:" > tagreport.txt
comm -23 tasktags paradigmtags >> tagreport.txt
echo "" >> tagreport.txt
echo "Missing in tags.txt:" >> tagreport.txt
cat meta/tags.txt |grep -v '#' |sort -u > taglist
cat tasktags | tr '+' '\n' | sort -u > tasklist
comm -23 tasklist taglist >> tagreport.txt
echo "" >> tagreport.txt
echo "Taskstrings to check (only testing verbs and nouns):" >> tagreport.txt
grep 'N+IN' tasktags | sed 's/^/mahkahk\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt
grep 'N+AN' tasktags | sed 's/^/kohkôs\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt
grep 'V+AI' tasktags | sed 's/^/atoskêw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt

grep 'V+II' tasktags | sed 's/^/wâpan\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt
grep 'V+TI' tasktags | sed 's/^/pêtâw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt
grep 'V+TA' tasktags | sed 's/^/pêhtawêw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' >> tagreport.txt
see tagreport.txt

rm tasktags paradigmtags tasklist taglist
