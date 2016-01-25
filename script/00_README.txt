This directory contains some scripts for working
with lexical data for oahpa.

1. convert data from csv into oahpa-lexicon xml
 - 'c' in 'csv' is a very general label here (comma separated values)
 - this is the reason why the scripts are named 'uusv': underscore underscore separated values
field separator = __ (two underscores)
separator between items of same type (translations, semantic classes) = , (comma)

 java -Xmx2024m net.sf.saxon.Transform -it:main uusv2oahpa_xml_extened.xsl inFile=wordlist.csv src_lang=crk tgt_lang=eng

 ==> result files are generated in the directory defined in the variable outDir (here "xml-out")
 <xsl:variable name="outDir" select="'xml-out'"/>

input format:
LEMMA __ POS __ TRANSLATION_1,TRANSLATION_2,TRANSLATION_n __ SEMCLASS_1,SEMCLASS_2, SEMCLASS_n

NB 1: the first translation gets the attribute stat="pref"
NB 2: all translation get the same set of semantic classes
NB 3: if a lemma has different meanings it has to have as many entries as meanings
      and each e-element has to have an ID denoting its meaning

2. revert the xml file from aaabbb to bbbaaa

 java -Xmx2024m net.sf.saxon.Transform -it:main revert_oahpa-lexicon.xsl inDir=xml-out slang=LANG-CODE tlang=LANG-CODE

==> result files are generated in the directory defined in the variable outDir (here "_reverted2eng"
    because 'nob' is defined as target language 'tlang', generally _reverted2TLANG)
  <xsl:param name="outDir" select="concat('_reverted2', $tlang)"/>

NB: the parameter inDir should be adapted to whatever the input directory is

3. redistribute the reverted files by the pos values of the reverted entries
   (some pos values might be different than those of the original entries)

 java -Xmx2024m net.sf.saxon.Transform -it:main pos-split_reverted-data.xsl inDir=_reverted2SLANG

 java -Xmx2024m net.sf.saxon.Transform -it:main pos-split_reverted-data.xsl inDir=_reverted2nob

==> result files are generated outDir (CAVEAT: slang is not the original tlang!)
  <xsl:param name="outDir" select="concat('pos_redistr_', $slang)"/>

5. merge the possible doublings for each language and each file separately

 java -Xmx2024m net.sf.saxon.Transform -it:main merge_pos-split-data.xsl slang=SLANG

The script processes all the files in the directory pos_redistr_SLANG, e.g.
 java -Xmx2024m net.sf.saxon.Transform -it:main merge_pos-split-data.xsl slang=nob
processes all the files in the directory pos_redistr_nob.

==> result files are written into outDir (here: to_filter_nob)
  <xsl:variable name="outDir" select="concat('to_filter_', $slang)"/>


6. filter away the entries without stat="pref"

 java -Xmx2024m net.sf.saxon.Transform -it:main stat-filter_merged-data.xsl slang=SLANG 

The script processes all the files in the directory to_filter_SLANG, e.g.

 java -Xmx2024m net.sf.saxon.Transform -it:main stat-filter_merged-data.xsl slang=nob processes all the files in the directory to_filter_nob.

==> result files are written into outDir (nobfkv, engcrk, etc., generally: SLANGTLANG)
  <xsl:param name="outDir" select="concat($slang, $tlang)"/>

These directories that contain the bilingual reverted Oahpa lexicons should be copied under the directory ped/TLANG (parent directory of language material for TLANG-oahpa, e.g. ped/fkv for fkv-oahpa). 


