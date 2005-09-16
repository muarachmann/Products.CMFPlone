#
# Test toLocalizedTime script and TranslationServiceTool.
#
# Tries to cover http://plone.org/products/plone/roadmap/98
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

from DateTime.DateTime import DateTime
from zope.app.tests.placelesssetup import setUp, tearDown

class TestToLocalizedTime(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        setUp()
        self.script = self.portal.toLocalizedTime

    def testDateTimeArg(self):
        value = self.script(DateTime('Mar 9, 1997 1:45pm'),
                            long_format=True)
        # TranslationServiceTool falls back to time formats in site properties
        # because PTS isn't installed
        self.assertEquals(value, '1997-03-09 13:45')

    def testStringArg(self):
        value = self.script('Mar 9, 1997 1:45pm', long_format=True)
        # TranslationServiceTool falls back to time formats in site properties
        # because PTS isn't installed
        self.assertEquals(value, '1997-03-09 13:45')

    def beforeTearDown(self):
        tearDown()


class TestTranslationServiceTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        setUp()
        self.tool = self.portal.translation_service

    def testLocalized_time(self):
        value = self.tool.ulocalized_time('Mar 9, 1997 1:45pm',
                                         long_format=True)
        # TranslationServiceTool falls back to time formats in site properties
        # because PTS isn't installed
        self.assertEquals(value, '1997-03-09 13:45')

    def test_ulocalized_time_fetch_error(self):
        # http://plone.org/collector/4251
        error = "(Missing.Value,), {}"
	value = self.tool.ulocalized_time(error)
	self.failUnlessEqual(value, None)

    def beforeTearDown(self):
        tearDown()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestToLocalizedTime))
    suite.addTest(makeSuite(TestTranslationServiceTool))
    return suite

if __name__ == '__main__':
    framework()
