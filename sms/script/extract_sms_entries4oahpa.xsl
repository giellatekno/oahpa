<?xml version="1.0"?>
<!--+
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:fn="fn"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs fn local">
    
  <xsl:strip-space elements="*"/>

  <xsl:output method="text" name="txt"
	      encoding="UTF-8"
	      omit-xml-declaration="yes"
	      indent="no"/>

  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  

<xsl:function name="local:distinct-deep" as="node()*">
  <xsl:param name="nodes" as="node()*"/> 
 
  <xsl:sequence select=" 
    for $seq in (1 to count($nodes))
    return $nodes[$seq][not(local:is-node-in-sequence-deep-equal(
                          .,$nodes[position() &lt; $seq]))]
 "/>
   
</xsl:function>

<xsl:function name="local:is-node-in-sequence-deep-equal" as="xs:boolean">
  <xsl:param name="node" as="node()?"/> 
  <xsl:param name="seq" as="node()*"/> 
 
  <xsl:sequence select=" 
   some $nodeInSeq in $seq satisfies deep-equal($nodeInSeq,$node)
 "/>
   
</xsl:function>


  <xsl:param name="inFile" select="'_x_'"/>
  <xsl:param name="inDir" select="'src'"/>
  <xsl:param name="outDir" select="'oahpa_sms_src'"/>

  <xsl:variable name="debug" select="true()"/>
  <xsl:variable name="of" select="'xml'"/>
  <xsl:variable name="e" select="$of"/>

  <xsl:template match="/" name="main">
    
    <xsl:for-each select="collection(concat($inDir, '?select=*.xml'))">
      
      <xsl:variable name="current_file" select="substring-before((tokenize(document-uri(.), '/'))[last()], '.xml')"/>
      <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
      <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
      
      <xsl:message terminate="no">
	<xsl:value-of select="concat('Processing file: ', $current_file)"/>
      </xsl:message>
      
      <xsl:result-document href="{$outDir}/{$current_file}.{$e}" format="{$of}">
	<r xml:lang="sms">
	  <xsl:for-each select="./r/e[(.//sources/book/@name='kurss') or
				(.//sources/book/@name='200') or
				(.//sources/book/@name='100')]">

	    <xsl:variable name="c_e">
	      <e mg_c="{count(./mg)}">
		<lg>
		  <xsl:copy-of copy-namespaces="no" select="./lg/l"/>
		</lg>
		<xsl:copy-of copy-namespaces="no" select=".//sources"/>
		<xsl:for-each select="mg[not(contains(./@exclude,'oahpa'))]">
		  <mg>
		    <xsl:copy-of copy-namespaces="no" select="./semantics"/>
		    <xsl:for-each select="./tg[not(contains(./@exclude,'oahpa'))]">
		      <tg xml:lang="{./@xml:lang}">
			<xsl:for-each select="./t">
			  <xsl:copy-of copy-namespaces="no" select="."/>
			</xsl:for-each>
		      </tg>
		    </xsl:for-each>
		  </mg>
		</xsl:for-each>
	      </e>
	    </xsl:variable>
	    
	    <xsl:if test="count($c_e/e/mg) &gt;0">
	      <e mg_c="{count($c_e/e/mg)}">
		<xsl:copy-of copy-namespaces="no" select="$c_e/e/*"/>
	      </e>
	    </xsl:if>
	  </xsl:for-each>
	</r>
      </xsl:result-document>
    </xsl:for-each>
    
  </xsl:template>
  
</xsl:stylesheet>

