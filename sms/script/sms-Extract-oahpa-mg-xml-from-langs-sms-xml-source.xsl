<?xml version="1.0" encoding="utf-8"?>
<!-- This is for extracting mg content from main/langs/sms/src/morphology/stems
 -->
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:fn="http://www.w3.org/2005/02/xpath-functions">
  <xsl:output method="xml"
	      encoding="UTF-8"
	      omit-xml-declaration="no"
	      indent="yes"/>

  <xsl:variable name="XMLLANG" select="//r/@xml:lang"/>

<xsl:template match="/">
<r xmlns:fn="http://www.w3.org/2005/02/xpath-functions" 
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:hfp="http://www.w3.org/2001/XMLSchema-hasFacetAndProperty">
<xsl:attribute name="xml:lang">
  <xsl:value-of select="$XMLLANG"/>
</xsl:attribute>
<xsl:choose>
<xsl:when test="//r/e/lg/l">
  <xsl:for-each select="//r/e[mg/semantics/sem/@class='M_PEOPLE']
| //r/e[mg/semantics/sem/@class='M_ANIMAL']
| //r/e[mg/semantics/sem/@class='M_AURAL_CNT']
| //r/e[mg/semantics/sem/@class='M_DRINK']
| //r/e[mg/semantics/sem/@class='M_FEMALE']
| //r/e[mg/semantics/sem/@class='M_FemaleMale']
| //r/e[mg/semantics/sem/@class='M_FOOD_DISH']
| //r/e[mg/semantics/sem/@class='M_MALE']
| //r/e[mg/semantics/sem/@class='M_OLDERRELATIVE']
| //r/e[mg/semantics/sem/@class='M_VISUAL_CNT']
| //r/e[mg/semantics/sem/@class='M_V_COMM']
| //r/e[mg/semantics/sem/@class='M_V_ILL']
">
    <xsl:sort select="e[1]/lg/l/@pos"/>
    <xsl:sort select="e[1]/lg/l/@type"/>
    <xsl:sort select="e[1]/lg/l"/>
<xsl:variable name="CONTLEX" select="lg/stg/st[1]/@Contlex"/>
<xsl:variable name="POS" select="lg/l/@pos"/>
<e>
<lg>
<l>
<xsl:attribute name="Contlex">
  <xsl:value-of select="$CONTLEX"/>
</xsl:attribute>
<xsl:attribute name="pos">
  <xsl:value-of select="$POS"/>
</xsl:attribute>

<xsl:value-of select="lg/l"/>
</l>
<xsl:if test="lg/audio">
<xsl:copy-of select="lg/audio"/>
</xsl:if>
</lg>
<xsl:if test="sources">
<xsl:copy-of select="sources"/>
</xsl:if>
<xsl:choose>
<!-- thoughts not(contain(mg/@exclude,oahpa)) -->
<xsl:when test="mg/semantics/sem/@class">
<!-- | mg/semantics/sem/@class='M_AURAL_CNT' | mg/semantics/sem/@class='M_PEOPLE' | mg/semantics/sem/@class='M_MALE' | mg/semantics/sem/@class='M_FEMALE' | mg/semantics/sem/@class='M_V_COMM'"> -->
<xsl:copy-of select="mg"/>
</xsl:when>
</xsl:choose>
</e>
  </xsl:for-each>
</xsl:when>
</xsl:choose>
</r>
</xsl:template>
</xsl:stylesheet>
