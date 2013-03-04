# Script complains if directory has lexc files in it, so copy
echo "Compiling olo-fin.all.xml"
mkdir olo
cp $GTHOME/langs/olo/src/morphology/stems/*.xml `pwd`/olo/
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=`pwd`/olo/ > olo-fin.all.xml
rm -rf olo

echo "Compiling liv-fin.all.xml"
mkdir liv
cp $GTHOME/langs/liv/src/morphology/stems/*.xml `pwd`/liv/
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=`pwd`/liv/ > liv-fin.all.xml
rm -rf liv

echo "Compiling kpv-nob.all.xml"
mkdir kpv
cp $GTHOME/langs/kpv/src/morphology/stems/*.xml `pwd`/kpv/
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=`pwd`/kpv/ > kpv-nob.all.xml
rm -rf kpv

echo "Done"
