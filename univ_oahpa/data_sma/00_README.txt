This directory contains linguistic and meta-linguistic data
to feed the DB with.
 - meta: sets and super-sets used in the smaoahpa
 - sma: all entries from the smanob dict that are marked with application=oahpa
 - nob: all entries from the sma directory (i.e., the entries from smanob dict filtered by
        the application flag) reverted accordingly.
Now, the nobsma has been generated. Not yet merged! There might be some problems with the scopus
of books when merging.

=================================
Status of freezing file:

 - documentation about this issue is here 

      gtsvn/ped/sma/00_filtering-freezing-readme.txt

The (not that good) old way we generated smaoahpa source files out of
smanob dictionary files (outdatet):

=================================
Previous procedure -- filtering and reverting the smaoahpa data out of the smanob dictionary files:

NB: Don't use the dict/sma/src data for oahpa directly, use rather the filtering
    script get_sma-data.xsl. As a matter of fact, this was the idea in Cip's dream:
    you have all in a place but for each application, you extract the data you need.

The usual cycle:
1. filter data for sma-oahpa from the smanob dict
   get_sma-data.xsl
 -> result files generated in sma dir

2. revert smaxxx to xxxsma
   revert_sma-data.xsl
 -> result files in some tmp dir (reverted2xxx)

3. redistribute the reverted files by pos (some pos values might be different as the file name generated)
   pos-split_reverted-data.xsl  
 -> result files in some tmp dir (pos_redistr_xxx)

4. in pos_redistr_xxx: merge collect POS and phrase_POS in one file POS_xxxsma.xml

5. merge the possible doublings
   merge_pos-split-data.xsl inFile=pos_redistr_xxx/a_xxxsma.xml
 -> result files in to_filter_xxx dir

6. filter away the entries without stat="pref"
   stat-filter_merged-data.xsl
 -> result files in xxx dir

7. re-create the smaoahpa db on victorio:

