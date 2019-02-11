<?xml version="1.0"?>
<!--+
    | 
    | compares (ped vs. smenob) and put ped-flags on smenob-entries 
    | Usage: java net.sf.saxon.Transform -it main cfSmeSmj.xsl
    +-->

<!-- java -Xmx2048m net.sf.saxon.Transform -it main langs2langt.xsl inFile= -->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs local">

  <xsl:strip-space elements="*"/>

<!--   <xsl:output method="xml" name="xml" -->
<!--               encoding="UTF-8" -->
<!-- 	      omit-xml-declaration="no" -->
<!-- 	      indent="yes"/> -->

  <xsl:output method="text" name="txt"
              encoding="UTF-8"
	      omit-xml-declaration="yes"
	      indent="no"/>

  
  <!-- Input files -->
  <xsl:param name="inFile" select="'default.xml'"/>

  <!-- Output dir, files -->
  <xsl:variable name="outputDir" select="'yyy_outDir'"/>
  <!-- use only the first translation -->
<xsl:variable name="modus" select="'only_one'"/>
  <xsl:param name="srcl" select="'sme'"/>
  <xsl:param name="trgl" select="'fin'"/>
  
  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'txt'"/>
  <xsl:variable name="e" select="$output_format"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.xml')"/>
  <xsl:variable name="targets" select="'__nob__fin__swe__'"/>
  
  
  <xsl:template match="/" name="main">
    <xsl:choose>
      <xsl:when test="doc-available($inFile)">
	<xsl:variable name="out_tmp">
	  <lexicon>
	    <xsl:attribute name="xml:lang">
	      <xsl:value-of select="$trgl"/>
	    </xsl:attribute>
	    <!-- to generalize -->
	    <xsl:for-each select="doc($inFile)/lexicon/entry">
	      <xsl:value-of select="./lemma"/>
	      <xsl:value-of select="' --- '"/>

	      <xsl:for-each-group select="./translations/tr" group-by="./@xml:lang">
		<xsl:if test="(current-grouping-key() = 'nob') or (current-grouping-key() = 'fin') or (current-grouping-key() = 'swe')">
		  <xsl:value-of select="concat(' ' , current-grouping-key(), ': ')"/>
		  <xsl:for-each select="current-group()">
		    <xsl:value-of select="."/>
		    <xsl:if test="not(position() = last())">
		      <xsl:value-of select="' # '"/>
		    </xsl:if>
		  </xsl:for-each>
		  <xsl:if test="not(position() = last())">
		    <xsl:value-of select="' | '"/>
		  </xsl:if>
		</xsl:if>
	      </xsl:for-each-group>
	      <xsl:value-of select="'&#xa;'"/>
	    </xsl:for-each>
	  </lexicon>
	</xsl:variable>
	
	

	<!-- out -->
	<xsl:result-document href="{$outputDir}/{$file_name}.{$e}" format="{$output_format}">
	  <xsl:copy-of select="$out_tmp"/>
	</xsl:result-document>

      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate: </xsl:text><xsl:value-of select="$inFile"/><xsl:text>&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>


