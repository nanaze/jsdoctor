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
    self.assertEquals('goog.aaa.bbb', symbol.identifier)
    self.assertEquals('goog.aaa', symbol.namespace)    

    comment = symbol.comment
    self.assertEquals('Testing testing.\n@return {string} Dog.', comment.text)

    self.assertEquals(['Testing testing.'], comment.description_sections)

    self.assertEquals(1, len(comment.flags))

    flag = comment.flags[0]
    self.assertEquals('@return', flag.name)
    self.assertEquals('{string} Dog.', flag.text)

  def testIsIgnorableIdentifier(self):
    match = scanner.FindCommentTarget('  aaa.bbb = 3');
    self.assertEquals('aaa.bbb', match.group())
    self.assertFalse(source._IsIgnorableIdentifier(match))

    match = scanner.FindCommentTarget('  aaa.bbb(3)');
    self.assertEquals('aaa.bbb', match.group())
    self.assertTrue(source._IsIgnorableIdentifier(match))

    match = scanner.FindCommentTarget('  aaa.bbb[3])');
    self.assertEquals('aaa.bbb', match.group())
    self.assertTrue(source._IsIgnorableIdentifier(match))

  def testScanPrototypeProperty(self):
    test_source = source.ScanScript("""\
goog.provide('abc.Def');

/**
 * Test.
 */
abc.Def.prototype.ghi;
""")
    symbol = list(test_source.symbols)[0]
    self.assertEquals('ghi', symbol.property)
    
_TEST_SCRIPT = """
goog.provide('goog.aaa');
goog.provide('goog.bbb');

goog.require('goog.ccc');
goog.require('goog.ddd');

/**
 * Testing testing.
 * @return {string} Dog.
 */
goog.aaa.bbb;
"""

if __name__ == '__main__':
    unittest.main()



