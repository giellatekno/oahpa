This directory contains some scripts for working
with lexical data for oahpa.

1. convert data from csv into oahpa-lexicon xml
field separator = __ (two underscores) 
separator between items of same type (translations, semantic classes) = , (comma)

 java -Xmx2024m net.sf.saxon.Transform -it:main uusv2oahpa_xml.xsl inFile=wordlist.csv src_lang=fkv tgt_lang=nob

 ==> result files are generated in the directory defined in the variable outputDir (here "xml-out")
 <xsl:variable name="outputDir" select="'xml-out'"/>

input format:
LEMMA __ POS __ TRANSLATION_1,TRANSLATION_2,TRANSLATION_n __ SEMCLASS_1,SEMCLASS_2, SEMCLASS_n

NB 1: the first translation gets the attribute stat="pref"
NB 2: all translation get the same set of semantic classes
NB 3: if a lemma has different meanings it has to have as many entries as meanings
      and each e-element has to have an ID denoting its meaning


2. revert smaxxx to xxxsma
   revert_sma-data.xsl
 -> result files in some tmp dir (reverted2xxx)

3. redistribute the reverted files by pos (some pos values might be different as the file name generated)
   pos-split_reverted-data.xsl  
 -> result files in some tmp dir (pos_redistr_xxx)

4. in pos_redistr_xxx: merge collect POS and phrase_POS in one file POS_xxxsma.xml

5. merge the possible doublings
   merge_pos-split-data.xsl inFile=pos_redistr_xxx/a_xxxsma.xml
 -> result files in to_filter_xxx dir

6. filter away the entries without stat="pref"
   stat-filter_merged-data.xsl
 -> result files in xxx dir

7. re-create the smaoahpa db on victorio:

