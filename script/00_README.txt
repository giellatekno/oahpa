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

2. revert the xml file from aaabbb to bbbaaa

 java -Xmx2024m net.sf.saxon.Transform -it:main revert_oahpa-lexicon.xsl inDir=xml-out

==> result files are generated in the directory defined in the variable outputDir (here "_reverted2nob"
    because 'nob' is defined as target language 'tlang')
  <xsl:param name="outDir" select="concat('_reverted2', $tlang)"/>

NB: the parameter inDir should be adapted to whatever the input directory is

3. redistribute the reverted files by the pos values of the reverted entries
   (some pos values might be different than those of the original entries)

 java -Xmx2024m net.sf.saxon.Transform -it:main pos-split_reverted-data.xsl inDir=_reverted2nob

==> result files are generated outputDir (CAVEAT: slang is not the origianl tlang!)
  <xsl:param name="outDir" select="concat('pos_redistr_', $slang)"/>

5. merge the possible doublings in each file separately

 java -Xmx2024m net.sf.saxon.Transform -it:main merge_pos-split-data.xsl inFile=pos_redistr_nob/A_nobfkv.xml
 java -Xmx2024m net.sf.saxon.Transform -it:main merge_pos-split-data.xsl inFile=pos_redistr_nob/N_nobfkv.xml
 java -Xmx2024m net.sf.saxon.Transform -it:main merge_pos-split-data.xsl inFile=pos_redistr_nob/V_nobfkv.xml

==> result files are generated outputDir (here: to_filter_nob)
  <xsl:variable name="outputDir" select="concat('to_filter_', $slang)"/>

___end of docu update___

6. filter away the entries without stat="pref"
   stat-filter_merged-data.xsl
 -> result files in xxx dir

7. re-create the smaoahpa db on victorio:

