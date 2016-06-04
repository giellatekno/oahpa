# sh scripts/checkgrammartags.sh
# the output will be tags which are not in paradigm-files in meta
# and tags in task, but missing in tags.txt


grep grammar meta/verb_questions/* meta/noun_questions.xml meta/transl_questions.xml |cut -d '"' -f2  | sed 's/Animacy/AN/g' |sort -u > tasktags
cat meta/v_paradigms.txt meta/n_paradigms.txt meta/pron_paradigms.txt |sort > paradigmtags
echo "problematic tag string:"
comm -23 tasktags paradigmtags
echo "missing in tags.txt:"
cat meta/tags.txt |grep -v '#' |sort -u > taglist
cat tasktags | tr '+' '\n' | sort -u > tasklist
comm -23 tasklist taglist

rm tasktags paradigmtags tasklist taglist
