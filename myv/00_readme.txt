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

 
