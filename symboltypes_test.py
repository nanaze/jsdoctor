import symboltypes
import scanner
import source
import unittest

def _GetFirstSymbol(script):
  return _GetSymbols(script)[0]

def _GetSymbols(script):
  match_pairs = scanner.ExtractDocumentedSymbols(script)
  return list(source._YieldSymbols(match_pairs, set(['goog'])))

class SymbolTypesTestCase(unittest.TestCase):
  def assertSymbolType(self, type, script):
    symbol = _GetSymbols(script)[0]
    self.assertEquals(type, symboltypes.DetermineSymbolType(symbol))

  def testDetermineSymbolType(self):
    self.assertSymbolType(symboltypes.PROPERTY, """
/**
 * Cat's cradle.
 */
goog.bar.baz
""")

    self.assertSymbolType(symboltypes.FUNCTION, """
/**
 * @param foo
 */
goog.bar.baz
""")

    self.assertSymbolType(symboltypes.FUNCTION, """
/**
 * @return foo
 */
goog.bar.baz
""")

    self.assertSymbolType(symboltypes.ENUM, """
/**
 * @enum {string}
 */
goog.bar.baz
""")

    self.assertSymbolType(symboltypes.CONSTRUCTOR, """
/**
 * @constructor
 */
goog.bar.baz
""")

    self.assertSymbolType(symboltypes.INTERFACE, """
/**
 * @interface
 */
goog.bar.baz
""")      

    
      
    






if __name__ == '__main__':
  unittest.main()



