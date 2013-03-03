# Script complains if directory has lexc files in it, so copy
echo "Compiling kom2x.all.xml"
java -Xmx2048m -cp ~/lib/saxon9.jar -Dfile.encoding=UTF8 net.sf.saxon.Transform \
    -it:main $GTHOME/words/dicts/scripts/collect-dict-parts.xsl \
    inDir=$GTHOME/words/dicts/kom2X/src/ > kom2x.all.xml

echo "Done"
