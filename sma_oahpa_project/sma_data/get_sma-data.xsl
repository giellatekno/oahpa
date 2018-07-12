<?xml version="1.0"?>
<!--+
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		exclude-result-prefixes="xs xhtml">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <xsl:param name="inFile" select="'gogo_file'"/>
  <xsl:param name="inDir" select="'/Users/cipriangerstenberger/gtsvn/ped/sma/src'"/>
  <xsl:param name="slang" select="'sma'"/>
  <!-- tlang now locally set for both nob and swe -->
  <!--   <xsl:param name="tlang" select="'nob'"/> -->
  <xsl:variable name="outDir" select="'sma'"/>
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

      <xsl:variable name="c_file">
	<r xml:lang="{$slang}">
	<!-- take only entries that have an 'apps' element with an 'app' element with
             an attribute 'name' with value 'oahpa' -->
	  <xsl:for-each select="for $e in .//e[./apps/app/@name='oahpa'] return $e">
	    <!-- <xsl:copy-of select="." copy-namespaces="no"/> -->
	    <e>
	      <xsl:copy-of select="./@*"/>
	      <xsl:copy-of select="./lg" copy-namespaces="no"/>
	      <xsl:copy-of select="./stem" copy-namespaces="no"/>
	      <xsl:copy-of select="./apps" copy-namespaces="no"/>

	      <!-- old code -->
	      <!-- don't take mg elements with lang=sme;
		   don't take mg elements without a semantics group inside -->
	      <!-- <xsl:for-each select="./mg[not(./@xml:lang='sme')][./tg/semantics]"> -->

	      <!-- new code: take all -->
	      <xsl:for-each select="./mg">
		<mg>
		  <xsl:copy-of select="./@*"/>
		  <xsl:for-each select="./tg">
		    <tg>
		      <xsl:copy-of select="./@*"/>
		      <xsl:copy-of select="./semantics" copy-namespaces="no"/>
		      <xsl:variable name="tlang" select="./@xml:lang"/>
		      <xsl:if test="./*[./@oa = 'yes']/preceding-sibling::re">
			<re>
			  <xsl:attribute name="xml:lang">
			    <xsl:value-of select="$tlang"/>
			  </xsl:attribute>
			  <xsl:copy-of select="./*[./@oa = 'yes']/preceding-sibling::re/@*"/>
			  <xsl:copy-of select="normalize-space(./*[./@oa = 'yes']/preceding-sibling::re)"/>
			</re>
		      </xsl:if>
		      <!-- take any t-, tf, or te-element that is licensed for oahpa -->
		      <xsl:for-each select="./*[starts-with(local-name(.), 't')][./@oa = 'yes']">
			<xsl:element name="{local-name(.)}">
			  <xsl:copy-of select="./@pos"/>
			  <xsl:copy-of select="./@stat"/>
			  <xsl:copy-of select="./@tcomm"/>
			  <!-- add lang attribute in any case -->
			  <xsl:attribute name="xml:lang">
			    <xsl:value-of select="$tlang"/>
			  </xsl:attribute>
			  <xsl:value-of select="normalize-space(.)"/>
			</xsl:element>
		      </xsl:for-each>
		    </tg>
		  </xsl:for-each>
		</mg>
	      </xsl:for-each>
	    </e>
	  </xsl:for-each>
	</r>
      </xsl:variable>

      <xsl:if test="not(count($c_file//e) = 0)">      
	<xsl:result-document href="{$outDir}/{$current_file}" format="{$of}">
	  <xsl:copy-of select="$c_file"/>
	</xsl:result-document>
      </xsl:if>
    </xsl:for-each>
    
  </xsl:template>
  
</xsl:stylesheet>
