This directory contains material relevant to Oahpa!-nuõrti (smsoahpa). The lexical data is taken from a dictionary database called sms2X in ~/words/dicts.

Documentation for smsoahpa at http://gtweb.uit.no/cgi-bin/wiki/index.php/Smaoahpa (to be written)

=====
Notes on the CURRENT Oahpa user interface
=====
Book menue
==> includes only "all", but in the current version we have already two "books", hence:
1. "all"
2. "kurss"
3. "200"
4. "100"

Spellrelax does not work yet
 ==> to be implemented for Leksa
1. 
ˊ => richtig

´ => falsch aber muss für Leksa implementiert werden

ʹ => falsch aber muss für Leksa implementiert werden

2.
ʼ => richtig

' => falsch aber muss für leksa implementiert werden

3 ẹ ~ e

4. ˈ (kann ohne geschrieben werden)
Bsp: asdfˈoiuy => asdfoiuy
 ==> done for all X2sms

* spellrelax for Russian (ё ~ е)
   ==> done (in sms2rus)

NB: 
 - spellrelax for Oahpa is relevant ONLY for the transations because
    Leksa will never present relaxed forms!

Link to the dictionary
==> perhaps also a link to saan.oahpa.no?

Possible improvement in smsoahpa userinterface:
html-based input tool for special Skolt Saami letters, like we had earlier in the webdicts for sjd and sms


=====
Wishes for the NEXT Oahpa compilation
=====
The next compilation shall include the following part-lexica (other part-lexica in ~/src can be ignored for now):
* cmd/a_sms2X
* cmd/adp_sms2X
* cmd/adv_sms2X
* cmd/cc_sms2X
* cmd/cs_sms2X
* cmd/det_sms2X
* cmd/i_sms2X
* cmd/n_sms2X
* cmd/num_sms2X
* cmd/pcle_sms2X
* cmd/pro_sms2X
* cmd/prop_sms2X
* cmd/v_sms2X
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
* book="kurss" (~500 words) ==> 511
* book="200" (~200 words) ==> 276
* book="100" (~100 words) ==> 121

If possible, I would also like to include a "place name game" in LEKSA (from src dictionary files: prop_sms2X.xml with the tag book="prop".

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
 ==> added LANG and CLOTH to the meta-file!

=====
Preparing/Updating sms data:

The usual cycle:
0. filter only the files that are requested for oahpa and copy them
 into a TMP-DIR

1. filter relevant entries from the sms2X source files:
   sms_extract_entries4oahpa.xsl inDir=PATH/TO/THE/TMP-DIR

2. revert sms2xxx to xxx2sms
   sms_revert.xsl

3. redistribute the reverted files by pos (some pos values might be different as the file name generated)
   sms_pos-split_reverted.xsl

5. merge the possible doublings
   sms_merge_pos-split.xsl inFile=pos_redistr_xxx/a_xxxsma.xml

6. filter away the entries without stat="pref"
   sms_filter_merged.xsl inFile=.....

 ==> re-build the smsoahpa db on the server
      - todo

=================
 - spellrelax for reverted data
   ==> done
 - update db with spellrelax
   ==> done
