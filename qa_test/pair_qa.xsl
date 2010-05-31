<?xml version="1.0"?>
<!--+
    | 
    | The parameter: the path to the collection of XML-files to check
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inputDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:strip-space elements="*"/>

  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <xsl:output method="text" name="txt"
	      encoding="UTF-8"
	      omit-xml-declaration="yes"
	      indent="no"/>


  <!-- Input files -->
  <xsl:param name="inFile" select="'default.xml'"/>
  <xsl:param name="inputDir" select="'default'"/>
  <xsl:variable name="outputDir" select="'check_out'"/>
  <xsl:variable name="dt" select="'.'"/>
  <xsl:variable name="qm" select="'?'"/>

  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'txt'"/>
  <xsl:variable name="e" select="$output_format"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.xml')"/>

  <xsl:template match="/" name="main">

    <xsl:choose>
      <xsl:when test="doc-available($inFile)">
	<xsl:variable name="out_tmp">
	  <xsl:for-each select="doc($inFile)/q_tests/test/a">
	    <xsl:value-of select="concat(../q, ' ^sahka ', ., '&#xa;')"/>
	  </xsl:for-each>
	</xsl:variable>
	
	<!-- out -->
	<xsl:result-document href="{$outputDir}/gogo_{$file_name}.{$e}" format="{$output_format}">
	  <xsl:copy-of select="$out_tmp"/>
	</xsl:result-document>
	
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate: </xsl:text><xsl:value-of select="$inFile"/><xsl:text>&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  

  <xsl:template name="substring-after-last">
    <xsl:param name="input" />
    <xsl:param name="marker" />
    
    <xsl:choose>
      <xsl:when test="contains($input,$marker)">
	<xsl:call-template name="substring-after-last">
	  <xsl:with-param name="input" 
			  select="substring-after($input,$marker)" />
	  <xsl:with-param name="marker" select="$marker" />
	</xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="$input" />
      </xsl:otherwise>
    </xsl:choose>
    
  </xsl:template>
  
  
  
</xsl:stylesheet>
