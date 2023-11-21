<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="#all">
    
<xsl:output method="xml" encoding="UTF-8" indent="no"/>

<xsl:variable name="source">
    <xsl:value-of select="//meta:user-defined[@meta:name='source']"/>
</xsl:variable> 
    
<xsl:variable name="mainLang">
    <xsl:value-of select="//meta:user-defined[@meta:name='language']"/>
</xsl:variable> 
    
<!-- todo : gestion des espaces de noms -->
    
<!-- template de sauvegarde : ne devrait pas être employé… -->
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:include href="core_typo.xsl"/>
<xsl:include href="core_div-para.xsl"/>
<xsl:include href="core_figure.xsl"/>
<xsl:include href="core_list.xsl"/>
<xsl:include href="core_note.xsl"/>
<xsl:include href="core_cit.xsl"/>
<xsl:include href="core_code.xsl"/>
<xsl:include href="core_linking.xsl"/>
<xsl:include href="back.xsl"/>
<xsl:include href="front.xsl"/>
<xsl:include href="teiHeader.xsl"/>
    
<xsl:template match="/">
<!--<xsl:text disable-output-escaping="yes">&lt;!DOCTYPE TEI SYSTEM "../dtd/tei_all.dtd"&gt;</xsl:text>-->
  <TEI><!--change="metopes_edition"-->
    <xsl:call-template name="teiHeader"/>
    <text xml:id="text">
      <front>
          <titlePage>
              <xsl:if test="//*:p[@text:style-name='TEI_title:sup']">
                  <titlePart type="sup">
                      <xsl:apply-templates select="//*:p[@text:style-name='TEI_title:sup']/node()"/>
                  </titlePart>
              </xsl:if>
              <titlePart type="main">
                  <xsl:copy-of select="//text:h[@text:outline-level='0']/@xml:lang"/>
                  <xsl:apply-templates select="//text:h[@text:outline-level='0']" mode="front"/>
              </titlePart>
              <xsl:for-each select="//*:p[starts-with(@text:style-name,'TEI_title:') and not(@text:style-name='TEI_title:sup')]">
                  <xsl:variable name="titleType">
                      <xsl:choose>
                          <xsl:when test="contains(@text:style-name,'TEI_title:trl')">trl</xsl:when>
                          <xsl:otherwise><xsl:value-of select="substring-after(@text:style-name,'TEI_title:')"/></xsl:otherwise>
                      </xsl:choose>
                  </xsl:variable>
                  <titlePart>
                      <xsl:attribute name="type" select="$titleType"/>
                      <xsl:if test="contains(@text:style-name,'TEI_title:trl')">
                          <xsl:copy-of select="@xml:lang"/>
                       </xsl:if>
                      <xsl:apply-templates/>
                  </titlePart>
              </xsl:for-each>
          </titlePage>
          <!-- Review metadata for OpenEdition -->
          <xsl:if test="//*:p[@text:style-name='TEI_reviewed_reference'] and $source='OpenEdition'">
              <div type="reviewed">
                  <xsl:for-each select="//*:p[@text:style-name='TEI_reviewed_reference']">
                      <xsl:apply-templates select="." mode="front"/>
                  </xsl:for-each>
              </div>
          </xsl:if>
          <!-- Épigraphe -->
          <xsl:if test="//*:p[@text:style-name='TEI_epigraph'][parent::*:text]">
              <epigraph>
                <xsl:copy-of select="//*:p[@text:style-name='TEI_epigraph'][parent::*:text]/@xml:lang"/>
                <xsl:apply-templates select="//*:p[@text:style-name='TEI_epigraph'][parent::*:text]"/>
              </epigraph>
          </xsl:if>
      </front>
      <body>
        <xsl:choose>
            <xsl:when test="//text/text:*[following::*:div[@type='section1' and not(ancestor::*:floatingText)][1]]">
                <xsl:apply-templates select="//text/*[following::*:div[@type='section1'][1]]"/>
            </xsl:when>
            <xsl:when test="not(//text/text:*/*:div[@type='section1'])">
                <xsl:apply-templates select="//text/* except (//*:div[@type='appendix'] | //*:div[@type='bibliography'])"/>
            </xsl:when>
            <xsl:otherwise>
                <alertXSL>reprendre le template pour la gestion du body</alertXSL>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="//*:div[@type='section1' and not(ancestor::*:floatingText)][last()]"/>
      </body>
    </text>
  </TEI>
</xsl:template>
    
    
</xsl:stylesheet>