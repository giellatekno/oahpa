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
	    - done
	1.2 add ID as in smenob for possible entries that would be doubled in the sense of lemma string and pos string;
		Ex.: entry for "ungen"
	    - done
	1.3 delete possible entries that got stat="pref" only based on MWEs entires;
	    - done
	1.4 according to the latest specifications by Lene, don't merge nob entries with stat="pref":
	    1.4.1 add the disprefered sma-translation to each created
	    	     entry with stat="pref" 
		     -done
	    1.4.2 for entries with the same nob lemma, add prefered sma-translations to each other as
   	             acceptable answers
		     -done

@cip: From my point of view is now the merging process of the reverted
         nobsma data finished.

Ex. 1 (only one entry with this lemma in the whole file)

   <e id="rovdyrfritt_a" stat="pref"> 	     <== 1. every entry has an ID	2. stat=pref flag from the smanob-data in the nob-entry 
      <lg>
         <l pos="a">rovdyrfritt</l>
      </lg>
      <sources>		<== structure simplification: no apps/apps, just sources 
         <book name="åa5"/>
      </sources>
      <mg>
         <semantics>					<== sematics element on the mg-level, NOT on the tg-level anymore
            <sem class="NATURE_A"/>
            <sem class="HERDING"/>
         </semantics>
         <tg xml:lang="sma">				<== 'tg' means 'target language group' and is flagged with the language flag
            <t pos="a" stat="pref">aales</t> 	<== because of the new meaning of 'tg' there is no need for lang-flag on the t-level;  default flag for stat="pref" that can be changed manually as needed
         </tg>
      </mg>
   </e>


Ex. 2 (several entries with the samme lemma string): Et godt eksempel for det er "dårlig"!

 1. a number in initial position of the ID means that there are more
     than one entry with the same lemma string in the file
 2. in addition to the t-element from the reverted entry, there are
     t-values of the parallel entries with the same nob lemma string
     as acceptable answers for the LEKSA play,  each of them carries
     the infos on semantic class, book, and a flag nob-stat meaning "I
     am a default t in a parallel nob entry"
     <t pos="a" sem-cl="BODY_A" src="dej-åa6-åa4-åa6" nob-stat="yes">mådtan</t>	
     as well as all t-element values that don't have a stat="pref"
     flag in the smanob files, i.e., only sem-cl and book infos.
            <t pos="a" sem-cl="EXPERIENCE_A-CLOTHES_A-WEATHER_A-BODY_A" src="s2-a1-dej"
               nob-stat="yes">nåekies</t>

   <e id="1_dårlig_a" stat="pref">
      <lg>
         <l pos="a">dårlig</l>
      </lg>
      <sources>
         <book name="s2"/>
         <book name="åa6"/>
         <book name="åa4"/>
      </sources>
      <mg>
         <semantics>
            <sem class="WEATHER_A"/>
         </semantics>
         <tg xml:lang="sma">
            <t pos="a" stat="pref">geerve</t>
            <t pos="a" sem-cl="BODY_A" src="s2" nob-stat="yes">madtan</t>
            <t pos="a" sem-cl="BODY_A" src="dej-åa6-åa4-åa6" nob-stat="yes">mådtan</t>
            <t pos="a" sem-cl="EXPERIENCE_A-CLOTHES_A-WEATHER_A-BODY_A" src="s2-a1-dej"
               nob-stat="yes">nåekies</t>
         </tg>
      </mg>
   </e>
   <e id="2_dårlig_a" stat="pref">
      <lg>
         <l pos="a">dårlig</l>
      </lg>
      <sources>
         <book name="s2"/>
      </sources>
      <mg>
         <semantics>
            <sem class="BODY_A"/>
         </semantics>
         <tg xml:lang="sma">
            <t pos="a" stat="pref">madtan</t>
            <t pos="a" sem-cl="WEATHER_A" src="s2-åa6-åa4" nob-stat="yes">geerve</t>
            <t pos="a" sem-cl="BODY_A" src="dej-åa6-åa4-åa6" nob-stat="yes">mådtan</t>
            <t pos="a" sem-cl="EXPERIENCE_A-CLOTHES_A-WEATHER_A-BODY_A" src="s2-a1-dej"
               nob-stat="yes">nåekies</t>
         </tg>
      </mg>
   </e>
   <e id="3_dårlig_a" stat="pref">
      <lg>
         <l pos="a">dårlig</l>
      </lg>
      <sources>
         <book name="s2"/>
         <book name="a1"/>
         <book name="dej"/>
      </sources>
      <mg>
         <semantics>
            <sem class="EXPERIENCE_A"/>
            <sem class="CLOTHES_A"/>
            <sem class="WEATHER_A"/>
            <sem class="BODY_A"/>
         </semantics>
         <tg xml:lang="sma">
            <t pos="a" stat="pref">nåekies</t>
            <t pos="a" sem-cl="WEATHER_A" src="s2-åa6-åa4" nob-stat="yes">geerve</t>
            <t pos="a" sem-cl="BODY_A" src="s2" nob-stat="yes">madtan</t>
            <t pos="a" sem-cl="BODY_A" src="dej-åa6-åa4-åa6" nob-stat="yes">mådtan</t>
         </tg>
      </mg>
   </e>


