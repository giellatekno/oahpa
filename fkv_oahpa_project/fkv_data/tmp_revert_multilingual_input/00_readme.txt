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

Example:
 1. first run the revert script as usual:
  __input__
  the xml-out contains files named as:
A_fkvnob_fin_eng.xml   
Adv_fkvnob_fin_eng.xml
...
 __commando__
java -Xmx2024m net.sf.saxon.Transform -it:main revert_oahpa-lexicon.xsl inDir=xml-out slang=fkv tlang=nob

 2. then rename the files from the xml-out directory with the script local_rename_1.sh
 __commando__
sh local_rename_1.sh 

 __input for the reversion to fin__
tmp_revert_multilingual_input>ls xml-out/
A_fkvfin.xml   MWE_fkvfin.xml POS_fkvfin.xml Pr_fkvfin.xml
Adv_fkvfin.xml N_fkvfin.xml   Po_fkvfin.xml  V_fkvfin.xml

 __commando__
java -Xmx2024m net.sf.saxon.Transform -it:main revert_oahpa-lexicon.xsl inDir=xml-out slang=fkv tlang=fin

 3. the rename the files from the xml-out directory with the script local_rename_2.sh
__commando__
sh local_rename_1.sh

 __input for the reversion to eng__
tmp_revert_multilingual_input>ls xml-out/
A_fkveng.xml   MWE_fkveng.xml POS_fkveng.xml Pr_fkveng.xml
Adv_fkveng.xml N_fkveng.xml   Po_fkveng.xml  V_fkveng.xml

__commando__
java -Xmx2024m net.sf.saxon.Transform -it:main revert_oahpa-lexicon.xsl inDir=xml-out slang=fkv tlang=eng

Done!

