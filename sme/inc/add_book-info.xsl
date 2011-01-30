<?xml version="1.0"?>
<!--+
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inputDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		exclude-result-prefixes="xs">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <xsl:param name="inFile" select="'lemmat_1V'"/>
  <xsl:param name="inDir" select="'indir_test'"/>
  <xsl:variable name="outDir" select="'outdir'"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  <xsl:variable name="slang" select="'sme'"/>
  <xsl:variable name="tlang" select="'nob'"/>
  <!--   <xsl:variable name="theBook" select="'åa4'"/> -->
  <xsl:variable name="theBook" select="'sam1031_1'"/>
  
  <xsl:template match="/" name="main">
    <xsl:if test="not(unparsed-text-available($inFile))">
      <xsl:message terminate="yes">
	<xsl:value-of select="concat($nl, 'ERROR: unable to open file ', $inFile, $nl)"/>
      </xsl:message>
    </xsl:if>

    <xsl:variable name="source" select="unparsed-text($inFile)"/>
    <!--     <xsl:variable name="file_lines" select="tokenize($source, '&#xa;')" as="xs:string+"/> -->
    
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
      
      <xsl:variable name="cufi">
	<r xml:lang="{$slang}">
	  <xsl:for-each select="./lexicon/entry">
	    <xsl:variable name="lemma" select="./lemma"/>

	    <xsl:if test="not(exists(tokenize($source, $nl)[. = $lemma]))">
	      <xsl:copy-of select="."/>
	    </xsl:if>
	    
	    <xsl:if test="exists(tokenize($source, $nl)[. = $lemma])">
	      <entry>
		<xsl:copy-of select="./@*"/>
		<xsl:copy-of select="./lemma"/>
		<xsl:copy-of select="./pos"/>
		<xsl:copy-of select="./translations"/>
		<xsl:copy-of select="./valency"/>
		<xsl:copy-of select="./semantics"/>
		<xsl:copy-of select="./stem"/>
		    <sources>
		      <xsl:copy-of select="./sources/*"/>
		      <book name="{$theBook}"/>
		    </sources>
		  <xsl:copy-of select="./sources/*"/>
	      </entry>
	    </xsl:if>
	  </xsl:for-each>
	</r>
      </xsl:variable>
      
      <xsl:result-document href="{$outDir}/{$current_file}" format="{$of}">
	<xsl:copy-of select="$cufi"/>
      </xsl:result-document>
    </xsl:for-each>
    
  </xsl:template>
  
</xsl:stylesheet>
