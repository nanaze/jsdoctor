import scanner
import unittest

class ScannerTestCase(unittest.TestCase):

  def testProvides(self):
    source = """
goog.provide('goog.dom');
goog.provide('goog.style');

goog.require('goog.array');
goog.require('goog.string');
"""
    provides = list(scanner.YieldProvides(source))
    requires = list(scanner.YieldRequires(source))

    self.assertEquals(['goog.dom', 'goog.style'], provides)
    self.assertEquals(['goog.array', 'goog.string'], requires)


  def testFindDocComments(self):
    matches = list(scanner.FindJsDocComments(_TEST_SCRIPT))
    self.assertEquals(1, len(matches))

    match = matches[0]
    self.assertEquals(10, match.start())
    self.assertEquals(34, match.end())

  def testFindIdentifier(self):
    match = list(scanner.FindJsDocComments(_TEST_SCRIPT))[0]
    identifier_match = scanner.FindNextIdentifer(match.string, match.end())
    self.assertEquals('goog.bar.baz', identifier_match.group())

  def testExtractText(self):
    script = """
/**
 * Slaughterhouse five.
 *
 * @return {string} The result, as a string.
 */
"""
    
    match = list(scanner.FindJsDocComments(script))[0]
    comment = match.group()
    text = scanner.ExtractTextFromJsDocComment(comment)
    self.assertEquals('Slaughterhouse five.\n\n' +
                      '@return {string} The result, as a string.',
                      text)

  def testExtractDocumentedSymbols(self):
    script = """
/**
 * Test goog dom.
 *
 * One two three.
 */
goog.dom.test

/**
 * Test goog style.
 *
 * Four five six.
 */
goog.style.test
"""

    pairs = list(scanner.ExtractDocumentedSymbols(script))

    self.assertEquals(2, len(pairs))

    jsdoc, symbol = pairs[0]
    self.assertEquals(
      'Test goog dom.\n\nOne two three.',
      jsdoc.GetText())
    self.assertEquals('goog.dom.test', symbol.GetSymbol())

    jsdoc, symbol = pairs[1]
    self.assertEquals(
      'Test goog style.\n\nFour five six.',
      jsdoc.GetText())
    self.assertEquals('goog.style.test', symbol.GetSymbol())


  def testOddIdentifier(self):
    test_script = """\
/**
 * Moose.
 */
goog
.
bar.
baz   .
qux =
"""

    match = list(scanner.FindJsDocComments(test_script))[0]
    identifier_match = scanner.FindNextIdentifer(match.string, match.end())
    symbol = scanner.StripWhitespace(identifier_match.group())
    self.assertEquals('goog.bar.baz.qux', symbol)

_TEST_SCRIPT = """\
var = 2;

/**
 * Cat's cradle.
 */
goog.bar.baz
"""



if __name__ == '__main__':
    unittest.main()



