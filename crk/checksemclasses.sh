# sh checksemclasses.sh

grep 'sem cl' meta/transl_questions.xml meta/noun_questions.xml meta/verb_questions/*xml |cut -d '"' -f2 |sort -u > tasksem
grep 'sem cl' src/*xml | cut -d '"' -f2 |sort -u > semlex
comm -23 tasksem semlex
rm  tasksem semlex

