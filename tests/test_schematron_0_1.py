# coding: utf-8
from __future__ import unicode_literals
import unittest
import io

from lxml import isoschematron, etree

from packtools.catalogs import catalog


SCH = etree.parse(catalog.SCHEMAS['eps-0.1'])


def TestPhase(phase_name, cache):
    """Factory of parsed Schematron phases.

    :param phase_name: the phase name
    :param cache: mapping type
    """
    if phase_name not in cache:
        phase = isoschematron.Schematron(SCH, phase=phase_name)
        cache[phase_name] = phase

    return cache[phase_name]


class PhaseBasedTestCase(unittest.TestCase):
    cache = {}

    def _run_validation(self, sample):
        schematron = TestPhase(self.sch_phase, self.cache)
        return schematron.validate(etree.parse(sample))


class CollabTests(PhaseBasedTestCase):
    """Tests for //contrib-id element.
    """
    sch_phase = 'phase.collab'

    def test_case_1(self):
        """
        valid minimum collab
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="group">
                            <collab>
                              <named-content content-type="name">The Mouse Fenome Sequening Consortium</named-content>
                            </collab>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        invalid minimum collab with empty named-content
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="group">
                            <collab>
                              <named-content content-type="name"></named-content>
                            </collab>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

class ContribIdTests(PhaseBasedTestCase):
    """Tests for //contrib-id element.
    """
    sch_phase = 'phase.contrib-id'

    def test_case_1(self):
        """
        valid @contrib-id-type=orcid in contrib-id
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <contrib-id contrib-id-type="orcid">0000-0003-2125-060X</contrib-id>
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        invalid contrib-id wihtout value
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <contrib-id contrib-id-type="orcid"></contrib-id>
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_3(self):
        """
        invalid contrib-id with contrib-id-type not allowed
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <contrib-id contrib-id-type="xxx"></contrib-id>
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_4(self):
        """
        invalid contrib-id with values that seems to be an URL
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-8528-2091</contrib-id>
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_5(self):
        """
        invalid contrib-id without contrib-id-type.
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <contrib-id>0000-0001-8528-2091</contrib-id>
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ContribTests(PhaseBasedTestCase):
    """Tests for //contrib element.
    """
    sch_phase = 'phase.contrib'

    def test_case_1(self):
        """
        valid @contrib-type=person in contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="person">
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        valid @contrib-type=group in contrib

        According to JATS4M contrib-type=group must have a element collab inside
        see: https://github.com/substance/dar/blob/master/DarArticle.md#contrib-group
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="group">
                            <collab>
                              <contrib-group>
                                <contrib>
                                  <name>
                                    <surname>Arrighi</surname>
                                    <given-names>Laurence</given-names>
                                  </name>
                                </contrib>
                              </contrib-group>
                            </collab>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_3(self):
        """
        invalid @contrib-type=group in contrib

        According to JATS4M contrib-type=group must have a element collab inside
        see: https://github.com/substance/dar/blob/master/DarArticle.md#contrib-group
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                    <front>
                      <article-meta>
                        <contrib-group>
                          <contrib contrib-type="group">
                            <name>
                              <surname>Arrighi</surname>
                              <given-names>Laurence</given-names>
                            </name>
                          </contrib>
                        </contrib-group>
                      </article-meta>
                    </front>
                  </article>
               """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_4(self):
        """
        invalid @contrib-type in  contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib contrib-type="unknow">
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_5(self):
        """
        valid contrib without @contrib-type
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_6(self):
        """
        invalid element aff not authorized in contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                              <aff>
                              </aff>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_7(self):
        """
        invalid element aff-alternatives not authorized in contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                              <aff-alternatives>
                                <aff></aff>
                              </aff-alternatives>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ContribGroupTests(PhaseBasedTestCase):
    """Tests for //contrib-group element.
    """
    sch_phase = 'phase.contrib-group'

    def test_case_1(self):
        """
        valid @content-type in contrib-group
        """
        for data in ['author', 'editor']:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                        <front>
                          <article-meta>
                            <contrib-group content-type="%s">
                              <contrib>
                                <name>
                                  <surname>Arrighi</surname>
                                  <given-names>Laurence</given-names>
                                </name>
                              </contrib>
                            </contrib-group>
                          </article-meta>
                        </front>
                      </article>
                   """ % data
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        invalid @content-type in  contrib-group
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group content-type="unknow">
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_3(self):
        """
        valid contrib-group without @content-type
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_4(self):
        """
        invalid element aff not authorized in contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                            <aff>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_5(self):
        """
        invalid element aff-alternatives not authorized in contrib
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                            <aff-alternatives>
                              <aff></aff>
                            </aff-alternatives>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class NameTests(PhaseBasedTestCase):
    """Tests for //name element.
    """
    sch_phase = 'phase.name'

    def test_case_1(self):
        """
        valid author name
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        invalid author name, surname empty
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname></surname>
                                <given-names>Laurence</given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_3(self):
        """
        invalid author name, given-names empty
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names></given-names>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_4(self):
        """
        invalid author name, prefix empty
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurance</given-names>
                                <prefix></prefix>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_5(self):
        """
        invalid author name, suffix empty
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <name>
                                <surname>Arrighi</surname>
                                <given-names>Laurance</given-names>
                                <prefix>Dr.</prefix>
                                <suffix></suffix>
                              </name>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class PermissionsTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/permissions/license element.
    """
    sch_phase = 'phase.permissions'

    def test_missing_permissions_elem(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_license(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


    def test_permissions_within_elements_of_the_body(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Fig. 1</label>
                              <caption>
                                <title>título da imagem</title>
                              </caption>
                              <graphic xlink:href="image.tif"/>
                              <permissions>
                                <copyright-statement>Copyright © 2014 Érudit</copyright-statement>
                                <copyright-year>2014</copyright-year>
                                <copyright-holder>Érudit</copyright-holder>
                                <license xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
                                         xml:lang="en">
                                  <license-p>This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.</license-p>
                                </license>
                              </permissions>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_irrestrict_use_licenses_within_elements_in_the_body(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Fig. 1</label>
                              <caption>
                                <title>título da imagem</title>
                              </caption>
                              <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                              <permissions>
                                <copyright-statement>Copyright © 2014 Érudit</copyright-statement>
                                <copyright-year>2014</copyright-year>
                                <copyright-holder>Érudit</copyright-holder>
                                <license xlink:href="http://creativecommons.org/licenses/by/2.0/"
                                         xml:lang="en">
                                  <license-p>This is an open-access article distributed under the terms of...</license-p>
                                </license>
                              </permissions>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_main_article_copyright_info(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <copyright-statement>Copyright © 2014 Érudit</copyright-statement>
                            <copyright-year>2014</copyright-year>
                            <copyright-holder>Érudit</copyright-holder>
                            <license xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_main_article_copyright_info_translations(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <copyright-statement>Copyright © 2014 Érudit</copyright-statement>
                            <copyright-year>2014</copyright-year>
                            <copyright-holder>Érudit</copyright-holder>
                            <license xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                            <license xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="pt">
                              <license-p>
                                Este é um artigo em acesso aberto distribuido sob os termos...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

class TransAbstractTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/abstract elements.
    """
    sch_phase = 'phase.trans-abstract'

    def test_is_present_with_p(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <trans-abstract xml:lang="fr">
                            <p>Cet article a pour objectif d’analyser...</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_absense_of_p_or_sec(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <trans-abstract xml:lang="fr">
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_is_present_with_sec(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <trans-abstract xml:lang="fr">
                            <sec>
                              <title>Sec Title</title>
                              <p>Sec content</p>
                            </sec>
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_without_lang(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article>
                      <front>
                        <article-meta>
                          <trans-abstract>
                            <p>Cet article a pour objectif d’analyser...</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AbstractTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/abstract elements.
    """
    sch_phase = 'phase.abstract'

    def test_is_present_with_p(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <abstract xml:lang="fr">
                            <p>Cet article a pour objectif d’analyser...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_absense_of_p_or_sec(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <abstract xml:lang="fr">
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_is_present_with_sec(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <abstract xml:lang="fr">
                            <sec>
                              <title>Sec Title</title>
                              <p>Sec content</p>
                            </sec>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_without_lang(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article>
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Cet article a pour objectif d’analyser...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class KwdTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/kwd-group/kwd elements.
    """
    sch_phase = 'phase.kwd'

    def test_ok(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_content(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd></kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class KwdGroupTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/kwd-group elements.
    """
    sch_phase = 'phase.kwd-group'

    def test_unespected_nested_kwd(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                            <nested-kwd>
                                <kwd>nested keyword</kwd>
                            </nested-kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_unespected_compounded_kwd(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                            <compounded-kwd>
                                <kwd>nested keyword</kwd>
                            </compounded-kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_title(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_single_occurence(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="fr">
                            <title>Mots-clés</title>
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_single_occurence_missing_lang(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <title>Mots-clés</title>
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_many_occurencies(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="en">
                            <title>Keywords</title>
                            <kwd>Canadian Francophone minority</kwd>
                            <kwd>language quality</kwd>
                          </kwd-group>
                          <kwd-group xml:lang="ft">
                            <title>Mots-clés</title>
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_many_occurencies_without_lang(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <title>Keywords</title>
                            <kwd>Canadian Francophone minority</kwd>
                            <kwd>language quality</kwd>
                          </kwd-group>
                          <kwd-group>
                            <title>Mots-clés</title>
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_some_occurencies_without_lang(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <title>Keywords</title>
                            <kwd>Canadian Francophone minority</kwd>
                            <kwd>language quality</kwd>
                          </kwd-group>
                          <kwd-group xml:lang="ft">
                            <title>Mots-clés</title>
                            <kwd>francophonie minoritaire canadienne</kwd>
                            <kwd>qualité de la langue</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

class ArticleIdTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/article-id elements.
    """
    sch_phase = 'phase.article-id'

    def test_article_id_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_pub_id_type_doi_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='publisher-id'>128129ar</article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_pub_id_type_doi(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'>10.1590/1414-431X20143434</article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_pub_id_type_doi_is_empty(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'/>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_pub_id_type(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='unknown'>10.1590/1414-431X20143434</article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_pub_id_type_case2(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='unknown'>10.1590/1414-431X20143434</article-id>
                          <article-id pub-id-type='doi'>10.1590/1414-431X20143434</article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_valid_pub_id_type_values(self):
        for typ in ['doi', 'publisher-id']:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <article-id pub-id-type='%s'>10.1590/1414-431X20143433</article-id>
                              <article-id pub-id-type='doi'>10.1590/1414-431X20143434</article-id>
                            </article-meta>
                          </front>
                        </article>
                     """ % typ
            sample = io.BytesIO(sample.encode('utf-8'))
            self.assertTrue(self._run_validation(sample))

    def test_invalid_doi(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'>
                            https://dx.doi.org/10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_doi_with_white_spaces_and_line_breaks(self):
        """
        DOI's must not have white spaces or line breaks
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))


class HistoryTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/history
    """
    sch_phase = 'phase.history'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_date_type_allowed_values(self):
        for pub_type in ['accepted', 'corrected', 'published', 'preprint',
                'retracted', 'received', 'review-received', 'review-requested']:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <history>
                                <date date-type="%s">
                                  <day>17</day>
                                  <month>03</month>
                                  <year>2014</year>
                                </date>
                              </history>
                            </article-meta>
                          </front>
                        </article>
                     """ % pub_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_date_type_disallowed_values(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="invalid">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_date_type_allowed_values_multi(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                            <date date-type="accepted">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class fpage_OR_elocationTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/fpage or elocation-id elements.
    """
    sch_phase = 'phase.fpage_or_elocation-id'

    def test_case1(self):
        """
        fpage is True
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        fpage is True
        elocation-id is False
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        fpage is False
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        fpage is False
        elocation-id is False
        fpage v elocation-id is False
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_fpage(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage></fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_lpage(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>33</fpage>
                          <lpage></lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_elocationid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id></elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class MonthTests(PhaseBasedTestCase):
    """Tests for //month elements.
    """
    sch_phase = 'phase.month'

    def test_range_1_12(self):
        for month in range(1, 13):
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date>
                                <month>%s</month>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % month
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_range_01_12(self):
        for month in range(1, 13):
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date>
                                <month>%02d</month>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % month
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_out_of_range(self):

        sample = u"""<article>
                      <front>
                        <article-meta>
                          <pub-date>
                            <month>13</month>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_must_be_integer(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <pub-date>
                            <month>January</month>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_is_present_in_elementcitation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <month>02</month>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_twice_in_elementcitation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <month>02</month>
                              <month>02</month>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_is_absent_in_elementcitation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class PubDateTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/pub-date elements.
    """
    sch_phase = 'phase.pub-date'

    def test_pub_type_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <pub-date>
                            <day>17</day>
                            <month>03</month>
                            <year>2014</year>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_pub_type_allowed_values(self):
        for pub_type in ['epub', 'epub-ppub']:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date pub-type="%s">
                                <day>17</day>
                                <month>03</month>
                                <year>2014</year>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % pub_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_pub_type_disallowed_value(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <pub-date pub-type="wtf">
                            <day>17</day>
                            <month>03</month>
                            <year>2014</year>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class IssueTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/issue
      - article/back/ref-list/ref/element-citation/issue
    """
    sch_phase = 'phase.issue'

    def test_absent_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue></issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue>10</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_in_front_cardinality_error(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue>10</issue>
                          <issue>10</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class VolumeTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/volume
      - article/back/ref-list/ref/element-citation/volume
    """
    sch_phase = 'phase.volume'

    def test_absent_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <volume></volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <volume>10</volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_in_front_cardinality_error(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <volume>10</volume>
                          <volume>10</volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ElementFnGroupTests(PhaseBasedTestCase):
    sch_phase = 'phase.fn-group'

    def test_case_1(self):
        """
        fn have @id
        """
        sample = u"""<article>
                      <back>
                        <fn-group>
                          <fn id="fn1">
                            <title>Footnote Title</title>
                            <p>Footnote Content</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        fn must have @id
        """
        sample = u"""<article>
                      <back>
                        <fn-group>
                          <fn>
                            <title>Footnote Title</title>
                            <p>Footnote Content</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_3(self):
        """
        fn-group must have at least one element fn
        """
        sample = u"""<article>
                      <back>
                        <fn-group>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ElementAppTests(PhaseBasedTestCase):
    sch_phase = 'phase.app'

    def test_case_1(self):
        """
        app have @id
        """
        sample = u"""<article>
                      <back>
                        <app-group>
                          <app id="app1">
                            <title>Appendix Title</title>
                            <p>Appendix Content</p>
                          </app>
                        </app-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        app must have @id
        """
        sample = u"""<article>
                      <back>
                        <app-group>
                          <app>
                            <title>Appendix Title</title>
                            <p>Appendix Content</p>
                          </app>
                        </app-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ElementPubIDTests(PhaseBasedTestCase):

    sch_phase = 'phase.pub-id'

    def test_case_1(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                              <pub-id pub-id-type="doi">10.1019/anydoi.123</pub-id>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case_2(self):
        """
        pub-id must have @pub-id-type
        """
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                              <pub-id>10.1019/anydoi.123</pub-id>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case_3(self):
        """
        pub-id must have content
        """
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                              <pub-id pub-id-type="doi">
                              </pub-id>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ElementCitationTests(PhaseBasedTestCase):
    """Tests for article/back/ref-list/ref element.
    """
    sch_phase = 'phase.element-citation'

    def test_element_citation_has_styled_content(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_element_citation_hasnot_styled_content(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class RefTests(PhaseBasedTestCase):
    """Tests for article/back/ref-list/ref element.
    """
    sch_phase = 'phase.ref'

    def test_element_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_element_citation_cannot_be_present_twice(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref id="R57">
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                            </element-citation>
                            <element-citation publication-type="journal">
                              <styled-content specific-use="display">
                                Traisnel, C. et Violette, I. (2010). Qui ça, nous? La question des identités multiples dans l'aménagement d'une représentation de la francophonie en Acadie du Nouveau-Brunswick. In Bélanger, N., Garant, N., Dalley, P. et Desabrais, P. (dir.). Produire et reproduire la francophonie en la nommant. Sudbury : Prise de parole. 101-122.
                              </styled-content>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_element_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AckTests(PhaseBasedTestCase):
    """Tests for article/back/ack element.
    """
    sch_phase = 'phase.ack'

    def test_with_sec(self):
        sample = u"""<article>
                      <back>
                        <ack>
                          <sec>
                            <p>Some</p>
                          </sec>
                        </ack>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_without_sec(self):
        sample = u"""<article>
                      <back>
                        <ack>
                          <title>Acknowledgment</title>
                          <p>Some text</p>
                        </ack>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class JournalIdTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-id elements.

    Ticket #1 makes @journal-id-type="publisher-id" mandatory.
    """
    sch_phase = 'phase.journal-id'

    def test_case1(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher">
                            RUM
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case2(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="erudit">
                            RUM
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        presence(@publisher-id) is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type='doi'>
                            123.plin
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_erudit_id_cannot_be_empty(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="erudit"></journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ISSNTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/issn elements.
    """
    sch_phase = 'phase.issn'

    def test_case1(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub">
                            1712-2139
                          </issn>
                          <issn pub-type="ppub">
                            0316-6368
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is False
        A v B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub">
                            1712-2139
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="ppub">
                            0316-6368
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is False
        A v B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn>
                            1712-2139
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is False
        A v B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn>
                            0316-6368
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_issn(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub"></issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_regex_case1(self):
        """
        Testing a invalid ISSN
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                            <issn pub-type="epub">1234-123A</issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_regex_case2(self):
        """
        Testing a valid ISSN with X
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                            <issn pub-type="epub">1234-123X</issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_regex_case3(self):
        """
        Testing a valid ISSN with x (lower)
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                            <issn pub-type="epub">1234-123x</issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_regex_case4(self):
        """
        Testing a valid ISSN finishing with a number
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                            <issn pub-type="epub">1234-1234</issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ArticleAttributesTests(PhaseBasedTestCase):
    """Tests for article element.
    """
    sch_phase = 'phase.article-attrs'

    def test_allowed_article_types(self):
        for art_type in [
                'addendum', 'research-article', 'review-article',
                'letter', 'article-commentary', 'brief-report', 'rapid-communication',
                'oration', 'discussion', 'editorial', 'interview', 'correction',
                'guidelines', 'other', 'obituary', 'case-report', 'book-review',
                'reply', 'retraction', 'partial-retraction', 'clinical-trial',
                'announcement', 'calendar', 'in-brief', 'book-received', 'news',
                'reprint', 'meeting-report', 'abstract', 'product-review',
                'dissertation', 'translation'
        ]:

            sample = u"""<article article-type="%s" xml:lang="en" dtd-version="1.1" specific-use="eps-0.1">
                        </article>
                     """ % art_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_article_type(self):
        sample = u"""<article article-type="invalid" dtd-version="1.1" specific-use="eps-0.1">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_article_type(self):
        sample = u"""<article xml:lang="en" dtd-version="1.1" specific-use="eps-0.1">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_xmllang(self):
        sample = u"""<article article-type="research-article" dtd-version="1.1" specific-use="eps-0.1">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_dtdversion(self):
        sample = u"""<article article-type="research-article" xml:lang="en" specific-use="eps-0.1">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_sps_version(self):
        sample = u"""<article article-type="research-article" dtd-version="1.1" xml:lang="en">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_sps_version(self):
        sample = u"""<article article-type="research-article" dtd-version="1.1" xml:lang="en" specific-use="sps-1.0">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class PublisherTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/publisher elements.
    """
    sch_phase = 'phase.publisher'

    def test_publisher_is_present(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <publisher>
                            <publisher-name>Revue de l'Université de Moncton</publisher-name>
                          </publisher>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_publisher_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_publisher_is_empty(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <publisher>
                            <publisher-name></publisher-name>
                          </publisher>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class JournalMetaTests(PhaseBasedTestCase):

    """Tests for article/front/journal-meta elements.
    """
    sch_phase = 'phase.journal-meta'

    def test_case1(self):
        """
        A: presence(journal-id[@journal-group-id="erudit"]) is False
        B: presence(journal-title-group) is False
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>

                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case2(self):
        """
        A: presence(journal-id[@journal-group-id="erudit"]) is True
        B: presence(journal-title-group) is False
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="erudit">rum</journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        A: presence(journal-id[@journal-group-id="erudit"]) is False
        B: presence(journal-title-group) is True
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group></journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        A: presence(journal-id[@journal-group-id="erudit"]) is True
        B: presence(journal-title-group) is True
        A ^ B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="erudit">rum</journal-id>
                          <journal-title-group></journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case5(self):
        """
        A: presence(journal-id[@journal-group-id="erudit"]) is False
        B: presence(journal-title-group) is True
        A ^ B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher">rum</journal-id>
                          <journal-title-group></journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class JournalTitleGroupTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-title-group elements.
    """
    sch_phase = 'phase.journal-title-group'

    def test_case1(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title xml:lang="fr">
                              Revue de l'Université de Moncton
                            </journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_journal_title(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title xml:lang="fr"></journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_journal_title_without_lang(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>Revue de l'Université de Moncton</journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class TransTitleGroupTests(PhaseBasedTestCase):
    sch_phase = 'phase.trans-title-group'

    def test_lang_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <trans-title-group>
                              <trans-title>
                                Journal of the University of Moncton
                              </trans-title>
                            </trans-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_lang_is_present(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <trans-title-group xml:lang="en">
                              <trans-title>
                                Journal of the University of Moncton
                              </trans-title>
                            </trans-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class TransTitleTests(PhaseBasedTestCase):
    sch_phase = 'phase.trans-title'

    def test_lang_trans_title_is_present(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <trans-title-group>
                              <trans-title xml:lang="en">
                                Journal of the University of Moncton
                              </trans-title>
                            </trans-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_lang_trans_title_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <trans-title-group>
                              <trans-title>
                                Journal of the University of Moncton
                              </trans-title>
                            </trans-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class XrefRidTests(PhaseBasedTestCase):
    """Tests for //xref[@rid]
    """
    sch_phase = 'phase.rid_integrity'

    def test_mismatching_rid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <xref ref-type="aff" rid="aff1">
                                <sup>I</sup>
                              </xref>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_matching_rid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <xref ref-type="aff" rid="aff1">
                                <sup>I</sup>
                              </xref>
                            </contrib>
                          </contrib-group>
                          <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">
                              Secretaria Municipal de Saude de Belo Horizonte
                            </institution>
                            <addr-line>
                              <named-content content-type="city">Belo Horizonte</named-content>
                              <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">
                              Secretaria Municipal de Saude de Belo Horizonte. Belo Horizonte, MG, Brasil
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_mismatching_reftype(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <table-wrap id="t01">
                          </table-wrap>
                        </sec>
                        <sec>
                          <p>
                            <xref ref-type="aff" rid="t01">table 1</xref>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class XrefRefTypeTests(PhaseBasedTestCase):
    """Tests for //xref[@ref-type]
    """
    sch_phase = 'phase.xref_reftype_integrity'

    def test_allowed_ref_types(self):
        for reftype in ['aff', 'app', 'author-notes', 'bibr', 'contrib',
                        'corresp', 'disp-formula', 'fig', 'fn', 'sec',
                        'supplementary-material', 'table', 'table-fn',
                        'boxed-text']:
            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <xref ref-type="%s">foo</xref>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % reftype
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_ref_types(self):
        for reftype in ['chem', 'kwd', 'list', 'other', 'plate'
                        'scheme', 'statement']:
            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <xref ref-type="%s">foo</xref>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % reftype
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertFalse(self._run_validation(sample))
