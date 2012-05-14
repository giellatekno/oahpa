Goal: smnoahpa

1. check data
  - what is the distribution of semantic classes? 
grep -h '<sem ' *.xml | sort | uniq -c | sort -nr > sem_class_distribution.txt

Cip's observation: very many small groups, a lot of singletons
 ==> check them, Trond!
 - is there any meta-data/semantical_classes.xml file?

2. revert data to finsmn
 ==> do it, Cip!

Usual checks:

src>grep -h '<e>' *.xml | wc -l
    1314
src>grep -h '<mg' *.xml | wc -l
    1319
src>grep -h '<tg' *.xml | wc -l
    1319
 ==> more mg-elements than entries; this shouldn't be so!
 ==> to check ==> done and corrected



