import scanner
import source
import unittest

class SourceTestCase(unittest.TestCase):

  def testScanSource(self):
    
    test_source = source.ScanScript(_TEST_SCRIPT)
    self.assertEquals(
      set(['goog.aaa', 'goog.bbb']), test_source.provides)
    self.assertEquals(
      set(['goog.ccc', 'goog.ddd']), test_source.requires)

    self.assertEquals(1, len(test_source.symbols))

    symbol = list(test_source.symbols)[0]
    self.assertEquals('Testing testing.', symbol.comment.text)
    self.assertEquals('goog.aaa.bbb', symbol.identifier)

  def testIsMethodCall(self):
    match = scanner.FindNextIdentifer('  aaa.bbb = 3');
    self.assertEquals('aaa.bbb', match.group())
    self.assertFalse(source._IsMethodCall(match))

    match = scanner.FindNextIdentifer('  aaa.bbb(3)');
    self.assertEquals('aaa.bbb', match.group())
    self.assertTrue(source._IsMethodCall(match))
    
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



