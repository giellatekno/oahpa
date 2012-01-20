This is a directory for automatizing question-answer pair testing.

preliminary version of the script

1. single dialogue test:
 - test all questions in a single dialogue
 - input file is the dialogue file in xml format

command:
perl test_qa.pl xyz_firstmeeting.xml


2. all dialogues test:
 - test all questions in all dialogues
 - the input file is generated from all dialogue files
   in a directory by the script extract_questions.xsl
  


perl test_all_qa.pl all_dialogues.xml

output:
tmp_data.txt (intermediate data just for check)
final_data.txt

