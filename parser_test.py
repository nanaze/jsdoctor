import parser
import unittest

class ParserTestCase(unittest.TestCase):

  def testFindDocComments(self):
    matches = list(parser.FindJsDocComments(_TEST_SCRIPT))
    self.assertEquals(1, len(matches))

    match = matches[0]
    self.assertEquals(10, match.start())
    self.assertEquals(34, match.end())

  def testFindIdentifier(self):
    match = list(parser.FindJsDocComments(_TEST_SCRIPT))[0]
    identifier_match = parser.FindIdentiferForComment(match)
    self.assertEquals('goog.bar.baz', identifier_match.group())


_TEST_SCRIPT = """\
var = 2;

/**
 * Cat's cradle.
 */
goog.bar.baz
"""

if __name__ == '__main__':
    unittest.main()



