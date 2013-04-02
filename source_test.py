import source
import unittest

class SourceTestCase(unittest.TestCase):

  def testScanSource(self):
    
    test_source = source.ScanScript(_TEST_SCRIPT)
    self.assertEquals(
      set(['goog.aaa', 'goog.bbb']), test_source.provides)
    self.assertEquals(
      set(['goog.ccc', 'goog.ddd']), test_source.requires)

    self.assertEquals(1, len(test_source.comments))

    comment = list(test_source.comments)[0]
    self.assertEquals('Testing testing.', comment.text)
    self.assertEquals('goog.aaa.bbb', comment.symbol.identifier)
    
_TEST_SCRIPT = """
goog.provide('goog.aaa');
goog.provide('goog.bbb');

goog.require('goog.ccc');
goog.require('goog.ddd');

/**
 * Testing testing.
 */
goog.aaa.bbb;
"""

if __name__ == '__main__':
    unittest.main()



