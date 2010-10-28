<?xml version="1.0"?>

<!--+
    | Transforms a csv file with two fields - "lemma","part-of-speech", etc. - into a sma oahpa gtdict xml format
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
              doctype-system="../../../words/dicts/scripts/gt_dictionary.dtd"
	      doctype-public="-//DivvunGiellatekno//DTD Dictionaries//Multilingual"
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
  <xsl:variable name="outputDir" select="'out-xml'"/>

  <xsl:param name="file" select="'inc/fellesliste.txt'"/>
  <xsl:variable name="lf" select="'&#xa;'"/>
  <xsl:variable name="cr" select="'&#xd;'"/>
  <xsl:variable name="tb" select="'&#x9;'"/>
  <xsl:variable name="sp" select="'&#x20;'"/>
  <xsl:variable name="nbs1" select="'&#xa0;'"/>
  <xsl:variable name="nbs2" select="'&#160;'"/>

  <xsl:variable name="regex">^([^	]+)	+([^	]+)	+([^	]+)	+(.*$)</xsl:variable>

<!--   <xsl:variable name="regex">^([^$tb]+)+$tb+([^$tb]+)(.*$)</xsl:variable> -->

  <xsl:template match="/" name="main">
    
    <xsl:choose>
      <xsl:when test="unparsed-text-available($file)">

	<xsl:variable name="file_name" select="substring-before($file, '.txt')"/>

	<xsl:variable name="source" select="unparsed-text($file)"/>
	<xsl:variable name="lines" select="tokenize($source, $lf)" as="xs:string+"/>
	<xsl:variable name="output">
	  <r>
	    <!-- capture the patterns and their meanings -->
	    <xsl:for-each select="$lines">
	      <xsl:analyze-string select="." regex="{$regex}" flags="s">
		<xsl:matching-substring>
		  <e>
		    <!-- 		    <xsl:attribute name="src"> -->
		    <!-- 		      <xsl:value-of select="$file_name"/> -->
		    <!-- 		    </xsl:attribute> -->
		    <xsl:variable name="lemma" select="regex-group(1)"/>
		    <xsl:variable name="pos" select="regex-group(2)"/>
		    <xsl:variable name="trans" select="regex-group(3)"/>
		    <xsl:variable name="book" select="regex-group(4)"/>
		    <xsl:variable name="current_pos" select="tokenize($pos, $sp)"/>
		    <lg>
		      <l>
			<!-- here, I assume that only verbs have extra information separated by space -->
			<xsl:if test="count($current_pos) = 1">
			  <xsl:attribute name="pos">
			    <xsl:value-of select="lower-case($pos)"/>
			  </xsl:attribute>
			</xsl:if>
			<xsl:if test="count($current_pos) = 2">
			  <xsl:attribute name="pos">
			    <xsl:value-of select="lower-case($current_pos[1])"/>
			  </xsl:attribute>
			  <xsl:attribute name="class">
			    <xsl:value-of select="$current_pos[2]"/>
			  </xsl:attribute>
			</xsl:if>
			<xsl:value-of select="normalize-space($lemma)"/>
		      </l>
		    </lg>
		    <apps>
		      <app name="oahpa">
			<sources>
			  <xsl:for-each select="tokenize($book, ',')">
			    <book name="{normalize-space(.)}"/>
			  </xsl:for-each>
			</sources>
		      </app>
		    </apps>
		    <mg>
		      <tg>
			<semantics> 
			  <sem class="LANGUAGEPART"/> 
			  <sem class="NUMNOUN"/> 
			</semantics>
			<xsl:for-each select="tokenize($trans, ';')">
			  <t pos="{lower-case($current_pos[1])}" xml:lang="nob">
			    <xsl:value-of select="normalize-space(.)"/>
			  </t>
			</xsl:for-each>
		      </tg>
		    </mg>

		    <!-- the correct method -->
		    <!-- 		    <xsl:for-each select="tokenize($trans, ';')"> -->
		    <!-- 		      <mg> -->
		    <!-- 			<tg> -->
		    <!-- 			  <xsl:for-each select="tokenize(., ',')"> -->
		    <!-- 			    <t pos="xxx" xml:lang="nob"> -->
		    <!-- 			      <xsl:value-of select="normalize-space(.)"/> -->
		    <!-- 			    </t> -->
		    <!-- 			  </xsl:for-each> -->
		    <!-- 			</tg> -->
		    <!-- 		      </mg> -->
		    <!-- 		    </xsl:for-each> -->

		  </e>
		</xsl:matching-substring>
		<xsl:non-matching-substring>
		  <xxx><xsl:value-of select="."/></xxx>
		</xsl:non-matching-substring>
	      </xsl:analyze-string>
	    </xsl:for-each>
	  </r>
	</xsl:variable>

	<!-- output -->
	<xsl:for-each-group select="$output/r/e" group-by="./lg/l/@pos">
	  <xsl:result-document href="{$outputDir}/{current-grouping-key()}_sma-oahpa.{$e}">
	    <xsl:processing-instruction name="xml-stylesheet"> title="Dictionary view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary.css" type="text/css"</xsl:processing-instruction>
	    <xsl:value-of select="'&#xa;'"/>	    
	    <xsl:processing-instruction name="xml-stylesheet">alternate="yes" title="Hierarchical view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary_alt.css" type="text/css"</xsl:processing-instruction>
	    <xsl:value-of select="'&#xa;'"/>
	    <r>
	      <xsl:copy-of select="current-group()"/>
	    </r>
	  </xsl:result-document>
	</xsl:for-each-group>
	
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate : </xsl:text><xsl:value-of select="$file"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>

