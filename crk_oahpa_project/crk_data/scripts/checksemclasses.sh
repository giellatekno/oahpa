# sh scripts/checksemclasses.sh
# script for checking semclasses used in tasks, with semclasses in lexicon files. This is a simple script, not taking into account PoS or animacy.
echo ""

grep 'sem cl' ../meta_data/transl_questions.xml ../meta_data/noun_questions.xml ../meta_data/verb_questions/*xml |cut -d '"' -f2 |sort -u > tasksem
grep 'sem cl' ../src/*xml | cut -d '"' -f2 |sort -u > semlex

echo "semantic classes in tasks and lexicon. Problematic ones:"

comm -23 tasksem semlex
rm  tasksem semlex
