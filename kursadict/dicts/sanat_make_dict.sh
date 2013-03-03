# Script complains if directory has lexc files in it, so copy
echo "Compiling olo-fin.all.xml"
mkdir `pwd`/olo
cp $GTHOME/langs/olo/src/morphology/stems/*.xml `pwd`/olo/
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=`pwd`/olo/ > olo-fin.all.xml
rm -rf `pwd`/olo


echo "Done"
