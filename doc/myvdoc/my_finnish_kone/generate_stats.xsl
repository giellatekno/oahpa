<?xml version="1.0"?>
<!--+
    | Usage: java -Xmx2048m net.sf.saxon.Transform -it main THIS_SCRIPT PARAMETER=value
    | 
    +-->

<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xs="http://www.w3.org/2001/XMLSchema"
		xmlns:xhtml="http://www.w3.org/1999/xhtml"
		xmlns:local="nightbar"
		exclude-result-prefixes="xs xhtml local">

  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" name="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>
  <xsl:output method="xml" name="html"
              encoding="UTF-8"
              omit-xml-declaration="yes"
              indent="yes"/>
  <xsl:output method="text" name="txt"
              encoding="UTF-8"/>

  <xsl:param name="homeDir" select="'/Users/cipriangerstenberger'"/>
  <xsl:param name="outFile" select="'lang_stats'"/>
  <xsl:variable name="of" select="'html'"/>
  <xsl:variable name="e" select="$of"/>
  <xsl:variable name="debug" select="false()"/>
  <xsl:variable name="nl" select="'&#xa;'"/>
  <xsl:variable name="sr" select="'\*'"/>
  <xsl:variable name="pre_path" select="concat($homeDir,'/main/langs/')"/>
  <xsl:variable name="langs" select="'izh kca kpv liv mdf mhr mrj myv nio olo udm vep vro yrk'"/>
  <xsl:variable name="stems" select="'/src/morphology/stems'"/>

  <xsl:template match="/" name="main">

    <xsl:variable name="stats">
      <xsl:for-each select="tokenize($langs, ' ')">
	<lang code="{.}">
	  <xsl:variable name="inDir" select="concat($pre_path,.,$stems)"/>
	  
	  <xsl:message terminate="no">
	    <xsl:value-of select="concat('              ==============', $nl)"/>
	    <xsl:value-of select="concat('                  dir ', ., $nl)"/>
	    <xsl:value-of select="'              =============='"/>
	  </xsl:message>
	  
	  <xsl:for-each select="for $f in collection(concat($inDir,'?recurse=no;select=*.xml;on-error=warning')) return $f">
	    
	    <xsl:variable name="current_file" select="(tokenize(document-uri(.), '/'))[last()]"/>
	    <xsl:variable name="current_dir" select="substring-before(document-uri(.), $current_file)"/>
	    <xsl:variable name="current_location" select="concat($inDir, substring-after($current_dir, $inDir))"/>
	    <xsl:variable name="file_name" select="substring-before($current_file, '.xml')"/>      
	    
	    <xsl:if test="true()">
	      <xsl:message terminate="no">
		<xsl:value-of select="concat('processing file ', $file_name, $nl)"/>
		<xsl:value-of select="'.......'"/>
	      </xsl:message>
	    </xsl:if>
	    <xsl:variable name="c1" select="count(./r/e/mg/tg[./@xml:lang='fin']//t[not(. = '')])"/>
	    <xsl:variable name="c2" select="count(./r/e[./mg/tg[./@xml:lang='fin']//t[not(. = '')]])"/>
	    <file name="{$file_name}" t_fin="{$c1}" entry="{$c2}"/>
	  </xsl:for-each>
	</lang>
      </xsl:for-each>
    </xsl:variable>
    
    <xsl:result-document href="{$outFile}_{substring-before(concat(current-date(),''),'+')}.{$of}" format="{$of}">
      <!--count(r/e[mg/tg[@lang='fin']/t/text() | mg/tg[@lang='fin']/tCtn/t/text()])-->
      <html>
	<head>
	  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	  <title>Statistics of language development</title>
	</head>
	<body>
	  <h3>
	    Statistics of language development from 
	    <span style="color:grey;">
	      <xsl:value-of select="substring-before(concat(current-dateTime(),''),'T')"/>
	    </span>
	  </h3>
	  <table border="1" cellpadding="10" cellspacing="0">
	    <tr>
	      <th width="100px">Go to: </th>
	      <xsl:for-each select="$stats/lang">
		<th width="50px">
		  <a href="{concat('#lang_',./@code)}">
		  <xsl:value-of select="./@code"/>
		  </a>
		</th>
	      </xsl:for-each>
	    </tr>
	  </table>
	  
	  <hr style="width: 100%" />
	  
	  <table border="1" cellpadding="10" cellspacing="0">
	    <xsl:for-each select="$stats/lang">
	      <tr>
		<td align="center">
		  <span style="color:#000000;font-weight:bold;font-size:18px;">
		    <a name="{concat('lang_',./@code)}">
		      <xsl:value-of select="./@code"/>
		    </a>
		  </span>
		</td>
		<td>
		  <span style="color:gray;font-style:italic">
		    <xsl:value-of select="'file name'"/>
		  </span>
		</td>
		<td>
		  <span style="color:gray;font-style:italic">
		    <xsl:value-of select="'number of non-empty Finnish translations'"/>
		  </span>
		</td>
		<td>
		  <span style="color:gray;font-style:italic">
		    <xsl:value-of select="'number of entries with at least one non-empty Finnish translation'"/>
		  </span>
		</td>
	      </tr>
	      <xsl:for-each select="./file">
		<tr>
		  <td></td>
		  <td><xsl:value-of select="./@name"/></td>
		  <td><xsl:value-of select="./@t_fin"/></td>
		  <td><xsl:value-of select="./@entry"/></td>
		</tr>
	      </xsl:for-each>
	    </xsl:for-each>
	  </table>
	  
	  <!-- fine print: -->
	  <br/>
	  Data points generated on <span style="color:#000000;font-style:italic"><xsl:value-of select="substring-before(concat(current-dateTime(),''),'T')"/></span> at <span style="color:#000000;font-style:italic"><xsl:value-of select="substring-after(substring-after(concat(current-dateTime(),''),'T'),':')"/></span>
	</body>
      </html>
    </xsl:result-document>
    
  </xsl:template>
  
</xsl:stylesheet>
