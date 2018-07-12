<?xml version="1.0"?>
<!--+
    | script to revert sma-oahpa dictionaries from slang to tlang (nob or swe)
    | Usage: java net.sf.saxon.Transform -it main THIS_SCRIPT inDir=DICT_DIR
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
  <xsl:param name="inDir" select="'sma'"/>
  <!-- source language -->
  <xsl:param name="slang" select="'sma'"/>
  <!-- target language: nob is default! -->
  <xsl:param name="tlang" select="'swe'"/>
  <!-- Output dir, files -->
  <xsl:param name="outDir" select="concat('reverted2', $tlang)"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  
  <xsl:template match="/" name="main">
    <xsl:for-each select="for $f in collection(concat($inDir,'?recurse=no;select=*.xml;on-error=warning')) return $f">
      
      <xsl:variable name="current_file" select="(tokenize(document-uri(.), '/'))[last()]"/>
      <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
      <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
      
      <xsl:if test="$debug">
	<xsl:message terminate="no">
	  <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
	  <xsl:value-of select="concat('processing file ', $current_file, $nl)"/>
	  <xsl:value-of select="'-----------------------------------------'"/>
	</xsl:message>
      </xsl:if>
      
      <xsl:variable name="out_tmp">
	<r xml:lang="{$tlang}">
	  <xsl:for-each select="./r/e">
	    
	    <!-- <xsl:for-each select="./mg/tg/*[./@stat = 'pref']"> -->
	    <xsl:for-each select="./mg[./semantics]/tg[./@xml:lang = $tlang]/*[starts-with(local-name(), 't')]">
	      <!-- <xsl:for-each select="./mg[./@xml:lang = $tlang]/tg"> -->
	      <!-- <xsl:variable name="cn" select="./*[not(local-name() = 'semantics')][not(local-name() = 're')][1]"/> -->
	      <!-- <xsl:variable name="cn" select="./*[./@stat = 'pref']"/> -->

	      <!-- if there is a pos attribute which is not empty take it otherwise use the pos value of the lemma -->
	      <xsl:variable name="c_pos" select="if (./@pos and not(./@pos = '')) then ./@pos else ../../../lg/l/@pos"/>
	      
	      <xsl:if test="$debug">
		<xsl:message terminate="no">
		  <xsl:value-of select="concat('pos: ', $c_pos, ' ___ lemma ' , ., $nl)"/>
		</xsl:message>
	      </xsl:if>

	      <e>
		<xsl:if test="(./@stat) and (./@stat = 'pref')">
		  <xsl:attribute name="stat">
		    <xsl:value-of select="'pref'"/>
		  </xsl:attribute>
		</xsl:if>
		<lg>
		  <l pos="{$c_pos}">
		    <xsl:value-of select="normalize-space(.)"/>
		  </l>
		</lg>
		<xsl:copy-of select="./../../../sources" copy-namespaces="no"/>
		<mg>
		  <xsl:copy-of select="../../semantics" copy-namespaces="no"/>
		  <tg xml:lang="{$slang}">
		    <xsl:copy-of select="../re[1]" copy-namespaces="no"/>
		    <xsl:if test="((local-name(.) = 't') or (local-name(.) = 'tf')) and (../te[./position() + 1])">
		      <re>
			<xsl:value-of select="../te[./position() + 1]"/>
		      </re>
		    </xsl:if>
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
      </xsl:variable>
      
      <xsl:result-document href="{$outDir}/{concat(substring-before($current_file, '_smanob'), '_', $tlang, $slang)}.{$e}" format="{$of}">
	<xsl:copy-of select="$out_tmp"/>
      </xsl:result-document>
      
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>


