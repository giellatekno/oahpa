This directory contains the files relevant to the smaoahpa application.
 - src: the source files with the lexicon smaX (i.e., smanob, smaswe, smaeng)
 - Xsma: the reverted files from smaX to Xsma

Caveat: the reverted files are already frozen, i.e., 
	they are ready for extension for synonyms and the like.
	The exception thereof is the swesma dir because at the moment it is not
	worth to revert them, there a too few real translations for swe in the smaswe files.

In the following is the summary of the CLT meeting:

1. Topic: nobsme handling of MWEs and stat="pref"
	1.1 extract all sma-MWEs into a separate file;
	1.2 add ID as in smenob for possible entries that would be doubled in the sense of lemma string and pos string;
		Ex.: entry for "ungen"
	1.3 delete possible entries that got stat="pref" only based on MWEs entires;
	1.4 delete semantic sets from translations that are not relevant for the nobsma-Leksa, i.e.,
   	    put the translations that are not marked with stat="pref" in the same sematic group with
   	    the marked one even if they don't share the same semantics classification;
		Ex.: entry for "spor"

2. Topic: level simplification in the dictionary from 3 to 2 levels in the meaning groups

	1.1 structurally there are still three levels:
  	    - mg: meaning groups
	    - tg: target language group
      		  THIS is the difference, this group denotes NOT a slight difference
		  in translation wrt. some meaning shadows but it only groups 
		  transaltions similar translation based on targe language.

     Ex. from the original Cip's dream files:

  <e id="láibi">
     <l>láibi</l>
     <mg>
	<semantics>
	  <sem class="FOOD"/>
	  <sem class="FOOD/DRINK"/>
	</semantics>
	<tg xml:lang="nob">
	  <t idref="brød">brød</t>
	  <t idref="fladbrød">fladbrød</t>
	</tg>
	<tg xml:lang="fin">
	  <t idref="leipä">leipä</t>
	</tg>
	<tg xml:lang="eng">
	  <t idref="bread">bread</t>
	</tg>
     </mg>
  </e>


vs. not grouped based on target language

  <e id="láibi">
     <l>láibi</l>
     <mg>
	<semantics>
	  <sem class="FOOD"/>
	  <sem class="FOOD/DRINK"/>
	</semantics>
	<t idref="brød" xml:lang="nob">brød</t>
	<t idref="fladbrød" xml:lang="nob">fladbrød</t>
	<t idref="leipä" xml:lang="fin">leipä</t>
	<t idref="bread" xml:lang="eng">bread</t>
     </mg>
  </e>

The CLT-group voted unanimously FOR the Cip's dream solution!

Here a small note wrt. this solution: all sme mgs in the smaX files will be now
part of the mgs containing nob and swe, which is in the very spirit of Cip's dream.

================
Starting testing for level simplification (it is not that simple):
 - excluding file: names.xml propPl_smanob.xml

sma>grep -h '<mg_test' _mg_check/*.xml | sort | uniq -c | sort -nr  

(I) Assuming that each tg-nob has a pendant tg-swe or tg-sme, these are
    non-problematic cases:

3470          <mg_test stamp="tg-nob_tg-swe"/>
  200          <mg_test stamp="tg-nob_tg-swe_tg-nob_tg-swe"/>
    32          <mg_test stamp="tg-nob_tg-swe_tg-nob_tg-swe_tg-nob_tg-swe"/>
      6          <mg_test stamp="tg-nob_tg-swe_tg-nob_tg-swe_tg-nob_tg-swe_tg-nob_tg-swe"/>
      4          <mg_test stamp="tg-sme_tg-nob"/>


(II) Under the same assumption, these file are problematic for an
     automatic meaning group unification:

 178          <mg_test stamp="tg-sme"/>
     7          <mg_test stamp="tg-nob_tg-swe_tg-nob_tg-swe_tg-swe"/>
     3          <mg_test stamp="tg-swe"/>
     3          <mg_test stamp="tg-nob"/>
     1          <mg_test stamp="tg-sme_tg-nob_tg-nob"/>
     1          <mg_test stamp="tg-nob_tg-nob_tg-swe"/>


