<?xml version="1.0"?>
<!--+
    | 
    | File to translate smeX to Xsme
    | Usage: see next line.
    +-->

<!-- java -Xmx2048m net.sf.saxon.Transform -it main langs2langt.xsl inFile= -->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs local">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  
  <!-- Input files -->
  <xsl:param name="inFile" select="'default.xml'"/>

  <!-- Output dir, files -->
  <xsl:variable name="outputDir" select="'outDir'"/>
  <!-- use only the first translation -->
  <xsl:variable name="modus" select="'only_one'"/>
  <xsl:param name="srcl" select="'sme'"/>
  <xsl:param name="trgl" select="'nob'"/>
  
  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'xml'"/>
  <xsl:variable name="e" select="$output_format"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.xml')"/>
  
  
  
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
	      <xsl:if test="$modus = 'only_one'">
		<xsl:variable name="trgl_lemma" select="normalize-space(./translations/tr[./@xml:lang = $trgl][1])"/>
		<entry>
		  <xsl:if test="not($trgl_lemma = '')">
		    <xsl:attribute name="id">
		      <xsl:value-of select="$trgl_lemma"/>
		    </xsl:attribute>
		    <lemma>
		      <xsl:value-of select="$trgl_lemma"/>
		    </lemma>
		  </xsl:if>
		  <!-- be prepared for all -->
		  <xsl:if test="$trgl_lemma = ''">
		    <xsl:attribute name="id">
		      <xsl:value-of select="'xxx'"/>
		    </xsl:attribute>
		    <lemma>
		      <xsl:value-of select="'xxx'"/>
		    </lemma>
		  </xsl:if>
		  <pos>
		    <xsl:attribute name="class">
		      <xsl:value-of select="./pos/@class"/>
		    </xsl:attribute>
		  </pos>
		  <translations>
		    <tr>
		      <xsl:attribute name="xml:lang">
			<xsl:value-of select="$srcl"/>
		      </xsl:attribute>
		      <xsl:value-of select="normalize-space(./lemma)"/>
		    </tr>
		  </translations>
		  <xsl:copy-of select="./semantics"/>
		  <xsl:copy-of select="./sources"/>
		</entry>
	      </xsl:if>
	      <xsl:if test="$modus = 'all'">
		<xsl:for-each select="./translations/tr[./@xml:lang = $trgl]">
		  <entry>
		    <xsl:attribute name="id">
		      <xsl:value-of select="normalize-space(.)"/>
		    </xsl:attribute>
		    <lemma>
		      <xsl:value-of select="normalize-space(.)"/>
		    </lemma>
		    <pos>
		      <xsl:attribute name="class">
			<xsl:value-of select="../../pos/@class"/>
		      </xsl:attribute>
		    </pos>
		    <translations>
		      <tr>
			<xsl:attribute name="xml:lang">
			  <xsl:value-of select="$srcl"/>
			</xsl:attribute>
			<xsl:value-of select="normalize-space(../../lemma)"/>
		      </tr>
		    </translations>
		    <xsl:copy-of select="../../semantics"/>
		    <xsl:copy-of select="../../sources"/>
		  </entry>
		</xsl:for-each>
	      </xsl:if>
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


