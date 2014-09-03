<?xml version="1.0"?>
<!--+
    | Task: redistribute dictionary entries by pos after a dictionary conversion
    | The parameter: the path to the collection of XML-files to compile
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main (_sax) NAME_OF_THIS_SCRIPT inDir=DIR
    +-->
<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		exclude-result-prefixes="xsl xs xhtml">
  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:param name="inDir" select="concat('_reverted2', $slang)"/>
  <xsl:param name="outDir" select="concat('pos_redistr_', $slang)"/>
  <xsl:param name="slang" select="'eng'"/>
  <xsl:param name="tlang" select="'crk'"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  <xsl:template match="/" name="main">
    
    <xsl:for-each-group select="collection(concat($inDir, '?recurse=no;select=*.xml;on-error=warning'))//e" group-by="./lg/l/@pos">
      
      <!--     <xsl:for-each-group select="collection(concat($inDir, '?recurse=no;select=*.xml;on-error=warning'))//e"  -->
      <!-- 			group-by="substring(./lg/l/@pos, string-length(./lg/l/@pos))"> -->
      
      <xsl:if test="$debug">
	<xsl:message terminate="no">
	  <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
	  <xsl:value-of select="concat('processing pos ', current-grouping-key(), $nl)"/>
	  <xsl:value-of select="'-----------------------------------------'"/>
	</xsl:message>
      </xsl:if>
      
      <xsl:result-document href="./{$outDir}/{current-grouping-key()}_{$slang}{$tlang}.{$e}" format="{$of}">
	<r xml:lang="{$slang}">
	  <xsl:copy-of copy-namespaces="no" select="current-group()"/>
	</r>
      </xsl:result-document>
    </xsl:for-each-group>
    
  </xsl:template>
</xsl:stylesheet>
  
