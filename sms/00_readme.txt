This directory contains material relevant to Oahpa!-nuõrti (smsoahpa). The lexical data is taken from a dictionary database called sms2X in ~/words/dicts.

Documentation for smsoahpa at http://victorio.uit.no/cgi-bin/wiki/index.php/Smsoahpa (to be written)

=====
State of the art:

Currently, our preliminary version of Oahpa!-nuõrti includes two "books", which are actually not schoolbooks, but just lists of basic vocabulary:
* book="100" (~100 words)
* book="200" (~200 words)

Bugs in current smsoahpa:
*Select the language pair: "Skolt Sámi to Finnish" occurs twice, but "Skolt Sámi to English" is missing

Possible improvement in smsoahpa userinterface:
*html-based input tool for special Skolt Saami letters, like http://victorio-old.uit.no/webdict/index_sms-nob.html

=====
The current compilation shall include the following part-lexica:
*a_sms2X
*cc_sms2X
*cs_sms2X
*det_sms2X
*i_sms2X
*prop_sms2X

*der/der_adv_sms2X

*inf/inf_det_sms2X
*inf/inf_adv_sms2X

(the other xml source files are almost ready)

The current version to be compiled should include all entries tagged with:
<usage oahpa="yes"/>

These include:
* book="kurss" (schoolbook in Finnish, Russian and Norwegian versions, see the Norwegian version here: http://omnibus.uni-freiburg.de/~mr5496/downl/Kurss_nob.pdf)
* book="200" (~200 words)
* book="100" (~100 words)
(a third book=lookkamkerjj is not ready for oahpa yet and should be ignored for now)

Also a "place name game" could perhaps be included in LEKSA (from src dictionary files: prop_sms2X.xml with the tag type="place")

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
For now we use only these supersets. Two sets (LANG "Språk" and CLOTH "Klær") are still excluded because we do not have enough entries there yet.

Menue for book names:
1. "all"
2. "Kurss"
3. "200"
4. "100"

=====
Future compilations (noch nicht zuende gedacht:): 
*"termm" - different term(inological) lists, which are not completely included in the textbook or the basic vocabulary lists.

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

 ==> re-build the smsoahpa db on victorio

=====
Micha (old note):

1. Overwrite (delete) the current Oahpa!-nuōrti (which was only a preliminary version of book="100").

2. For LEKSA use only entries tagged as <book name="200"> in sms2X (for which <book name="100"> is a subset), but exclude <mg>s of entries tagged as <mg oahpa="excl">.

3. For the Placename game in LEKSA use entries tagged as <l pos="pn" class="place"> (if not <mg oahpa="excl">).

6. dis/preferred variants in <l> and <t>
* in <l> I mark only dispreferred variants (oahpa="dispref"), i.e. a translation variant which is accepted as answer in the reversed x-sms LEKSA game without being shown as the right answer
* in <t> I mark only the preferred variant (oahpa="pref"), i.e. a translation variant which is always shown as the right answer in the sms-x LEKSA game
* oahpa="excl" in <t> marks variants which are excluded from the LEKSA game

A few more conventions:
* Accepted but not recommended entries are
** dialectal variants of sms lemmata (like <lv variant="dial" source="1991">kueˊhtt</lv>)
** diminutive and attributive derivations of sms-lemmata (like _piânˈnǥaž_ tagged as <der gloss="dim">piânˈnǥaž</der> or _jorbb_ tagged as <der gloss="attr">jorbb</der>)
** inflected forms of translations (like _длинен_ tagged as <t pos="a:attr" pred="длинен">длинный</t> or _tørt, tørre_ tagged as <t pos="a:utr" n="tørt" pl="tørre">tørr</t>)

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



