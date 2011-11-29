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


3. empty swe t-elements: to be transferred from the nob pendants
 ==> todo

sme>grep '<t stat="pref"/>' *xml | sort | uniq -c | sort -nr 
 251 prop_smenob.xml:            <t stat="pref"/>
  67 multiword_smenob.xml:            <t stat="pref"/>

4. check the consistency of propernouns pos assignment:
 - pos="prop" vs. pos="n" type="prop"
 - at the moment, just overtaken strukture from the sme lemmata

