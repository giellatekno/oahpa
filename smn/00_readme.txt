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

2. revert data to finsmn
 ==> partly done, the problem is the stat="pref" flag.

Cip2Trond: If there are more than one t-element in the tg-element
           can I take the first one as pref?
           
TT: Yes.           
 ==> DONE!