============
VERY IMPORTANT:
============

Due to the changed format, following places have to be adapted
accordingly:
 1. for the work with XMLmind: dtd and css file
 2. for the db feeding: Ryan's Pythons scripts 
=============================================


Observations when feature merging:

   O-1: books that come from different types of entries (pref
   	    vs. non-pref) have to be marked as such

   O-2: sma translations that stem from different types of entries (pref
   	    vs. non-pref) have to be marked as such wrt. semantics
   	    because these features will be merged


Test FØR unifisering av mg in nobsma:


data_sma>grep -h '<e counter' to_filter_nob/*.xml | sort | uniq -c | sort -nr 

a. Possible automatic processing (all entries that have only one
meaning group stemming from a nob-translation with stat="pref"):
2267    <e counter="1" p_cntr="1" dp_cntr="0" stat="pref">
 307    <e counter="2" p_cntr="1" dp_cntr="1" stat="pref">
  77    <e counter="3" p_cntr="1" dp_cntr="2" stat="pref">
  19    <e counter="4" p_cntr="1" dp_cntr="3" stat="pref">
   5    <e counter="5" p_cntr="1" dp_cntr="4" stat="pref">
   2    <e counter="7" p_cntr="1" dp_cntr="6" stat="pref">
   1    <e counter="10" p_cntr="1" dp_cntr="9" stat="pref">


b.  Difficult automatic processing (the rest):

 b.1: 

 - When to unifiy two or more mgs stemming from a nob-translation with
    stat="pref"?

 - When total overlapping of sem-classes or even for partial
    overlapping?

 - What about if their sem-classes are totally different? Shall they
   get separate entries with different IDs as with the sme-oahpa data
   or not?

186    <e counter="2" p_cntr="2" dp_cntr="0" stat="pref">
 19    <e counter="3" p_cntr="3" dp_cntr="0" stat="pref">
  4    <e counter="4" p_cntr="4" dp_cntr="0" stat="pref">
  1    <e counter="5" p_cntr="5" dp_cntr="0" stat="pref">


 b.2: same questions as in b.2 but in addition is also the question of
        which mg from the prefered ones shall get which translation
        from the disprefered ones?

 54    <e counter="3" p_cntr="2" dp_cntr="1" stat="pref">
  21    <e counter="4" p_cntr="2" dp_cntr="2" stat="pref">
 10    <e counter="4" p_cntr="3" dp_cntr="1" stat="pref">
   6    <e counter="5" p_cntr="3" dp_cntr="2" stat="pref">
   6    <e counter="5" p_cntr="2" dp_cntr="3" stat="pref">
   2    <e counter="6" p_cntr="3" dp_cntr="3" stat="pref">
   2    <e counter="6" p_cntr="2" dp_cntr="4" stat="pref">
   2    <e counter="5" p_cntr="4" dp_cntr="1" stat="pref">
   1    <e counter="8" p_cntr="6" dp_cntr="2" stat="pref">
   1    <e counter="8" p_cntr="4" dp_cntr="4" stat="pref">
   1    <e counter="7" p_cntr="4" dp_cntr="3" stat="pref">
   1    <e counter="7" p_cntr="2" dp_cntr="5" stat="pref">
   1    <e counter="6" p_cntr="4" dp_cntr="2" stat="pref">

Another question is about the interplay between the scope of semantic
classes and that of the books after reverting the smanob to nobsma.



New statistics after cleaning up the only morfa-relevant entries
marked in the semantic class with an initial "m": 

data_sma>grep -h '<e' to_filter_nob/*.xml | sort | uniq -c | sort -nr 
2198    <e counter="1" p_cntr="1" dp_cntr="0" stat="pref">
 292    <e counter="2" p_cntr="1" dp_cntr="1" stat="pref">
 186    <e counter="2" p_cntr="2" dp_cntr="0" stat="pref">
  77    <e counter="3" p_cntr="1" dp_cntr="2" stat="pref">
  53    <e counter="3" p_cntr="2" dp_cntr="1" stat="pref">
  19    <e counter="4" p_cntr="2" dp_cntr="2" stat="pref">
  19    <e counter="4" p_cntr="1" dp_cntr="3" stat="pref">
  19    <e counter="3" p_cntr="3" dp_cntr="0" stat="pref">
  10    <e counter="4" p_cntr="3" dp_cntr="1" stat="pref">
   6    <e counter="5" p_cntr="3" dp_cntr="2" stat="pref">
   5    <e counter="5" p_cntr="2" dp_cntr="3" stat="pref">
   5    <e counter="5" p_cntr="1" dp_cntr="4" stat="pref">
   4    <e counter="4" p_cntr="4" dp_cntr="0" stat="pref">
   2    <e counter="7" p_cntr="1" dp_cntr="6" stat="pref">
   2    <e counter="6" p_cntr="3" dp_cntr="3" stat="pref">
   2    <e counter="6" p_cntr="2" dp_cntr="4" stat="pref">
   2    <e counter="5" p_cntr="4" dp_cntr="1" stat="pref">
   1    <e counter="8" p_cntr="6" dp_cntr="2" stat="pref">
   1    <e counter="8" p_cntr="4" dp_cntr="4" stat="pref">
   1    <e counter="7" p_cntr="4" dp_cntr="3" stat="pref">
   1    <e counter="7" p_cntr="2" dp_cntr="5" stat="pref">
   1    <e counter="6" p_cntr="4" dp_cntr="2" stat="pref">
   1    <e counter="5" p_cntr="5" dp_cntr="0" stat="pref">
   1    <e counter="10" p_cntr="1" dp_cntr="9" stat="pref">



2. Topic: level simplification in the dictionary from 3 to 2 levels in the meaning groups

	2.1 structurally there are still three levels:
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
part of the mgs containing nob and swe, which is in the very spirit of
Cip's dream.

	2.2 tasks:
  	    2.2.1 unify meaning groups that have been separated ONLY
	       because of sme-language: this can be done ONLY if there
	       is a parallelity of sme- vs. non-sme-mgs 

	    2.2.2 split (old) tg into different groups if the
      		  semantics are different: this is possible ONLY if
      		  there are semantic groups with ANY tg in the mg

	    2.2.3 group (old) tg to the same meaning group if the
      		  semantics are he: this is possible ONLY if
      		  there are semantic groups with ANY tg in the mg
		  (see the pre-tests below)

================
Starting testing for level simplification (it is not that simple):
 - excluding file: names.xml propPl_smanob.xml

Test 1: checking the content of each e-element: 
     Question: How many mg-elements are there? Should be unified
     (because of lang feature sme) or let as they are (because thery
     represent genuinely different meanings)?

sma>grep -h '<e_test' _mg_check/* | sort | uniq -c | sort -nr 

(I) Assuming that these mg-elements denote different meanings, the
following entries are not challenging:
2083       <e_test stamp="lg_stem_apps_mg"/>
  889       <e_test stamp="lg_apps_mg"/>
  170       <e_test stamp="lg_stem_apps_mg_mg"/>
    31       <e_test stamp="lg_apps_mg_mg"/>
    30       <e_test stamp="lg_stem_apps_mg_mg_mg"/>
    28       <e_test stamp="lg_mg"/>
      5       <e_test stamp="lg_apps_mg_mg_mg"/>
      4       <e_test stamp="lg_stem_mg"/>
      3       <e_test stamp="lg_stem_apps_mg_mg_mg_mg"/>
      1       <e_test stamp="lg_mg_mg"/>
      1       <e_test stamp="lg_apps_mg_mg_mg_mg_mg"/>

(II) Assuming that there is a parallelity between non-sme and sme mgs
 AND that the non-sme mg has only ONE tg (modulo lang nob/swe) there
 is no problem with the following entries:
 166       <e_test stamp="lg_stem_apps_mg_mg-sme"/>


(III) The following entries have to be corrected manually because they
  are not symetric wrt. sme vs. non-sme mg:
   9       <e_test stamp="lg_stem_apps_mg_mg_mg-sme"/>
   3       <e_test stamp="lg_stem_apps_mg_mg_mg-sme_mg-sme"/>
   2       <e_test stamp="lg_apps_mg_mg-sme"/>



Test 2: checking the content of each mg: 

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


