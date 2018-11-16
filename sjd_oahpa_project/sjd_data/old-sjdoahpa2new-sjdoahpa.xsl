<?xml version="1.0"?>
<!--+
    | 
    | Script for transforming the smeoahpa source files into the smaoahpa format, i.e., into a more dictionary-like format
    | Usage: java net.sf.saxon.Transform -it main STYLESHEET_NAME.xsl (inFile=INPUT_FILE_NAME.xml | inDir=INPUT_DIR)
    +-->

<!-- java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main old-oahpa2new-oahpa.xsl inDir=src -->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:local="nightbar"
		xmlns:fmp="http://www.filemaker.com/fmpxmlresult"
		xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
		exclude-result-prefixes="xs local fmp ss">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
              encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  
  <!-- Input -->
  <xsl:param name="inFile" select="'xxxfilexxx'"/>
  <xsl:param name="inDir" select="'xxxdirxxx'"/>
  
  <!-- Output -->
  <xsl:variable name="outputDir" select="'000_outDir'"/>
  
  <!-- Patterns for the feature values -->
  <xsl:variable name="output_format" select="'xml'"/>
  <xsl:variable name="e" select="$output_format"/>
  <xsl:variable name="file_name" select="substring-before((tokenize($inFile, '/'))[last()], '.xml')"/>
  <xsl:variable name="nl" select="'&#xA;'"/>
  <xsl:variable name="debug" select="true()"/>
  
  
  
  <xsl:template match="/" name="main">
    
    <xsl:if test="doc-available($inFile)">

      <xsl:message terminate="no">
	<xsl:value-of select="concat('Processing file: ', $inFile)"/>
      </xsl:message>
      
      <xsl:call-template name="processFile">
	<xsl:with-param name="theFile" select="document($inFile)"/>
	<xsl:with-param name="theName" select="$file_name"/>
      </xsl:call-template>
    </xsl:if>

    <!-- xsl:if test="doc-available($inDir)" -->
    <xsl:if test="not($inDir = 'xxxdirxxx')">
      <xsl:for-each select="for $f in collection(concat($inDir, '?select=*.xml')) return $f">
	
	<xsl:variable name="current_file" select="substring-before((tokenize(document-uri(.), '/'))[last()], '.xml')"/>
	<xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
	<xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
	
	<xsl:message terminate="no">
	  <xsl:value-of select="concat('Processing file: ', $current_file)"/>
	</xsl:message>

	<xsl:call-template name="processFile">
	  <xsl:with-param name="theFile" select="."/>
	  <xsl:with-param name="theName" select="$current_file"/>
	</xsl:call-template>
      </xsl:for-each>
    </xsl:if>
    
	
    
    <xsl:if test="not(doc-available($inFile) or not($inDir = 'xxxdirxxx'))">
      <xsl:value-of select="concat('Neither ', $inFile, ' nor ', $inDir, ' found.', $nl)"/>
    </xsl:if>
    
  </xsl:template>

  <xsl:template name="processFile">
    <xsl:param name="theFile"/>
    <xsl:param name="theName"/>

    <xsl:variable name="output">
      <r>
	<xsl:copy-of select="$theFile/lexicon/@*"/>
	<xsl:for-each select="$theFile/lexicon/entry">
	  <xsl:message terminate="no">
	    <xsl:value-of select="concat('Entry ', ./lemma)"/>
	  </xsl:message>
	  <e>
	    <xsl:copy-of select="./@*"/>
	    <lg>
	      <l pos="{lower-case(./pos/@class)}">
		<xsl:if test="./pos/@type">
		  <xsl:attribute name="type">
		    <xsl:value-of select="lower-case(./pos/@type)"/>
		  </xsl:attribute>
		</xsl:if>
		<xsl:if test="./pos/@gen_only">
		  <xsl:attribute name="gen_only">
		    <xsl:value-of select="./pos/@gen_only"/>
		  </xsl:attribute>
		</xsl:if>
		<xsl:if test="./stem/@class">
		  <xsl:attribute name="stem">
		    <xsl:variable name="cc" select="normalize-space(./stem/@class)"/>
		    <xsl:value-of select="if ($cc = 'bisyllabic') then '2syll' else
					  if ($cc = 'trisyllabic') then '3syll' else
					  if ($cc = 'contracted') then 'Csyll' else 'xxx'"/>
		  </xsl:attribute>
		</xsl:if>
		<xsl:for-each select="./stem/@*[not(local-name() = 'class')]">
		  <xsl:copy-of select="."/>
		</xsl:for-each>
		<xsl:value-of select="normalize-space(./lemma)"/>
	      </l>
	      <!-- xsl:if test="./stem/@class">
		   <stem_test>
		   <xsl:variable name="cc" select="normalize-space(./stem/@class)"/>
		   <xsl:value-of select="if ($cc = 'bisyllabic') then '2syll' else
		   if ($cc = 'trisyllabic') then '3syll' else
		   if ($cc = 'contracted') then 'Csyll' else 'xxx'"/>
		   </stem_test>
		   </xsl:if -->
	    </lg>
	    <xsl:copy-of select="./dialect"/>
	    <xsl:copy-of select="./sources"/>
	    <mg>
	      <xsl:copy-of select="./semantics"/>
	      <xsl:variable name="cTrans" select="./translations"/>
	      <xsl:variable name="tTrans">
		<xsl:for-each select="('rus', 'eng', 'sme', 'nob', 'fin', 'ger')">
		  <xsl:variable name="cl" select="."/>
		  <tg xml:lang="{$cl}">
		    <xsl:if test="not($cTrans/tr[./@xml:lang = $cl])">
		      <t stat="pref">
			<xsl:value-of select="concat(normalize-space($cTrans/tr[./@xml:lang = 'eng'][01]), '_', upper-case($cl))"/>
		      </t>
		    </xsl:if>
		    <xsl:for-each select="$cTrans/tr[./@xml:lang = $cl][not(normalize-space(./text()) = '')]">
		      <t>
			<xsl:if test="position() = 1">
			  <xsl:attribute name="stat">
			    <xsl:value-of select="'pref'"/>
			  </xsl:attribute>
			</xsl:if>
			<xsl:copy-of select="./@tcomm"/>
			<xsl:value-of select="normalize-space(.)"/>
		      </t>
		    </xsl:for-each>
		  </tg>
		</xsl:for-each>
	      </xsl:variable>
	      <xsl:copy-of select="$tTrans"/>
	    </mg>
	  </e>
	</xsl:for-each>
      </r>
    </xsl:variable>

    <!-- output file -->
    <xsl:result-document href="{$outputDir}/{$theName}.{$e}" format="{$output_format}">
      <xsl:copy-of select="$output"/>
    </xsl:result-document>
    
  </xsl:template>
  
</xsl:stylesheet>

