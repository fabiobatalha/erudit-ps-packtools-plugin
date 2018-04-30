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


class JournalIdTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-id elements.

    Ticket #1 makes @journal-id-type="publisher-id" mandatory.
    """
    sch_phase = 'phase.journal-id'

    def test_case1(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="nlm-ta">
                            Rev Saude Publica
                          </journal-id>
                          <journal-id journal-id-type="publisher-id">
                            RSP
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="nlm-ta">
                            Rev Saude Publica
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher-id">
                            RSP
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        presence(@nlm-ta) is False
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

    def test_publisher_id_cannot_be_empty(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher-id"></journal-id>
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
                            0959-8138
                          </issn>
                          <issn pub-type="ppub">
                            0959-813X
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
                            0959-8138
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
                            0959-813X
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
                            0959-813X
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
                            0959-813X
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
                            <publisher-name>British Medical Journal</publisher-name>
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


class JournalTitleGroupTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-title-group elements.
    """
    sch_phase = 'phase.journal-title-group'

    def test_journal_title_group_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case1(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>
                              Revista de Saude Publica
                            </journal-title>
                            <abbrev-journal-title abbrev-type='erudit'>
                              Rev. Saude Publica
                            </abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>
                              Revista de Saude Publica
                            </journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <abbrev-journal-title abbrev-type='publisher'>
                              Rev. Saude Publica
                            </abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
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
                            <journal-title></journal-title>
                            <abbrev-journal-title abbrev-type='publisher'>Rev. Saude Publica</abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_abbrev_journal_title(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>Revista de Saude Publica</journal-title>
                            <abbrev-journal-title abbrev-type='publisher'></abbrev-journal-title>
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
