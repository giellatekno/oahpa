Goal: smnoahpa

1. check data
  - what is the distribution of semantic classes? 
grep -h '<sem ' *.xml | sort | uniq -c | sort -nr > sem_class_distribution.txt

Cip's observation: very many small groups, a lot of singletons
 ==> check them, Trond!
 - is there any meta-data/semantical_classes.xml file?

2. revert data to finsmn
 ==> partly done, the problem is the stat="pref" flag.

Cip2Trond: If there are more than one t-element in the tg-element
           can I take the first one as pref?

