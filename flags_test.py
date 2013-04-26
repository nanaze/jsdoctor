
import flags
import unittest
import re

class FlagTestCase(unittest.TestCase):

  def testParseParamDescription(self):

    desc = '{!bbb|ccc?} aaa This \nis the desc.  '
    self.assertEquals(
      ('aaa', '!bbb|ccc?', 'This \nis the desc.'),
      flags.ParseParameterDescription(desc))

    desc = '{...*} var_args The items to substitute into the pattern.'
    self.assertEquals(
      ('var_args', '...*', 'The items to substitute into the pattern.'),
      flags.ParseParameterDescription(desc))

    self.assertRaises(
      ValueError, 
      lambda: flags.ParseParameterDescription('desc without type'))

  def testParseReturnDescription(self):

    desc = '  {!bbb|ccc?} This \nis the desc.   '
    self.assertEquals(
      ('!bbb|ccc?', 'This \nis the desc.'),
      flags.ParseReturnDescription(desc))

    self.assertRaises(
      ValueError, 
      lambda: flags.ParseReturnDescription('desc without type'))
  
    
if __name__ == '__main__':
    unittest.main()



