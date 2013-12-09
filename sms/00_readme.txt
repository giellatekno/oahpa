This directory contains material relevant to Oahpa!-nuõrti (smsoahpa). The lexical data is taken from a dictionary database called sms2X in ~/words/dicts.

Documentation for smsoahpa at http://victorio.uit.no/cgi-bin/wiki/index.php/Smsoahpa (to be written)

=====
Notes on the current Oahpa user interface
=====
Book menue
==> includes only "all", but in the current version we have already two "books", hence:
1. "all"
2. "200"
3. "100"

Spellrelex does not work yet
==>apostrophes (already inluded in spellrelax source code)
==>we also need spellrelax for Skolt Saami ẹ ~ e (the first one always to be shown, the second one to be accepted)

In Numra, the ordinals do not work yet
===> neither way works String to Numeral or Numeral to String
==> also in both cases it shows String to Numeral input

Link to the dictionary
==> perhaps also a link to saan.oahpa.no?

=====
Notes on the next Oahpa compilation
=====
The next compilation shall include the following part-lexica (other part-lexica in ~/src can be ignored for now):
* a_sms2X
* adp_sms2X
* adv_sms2X
* cc_sms2X
* cs_sms2X
* det_sms2X
* i_sms2X
* n_sms2X
* num_sms2X
* pcle_sms2X
* pro_sms2X
* prop_sms2X
* v_sms2X
* der/der_a_sms2X
* der/der_adv_sms2X
* der/der_n_sms2X
* der/der_num_sms2X
* der/der_pro_sms2X
* inf/inf_adv_sms2X
* inf/inf_det_sms2X
* inf/inf_v_sms2X
* mwe/mwe_sms2X

