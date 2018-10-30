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
    <active pattern="pub-id_doi_value"/>
  </phase>

  <phase id="phase.app">
    <active pattern="app_has_id"/>
  </phase>

  <phase id="phase.ack">
    <active pattern="ack"/>
  </phase>

  <phase id="phase.fn-group">
    <active pattern="fn_has_id"/>
    <active pattern="fn-group_has_fn"/>
  </phase>

  <phase id="phase.volume">
    <active pattern="volume_notempty"/>
    <active pattern="volume_cardinality_at_element-citation"/>
    <active pattern="volume_cardinality_at_article-meta"/>
    <active pattern="volume_cardinality_at_product"/>
  </phase>
  
  <phase id="phase.issue">
    <active pattern="issue_notempty"/>
    <active pattern="issue_cardinality_at_element-citation"/>
    <active pattern="issue_cardinality_at_article-meta"/>
  </phase>

  <phase id="phase.pub-date">
    <active pattern="pub-date_publication_format"/>
    <active pattern="pub-date_date_type"/>
    <active pattern="pub-date_must_have_date-type"/>
    <active pattern="pub-date_with_date-type_equal_pub_must_have_publication-format"/>
    <active pattern="pub-date_must_have_date-type_pub"/>
    <active pattern="pub-date_must_have_date-type_issue"/>
  </phase>

  <phase id="phase.month">
    <active pattern="month"/>
    <active pattern="month_cardinality_element-citation"/>
    <active pattern="month_cardinality_article-meta"/>
  </phase>

  <phase id="phase.fpage_or_elocation-id">
    <active pattern="fpage_or_elocation-id"/>
    <active pattern="fpage_notempty"/>
    <active pattern="lpage_notempty"/>
    <active pattern="elocation-id_notempty"/>
  </phase>

  <phase id="phase.history">
    <active pattern="history"/>
    <active pattern="history_has_date"/>
  </phase>

  <phase id="phase.article-id">
    <active pattern="article-id_notempty"/>
    <active pattern="article-id_attributes"/>
    <active pattern="article-id_pub-id-type_values"/>
    <active pattern="article-id_doi_value"/>
  </phase>

  <phase id="phase.kwd-group">
    <active pattern="kwd-group_lang"/>
    <active pattern="kwd-group_cannot_have_nested-kwd"/>
    <active pattern="kwd-group_cannot_have_compounded-kwd"/>
  </phase>

  <phase id="phase.abstract">
    <active pattern="abstract_lang"/>
    <active pattern="abstract_has_p_or_sec"/>
  </phase>

  <phase id="phase.trans-abstract">
    <active pattern="trans-abstract_lang"/>
    <active pattern="trans-abstract_has_p_or_sec"/>
  </phase>

  <phase id="phase.permissions">
    <active pattern="permissions_must_exists"/>
    <active pattern="permissions_has_license"/>
  </phase>

  <phase id="phase.name">
    <active pattern="prefix_notempty"/>
    <active pattern="suffix_notempty"/>
    <active pattern="surname_notempty"/>
    <active pattern="given-names_notempty"/>
  </phase>

  <phase id="phase.contrib-group">
    <active pattern="contrib-group_content-type_values_in_article-meta"/>
    <active pattern="contrib-group_content-type_values_in_journal-meta"/>
    <active pattern="contrib-group_cannot_have_aff"/>
    <active pattern="contrib-group_cannot_have_aff-alternatives"/>
  </phase>

  <phase id="phase.contrib">
    <active pattern="contrib_contrib-type_values"/>
    <active pattern="contrib_contrib-type_group_must_have_collab"/>
    <active pattern="contrib_cannot_have_aff"/>
    <active pattern="contrib_cannot_have_aff-alternatives"/>
  </phase>

  <phase id="phase.contrib-id">
    <active pattern="contrib-id_notempty"/>
    <active pattern="contrib-id_must_have_contrib-id-type"/>
    <active pattern="contrib-id_contrib-id-type_values"/>
    <active pattern="contrib-id_avoid_url_in_value"/>
  </phase>

  <phase id="phase.collab">
    <active pattern="collab_must_have_named-content"/>
    <active pattern="collab_must_have_named-content_notempty"/>
  </phase>

  <phase id="phase.xref_reftype_integrity">
    <active pattern="xref-reftype-values"/>
  </phase>

  <phase id="phase.rid_integrity">
    <active pattern="xref-reftype-integrity-aff"/>
  </phase>

  <phase id="phase.aff">
    <active pattern="aff_must_have_id"/>
    <active pattern="aff_must_have_institution_with_content-type_orgname"/>
  </phase>

  <phase id="phase.institution">
    <active pattern="institution_must_have_content-type"/>
    <active pattern="institution_content-type_values"/>
  </phase>

  <phase id="phase.counts">
    <active pattern="counts_tables"/>
    <active pattern="counts_refs"/>
    <active pattern="counts_figs"/>
    <active pattern="counts_equations"/>
    <active pattern="counts_pages"/>
  </phase>

  <phase id="phase.seclabel">
    <active pattern="seclabel_has_once"/>
    <active pattern="seclabel_notempty"/>
  </phase>

  <phase id="phase.fig">
    <active pattern="fig_has_id"/>
    <active pattern="fig_has_label"/>
    <active pattern="fig_has_graphic"/>
  </phase>

  <phase id="phase.xhtml-table">
    <active pattern="xhtml-table"/>
  </phase>

  <phase id="phase.table-wrap">
    <active pattern="table-wrap_has_id"/>
    <active pattern="table-wrap_has_label"/>
    <active pattern="table-wrap_has_one_of_table_or_graphic"/>
  </phase>

  <phase id="phase.self-uri">
    <active pattern="self-uri_has_xlinkhref"/>
  </phase>

  <phase id="phase.ext-link">
    <active pattern="ext-link_has_xlinkhref"/>
  </phase>

  <phase id="phase.issue-title">
    <active pattern="issue-title_has_lang"/>
  </phase>

  <phase id="phase.list">
    <active pattern="list_attributes"/>
    <active pattern="list_list-type-values"/>
  </phase>

  <!--
    Abstract Patterns
  -->

  <pattern abstract="true" id="occurs_once">
    <rule context="$base_context">
      <assert test="count($element) = 1">
        Element '<name/>': There must be one element <value-of select="name($element)"/>.
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

  <pattern abstract="true" id="assert-not-empty" xmlns="http://purl.oclc.org/dsdl/schematron">
    <title>
      Check if the element's text is at least one character long.
    </title>

    <rule context="$base_context">
      <assert test="string-length(normalize-space($assert_expr)) != 0">
        Element '<name/>': <value-of select="$err_message"/>
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="xref-reftype-integrity-base">
    <title>
      Make sure all references to are reachable.
    </title>

    <rule context="//xref[@ref-type='$ref_type']">
      <assert test="@rid = $ref_elements">
        Element '<name/>', attribute rid: Mismatching id value '<value-of select="@rid"/>' of type '<value-of select="@ref-type"/>'.
      </assert>
    </rule>
  </pattern>

  <!--
    Patterns - sets of rules.
  -->

  <pattern id="list_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="//list">
      <assert test="@list-type">
        Element 'list': Missing attribute list-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="list_list-type-values">
    <title>
      Allowed values for list/@list-type
    </title>

    <rule context="//list[@list-type]">
      <assert test="@list-type = 'order' or
                    @list-type = 'bullet' or
                    @list-type = 'alpha' or
                    @list-type = 'roman' or
                    @list-type = 'simple'">
        Element 'list', attribute list-type: Invalid value '<value-of select="@list-type"/>'.
      </assert>
    </rule>
  </pattern>


  <pattern id="issue-title_has_lang">
    <rule context="article/front/article-meta/issue-title">
      <assert test="@xml:lang">
        Element 'issue-title': Missing attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="table-wrap_has_one_of_table_or_graphic">
    <title>
      - Make sure name, etal and collab are not child of element-citation.
      - element-citation can be only child of ref elements.
    </title>

    <rule context="//table-wrap">
      <assert test="table or graphic">
        Element 'table-wrap': Must have one of table or graphic elements.
      </assert>
    </rule>
  </pattern>

  <pattern id="self-uri_has_xlinkhref">
    <rule context="//self-uri">
      <assert test="@xlink:href">
        Element 'self-uri': Missing attribute xlink:href.
      </assert>
    </rule>
  </pattern>

  <pattern id="ext-link_has_xlinkhref">
    <rule context="//ext-link">
      <assert test="@xlink:href">
        Element 'ext-link': Missing attribute xlink:href.
      </assert>
    </rule>
  </pattern>

  <pattern id="table-wrap_has_label" is-a="occurs_once">
    <param name="base_context" value="//table-wrap"/>
    <param name="element" value="label"/>
  </pattern>

  <pattern id="table-wrap_has_id">
    <title>
      table-wrap elements must have attribute id.
    </title>

    <rule context="//table-wrap">
      <assert test="@id">
          Element 'table-wrap': Missing Attribute @id.
      </assert>
    </rule>
  </pattern>

  <pattern id="xhtml-table">
    <title>
      Tables should be fully tagged. tr elements are not supposed to be declared
      at toplevel.
    </title>

    <rule context="//table">
      <assert test="not(tr)">
        Element 'table': Unexpected element tr.
      </assert>
      <assert test="not(tbody//th)">
        Element 'table': Unexpected element th inside tbody.
      </assert>
      <assert test="not(thead//td)">
        Element 'table': Unexpected element td inside thead.
      </assert>
    </rule>
  </pattern>

  <pattern id="fig_has_id">
    <title>
      fig elements must have attribute id.
    </title>

    <rule context="//fig">
      <assert test="@id">
          Element 'fig': Missing Attribute @id.
      </assert>
    </rule>
  </pattern>

  <pattern id="fig_has_graphic" is-a="occurs_once">
    <param name="base_context" value="//fig"/>
    <param name="element" value="graphic"/>
  </pattern>

  <pattern id="fig_has_label" is-a="occurs_once">
    <param name="base_context" value="//fig"/>
    <param name="element" value="label"/>
  </pattern>

  <pattern id="seclabel_has_once" is-a="occurs_once">
    <param name="base_context" value="//sec"/>
    <param name="element" value="label"/>
  </pattern>

  <pattern id="seclabel_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//sec/label"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="counts_tables">
    <title>
      Make sure the total number of tables are correct.
    </title>

    <rule context="article/front/article-meta/counts/table-count">
      <assert test="@count = count(//table-wrap)">
        Element 'table-count': Wrong value in table-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_refs">
    <title>
      Make sure the total number of refs are correct.
    </title>

    <rule context="article/front/article-meta/counts/ref-count">
      <assert test="@count = count(//ref)">
        Element 'ref-count': Wrong value in ref-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_figs">
    <title>
      Make sure the total number of figures are correct.
    </title>

    <rule context="article/front/article-meta/counts/fig-count">
      <assert test="@count = count(//fig)">
        Element 'fig-count': Wrong value in fig-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_equations">
    <title>
      Make sure the total number of equations are correct.
    </title>

    <rule context="article/front/article-meta/counts/equation-count">
      <assert test="@count = count(//disp-formula)">
        Element 'equation-count': Wrong value in equation-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_pages">
    <title>
      Make sure the total number of pages are correct.
    </title>

    <rule context="article/front/article-meta/counts/page-count">
      <assert test="(/article/front/article-meta/lpage = 0 and
                     /article/front/article-meta/fpage = 0 and
                     @count = 0) or 
                     (regexp:test(/article/front/article-meta/fpage, '\D', 'i') or
                      regexp:test(/article/front/article-meta/lpage, '\D', 'i')) or
                     string-length(/article/front/article-meta/elocation-id) > 0 or
                     (@count = ((/article/front/article-meta/lpage - /article/front/article-meta/fpage) + 1))">
        Element 'page-count': Wrong value in page-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="institution_content-type_values">
    <title>
      institution elements attribute content-type allowed values.
    </title>

    <rule context="article/front/article-meta/aff/institution[@content-type]">
      <assert test="@content-type = 'orgname' or
                    @content-type = 'orgdiv1' or
                    @content-type = 'orgdiv2' or
                    @content-type = 'orgdiv3' or
                    @content-type = 'original'">
        Element 'institution', attribute content-type: Invalid value "<value-of select="@content-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="institution_must_have_content-type">
    <title>
      institution elements must have attribute content-type.
    </title>

    <rule context="article/front/article-meta/aff/institution">
      <assert test="@content-type">
          Element 'institution': Missing Attribute @content-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="aff_must_have_id">
    <title>
      aff elements must have attribute id.
    </title>

    <rule context="article/front/article-meta/aff">
      <assert test="@id">
          Element 'aff': Missing Attribute @id.
      </assert>
    </rule>
  </pattern>

  <pattern id="aff_must_have_institution_with_content-type_orgname">
    <title>
      aff elements must have a institution with @content-type=orgname.
    </title>

    <rule context="article/front/article-meta//aff">
      <assert test="institution[@content-type='orgname']">
          Element 'aff': Missing Element institution with @content-type=orgname.
      </assert>
    </rule>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-aff">
    <param name="ref_type" value="aff"/>
    <param name="ref_elements" value="//aff/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-app">
    <param name="ref_type" value="app"/>
    <param name="ref_elements" value="//app/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-author-notes">
    <param name="ref_type" value="author-notes"/>
    <param name="ref_elements" value="//author-notes/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-bibr">
    <param name="ref_type" value="bibr"/>
    <param name="ref_elements" value="//ref/@id | //element-citation/@id | //mixed-citation/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-contrib">
    <param name="ref_type" value="contrib"/>
    <param name="ref_elements" value="//contrib/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-corresp">
    <param name="ref_type" value="corresp"/>
    <param name="ref_elements" value="//corresp/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-disp-formula">
    <param name="ref_type" value="disp-formula"/>
    <param name="ref_elements" value="//disp-formula/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-fig">
    <param name="ref_type" value="fig"/>
    <param name="ref_elements" value="//fig/@id | //fig-group/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-fn">
    <param name="ref_type" value="fn"/>
    <param name="ref_elements" value="//fn/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-sec">
    <param name="ref_type" value="sec"/>
    <param name="ref_elements" value="//sec/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-supplementary-material">
    <param name="ref_type" value="supplementary-material"/>
    <param name="ref_elements" value="//supplementary-material/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-table">
    <param name="ref_type" value="table"/>
    <param name="ref_elements" value="//table-wrap/@id | //table-wrap-group/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-table-fn">
    <param name="ref_type" value="table-fn"/>
    <param name="ref_elements" value="//table-wrap-foot/fn/@id"/>
  </pattern>

  <pattern id="xref-reftype-values">
    <title>
      Validate the ref-type value against a list.
    </title>

    <rule context="//xref[@ref-type]">
      <assert test="@ref-type = 'aff' or
                    @ref-type = 'app' or
                    @ref-type = 'author-notes' or
                    @ref-type = 'bibr' or 
                    @ref-type = 'contrib' or
                    @ref-type = 'corresp' or
                    @ref-type = 'disp-formula' or
                    @ref-type = 'fig' or 
                    @ref-type = 'fn' or
                    @ref-type = 'sec' or
                    @ref-type = 'supplementary-material' or
                    @ref-type = 'table' or
                    @ref-type = 'table-fn' or
                    @ref-type = 'boxed-text'">
        Element 'xref', attribute ref-type: Invalid value "<value-of select="@ref-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="collab_must_have_named-content">
    <title>
      collab elements must have a named-content with @content-type=name.
    </title>

    <rule context="//collab">
      <assert test="named-content[@content-type='name']">
          Element 'collab': Missing Element named-content with @content-type=name.
      </assert>
    </rule>
  </pattern>

  <pattern id="collab_must_have_named-content_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//collab/named-content"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="contrib-id_must_have_contrib-id-type">
    <title>
      Make sure all contrib-id elements have contrib-id-type.
    </title>

    <rule context="//contrib-id">
      <assert test="@contrib-id-type">
        Element 'contrib-id': Missing attribute contrib-id-type.
      </assert>  
    </rule>
  </pattern>

  <pattern id="contrib-id_avoid_url_in_value">
    <title>
      Only accept ids that seems not to be an URL.
    </title>

    <rule context="//contrib-id">
      <assert test="not(regexp:test(current(), 'http'))">
        Element 'contrib-id': Invalid value '<value-of select="current()"/>'. Value can not be a URL.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-id_contrib-id-type_values">
    <title>
      Make sure @contrib-id-type in contrib-id accepted values.
    </title>
    <rule context="article/front/article-meta/contrib-group/contrib[@contrib-id-type]">
      <assert test="@contrib-id-type='orcid' or 
                    @contrib-id-type='researchid' or
                    @contrib-id-type='scopus'">
        Element 'contrib-id', attribute contrib-id-type: Invalid value "<value-of select="@contrib-id-type"/>". 
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//contrib-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="contrib-group_cannot_have_aff-alternatives">
    <title>
      contrib-group elements cannot have the element aff-alternatives.
    </title>

    <rule context="//contrib-group">
      <assert test="not(aff-alternatives)">
          Element 'contrib-group': Unexpected element aff-laternatives.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-group_cannot_have_aff">
    <title>
      contrib-group elements cannot have the element aff.
    </title>

    <rule context="//contrib-group">
      <assert test="not(aff)">
          Element 'contrib-group': Unexpected element aff.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib_cannot_have_aff-alternatives">
    <title>
      contrib elements cannot have the element aff-alternatives.
    </title>

    <rule context="//contrib">
      <assert test="not(aff-alternatives)">
          Element 'contrib': Unexpected element aff-laternatives.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib_cannot_have_aff">
    <title>
      contrib elements cannot have the element aff.
    </title>

    <rule context="//contrib">
      <assert test="not(aff)">
          Element 'contrib': Unexpected element aff.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib_contrib-type_group_must_have_collab">
    <title>
      Make sure contrib with @contrib-type=groub must have a collab inside according to JATS4M rules.
      see: https://github.com/substance/dar/blob/master/DarArticle.md#contrib-group
    </title>
    <rule context="article/front/article-meta/contrib-group/contrib[@contrib-type='group']">
      <assert test="collab">
        Element 'contrib[@contrib-group="group"]': Missing element collab.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib_contrib-type_values">
    <title>
      Make sure @contrib-type in contrib accepts only JATS4M values.
    </title>
    <rule context="article/front/article-meta/contrib-group/contrib[@contrib-type]">
      <assert test="@contrib-type='person' or 
                    @contrib-type='group'">
        Element 'contrib', attribute contrib-type: Invalid value "<value-of select="@contrib-type"/>". 
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-group_content-type_values_in_journal-meta">
    <title>
      Make sure @content-type in contrib-group accepts only JATS4M values.
    </title>
    <rule context="article/front/journal-meta/contrib-group[@content-type]">
      <assert test="@content-type='manager' or 
                    @content-type='editor'">
        Element 'contrib-group', attribute content-type: Invalid value "<value-of select="@content-type"/>". 
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-group_content-type_values_in_article-meta">
    <title>
      Make sure @content-type in contrib-group accepts only JATS4M values.
    </title>
    <rule context="article/front/article-meta/contrib-group[@content-type]">
      <assert test="@content-type='author' or 
                    @content-type='editor'">
        Element 'contrib-group', attribute content-type: Invalid value "<value-of select="@content-type"/>". 
      </assert>
    </rule>
  </pattern>

  <pattern id="prefix_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//prefix"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="suffix_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//suffix"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="surname_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//surname"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="given-names_notempty" is-a="assert-not-empty">
    <param name="base_context" value="//given-names"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="permissions_has_license">
    <title>
      Make sure all permissions element must have license.
    </title>

    <rule context="//permissions">
      <assert test="license">
        Element 'permissions': Missing element license.
      </assert>  
    </rule>
  </pattern>

  <pattern id="permissions_must_exists">
    <title>
      Make sure all article-meta element must have permissions.
    </title>

    <rule context="article/front/article-meta">
      <assert test="permissions">
        Element 'article-meta': Missing element permissions.
      </assert>  
    </rule>
  </pattern>

  <pattern id="trans-abstract_has_p_or_sec">
    <title>
      Make sure all abstract elements must have element p or sec.
    </title>

    <rule context="article/front/article-meta/trans-abstract">
      <assert test="p or sec">
        Element 'trans-abstract': Missing element p or sec.
      </assert>  
    </rule>
  </pattern>

  <pattern id="trans-abstract_lang">
    <title>
      Make sure all abstract elements have xml:lang attribute.
    </title>

    <rule context="article/front/article-meta/trans-abstract">
      <assert test="@xml:lang">
        Element 'trans-abstract': Missing attribute xml:lang.
      </assert>  
    </rule>
  </pattern>

  <pattern id="abstract_has_p_or_sec">
    <title>
      Make sure all abstract elements must have element p or sec.
    </title>

    <rule context="article/front/article-meta/abstract">
      <assert test="p or sec">
        Element 'abstract': Missing element p or sec.
      </assert>  
    </rule>
  </pattern>

  <pattern id="abstract_lang">
    <title>
      Make sure all abstract elements have xml:lang attribute.
    </title>

    <rule context="article/front/article-meta/abstract">
      <assert test="@xml:lang">
        Element 'abstract': Missing attribute xml:lang.
      </assert>  
    </rule>
  </pattern>

  <pattern id="kwd-group_cannot_have_nested-kwd">
    <title>
      kwd-group elements cannot have the element nested-kwd.
    </title>

    <rule context="article/front/article-meta/kwd-group">
      <assert test="not(nested-kwd)">
          Element 'kwd-group': Unexpected element nested-kwd.
      </assert>
    </rule>
  </pattern>

  <pattern id="kwd-group_cannot_have_compounded-kwd">
    <title>
      kwd-group elements cannot have the element compounded-kwd.
    </title>

    <rule context="article/front/article-meta/kwd-group">
      <assert test="not(compounded-kwd)">
          Element 'kwd-group': Unexpected element compounded-kwd.
      </assert>
    </rule>
  </pattern>

  <pattern id="kwd-group_lang">
    <title>
      Make sure all kwd-group elements have xml:lang attribute.
    </title>

    <rule context="article/front/article-meta/kwd-group">
      <assert test="@xml:lang">
        Element 'kwd-group': Missing attribute xml:lang.
      </assert>  
    </rule>
  </pattern>

  <pattern id="article-id_doi_value">
    <title>
      Only accept DOI's in its raw format.
      regex: /^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i
      source: https://www.crossref.org/blog/dois-and-matching-regular-expressions/
    </title>

    <rule context="article/front/article-meta/article-id[@pub-id-type='doi']">
      <assert test="regexp:test(current(), '(\s+|^)10.(\d{4}|\d{5}|\d{6}|\d{7}|\d{8}|\d{9})/[-._;()/:a-zA-Z0-9]+(\s+|$)')">
        Element 'article-id[@pub-id-type="doi"]': Invalid value '<value-of select="current()"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="article-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/article-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="article-id_attributes">
    <title>
      Mandatory attributes are present.
    </title>
    <rule context="article/front/article-meta/article-id">
      <assert test="@pub-id-type">
        Element 'article-id': Missing attribute @pub-id-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="article-id_pub-id-type_values">
    <title>
      Values are known.
    </title>
    <rule context="article/front/article-meta/article-id[@pub-id-type]">
      <assert test="@pub-id-type = 'doi' or 
                    @pub-id-type = 'publisher-id'">
        Element 'article-id', attribute pub-id-type: Invalid value "<value-of select="@pub-id-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="history_has_date">
    <rule context="article/front/article-meta/history">
      <assert test="date">
        Element 'history': Missing elements date.
      </assert>
    </rule>
  </pattern>

  <pattern id="history">
    <title>
      Restrict the valid values of history/date/[@date-type].
    </title>

    <rule context="article/front/article-meta/history/date">
      <assert test="@date-type = 'received' or 
                    @date-type = 'accepted' or
                    @date-type = 'corrected' or
                    @date-type = 'published' or
                    @date-type = 'preprint' or
                    @date-type = 'retracted' or
                    @date-type = 'review-requested' or
                    @date-type = 'review-received'">
        Element 'date', attribute date-type: Invalid value "<value-of select="@date-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="fpage_or_elocation-id">
    <rule context="article/front/article-meta">
      <assert test="fpage or elocation-id">
        Element 'article-meta': Missing elements fpage or elocation-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="fpage_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/fpage"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="lpage_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/lpage"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="elocation-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/elocation-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="month">
    <title>
      Only integers between 1 and 12.
    </title>

    <rule context="//month">
      <assert test="regexp:test(current(), '^(0?[1-9]{1}|[10-12]{2})$')">
        Element 'month': Invalid value '<value-of select="current()"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="month_cardinality_element-citation" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation"/>
    <param name="element" value="month"/>
  </pattern>

  <pattern id="month_cardinality_article-meta" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/front/article-meta/pub-date"/>
    <param name="element" value="month"/>
  </pattern>

  <pattern id="pub-date_must_have_date-type_pub">
    <title>
      Element pub-date must have one occurrence with @pub-type=pub.
    </title>

    <rule context="article/front/article-meta">
      <assert test="pub-date[@date-type='pub']">
          Element 'article-meta': Expected element pub-date with attribute date-type=pub.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_must_have_date-type_issue">
    <title>
      Element pub-date must have one occurrence with pub-type=issue.
    </title>

    <rule context="article/front/article-meta">
      <assert test="pub-date[@date-type='issue']">
          Element 'article-meta': Expected element pub-date with attribute date-type=issue.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_with_date-type_equal_pub_must_have_publication-format">
    <title>
      pub-date elements with attribute date-type=pub must have attribute publication-format.
    </title>

    <rule context="article/front/article-meta/pub-date[@date-type='pub']">
      <assert test="@publication-format">
          Element 'pub-date': Missing Attribute @publication-format.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_must_have_date-type">
    <title>
      pub-date elements must have attribute date-type.
    </title>

    <rule context="article/front/article-meta/pub-date">
      <assert test="@date-type">
          Element 'pub-date': Missing Attribute @date-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_publication_format">
    <title>
      Restrict the valid values of pub-date[@publication-format].
    </title>

    <rule context="article/front/article-meta/pub-date[@date-type='pub']">
      <assert test="@publication-format = 'epub' or
                    @publication-format = 'epub-ppub'">
        Element 'pub-date', attribute publication-format: Invalid value "<value-of select="@publication-format"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_date_type">
    <title>
      Restrict the valid values of pub-date[@date-type]. They are all the suggested values in JATS 1.1 plus the value "issue" requested by Érudit PS.
    </title>

    <rule context="article/front/article-meta/pub-date">
      <assert test="@date-type = 'pub' or
                    @date-type = 'issue'">
        Element 'pub-date', attribute date-type: Invalid value "<value-of select="@date-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="volume_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/volume"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="volume_cardinality_at_element-citation" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation"/>
    <param name="element" value="volume"/>
  </pattern>

  <pattern id="volume_cardinality_at_article-meta" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/front/article-meta"/>
    <param name="element" value="volume"/>
  </pattern>

  <pattern id="volume_cardinality_at_product" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/front/article-meta/product"/>
    <param name="element" value="volume"/>
  </pattern>

  <pattern id="issue_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/issue"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="issue_cardinality_at_element-citation" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation"/>
    <param name="element" value="issue"/>
  </pattern>

  <pattern id="issue_cardinality_at_article-meta" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/front/article-meta"/>
    <param name="element" value="issue"/>
  </pattern>

  <pattern id="issue_cardinality_at_product" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/front/article-meta/product"/>
    <param name="element" value="issue"/>
  </pattern>

  <pattern id="fn-group_has_fn">
    <rule context="article/back/fn-group">
      <assert test="fn">
        Element 'fn-group': Missing element fn.
      </assert>
    </rule>
  </pattern>

  <pattern id="fn_has_id">
    <rule context="article/back/fn-group/fn">
      <assert test="@id">
        Element 'fn': Missing attribute @id.
      </assert>
    </rule>
  </pattern>

  <pattern id="app_has_id">
    <rule context="article/back/app-group/app">
      <assert test="@id">
        Element 'app': Missing attribute @id.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-id_doi_value">
    <title>
      Only accept DOI's in its raw format.
      regex: /^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i
      source: https://www.crossref.org/blog/dois-and-matching-regular-expressions/
    </title>

    <rule context="article/back/ref-list/ref/element-citation/pub-id[@pub-id-type='doi']">
      <assert test="regexp:test(current(), '^10.(\d{4}|\d{5}|\d{6}|\d{7}|\d{8}|\d{9})/[-._;()/:a-zA-Z0-9]+$')">
        Element 'pub-id[@pub-id-type="doi"]': Invalid value '<value-of select="current()"/>'.
      </assert>
    </rule>
  </pattern>

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
                    @journal-id-type = 'ojs' or 
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

