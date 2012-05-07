Action points for synchronizing sjdrus with russjd, engsjd, etc.

Problem: both sjdrus and russjd have been changed.

According to Trond, all changes in russjd-files can be ignored
with exception of t-elements with spelling variants.

At the moment the synchronization is important, not the stat-pref value.
After syncing, the different values can be swapped at will.
The biggest issue is the inconsistency in the data.

Example 1: xxb-variant as stat-pref but there is only the h-variant in sjdrus
-            <t pos="a" stat="pref">чоаххьпэ</t>
-            <t pos="a">чоаһпэ</t>
+            <t pos="a" stat="pref">чоаһпэ</t>
+            <t pos="a">чоаххьпэ</t>

 ==> solution: replace 'чоаһпэ' by 'чоаххьпэ' in the sjdrus-file


Example 2: both xxb- and h-variants are in the sjdrus-file as separate entries.
Why? This seems to be the only occurence, please have a look at it and change it accordingly.

 ==> solution: unify the two entries with the correct spelling variant as lemma

-            <t pos="n" stat="pref">па̄ххьк</t>
-            <t pos="n">па̄һкь</t>
+            <t pos="n" stat="pref">па̄һкь</t>
+            <t pos="n">па̄ххьк</t>

   <e>
      <lg>
         <l pos="n">па̄ххьк</l>
      </lg>
      <sources>
         <book name="l2"/>
         <book name="Saamkilsyjjt"/>
      </sources>
      <mg>
         <semantics>
            <sem class="PLACE_NATURE"/>
            <sem class="TRAVEL"/>
         </semantics>
         <tg xml:lang="rus">
            <t stat="pref">гора без растительности</t>
            <t>гора в тундре</t>
            <t>гора крутая</t>
         </tg>
         <tg xml:lang="eng">
            <t stat="pref">mountain in the tundra</t>
         </tg>

   <e id="па̄һкь">
      <lg>
         <l pos="n">па̄һкь</l>
      </lg>
      <sources>
         <book name="l2"/>
      </sources>
      <mg>
         <semantics>
            <sem class="NATURE"/>
         </semantics>
         <tg xml:lang="rus">
            <t stat="pref">гора</t>
         </tg>
         <tg xml:lang="eng">
            <t stat="pref">mountain</t>
         </tg>




