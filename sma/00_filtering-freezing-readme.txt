This file contains the current work with filtering and freezing of
smanob files stemming from the dict directory.
It is aimed to ease the communication between Cip, Lene and Trond, the reason
is that the 00_readme.txt file was meant for the steady filtering and reverting files.

File locations:

1. smaX (X=nob, X=swe)
 - for the Røros team, Lene and Cip: gtsvn/ped/sma/src
 - for Cip, Lene and Ryan: pedversions/smaoahpa/data_sma/sma (this will be changed etter hvert!)

2. Xsma:
 - for the Røros team, Lene and Cip: gtsvn/ped/sma/Xsma
 - for Cip, Lene and Ryan: pedversions/smaoahpa/data_sma/X (this will be changed etter hvert!)

File status:

1. smaX 
1.a. in gtsvn/ped/sma/src:

a_smanob.xml         
adv_smanob.xml       
multiword_smanob.xml 
n_smanob.xml         
propPl_smanob.xml
prop_smanob.xml
v_smanob.xml
 ==> all the files above have been filtered and synchronized between
 pedversions/.../sma and ped/sma/src directories

names.xml   ==> no reverting needed; synchronized with the file in pedversions/.../meta/names.xml         
num_smanob.xml ==> filtered; no reverting needed; synchronized with the file in pedversions/.../meta/num_smanob.xml       
pronPers_smanob.xml  ==> no filtering now; no reverting; Lene is in charge of synchronizing it with that in pedversions/.../meta

These files are the input files for the filtering operation. Anybody can work with them.
They will be replaced by the filtered ones when testing is done (working on it now).

1.b. in pedversions/smaoahpa/data_sma/sma:
These are the filtered files that are now tested, checked in, and
synchronized with the ped/sma/src dir
    ==> done 
2. Xsma 
2.a. in gtsvn/ped/sma/src:
At the moment, there is no such file in there, because these have to be reverted from the filtered ones.
 ==> done

2.b. in pedversions/smaoahpa/data_sma/X:
 reverting from smaX to Xsma ==> done

File synchronization until we will have only ONE place to work with them (i.e., also for Ryan!):
1. file to be reverted for Xsma:
 ==> done
 person in charge of that: Ciprian

2. non-revertable file:

 person in charge of that: Lene

==========================================
Some notes for a common ground in our work:
==========================================

Default values are "xxx" (using both "XXX" and "yyy" and "YYY"
leads to unnecessary problems, both when using grep, and find and when
writing patterns during programming)

"???" are definitely NOT wished, yet unfortunately, it seems to be
some default of the XMlmind (Sjur kindly check it) 

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



==========================================
Some observations:
==========================================

In my humble opinion this is not a pron but rather an adj. Check and
   correct if needed.

   <l pos="pron">forskjellig</l>
