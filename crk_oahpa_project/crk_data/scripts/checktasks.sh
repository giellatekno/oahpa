# test for checking task id's

echo ""

echo "Checking task id's"
echo 'q id dublets:'
grep 'q id=' ../meta_data/transl_questions.xml ../meta_data/noun_questions.xml ../meta_data/verb_questions/*xml |cut -d '"' -f2 | sort | uniq -d
echo "Task types in a document, opening now. Check against python file."
echo ""

echo 'Task types:'  > taskreport
grep 'qtype' ../meta_data/transl_questions.xml ../meta_data/noun_questions.xml ../meta_data/verb_questions/*xml |cut -d '>' -f2 |cut -d '<' -f1 |sort -u  >> taskreport
open taskreport
