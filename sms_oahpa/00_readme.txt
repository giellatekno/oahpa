Directory for the sms_oahpa with new code (like sma_oahpa and univ_oahpa).

The planned next version of smsoahpa should include all entries tagged with
* book="200" - basic semantic meanings (~100 items)
* book="100" - basic semantic meanings (~200 items)

The planned overnext version of smsoahpa will include all entries tagged with
* book="kurss" - a textbook in Finnish, currently being translated into Russian and Norwegian
* book="termm" - different term(inological) lists, which are not completely included in the textbook or the basic vacobulary lists.

Perhaps we also need intermediate steps for compiling the overnext smsoahpas.

=====
TODO
=====
Compiling the current database (sms_common.xml) into Oahpa!-nuõrti

0. First split sms_common.xml according to different pos. Ciprian, what do you think?

===========
cip: starting now...

note_01: ambiguous format

        <e meta="03">
                <lg>
                        <l pos="pcle">-i</l>
                </lg>
                <sources>
                        <book name="kurss" lesson="1"/>
                </sources>
                <mg>
                        <semantics>
                                <sem class="xxx"/>
                        </semantics>
                        <tg xml:lang="rus">
                                <t pos="pcle">ведь</t>
                        </tg>
                        <tg xml:lang="rus">
                                <t pos="pcle">же</t>
                        </tg>
                        <tg xml:lang="fin">
                                <t pos="pcle">-pa</t>
                                <t pos="pcle">-pä</t>
                        </tg>
                        <tg xml:lang="fin">
                                <t pos="pcle">-han</t>
                                <t pos="pcle">-hän</t>
                        </tg>

 todo: 
     either you put 
        (a) all the t-elements under a single tg-element
        (b) split the meaning group into two (or how many you need)
        (c) split the entrie into two (or how many you need)

As far as I remember, I the dict-format we have one dict-entry with several
meaning groups, while in the Ohapa-dicts we have as many entries as meaning groups.

=========

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


