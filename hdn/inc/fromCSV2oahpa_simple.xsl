<?xml version="1.0"?>
<!--+
    | Transforms a csv file with four fields - 
    | LEMMA __ POS __ TRANSLATION_1,TRANSLATION_2,TRANSLATION_n __ SEMCLASS_1,SEMCLASS_2, SEMCLASS_n
    | into oahpa lexicon files in  xml format split by pos values
    | Usage: java -Xmx2024m net.sf.saxon.Transform -it:main fromCSV2oahpa_simple.xsl inFile=inputfile.csv src_lang=hdn tgt_lang=eng
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
              indent="yes"/>

  <!--xsl:output method="xml"
              encoding="UTF-8"
              omit-xml-declaration="no"
              doctype-system="rootdict"
              doctype-public="-//XMLmind//DTD fitswe//FI ../script/fitswe.dtd"
              indent="yes"/-->


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

  <xsl:param name="inFile" select="'default.csv'"/>
  <xsl:param name="src_lang" select="'fkv'"/>
  <xsl:param name="tgt_lang" select="'nob'"/>

  <xsl:variable name="e" select="'xml'"/>
  <xsl:variable name="outDir" select="'xml-out'"/>
  <xsl:variable name="nl" select="'&#xa;'"/>

  <xsl:template match="/" name="main">
    
    <xsl:choose>
      <xsl:when test="unparsed-text-available($inFile)">

	<xsl:variable name="inFile_name" select="substring-before($inFile, '.csv')"/>

	<xsl:variable name="source" select="unparsed-text($inFile)"/>
	<xsl:variable name="lines" select="tokenize($source, '&#xa;')" as="xs:string+"/>
	<xsl:variable name="output">
	  <r xml:lang="{$src_lang}">
	    <!-- capture the patterns=columns and their meanings -->
	    <xsl:for-each select="$lines">
	      <!-- two underscores as field separator -->
	      <xsl:variable name="current_lemma" select="tokenize(., '__')"/>
	      <e>
		<xsl:variable name="lemma" select="normalize-space($current_lemma[1])"/>
		<xsl:variable name="pos" select="normalize-space($current_lemma[2])"/>
		<xsl:variable name="translations" select="normalize-space($current_lemma[3])"/>
		<xsl:variable name="sem_classes" select="normalize-space($current_lemma[4])"/>
		<lg>
		  <l>
		    <xsl:attribute name="pos">
		      <xsl:value-of select="$pos"/>
		    </xsl:attribute>
		    <xsl:copy-of select="$lemma"/>
		  </l>
		  <!-- default structure for the book elements -->
		  <sources>
		    <book name="xxx"/>
		  </sources>
		</lg>
		<mg>
		  <semantics>
		    <!-- COMMA as separator between SEM_CLASS values -->
		    <xsl:for-each select="tokenize($sem_classes, ',')">
		      <sem class="{normalize-space(.)}"/>
		    </xsl:for-each>
		  </semantics>
		  <tg xml:lang="{$tgt_lang}">
		    <!-- COMMA as separator between TRANSLATION values -->
		    <xsl:for-each select="tokenize($translations, ',')">
		    <!-- as a default all translations get the same
			 pos value as the lemma -->
		      <t pos="{$pos}">
			<!-- additionally, the first translations gets
			the attribute-value pair stat="pref" --> 
			<xsl:if test="position() = 1">
			  <xsl:attribute name="stat">
			    <xsl:value-of  select="'pref'"/>
			  </xsl:attribute>
			</xsl:if>
			<xsl:value-of select="normalize-space(.)"/>
		      </t>
		    </xsl:for-each>
		  </tg>
		</mg>
	      </e>
	    </xsl:for-each>
	  </r>
	</xsl:variable>
	
	<!-- pos-based output -->
	<xsl:for-each-group select="$output/r/e" group-by="./lg/l/@pos">
	  <xsl:variable name="current_outfile" select="concat(current-grouping-key(),'_',$src_lang,$tgt_lang)"/>
	  <xsl:result-document href="{$outDir}/{$current_outfile}.{$e}">
	    <!--xsl:processing-instruction name="xml-stylesheet">type="text/css" href="../script/fitswe.css"</xsl:processing-instruction>
	    <xsl:value-of select="'&#xA;'"/-->

	    <xsl:message terminate="no">
              <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
              <xsl:value-of select="concat('generating file ', $current_outfile, $nl)"/>
              <xsl:value-of select="'-----------------------------------------'"/>
            </xsl:message>
	    
	    <r xml:lang="{$src_lang}">
	      <xsl:copy-of select="current-group()"/>
	    </r>
	  </xsl:result-document>
	</xsl:for-each-group>
	
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>Cannot locate : </xsl:text><xsl:value-of select="$inFile"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>

