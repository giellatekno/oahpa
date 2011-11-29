This is a documentation about
the work on the source files for all languages.

1. adding dummy finsk-ord_ENG for the empty t-elements

Some tests reveal that even fin is not totally covered!

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
sme>grep '<tg xml:lang="nob"/>' *.xml | wc -l 
       0
sme>grep '<tg xml:lang="fin"/>' *.xml | wc -l 
      41
sme>grep '<tg xml:lang="swe"/>' *.xml | wc -l 
      46
sme>grep '<tg xml:lang="eng"/>' *.xml | wc -l 
     255
sme>grep '<tg xml:lang="deu"/>' *.xml | wc -l 
     256



