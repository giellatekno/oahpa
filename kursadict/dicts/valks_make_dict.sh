# Script complains if directory has lexc files in it, so copy
echo "Compiling myv / Erzya Mordvin"
mkdir myv
cp $GTHOME/langs/myv/src/morphology/stems/*.xml `pwd`/myv/
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=`pwd`/myv/ > myv-all.xml
rm -rf myv

echo "Done"
