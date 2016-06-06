# test for checking task id's 

echo ""  

echo "Checking task id's" 
echo 'q id dublets:'  
grep 'q id=' meta/transl_questions.xml meta/noun_questions.xml meta/verb_questions/*xml |cut -d '"' -f2 | sort | uniq -d  
echo "Task types in a document, opening now. Check against python file." 
echo ""  

echo 'Task types:'  > taskreport
grep 'qtype' meta/transl_questions.xml meta/noun_questions.xml meta/verb_questions/*xml |cut -d '>' -f2 |cut -d '<' -f1 |sort -u  >> taskreport
open taskreport