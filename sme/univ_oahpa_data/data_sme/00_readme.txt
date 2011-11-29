This is a documentation about
the work on the source files for all languages.

1. adding dummy finsk-ord_ENG for the empty t-elements


sme>grep '<tg xml:lang="nob"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="fin"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="swe"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="eng"' *.xml | wc -l 
    2926
sme>grep '<tg xml:lang="deu"' *.xml | wc -l 
    2926
 ==> tg for all languages


sme>grep '<tg xml:lang="nob"/>' *.xml | wc -l 
       0
sme>grep '<tg xml:lang="fin"/>' *.xml | wc -l 
      41
sme>grep '<tg xml:lang="swe"/>' *.xml | wc -l 
      41
 ==> only in num (there is not translation needed apparently)

sme>grep '<tg xml:lang="eng"/>' *.xml | wc -l 
     255
sme>grep '<tg xml:lang="deu"/>' *.xml | wc -l 
     256
 ==> todo


