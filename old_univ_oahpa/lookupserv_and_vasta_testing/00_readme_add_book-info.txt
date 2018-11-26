
java -Xmx2048m net.sf.saxon.Transform -it main add_book-info.xsl inDir=outd inFile=Lemma_fra_bok4

inDir is the directory of file to which the book info is to be added.
inFile is a file containing one word per line format with the lemmata to which to add the book info.

These can  be specified in the file such that the command would be only:

java -Xmx2048m net.sf.saxon.Transform -it main add_book-info.xsl

The output directory and the book value are specified as variables in the script.
  <xsl:variable name="outDir" select="'outdx'"/>
  <xsl:variable name="theBook" select="'åa4'"/>

