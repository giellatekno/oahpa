<?xml version="1.0"?>
<!--+
    | 
    | filter entries that are not marked as stat="pref" 
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_SCRIPT inFile=INPUT_FILE.xml
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:functx="http://www.functx.com"
		exclude-result-prefixes="xs functx">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:function name="functx:is-node-in-sequence-deep-equal" as="xs:boolean" 
		xmlns:functx="http://www.functx.com" >
    <xsl:param name="node" as="node()?"/> 
    <xsl:param name="seq" as="node()*"/> 
    
    <xsl:sequence select=" 
			  some $nodeInSeq in $seq satisfies deep-equal($nodeInSeq,$node)
			  "/>
    
  </xsl:function>
  
  <xsl:function name="functx:distinct-deep" as="node()*" 
		xmlns:functx="http://www.functx.com" >
    <xsl:param name="nodes" as="node()*"/> 
    
    <xsl:sequence select=" 
			  for $seq in (1 to count($nodes))
			  return $nodes[$seq][not(functx:is-node-in-sequence-deep-equal(
			  .,$nodes[position() &lt; $seq]))]
			  "/>
  </xsl:function>
  
  <!-- parameters -->
  <!-- input dir -->
  <xsl:param name="inDir" select="concat('to_filter_',$slang)"/>
  <!-- <xsl:param name="inFile" select="'default.xml'"/> -->
  <xsl:param name="slang" select="'sme'"/>
  <xsl:param name="tlang" select="'eng'"/>
  <xsl:param name="outDir" select="concat($slang,$tlang)"/>
  
  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'xml'"/>
  <xsl:variable name="e" select="$output_format"/>
    
  <xsl:template match="/" name="main">
    <xsl:for-each select="for $f in collection(concat($inDir,'?recurse=no;select=*.xml;on-error=warning')) return $f">
      
      <xsl:variable name="current_file" select="(tokenize(document-uri(.), '/'))[last()]"/>
      <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
      <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
      <xsl:variable name="file_with_path" select="concat($current_location, $current_file)"/>
      <xsl:variable name="file_name" select="substring-before((tokenize($current_file, '/'))[last()], '.xml')"/> <!-- was: $inFile -->

    <xsl:value-of select="concat(' processing file ', $current_file)"/>
    <xsl:choose>
      <xsl:when test="doc-available($file_with_path)">
	<xsl:variable name="out_tmp">
	  <r>
	    <xsl:copy-of select="doc($file_with_path)/r/@*"/>
	    <xsl:copy-of select="doc($file_with_path)/r/e[./@stat = 'pref']"/>
	  </r>
	</xsl:variable>
	
	<!-- out -->
	<xsl:result-document href="{$outDir}/{$file_name}.{$e}" format="{$output_format}">
	  <xsl:copy-of select="$out_tmp"/>
	</xsl:result-document>

      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate: </xsl:text><xsl:value-of select="$file_with_path"/><xsl:text>&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
   </xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>


