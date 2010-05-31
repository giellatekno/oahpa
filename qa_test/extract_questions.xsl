<?xml version="1.0"?>
<!--+
    | 
    | The parameter: the path to the collection of XML-files to check
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_FILE inputDir=DIR
    | 
    +-->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:param name="inputDir" select="'default'"/>
  <xsl:variable name="outputDir" select="'out_dir'"/>
  <xsl:variable name="e" select="'xml'"/>
  <xsl:variable name="dt" select="'.'"/>
  <xsl:variable name="qm" select="'?'"/>

  <xsl:template match="/" name="main">

    <xsl:variable name="output">
      <out>
	<xsl:for-each select="collection(concat($inputDir, '?select=dialogue_*.xml'))">
	  <xsl:variable name="filename" select="substring-before(tokenize(document-uri(.), '/')[last()], '.xml')"/>
	  <xsl:variable name="dial" select="substring-after($filename, 'dialogue_')"/>
	  <q_tests>
	    <xsl:attribute name="dialogue">
	      <xsl:value-of select="$dial"/>
	    </xsl:attribute>
	    <xsl:for-each select="dialogue/topic/utt[./@type = 'question']">
	      <test>
		<xsl:attribute name="name">
		  <xsl:value-of select="./@name"/>
		</xsl:attribute>
		<q>
		  <xsl:if test="contains(./text, $dt)">
		    
		    <xsl:variable name="only_q">
		      <xsl:call-template 
			  name="substring-after-last">
			<xsl:with-param name="input" select="./text" />
			<xsl:with-param name="marker" select="$dt" />
		      </xsl:call-template>
		    </xsl:variable>
		    
		    <xsl:if test="contains(normalize-space($only_q), $qm)">
		      <xsl:value-of select="substring-before(normalize-space($only_q), $qm)"/>
		    </xsl:if>
		    <xsl:if test="not(contains(normalize-space($only_q), $qm))">
		      <xsl:value-of select="normalize-space($only_q)"/>
		    </xsl:if>
		  </xsl:if>
		  
		  <xsl:if test="not(contains(./text, $dt))">
		    <xsl:if test="contains(normalize-space(./text), $qm)">
		      <xsl:value-of select="substring-before(normalize-space(./text), $qm)"/>
		    </xsl:if>
		    <xsl:if test="not(contains(normalize-space(./text), $qm))">
		      <xsl:value-of select="normalize-space(./text)"/>
		    </xsl:if>
		  </xsl:if>
		  
		</q>
		<a>
		  <xsl:value-of select="'xxx'"/>
		</a>
	      </test>
	    </xsl:for-each>
	  </q_tests>
	</xsl:for-each>
      </out>
    </xsl:variable>
    
    <!--     <xsl:copy-of select="$emptyFiles_pos"/> -->
    
    <!-- output the data into separate txt-files: pos it the file name descriptor-->
    <xsl:for-each select="$output/out/q_tests">
      <xsl:result-document href="{$outputDir}/out_{./@dialogue}.{$e}">
	
	<xsl:copy-of select="."/>
	
<!-- 	<xsl:for-each select="./lemma"> -->
<!-- 	  <xsl:value-of select="concat(., '&#xa;')"/> -->
<!-- 	</xsl:for-each> -->
      </xsl:result-document>
    </xsl:for-each>
    
    
  </xsl:template>
  

  <xsl:template name="substring-after-last">
    <xsl:param name="input" />
    <xsl:param name="marker" />
    
    <xsl:choose>
      <xsl:when test="contains($input,$marker)">
	<xsl:call-template name="substring-after-last">
	  <xsl:with-param name="input" 
			  select="substring-after($input,$marker)" />
	  <xsl:with-param name="marker" select="$marker" />
	</xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="$input" />
      </xsl:otherwise>
    </xsl:choose>
    
  </xsl:template>
  
  
  
</xsl:stylesheet>
