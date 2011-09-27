This file contains the current work with filtering and freezing of
smanob files stemming from the dict directory.
It is aimed to ease the communication between Cip, Lene and Trond, the reason
is that the 00_readme.txt file was meant for the steady filtering and reverting files.

Reverting smaswe to swesma

VIC - Very Important Check before any reverting to swesma:
 - check the language flag in all files systematically (cip)



1. Cip supposes that Ryan, Lene & Co don't need all attributes
from sma-lemma into sma-translation (ignore stat="pref" for now).
E.g.

<l gen_only="A+Attr" pos="a" stem="2syll">suejies</l>
vs.
<t pos="a">suejies</t>

2. Cip's reverting script copies the <re>-elements into the tg-element of the reverted file.
   Trond means that re-info is not needed at all in smaoahpa. It is true that apparently there
   is no re-element in the nobsma-files but there is some re-information in the l-element.

nobsma>grep '(om ' * | wc -l 
      42
v_nobsma.xml:         <l pos="v">reise seg (om hår)</l>
v_nobsma.xml:         <l pos="v">reke uten lov (om barn)</l>
v_nobsma.xml:         <l pos="v">slippe lett (om bark)</l>

Question: What to do with that? Shall I add the re automatically to the l-element in brackets?

3. weird IDs:

n_swesma.xml:   <e id="renoxe under första året efter kastrering, om den tappar hornen_n"
n_swesma.xml:   <e id="träd där man fästat skavjärn på för att dra skinn genom för mjukgörning_phrase_n"
prop_swesma.xml:   <e id="Renbetesdistrikt i området Nærøy, Leka, Namsskogan, Bindal, Brønnøy, Grane_phrase_prop"

Question to Ryan: Do you have problems with the db feeding? Is the id field big enough to store that?
Is that needed at all?

4. status of te-elements in the smanob (nobsma?) files:

statuset av te-elementen dem. Hva er det, hvordan brukes i smaoahpa,
hva er med innmating av databasen med dem og presentasjon i grensesnitten?

   
sma>grep '<te' * | wc -l
    262

Noe ar med tcomm, noe uten, noe er med pos, noe uten...

for eksempel:
v_smanob.xml:            <te dict="yes" oa="yes" tcomm="no">kastrere ved å bite over testiklene med tennene</te>
v_smanob.xml:            <te dict="yes" oa="yes" tcomm="no">kastrera med att bita över testiklarna med tänderna</te>
v_smanob.xml:            <te dict="yes" oa="yes" pos="phrase_v">disse når man går på myr</te>
v_smanob.xml:            <te dict="yes" oa="yes" pos="phrase_v"> når man går på t ex myr</te>
v_smanob.xml:            <te dict="yes" oa="yes">grynte når simla og kalven kaller på hverandre</te>
v_smanob.xml:            <te dict="yes" oa="yes">f.eks mat eller drikke</te>
v_smanob.xml:            <te dict="yes" oa="yes">kappe einer eller ris</te>
v_smanob.xml:            <te dict="yes" oa="yes">spile f.eks skinn, kjøtt, fisk til tørking</te>
v_smanob.xml:            <te dict="yes" oa="yes">trekkes ut og opp</te>
v_smanob.xml:            <te dict="yes" oa="yes">komme å gjøre noe</te>
v_smanob.xml:            <te dict="yes" oa="yes">be til Gud</te>
v_smanob.xml:            <te dict="yes" oa="yes">barke med kniv</te>
v_smanob.xml:            <te dict="yes" oa="yes">plukke bær</te>
v_smanob.xml:            <te dict="yes" oa="yes">putte noe et steds hen</te>
v_smanob.xml:            <te dict="yes" oa="yes">sette på gryte til koking</te>
v_smanob.xml:            <te dict="yes" oa="yes">bustes spesielt på hund når den blir sint</te>
v_smanob.xml:            <te dict="yes" oa="yes">brekke flere ting</te>
v_smanob.xml:            <te dict="yes" oa="yes">være noe eller noensteds</te>
v_smanob.xml:            <te dict="yes" oa="yes">synke i noe</te>






==========================================
Additional comments to Lene's idea of assigning sma pos multiword to the nob
entries after reverting:
==========================================

<quote>
Hei!

Jeg husker ikke om vi har snakka om det tidligere, men: multiword skal
fremdeles være multiword etter snuinga. Dvs at pos-informasjonen ikke
skal ha noen funskjon i snuingsprosessen. Selv om nob-oversettelsen
består av ett ord, skal det tilhører multiword-fila. Multiword viser
til at sma er multiword.

- Lene
</quote>


1. this information is anyhow in the data, namely with the sma entrie
(which becomes now a translation of the nob entry)

2. after reverting you have also dupicates stemming from different
smanob files in the nob data; these have to be merged in order not to
get some messy stuff with the database

3. technically, it is possible to have the former multiword entries in
the same file DESPITE the fact that the nob entries don't carry with
them the pos "multiword": the entries can be traced basen on the pos
of the sma "translations" (see 1. item above)





