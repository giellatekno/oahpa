<?xml version="1.0"?>
<!--+
    | 
    | compares two lists of words and outputs both the intersection set
    | and the set of items which are in the first but not in the second set
    | NB: The user has to adjust the paths to the input files accordingly
    | Usage: java net.sf.saxon.Transform -it main THIS_FILE
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		exclude-result-prefixes="xs">

  <xsl:strip-space elements="*"/>

  <xsl:output method="text" name="txt"
	      encoding="UTF-8"
	      omit-xml-declaration="yes"
	      indent="no"/>

  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:variable name="tab" select="'&#x9;'"/>
  <xsl:variable name="spc" select="'&#x20;'"/>
  <xsl:variable name="nl" select="'&#xA;'"/>
  <xsl:variable name="cl" select="':'"/>
  <xsl:variable name="scl" select="';'"/>
  <xsl:variable name="us" select="'_'"/>
  <xsl:variable name="qm" select="'&#34;'"/>
  <xsl:variable name="cm" select="','"/>

  <xsl:param name="sl" select="'sma'"/>
  <xsl:param name="tl" select="'nob'"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>

  <!-- input file, extention of the output file -->
  <xsl:param name="inFile" select="'vasta_input.txt'"/>
  <xsl:param name="outDir" select="'out'"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.txt')"/>

  <xsl:template match="/" name="main">
    
    <xsl:choose>
      <xsl:when test="unparsed-text-available($inFile)">
	<xsl:variable name="file" select="unparsed-text($inFile)"/>
	<xsl:variable name="file_lines" select="distinct-values(tokenize($file, $nl))" as="xs:string+"/>
	<xsl:variable name="file_lines" select="tokenize($file, $nl)" as="xs:string+"/>
	<xsl:variable name="dict" as="element()">
	  <q_tests>
	    <xsl:for-each select="$file_lines">
	      <xsl:variable name="normLine" select="normalize-space(.)"/>
	      <xsl:if test="not($normLine = '')">
		<xsl:variable name="name" select="normalize-space(substring-before($normLine, $cl))"/>
		<xsl:variable name="question" select="normalize-space(substring-after($normLine, $cl))"/>
		<test name="{$name}">
		  <q>
		    <xsl:copy-of select="$question"/>
		  </q>
		  <a>
		    <xsl:copy-of select="'xxx.'"/>
		  </a>
		</test>
	      </xsl:if>
	    </xsl:for-each>
	  </q_tests>
	</xsl:variable>
	<xsl:result-document href="{$outDir}/{$file_name}.{$e}" format="{$of}">
	  <xsl:copy-of copy-namespaces="no" select="$dict"/>
	</xsl:result-document>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="concat('Cannot locate file: ', $inFile, $nl)"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>
