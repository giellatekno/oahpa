<?xml version="1.0"?>
<!--+
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		exclude-result-prefixes="xs">

<!--   <xsl:strip-space elements="*"/> -->
  <xsl:output method="xml" name="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <xsl:param name="inDir" select="'src'"/>
  <xsl:param name="slang" select="'sma'"/>
  <xsl:param name="tlang" select="'nob'"/>
  <xsl:variable name="outDir" select="'_mg_check'"/>
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
	<xsl:for-each select="./r">
	  <r>
	    <xsl:copy-of select="./@*"/>
	    <!-- <xsl:copy-of select="./lics"/> -->
	    <xsl:for-each select="./e">
	      <e>
		<xsl:copy-of select="./@*"/>
		<xsl:if test="$debug">
		  <xsl:call-template name="flatten_node">
		    <xsl:with-param name="theNode" select="."/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:copy-of select="./lg"/>
		<xsl:copy-of select="./stem"/>
		<xsl:copy-of select="./apps"/>
		<xsl:for-each select="./mg">
		  <mg>
		    <xsl:copy-of select="./@*"/>
		    <xsl:if test="$debug">
		      <xsl:call-template name="flatten_node">
			<xsl:with-param name="theNode" select="."/>
		      </xsl:call-template>
		    </xsl:if>
		    <xsl:copy-of select="./*"/>
		  </mg>
		</xsl:for-each>
	      </e>
	    </xsl:for-each>
	  </r>
	</xsl:for-each>
      </xsl:variable>
      
      <xsl:if test="$debug">      
	<xsl:result-document href="{$outDir}/{$current_file}" format="{$of}">
	  <xsl:copy-of select="$c_file"/>
	</xsl:result-document>
      </xsl:if>
    </xsl:for-each>
    
  </xsl:template>
  
  <xsl:template name="flatten_node">
    <xsl:param name="theNode"/>
    
    <xsl:variable name="pattern">
      <xsl:for-each select="$theNode/*">
	<xsl:value-of select="lower-case(local-name(.))"/>

	<xsl:if test="./@xml:lang and not(./@xml:lang = '')">
	  <xsl:value-of select="concat('-', ./@xml:lang)"/>
	</xsl:if>
	
	<xsl:if test="not(position() = last())">
	  <xsl:value-of select="'_'"/>
	</xsl:if>
      </xsl:for-each>
    </xsl:variable>
    
    <xsl:element name="{concat(lower-case(local-name($theNode)), '_test')}">
      <xsl:attribute name="stamp">
	<xsl:value-of select="$pattern"/>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>



</xsl:stylesheet>
