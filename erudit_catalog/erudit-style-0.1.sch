<?xml version="1.0" encoding="utf-8"?>
<!--
Copyright 2018 Érudit.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="exslt"
        xml:lang="en">
  <ns uri="http://www.w3.org/1999/xlink" prefix="xlink"/>
  <ns uri="http://exslt.org/regular-expressions" prefix="regexp"/>

  <p>
  *******************************************************************************
   THINGS TO BE SURE BEFORE EDITING THIS FILE!

   The spec used is ISO-Schematron. 
   
   Some useful info:
     - The query language used is the extended version of XPath specified in XSLT.
     - The rule context is interpreted according to the Production 1 of XSLT. 
       The rule context may be the root node, elements, attributes, comments and 
       processing instructions. 
     - The assertion test is interpreted according to Production 14 of XPath, as 
       returning a Boolean value.

   For more info, refer to the official ISO/IEC 19757-3:2006(E) standard.
  
   The implementation of the schematron patterns comes with the idea of EPS as a
   set of constraints on top of JATS Publishing Tag Set v1.1 (JPTS)[1]. To keep
   consistency, please make sure:
  
     - DTD/XSD constraints are not duplicated here
  
   [1] http://jats.nlm.nih.gov/publishing/tag-library/1.1/
  *******************************************************************************
  </p>

  <!--
   Phases - sets of patterns.
   These are being used to help on tests isolation.
  -->

  <phase id="phase.journal-meta">
    <active pattern="journal-meta_has_journal-id"/>
    <active pattern="journal-meta_has_journal-title-group"/>
  </phase>

  <phase id="phase.journal-id">
    <active pattern="journal-id_notempty"/>
    <active pattern="journal-id_has_erudit-id"/>
    <active pattern="journal-id_values"/>
  </phase>

  <phase id="phase.issn">
    <active pattern="issn_pub_type_epub_or_ppub"/>
    <active pattern="issn_isvalid"/>
    <active pattern="issn_notempty"/>
  </phase>

  <phase id="phase.article-attrs">
    <active pattern="article_attributes"/>
    <active pattern="article_article-type-values"/>
    <active pattern="article_specific-use-values"/>
  </phase>

  <phase id="phase.publisher">
    <active pattern="publisher"/>
    <active pattern="publisher_notempty"/>
  </phase>

  <phase id="phase.journal-title-group">
    <active pattern="has_journal-title"/>
    <active pattern="journal-title_notempty"/>
    <active pattern="journal-id_notempty"/>
  </phase>

  <phase id="phase.trans-title-group">
    <active pattern="trans-title-group_lang"/>
  </phase>

  <phase id="phase.trans-title">
    <active pattern="trans-title_lang"/>
  </phase>

  <phase id="phase.ack">
    <active pattern="ack"/>
  </phase>

  <phase id="phase.ref">
    <active pattern="ref_has_element-citation"/>
    <active pattern="element-citation_cardinality"/>
  </phase>

  <phase id="phase.element-citation">
    <active pattern="element-citation_has_styled-content"/>
  </phase>

  <phase id="phase.styled-content">
    <active pattern="styled-content_notempty"/>
  </phase>

  <phase id="phase.pub-id">
    <active pattern="pub-id_has_pub-id-type"/>
    <active pattern="pub-id_notempty"/>
  </phase>

  <!--
    Abstract Patterns
  -->

  <pattern abstract="true" id="occurs_once">
    <rule context="$base_context">
      <assert test="count($element) = 1">
        Element '<name/>': There must be only one element <value-of select="name($element)"/>.
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="occurs_zero_or_once">
    <rule context="$base_context">
      <assert test="count($element) &lt; 2">
        Element '<name/>': There must be zero or one element <value-of select="name($element)"/>.
      </assert>
    </rule>
  </pattern>

  <pattern id="assert-not-empty" abstract="true" xmlns="http://purl.oclc.org/dsdl/schematron">
    <title>
      Check if the element's text is at least one character long.
    </title>

    <rule context="$base_context">
      <assert test="string-length(normalize-space($assert_expr)) != 0">
        Element '<name/>': <value-of select="$err_message"/>
      </assert>
    </rule>
  </pattern>

  <!--
    Patterns - sets of rules.
  -->

  <pattern id="pub-id_has_pub-id-type">
    <rule context="article/back/ref-list/ref/element-citation/pub-id">
      <assert test="@pub-id-type">
        Element 'pub-id': Missing attribute pub-id-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/back/ref-list/ref/element-citation/pub-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="journal-meta_has_journal-id">
    <rule context="article/front/journal-meta">
      <assert test="journal-id[@journal-id-type='erudit']">
        Element 'journal-meta': Missing element journal_id with attribute journal-id-type=erudit
      </assert>
    </rule>
  </pattern>

  <pattern id="journal-meta_has_journal-title-group">
    <rule context="article/front/journal-meta">
      <assert test="journal-title-group">
        Element 'journal-meta': Missing element journal-title-group.
      </assert>
    </rule>
  </pattern>

  <pattern id="has_journal-title">
    <rule context="article/front/journal-meta/journal-title-group">
      <assert test="journal-title">
        Element 'journal-title-group': Missing element journal-title.
      </assert>
    </rule>
    <rule context="article/front/journal-meta/journal-title-group/journal-title">
      <assert test="@xml:lang">
        Element 'jounrl-title': Missing attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="journal-title_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-title-group/journal-title"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="abbrev-journal-title_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-title-group/abbrev-journal-title"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="journal-id_cardinality" is-a="occurs_once">
    <param name="base_context" value="article/front/journal-meta/journal-title-group"/>
    <param name="element" value="journal-title"/>
  </pattern>

  <pattern id="element-citation_cardinality" is-a="occurs_once">
    <param name="base_context" value="article/back/ref-list/ref"/>
    <param name="element" value="element-citation"/>
  </pattern>

  <pattern id="styled-content_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/back/ref-list/ref/element-citation/styled-content"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="ref_has_element-citation">
    <title>
      element-citation is mandatory in ref.
    </title>

    <rule context="article/back/ref-list/ref">
      <assert test="element-citation">
        Element 'ref': Missing element element-citation.
      </assert>
    </rule>
  </pattern>

  <pattern id="element-citation_has_styled-content">
    <title>
      styled-content is mandatory in element-citation.
    </title>
    <rule context="article/back/ref-list/ref/element-citation">
      <assert test="styled-content">
        Element 'element-citation': Missing element styled-content.
      </assert>
    </rule>
  </pattern>

  <pattern id="ack">
    <title>
      Ack elements cannot be organized as sections (sec).
    </title>

    <rule context="article/back/ack">
      <assert test="not(sec)">
          Element 'ack': Unexpected element sec.
      </assert>
    </rule>
  </pattern>

  <pattern id="trans-title_lang">
    <rule context="article/front/journal-meta/journal-title-group/trans-title-group/trans-title">
      <assert test="not(@xml:lang)">
        Element 'trans-title': Unexpected attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="trans-title-group_lang">
    <rule context="article/front/journal-meta/journal-title-group/trans-title-group">
      <assert test="@xml:lang">
        Element 'trans-title-group': Missing attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="publisher">
    <rule context="article/front/journal-meta">
      <assert test="publisher">
        Element 'journal-meta': Missing element publisher.
      </assert>
    </rule>
  </pattern>

  <pattern id="publisher_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/publisher/publisher-name"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="article_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article">
      <assert test="@article-type">
        Element 'article': Missing attribute article-type.
      </assert>
      <assert test="@xml:lang">
        Element 'article': Missing attribute xml:lang.
      </assert>
      <assert test="@dtd-version">
        Element 'article': Missing attribute dtd-version.
      </assert>
      <assert test="@specific-use">
        Element 'article': Missing EPS version at the attribute specific-use.
      </assert>
    </rule>
  </pattern>

  <pattern id="article_article-type-values">
    <title>
      Allowed values for article/@article-type
    </title>

    <rule context="article[@article-type]">
        <assert test="@article-type = 'addendum' or
            @article-type = 'research-article' or
            @article-type = 'review-article' or
            @article-type = 'letter' or
            @article-type = 'article-commentary' or
            @article-type = 'brief-report' or
            @article-type = 'rapid-communication' or
            @article-type = 'oration' or
            @article-type = 'discussion' or
            @article-type = 'editorial' or
            @article-type = 'interview' or
            @article-type = 'correction' or
            @article-type = 'guidelines' or
            @article-type = 'other' or
            @article-type = 'obituary' or
            @article-type = 'case-report' or
            @article-type = 'book-review' or
            @article-type = 'reply' or
            @article-type = 'retraction' or
            @article-type = 'partial-retraction' or
            @article-type = 'clinical-trial' or
            @article-type = 'announcement' or
            @article-type = 'calendar' or
            @article-type = 'in-brief' or
            @article-type = 'book-received' or
            @article-type = 'news' or
            @article-type = 'reprint' or
            @article-type = 'meeting-report' or
            @article-type = 'abstract' or
            @article-type = 'product-review' or
            @article-type = 'dissertation' or
            @article-type = 'translation'">
        Element 'article', attribute article-type: Invalid value '<value-of select="@article-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="article_specific-use-values">
    <title>
      The SPS version must be declared in article/@specific-use 
    </title>

    <rule context="article[@specific-use]">
      <assert test="@specific-use = 'eps-0.1'">
        Element 'article', attribute specific-use: Invalid value '<value-of select="@specific-use"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="journal-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="journal-id_has_erudit-id">
    <title>
      There exists one journal-id[@journal-id-type='erudit'].
    </title>

    <rule context="article/front/journal-meta">
      <assert test="journal-id[@journal-id-type='erudit']">
        Element 'journal-meta': Missing element journal-id with journal-id-type="erudit".
      </assert>
    </rule>
  </pattern>

  <pattern id="journal-id_values">
    <rule context="article/front/journal-meta/journal-id[@journal-id-type]">
      <assert test="@journal-id-type = 'erudit' or 
                    @journal-id-type = 'publisher' or 
                    @journal-id-type = 'doi'">
        Element 'journal-id', attribute journal-id-type: Invalid value "<value-of select="@journal-id-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="issn_pub_type_epub_or_ppub">
    <rule context="article/front/journal-meta">
      <assert test="issn[@pub-type='epub'] or issn[@pub-type='ppub']">
        Element 'journal-meta': Missing element issn with pub-type=("epub" or "ppub").
      </assert>
    </rule>
  </pattern>

  <pattern id="issn_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/issn"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="issn_isvalid">
    <rule context="//issn">
      <assert test="regexp:test(current(), '[0-9]{4}-[0-9]{3}[0-9xX]')">
        Element 'issn': Invalid issn=([0-9]{4}-[0-9]{3}[0-9xX]).
      </assert>
    </rule>
  </pattern>
</schema>

