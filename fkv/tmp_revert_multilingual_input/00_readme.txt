Here is the trick to work with multilingual input:

Problem:
 - from csv to xml, the file names are generated automatically
   according to the source and target language
 - now Lene wanted to have multilingual input, hence the generated names
   look like: A_fkvnob_fin_eng.xml

 - the reverting script takes only ONE target language for the naming of
   the reverted files, namely the first after the src lang, here 'nob'

Solution:
 - the multilingual input files have to be renamed for each run
   so that the generated files can be created correctly.





