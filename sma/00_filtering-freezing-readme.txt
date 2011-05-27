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
names.xml   ==> no reverting needed; synchronized with the file in pedversions/.../meta/names.xml         
num_smanob.xml       
pronPers_smanob.xml  
propPl_smanob.xml
prop_smanob.xml
v_smanob.xml

These files are the input files for the filtering operation. Anybody can work with them.
They will be replaced by the filtered ones when testing is done (working on it now).

1.b. in pedversions/smaoahpa/data_sma/sma:
These are the filtered files that are now being tested (not yet checked in, comparing with previous versions)

2. Xsma 
2.a. in gtsvn/ped/sma/src:
At the moment, there is no such file in there, because these have to be reverted from the filtered ones.



2.b. in pedversions/smaoahpa/data_sma/X:
Still woring on them, first testing of filtered data.


File synchronization until we will have only ONE place to work with them (i.e., also for Ryan!):
1. file to be reverted for Xsma:

 person in charge of that: Ciprian

2. non-revertable file:

 person in charge of that: Lene




