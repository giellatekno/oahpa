<?xml version="1.0"?>
<!--+
    | Transforms a csv file with two fields - "lemma","part-of-speech"- into a fitswe gtdict xml format
    | NB: An XSLT-2.0-processor is needed!
    | Usage: java -Xmx2024m net.sf.saxon.Transform -it main THIS_SCRIPT file="INPUT-FILE"
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:fn="fn"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs fn local">
  
  <xsl:strip-space elements="*"/>
  <xsl:output method="xml"
              encoding="UTF-8"
              omit-xml-declaration="no"
              doctype-system="rootdict"
              doctype-public="-//XMLmind//DTD fitswe//FI ../script/fitswe.dtd"
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

  <xsl:variable name="e" select="'xml'"/>
  <xsl:variable name="outputDir" select="'xml-out'"/>

  <xsl:param name="file" select="'default.csv'"/>
  
  <xsl:template match="/" name="main">
    
    <xsl:choose>
      <xsl:when test="unparsed-text-available($file)">

	<xsl:variable name="file_name" select="substring-before($file, '.csv')"/>

	<xsl:variable name="source" select="unparsed-text($file)"/>
	<xsl:variable name="lines" select="tokenize($source, '&#xa;')" as="xs:string+"/>
	<xsl:variable name="output">
	  <rootdict>
	    <!-- capture the patterns and their meanings -->
	    <xsl:for-each select="$lines">
	      <xsl:analyze-string select="." regex='^"([^"]+)","([^"]+)"$' flags="s">
		<xsl:matching-substring>
		  <entry>
		    <xsl:attribute name="src">
		      <xsl:value-of select="$file_name"/>
		    </xsl:attribute>
		    <xsl:variable name="lemma" select="regex-group(1)"/>
		    <xsl:variable name="pos" select="regex-group(2)"/>
		    <lemma>
		      <xsl:attribute name="POS">
			<xsl:value-of select="$pos"/>
		      </xsl:attribute>
		      <xsl:copy-of select="normalize-space($lemma)"/>
		    </lemma>
		    <mgr>
		      <trgr>
			<trans decl="xxx">xxx</trans>
		      </trgr>
		    </mgr>
		  </entry>
		</xsl:matching-substring>
		<!-- 		  <xsl:non-matching-substring> -->
		<!-- 		    <xxx><xsl:value-of select="." /></xxx> -->
		<!-- 		  </xsl:non-matching-substring> -->
	      </xsl:analyze-string>
	    </xsl:for-each>
	  </rootdict>
	</xsl:variable>

	<!-- output -->
	<xsl:for-each-group select="$output/rootdict/entry" group-by="./lemma/@POS">
	  <xsl:result-document href="{$outputDir}/{current-grouping-key()}_fitswe.{$e}">
	    <xsl:processing-instruction name="xml-stylesheet">type="text/css" href="../script/fitswe.css"</xsl:processing-instruction>
	    <xsl:value-of select="'&#xA;'"/>
	    <rootdict>
	      <xsl:copy-of select="current-group()"/>
	    </rootdict>
	  </xsl:result-document>
	</xsl:for-each-group>
	
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate : </xsl:text><xsl:value-of select="$file"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>

