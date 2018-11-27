This is a documentation about
the work on the source files for all languages.

* src contains the smeX source files
* nobsme contains the reverted data from smeX
* finsme contains the reverted data from smeX
* meta contains addition data for feeding the db for sme_oahpa


Issues:
1. dummy _SWE t-elements: to be transferred from the nob pendants
 ==> todo

sme>grep '<t stat="pref"/>' *xml | sort | uniq -c | sort -nr 
 251 prop_smenob.xml:            <t stat="pref"/>
  67 multiword_smenob.xml:            <t stat="pref"/>

2. add synonyms from the old data from nobsme and finsme to the new data sets
 ==> todo

