<?xml version="1.0"?>
<!--+
    | script to revert sms-oahpa lexical data from slang to tlang 
    | Usage: java net.sf.saxon.Transform -it:main THIS_SCRIPT inDir=/PATH/TO/THE/INPUT_DIR/RELATIVE/TO/THIS/SCRIPT outDir=/PATH/TO/THE/OUTPUT_DIR/RELATIVE/TO/THIS/SCRIPT
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs local xhtml">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <!-- input dir -->
  <xsl:param name="inDir" select="'src'"/>
  <!-- source language -->
  <xsl:param name="slang" select="'sms'"/>
  <!-- target language: nob is default! -->
  <xsl:param name="tlang" select="'rus'"/>
  <!-- Output dir, files -->
  <xsl:param name="outDir" select="concat('reverted2', $tlang)"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  <xsl:variable name="_L2L" select="'_sms2X'"/>      
  

  <xsl:template match="/" name="main">
    <xsl:for-each select="for $f in collection(concat($inDir,'?recurse=no;select=*.xml;on-error=warning')) return $f">
      
      <xsl:variable name="current_file" select="(tokenize(document-uri(.), '/'))[last()]"/>
      <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
      <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
      <xsl:variable name="posFile" select="substring-before($current_file, $_L2L)"/>      

      <xsl:if test="$debug">
	<xsl:message terminate="no">
	  <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
	  <xsl:value-of select="concat('processing file ', $current_file, $nl)"/>
	  <xsl:value-of select="'-----------------------------------------'"/>
	</xsl:message>
      </xsl:if>
      
      <xsl:result-document href="{$outDir}/{concat($posFile, '_', $tlang, $slang)}.{$e}" format="{$of}">
	<r xml:lang="{$tlang}">
	  <xsl:for-each select="./r/e">
	    <xsl:for-each select="mg[semantics]/tg[@xml:lang = $tlang]/t">
	      <xsl:variable name="c_pos" select="if (./@pos and not(./@pos = '')) then ./@pos else ../../../lg/l/@pos"/>
	      <!-- mwe_-issue should be corrected in the input: this prefix is useless -->
	      <xsl:variable name="cc_pos" select="if (starts-with($c_pos, 'mwe_')) then substring-after($c_pos, 'mwe_') else $c_pos"/>
	      
	      <xsl:if test="$debug">
		<xsl:message terminate="no">
		  <xsl:value-of select="concat($cc_pos, ' ___  ' , ., $nl)"/>
		</xsl:message>
	      </xsl:if>

	      <xsl:variable name="t_counter" select='count(../t)'/>
	      
	      <e>
		<!-- this should be changed in the input files -->
		<xsl:if test="(./@oahpa) and (./@oahpa = 'pref')">
		  <xsl:attribute name="stat">
		    <xsl:value-of select="'pref'"/>
		  </xsl:attribute>
		</xsl:if>
		<!-- if there is only one t and it has no
		     stat_pref-value add one as default -->
		<xsl:if test="$t_counter = 1">
		  <xsl:attribute name="stat">
		    <xsl:value-of select="'pref'"/>
		  </xsl:attribute>
		</xsl:if>
		<lg>
		  <l pos="{$cc_pos}">
		    <xsl:value-of select="normalize-space(.)"/>
		  </l>
		</lg>
		<xsl:copy-of select="./../../../sources" copy-namespaces="no"/>
		<mg>
		  <xsl:copy-of select="../../semantics" copy-namespaces="no"/>
		  <tg xml:lang="{$slang}">
		    <t>
		      <xsl:copy-of select="./../../../lg/l/@pos"/>
		      <xsl:value-of select="normalize-space(./../../../lg/l)"/>
		    </t>
		  </tg>
		</mg>
	      </e>
	    </xsl:for-each>
	  </xsl:for-each>
	</r>
      </xsl:result-document>
      
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>


