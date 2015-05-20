
 - script to generate statistics for LANG/src/morphology/stems/*.xml

 - command:
java -Xmx8400m -Dfile.encoding=UTF8 net.sf.saxon.Transform -it:main generate_stats.xsl

 - parameters (defined either at command line or in the script):


  <xsl:param name="homeDir" select="'/ABS/PATH/TO/YOUR/HOME/DIR'"/>
  <xsl:param name="outFile" select="'lang_stats'"/>


