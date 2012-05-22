Goal: smnoahpa

1. check data
  - what is the distribution of semantic classes? 
grep -h '<sem ' *.xml | sort | uniq -c | sort -nr > sem_class_distribution.txt

Cip's observation: very many small groups, a lot of singletons
 ==> check them, Trond!
 - is there any meta-data/semantical_classes.xml file?
 
__TODO__:
* Make an ad-hoc collection of say 3 supersets for the 
  semantical_classes.xml file (__Trond__)
* Get the resource online (__Ciprian__) 
* Discuss with the Inari Sami (__Trond__)
* Split the ZZZ in relevant classes 

Note: Semantic class ILLNESS? Naja...
   <e id="sairaalloinen_a" stat="pref">
      <lg>
         <l pos="a">sairaalloinen</l>
      </lg>
      <sources>
         <book name="bio5"/>
      </sources>
      <mg>
         <semantics>
            <sem class="ILLNESS"/>
         </semantics>
         <tg xml:lang="smn">
            <t pos="a" stat="pref">puosâh</t>
         </tg>
      </mg>
   </e>

2. revert data to finsmn
 ==> DONE

3. debug and fix Leksa
 ==> ONGOING


4. put these entries in a separate mwe-file:

<l pos="n">kärŋilis tääsi</l>
<l pos="n">kume stielâs</l>
<l pos="n">lieggâ stielâs</l>
<l pos="n">kolmâ stielâs</l>
<l pos="n">kavrâs jorgáldâskiärdu</l>
<l pos="n">rapu jorgáldâskiärdu</l>
<l pos="n">stuorrâ syeiniaččin</l>
<l pos="n">kuuloold tábáhtuvvee hämimolsom</l>
<l pos="n">stuorrâ čäciluttihâš</l>
<l pos="n">uccâ čäciluttihâš</l>

