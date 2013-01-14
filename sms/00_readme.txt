This directory contains material relevant to Oahpa!-nuõrti. The  dictionary database (in /src) is imported from a "common" dictionary database called (~/sms2X).

Documentation for smsoahpa at http://victorio.uit.no/cgi-bin/wiki/index.php/Smsoahpa (to be written)

=====
State of the art:

Currently, our preliminary version of Oahpa!-nuõrti includes one "book", which is actually not a schoolbook, but just a list of basic vocabulary:
* book="100" (~100 words)
Tagging of semantic fields for these words is also only preliminary.

=====
Current plans:

The next version of Oahpa!-nuõrti, currently in the works, will include all entries tagged with:
* book="200" (~200 words)
This is still only a list of basic vocabulary, but it will already be useful for teaching beginners. Tagging of semantic fields for these words will also be improved.

=====
Future plans:

The planned next version of Oahpa!-nuõrti (to be compiled in intermediate steps) will include all entries tagged with:
* book="kurss" (schoolbook in Finnish, Russian and Norwegian versions, see the Norwegian version here: http://omnibus.uni-freiburg.de/~mr5496/downl/Kurss_nob.pdf)
* book="termm" - different term(inological) lists, which are not completely included in the textbook or the basic vocabulary lists.

=====
Micha (old note):

1. Overwrite (delete) the current Oahpa!-nuōrti (which was only a preliminary version of book="100").

2. For LEKSA use only entries tagged as <book name="200"> (for which <book name="100"> is a subset), but exclude <mg>s of entries tagged as <mg oahpa="excl">.

3. For the Placename game in LEKSA use entries tagged as <l pos="pn" class="place"> (if not <mg oahpa="excl">).

4. Three book names: "all", "100", "200".

5. Semantic sets for the new version:
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
For now we use only these supersets. Two sets (LANG "Språk" and CLOTH "Klær") are still excluded because we have not enough entries yet.

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

src>comm -12 new_sms-db.txt old_sms-db.txt | wc -l
      51
src>comm -23 new_sms-db.txt old_sms-db.txt | wc -l
     218
src>comm -13 new_sms-db.txt old_sms-db.txt | wc -l
      47
Ergo: There are 47 entries in the old db that are not covered by the new one.
    ==> merging the two dbs.

=====