The current version to be compiled should include all entries tagged with:
* book="kurss" (schoolbook in Finnish, Russian and Norwegian versions, see the Norwegian version here: http://omnibus.uni-freiburg.de/~mr5496/downl/Kurss_nob.pdf)
* book="200" (~200 words)
* book="100" (~100 words)
But please exclude all words tagged with <usage oahpa="excl"/>
 ==> cip: I will turn all these tags into attributes, at the moment it is inconsistent.

src/abbr_sms2X.xml:         <xg oahpa="excl" kurss="no">
src/n_sms2X.xml:         <usage oahpa="excl"/>
src/n_sms2X.xml:         <tg xml:lang="rus" oahpa="excl">
src/prop_sms2X.xml:         <usage oahpa="no"/>
src/prop_sms2X.xml:         <usage oahpa="yes"/>

=====

Semantic sets are the same as for the last version (defined in ~/meta-data):
* HUMAN "Menneske"
* SPACE "Rom"
* BODY "Kropp"
* SENSE "Egenskap, mengd, sinne"
* HOUSE "Hus"
* WORK "Arbeid og fritid"
* TIME "Tid"
* ZOO "Djur"
* BOT "Plant"
* FOOD "Mat og drikk"
* ENVIR "Verld"
Two more sets
* LANG "Språk"
* CLOTH "Klær"
should now have enough lemmas to be included

=====
Preparing/Updating sms data:

The usual cycle:
1. filter relevant entries from the sms2X source files:
   extract_book-200-e.xsl inDir=$GTHOME/main/words/dicts/sms2X/src

2. revert sms2xxx to xxx2sms
   sms_revert.xsl

3. redistribute the reverted files by pos (some pos values might be different as the file name generated)
   sms_pos-split_reverted.xsl

5. merge the possible doublings
   sms_merge_pos-split.xsl inFile=pos_redistr_xxx/a_xxxsma.xml

6. filter away the entries without stat="pref"
   sms_filter_merged.xsl inFile=.....

 ==> re-build the smsoahpa db on the server

======
FUTURE
======
Future compilations (perhaps): 
* spellrelax for Russian (ё ~ е)

* a "place name game" could perhaps be included in LEKSA (from src dictionary files: prop_sms2X.xml with the tag type="place"/class="place" (if not <mg excluded="oahpa").
 ==> not before Inari

* Possible improvement in smsoahpa userinterface:
html-based input tool for special Skolt Saami letters, like we had earlier in the webdicts for sjd and sms
 ==> cip: not before Inari 

*"termm" - different term(inological) lists, which are not completely included in the textbook or the basic vocabulary lists.
 == not before christmas

=====
Cip (old note):
For Opahpa-update, only entries with book=200 be use:
sms2X>grep '<e ' _spittOutCorpus/*.xml | wc -l
     269

_spittOutCorpus>grep '<e ' *.xml | cut -d ':' -f1 | sort | uniq -c | sort -nr
 102 n_sms2X.xml
  76 v_sms2X.xml
  48 a_sms2X.xml
  16 adv_sms2X.xml
  13 pro_sms2X.xml
   7 con_sms2X.xml
   5 num_sms2X.xml
   1 ord_sms2X.xml
   1 adp_sms2X.xml

A further point to take into accout:

_200-book_entry>grep '<e ' *.xml | wc -l
     269
_200-book_entry>grep '<mg' *.xml | wc -l
     306

 ==> tansform mg-dict-format into mg-oahpa-format:
     i.e., one entry per mg!

=====
Cip: 

sms db update 20130114:

  43          <xg oahpa="excl" kurss="no">
  44             <x pos="n">eeˊǩǩed</x>
  45             <xtg xml:lang="rus">
  46                <xt pos="n">лет</xt>
  47             </xtg>
  48             <xtg xml:lang="fin">
  49                <xt pos="n">vuotta</xt>
  50             </xtg>
  51          </xg>

 ==> Das ist nichts!

<tg xml:lang="LANG">
  <t .../>
  <t .../>
  <t .../>
</tg>

check pos values:

>          <l pos="mwe_n">fremre lår</l>
>       </lg>
>       <sources>
>          <book name="200" BEDLAN_ID="220"/>
>       </sources>
>       <mg>
>          <semantics>
>             <sem class="BODY">PART</sem>
>          </semantics>
>          <tg xml:lang="sms">
>             <t pos="a">ruõidd</t>
>          </tg>
>       </mg>
>    </e>


check pos and l value (it seems to be a re-item):
   <l pos="a">ikke av planter</l>
   <l pos="a">av planter</l>

aha: this is not a <t> but a <tr> and what is YOUR interpretation of it?

            <tr>anything but plants</tr>
            <tr>ikke av planter</tr>

Das mag ich nicht (vgl. mit dem element semantics oder example):
         <tg xml:lang="eng">
            <t pos="adv" oahpa="pref">therefore</t>
            <te>for that reason</te>
         </tg>

rus2sms
         <l pos="con">потому что</l>
         <l pos="con">потому, что</l>

=====

To correct 20130920:
 - ordinals >>> string2numeral: put the correct fst, the current one is the same as numeral2string
   test answers in ordinals >>> numeral2string: sms-inum.fst does not exist.
   Trond: Done.
   TODO: Look at the makefile procedure that did not make it automatially
   Trond, Sjur: Done.
   
=====
 - some comments on the new sms lexical data that has to be used for oahpa:

 1. inconsistencies in structures:

    (a)
         <tg xml:lang="sju">
            <t pos="a" pred="jårˈbada">jårbs</t>
            <t pos="a">mulˈlòda</t>
         </tg>
 
    (b)
         <tg xml:lang="eng" style="obs" oahpa="excl">
            <t pos="adv">whither</t>
         </tg>
         <tg xml:lang="eng" oahpa="pref">
            <t pos="adv">where</t>
         </tg>
         <tg xml:lang="eng">
            <t pos="mwe_adv">to where</t>
         </tg>
         <tg xml:lang="fin" oahpa="pref">
            <t pos="adv">mihin</t>
         </tg>
         <tg xml:lang="fin">
            <t pos="adv">minne</t>
         </tg>

=================
 - TODO: update localisation stuff
