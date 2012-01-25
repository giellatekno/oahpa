This is a directory for automatizing question-answer pair testing for
vasta, ceallka and sahka.

First, questions are extracted from xml or txt and paired with a dummy
answer, then this dummy answer is replaced by one or more answer the
question under consideration and the pair is sent to the CG grammar
for testing.

1. generate  question-dummy_answer pairs out of two different formats: txt and xml
  1.1. txt format is one question per line
      (a) only the question, for example
            Gosa don manat
      (b) question ID column as separator and question, for example
            id07: Gosa don manat
 Command:
   java net.sf.saxon.Transform -it main txt2qa-xml.xsl inFile=INPUT-FILE.txt outDir=OUTPUT-DIR

The output will be generated in OUTPUT-DIR/INPUT-FILE.xml.

  1.2. xml format as it is used in the xml files for oahpa:
      for Sahka, the command is

java net.sf.saxon.Transform -it main gen_sahka-qa-templates.xsl inDir=PATH/TO/INPUT-DIR outDir=PATH/TO/OUTPUT-DIR


2. test questions

perl qa-test_dialogue.pl QA-PAIR-FILE.xml MODE

The parameter MODE can be: vasta, cealkka, or sahka.

For example:
perl qa-test_dialogue.pl xyz_firstmeeting.xml sahka

----------------

cat qa_file | preprocess | usmeNorm | lookup2cg > interfil.txt

Det legges til delimiter mellom Q og A (se forms.py)
       if self.gametype=="sahka":
            analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + utterance_name +"\n"
        else:
            analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"



vasta:					
"<^qst>"
	 "^qst" QDL
	 
	 
sahka:
"<^sahka>"
	 "^sahka" QDL gosa_bidjat_TV 
	 
cat interfil.txt | vislcg3 -g ~/ped/sme/src/sme-ped.cg3


