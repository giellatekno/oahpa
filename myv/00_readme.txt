readme for myv

1. src data coverage tests
 - 3 entries in NProp lack translations completely
 
src>g '<l ' *|cut -d ':' -f1|t
   6 NProp_myv2X.xml

   src>g '<tg xml:lang="eng">' *|cut -d ':' -f1|t
   3 NProp_myv2X.xml

   src>g '<tg xml:lang="fin">' *|cut -d ':' -f1|t
   3 NProp_myv2X.xml

   src>g '<tg xml:lang="nob">' *|cut -d ':' -f1|t
   3 NProp_myv2X.xml

   src>g '<tg xml:lang="rus">' *|cut -d ':' -f1|t
   3 NProp_myv2X.xml

   src>g '<tg xml:lang="sme">' *|cut -d ':' -f1|t
   3 NProp_myv2X.xml

2. 4 sme-translations are just faked fin

src>g '<t ' *|g '_S'
N_myv2X.xml:            <t pos="N" stat="pref">metsävahti_SME</t>
N_myv2X.xml:            <t pos="N" stat="pref">mehiläistarha_SME</t>
N_myv2X.xml:            <t pos="N" stat="pref">kotikalja_SME</t>
N_myv2X.xml:            <t pos="N" stat="pref">rahka_SME</t>

3. <source>-element is floating ad libitum:

A_:
   <e>
      <lg>
         <l pos="A">алкине</l>
         <sources>
            <book name="K1"/>
         </sources>
      </lg>
      <mg>

NProp_:
   <e>
      <lg>
         <l gen_only="Sg" pos="N" type="Prop">Ботужвеле</l>
      </lg>
      <sources>
         <book name="K1"/>
      </sources>

N_:
   <e>
      <lg>
         <l pos="N">ава</l>
         <sources>
            <book name="K1"/>
         </sources>
      </lg>

V_:
  <e>
    <lg>
      <l pos="V">лакавтомс</l>

      <sources>
        <book name="K2"/>
      </sources>
    </lg>
  ==> todo for @cip via script!

4. sem classes prefixed with 'm' are for Morpha
   ==> hence useless at this moment!

src>g -h '<sem ' *|t
  15         <sem class="HUMAN_V"/>
  15             <sem class="FOOD_GROCERY"/>
   9         <sem class="mACTIVITY"/>
   9             <sem class="FOOD_DISH"/>
   8             <sem class="FOOD_A"/>
   7             <sem class="PLACE"/>
   7             <sem class="PEOPLE"/>
   7             <sem class="FAMILY"/>
   6             <sem class="DRINK"/>
   5         <sem class="FOODDRINK_V"/>
   5             <sem class="HUMAN_A"/>
   3         <sem class="MOVEMENT_V"/>
   3             <sem class="SETTLEMENT"/>
   3             <sem class="FOOD_GROCERY_PL"/>
   2             <sem class="mPERSNAME"/>
   1             <sem class="mMAL"/>
   1             <sem class="mFEM"/>
   1             <sem class="BIRD"/> 

5. sem classes in the src files should be adjusted to the
   classes as defined in the meta/semanticsets.xml
<lexicon>
  <subclasses class="HUMAN">  
    <sem class="PEOPLE"/>   
    <sem class="MYTH_BEING"/>   
    <sem class="FAMILY"/>
    <sem class="HUMAN_A"/>
    <sem class="HUMAN_V"/>
    <sem class="PLACE"/>
  </subclasses>
  <subclasses class="FOOD/DRINK">  
    <sem class="DRINK"/>
    <sem class="FOODDRINK_V"/>
    <sem class="FOOD_A"/>
    <sem class="FOOD_DISH"/>
    <sem class="FOOD_GROCERY"/>
  </subclasses>
