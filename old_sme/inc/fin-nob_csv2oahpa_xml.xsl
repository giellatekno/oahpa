<?xml version="1.0"?>
<!--+
    | 
    | compares two lists of words and outputs both the intersection set
    | and the set of items which are in the first but not in the second set
    | NB: The user has to adjust the paths to the input files accordingly
    | Usage: java net.sf.saxon.Transform -it main THIS_FILE
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		exclude-result-prefixes="xs">

  <xsl:strip-space elements="*"/>

  <xsl:output method="text" name="txt"
	      encoding="UTF-8"
	      omit-xml-declaration="yes"
	      indent="no"/>

  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:variable name="tab" select="'&#x9;'"/>
  <xsl:variable name="spc" select="'&#x20;'"/>
  <xsl:variable name="nl" select="'&#xA;'"/>
  <xsl:variable name="cl" select="':'"/>
  <xsl:variable name="scl" select="';'"/>
  <xsl:variable name="us" select="'_'"/>
  <xsl:variable name="rbl" select="'('"/>
  <xsl:variable name="rbr" select="')'"/>
  <xsl:variable name="qm" select="'&#34;'"/>
  <xsl:variable name="cm" select="','"/>
  <xsl:variable name="debug" select="true()"/>

  <!-- input file, extention of the output file -->
  <xsl:param name="inFile" select="'morelemmasfromfin.csv'"/>
  <xsl:param name="of" select="'xml'"/>
  <xsl:param name="outDir" select="'out'"/>
  
  <xsl:variable name="regex01">^([^_]+)_([^_]+)_([^_]+)_([^_]+)_(.*)$</xsl:variable>
  <xsl:variable name="regex02">^([^_]+)_([^_]+)_([^_]+)_(.*)$</xsl:variable>

  <xsl:template match="/" name="main">
    
    <xsl:choose>
      <xsl:when test="unparsed-text-available($inFile)">

	<xsl:if test="$debug">
	  <xsl:message terminate="no">
	    <xsl:value-of select="concat('-----------------------------------------', $nl)"/>
	    <xsl:value-of select="concat('processing file ', $inFile, $nl)"/>
	    <xsl:value-of select="'-----------------------------------------'"/>
	  </xsl:message>
	</xsl:if>
	
	<!-- file -->
	<xsl:variable name="file" select="unparsed-text($inFile)"/>
	<xsl:variable name="file_lines" select="distinct-values(tokenize($file, $nl))" as="xs:string+"/>
	<xsl:variable name="out_tmp" as="element()">
	  <r>
	    <xsl:for-each select="$file_lines">
	      <xsl:variable name="normLine" select="normalize-space(.)"/>
	      <xsl:analyze-string select="$normLine" regex="{$regex01}" flags="s">
		<xsl:matching-substring>
		  
		  <xsl:variable name="lemma" select="normalize-space(regex-group(1))"/>
		  <xsl:variable name="pos" select="lower-case(normalize-space(regex-group(2)))"/>
		  <xsl:variable name="target_fin" select="tokenize(regex-group(3), $cm)"/>
		  <xsl:variable name="target_nob" select="tokenize(regex-group(4), $cm)"/>
		  <xsl:variable name="sem_class" select="normalize-space(regex-group(5))"/>

		  <xsl:if test="$debug">
		    <xsl:message terminate="no">
		      <xsl:value-of select="concat('Patter 01 lemma: ', $lemma, $nl)"/>
		      <xsl:value-of select="'............'"/>
		    </xsl:message>
		  </xsl:if>
		  
		  <e>
		    <lg>
		      <l pos="{$pos}">
			<xsl:value-of select="$lemma"/>
		      </l>
		    </lg>
		    <mg>
		      <semantics>
			<sem class="{$sem_class}"/>
		      </semantics>
		      <tg xml:lang="nob">
			<xsl:for-each select="$target_nob">
			  <xsl:variable name="cTrans" select="normalize-space(.)"/>
			  <t pos="{$pos}">
			    <xsl:if test="position() = 1">
			      <xsl:attribute name="stat">
				<xsl:value-of select="'pref'"/>
			      </xsl:attribute>
			    </xsl:if>
			    <xsl:value-of select="$cTrans"/>
			  </t>
			</xsl:for-each>
		      </tg>
		      <tg xml:lang="fin">
			<xsl:for-each select="$target_fin">
			  <xsl:variable name="cTrans" select="normalize-space(.)"/>
			  <t pos="{$pos}">
			    <xsl:if test="position() = 1">
			      <xsl:attribute name="stat">
				<xsl:value-of select="'pref'"/>
			      </xsl:attribute>
			    </xsl:if>
			    <xsl:value-of select="$cTrans"/>
			  </t>
			</xsl:for-each>
		      </tg>
		    </mg>
		  </e>
		</xsl:matching-substring>
		<xsl:non-matching-substring>
		  <xsl:analyze-string select="$normLine" regex="{$regex02}" flags="s">
		    <xsl:matching-substring>
		      
		      <xsl:variable name="lemma" select="regex-group(1)"/>
		      <xsl:variable name="pos" select="lower-case(regex-group(2))"/>
		      <xsl:variable name="target_fin" select="tokenize(regex-group(3), $cm)"/>
		      <xsl:variable name="target_nob" select="tokenize(regex-group(4), $cm)"/>

		      <xsl:if test="$debug">
			<xsl:message terminate="no">
			  <xsl:value-of select="concat('Patter 02 lemma: ', $lemma, $nl)"/>
			  <xsl:value-of select="'............'"/>
			</xsl:message>
		      </xsl:if>
		      
		      <e>
			<lg>
			  <l pos="{$pos}">
			    <xsl:value-of select="$lemma"/>
			  </l>
			</lg>
			<mg>
			  <semantics>
			    <sem class="'YYY'"/>
			  </semantics>
			  <tg xml:lang="nob">
			    <xsl:for-each select="$target_nob">
			      <xsl:variable name="cTrans" select="normalize-space(.)"/>
			      <t pos="{$pos}">
				<xsl:if test="position() = 1">
				  <xsl:attribute name="stat">
				    <xsl:value-of select="'pref'"/>
				  </xsl:attribute>
				</xsl:if>
				<xsl:value-of select="$cTrans"/>
			      </t>
			    </xsl:for-each>
			  </tg>
			  <tg xml:lang="fin">
			    <xsl:for-each select="$target_fin">
			      <xsl:variable name="cTrans" select="normalize-space(.)"/>
			      <t pos="{$pos}">
				<xsl:if test="position() = 1">
				  <xsl:attribute name="stat">
				    <xsl:value-of select="'pref'"/>
				  </xsl:attribute>
				</xsl:if>
				<xsl:value-of select="$cTrans"/>
			      </t>
			    </xsl:for-each>
			  </tg>
			</mg>
		      </e>
		    </xsl:matching-substring>
		    <xsl:non-matching-substring>
		      <xsl:if test="$debug">
			<xsl:message terminate="no">
			  <xsl:value-of select="concat('non-matching-line', ., $nl)"/>
			  <xsl:value-of select="'............'"/>
			</xsl:message>
		      </xsl:if>
		      <xxx><xsl:value-of select="."/></xxx>
		    </xsl:non-matching-substring>
		  </xsl:analyze-string>
		</xsl:non-matching-substring>
	      </xsl:analyze-string>
	    </xsl:for-each>
	  </r>
	</xsl:variable>
	
	<!-- compute and output the intersection set: elements that are both in file 1 and in file 2 -->
	<xsl:result-document href="{$outDir}/{$inFile}.{$of}" format="{$of}">
	  <xsl:copy-of select="$out_tmp"/>
	</xsl:result-document>
	
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="concat('Cannot locate file: ', $inFile, $nl)"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>
