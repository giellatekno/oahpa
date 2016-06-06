# sh scripts/checkgrammartags.sh
# the output will be tags which are not in paradigm-files in meta
# and tags in task, but missing in tags.txt


grep grammar meta/verb_questions/* meta/noun_questions.xml meta/transl_questions.xml |cut -d '"' -f2  | sed 's/Animacy/AN/g' |sort -u > tasktags
cat meta/v_paradigms.txt meta/n_paradigms.txt meta/pron_paradigms.txt |sort > paradigmtags
cat meta/tags.txt |grep -v '#' |sort -u > taglist
cat tasktags | tr '+' '\n' | sort -u > tasklist

echo "Checking grammar strings in tasks. Problematic ones:"  
comm -23 tasktags paradigmtags  
echo "Checking tags in tags.txt. Problematic ones:"  
comm -23 tasklist taglist  
echo "Checking grammar tags. (only testing verbs and nouns)  Problematic ones:"  
grep 'N+IN' tasktags | sed 's/^/mahkahk\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?' 
grep 'N+AN' tasktags | sed 's/^/kohkôs\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?'  
grep 'V+AI' tasktags | sed 's/^/atoskêw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?'  

grep 'V+II' tasktags | sed 's/^/wâpan\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?'  
grep 'V+TI' tasktags | sed 's/^/pêtâw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?'  
grep 'V+TA' tasktags | sed 's/^/pêhtawêw\+/' |$HLOOKUP $GTHOME/langs/crk/src/generator-gt-norm.hfst |grep '?'  
 
rm tasktags paradigmtags tasklist taglist
