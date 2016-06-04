# test for checking task id's 

echo 'q id dublets:' > taskreport
grep 'q id=' meta/transl_questions.xml meta/noun_questions.xml meta/verb_questions/*xml |cut -d '"' -f2 | sort | uniq -d >> taskreport
echo '' >> taskreport
echo 'Task types:'  >> taskreport
grep 'qtype' meta/transl_questions.xml meta/noun_questions.xml meta/verb_questions/*xml |cut -d '>' -f2 |cut -d '<' -f1 |sort -u  >> taskreport
see taskreport