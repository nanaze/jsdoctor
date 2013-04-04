import jsdoc
import unittest

class JsDocTestCase(unittest.TestCase):

  def testProcessComment(self):
    descriptions, flags = jsdoc.ProcessComment(_SCRIPT)

    self.assertEquals([
      ('@flag', 'Thing thing'),
      ('@flag2', 'More thing.'),
      ('@flag3', 'More thing and\nmore thing.'),
      ('@flag4', 'One last thing.')],
      flags)

    self.assertEquals(
      ['This is a comment.', 'End of thing.'],
      descriptions)

  def testSplitSections(self):
    parts = list(jsdoc._YieldSections(_SCRIPT))
    self.assertEquals(
      ['@flag Thing thing',
       'This is a comment.',
       '@flag2 More thing.\n@flag3 More thing and\nmore thing.',
       'End of thing.\n@flag4 One last thing.'],
       parts)

  def testMatchFlags(self):
    matches = jsdoc._MatchFlags(_SCRIPT)
    flags = [match.group('flag') for match in matches]
    self.assertEquals(
      ['@flag', '@flag2', '@flag3', '@flag4'],
      flags)
    
_SCRIPT = """\
@flag Thing thing


This is a comment.

@flag2 More thing.
@flag3 More thing and
more thing.

End of thing.
@flag4 One last thing.
"""

if __name__ == '__main__':
  unittest.main()



