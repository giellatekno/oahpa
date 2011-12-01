This is a documentation about
the work on the source files for all languages.

1. adding dummy finsk-ord_ENG for the empty t-elements

sme>grep '<tg xml:lang="nob"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="fin"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="swe"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="eng"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="deu"' *.xml | wc -l 
    2926
 ==> tg for all languages

sme>grep '<tg xml:lang="nob"/>' *.xml | wc -l 
       0
sme>grep '<tg xml:lang="fin"/>' *.xml | wc -l 
      41
sme>grep '<tg xml:lang="swe"/>' *.xml | wc -l 
      41
 ==> only in num: according to Lene, we need the translations for numerals, too

sme>grep '<tg xml:lang="eng"/>' *.xml | wc -l 
     255
sme>grep '<tg xml:lang="deu"/>' *.xml | wc -l 
     256
 ==> done

sme>grep '_DEU' *xml | wc -l 
    2223
sme>grep '_ENG' *xml | wc -l 
    1714

2. add pos to the translation: there are pos attribute in smaoahpa but not in sme
 ==> done

3. empty swe t-elements: to be transferred from the nob pendants
 ==> todo

sme>grep '<t stat="pref"/>' *xml | sort | uniq -c | sort -nr 
 251 prop_smenob.xml:            <t stat="pref"/>
  67 multiword_smenob.xml:            <t stat="pref"/>

4. check the consistency of propernouns pos assignment:
 - pos="prop" vs. pos="n" type="prop"
 - at the moment, just overtaken strukture from the sme lemmata
 ==> todo

5. another question wrt. propernouns:
   Why are there two different files with propernouns?
	n_prop_smenob.xml  
	prop_smenob.xml 

According to Lene:
 - Alle lemmaene (bortsett fra ett) i n_prop_smenob.xml finnes i prop_smenob.xml.

Ergo: only prop_smenob.xml should be reverted


<quotation>
prop_nouns.xml - stedsnavn som var i nouns.xml. Det var meninga at de skulle inngå i MorfaS, men generinga har ikke fungert pga av disse krever N+Prop. Men det kunne være lurt å ha dem med i MorfaS, som nouns. - ny fil tmp_towards-sma-format/data_sme/sme/n_prop_smenob.xml
propernouns.xml - denne skal ikke genereres - kun for Leksa, flytta til 
</quotation>

By still, nothing from above is a suitable answer to my question:
 - Why are there two different file with propernouns?

6. lexicon extension from morelemmasfromfin.csv

 6.1 csv2xml step
  ==> done

Quick Test:
extend_lexicon>wc -l morelemmasfromfin.csv
     672 morelemmasfromfin.csv
extend_lexicon>grep '<e' out/morelemmasfromfin.csv.xml | wc -l 
     672

 6.2 adding book info from words/dicts/smefin/inc
    cealkke1.csv -> c1
    cealkke2.csv -> c2
    cealkke3.csv -> c3
    cealkke4.csv -> c4
    AA.csv -> AA
  ==> done

Check these entries for correct books and translations (search for "comment"):
   2 čáihni
   2 sierra
   2 lasi
   2 duohta
   2 besset

default <book name="xxx"/> as usual!

ghandi>grep '<e' * | cut -d ':' -f1 | sort | uniq -c | sort -nr
 323 n_smenob.xml
 179 v_smenob.xml
  89 adv_smenob.xml
  67 a_smenob.xml
  14 mwe_smenob.xml


 6.3 before merging with the existing entries, check for duplicates and the like
  ==> done

NB: search for "comment"

duplicates in adv_smenob.xml:
   2 visot
   2 sierra
   2 ollu
   2 hirbmat

Duplicates in noun and verb file: todo by native speakers

 6.4 pos-based splitting of the entries and merging with the existing entries
  ==> done

