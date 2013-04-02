import namespace
import unittest

class NamespaceTestCase(unittest.TestCase):

  def testGetNamespaceParts(self):
    self.assertEquals(
      ['goog', 'string', 'startsWith'],
      namespace.GetNamespaceParts('goog.string.startsWith'))

  def testIsSymbolPartOfNamespace(self):
    self.assertTrue(
      namespace.IsSymbolPartOfNamespace(
        'goog.string.startsWith',
        'goog.string'))

    self.assertFalse(
      namespace.IsSymbolPartOfNamespace(
        'goog.string',
        'goog.string.startsWith'))

    self.assertTrue(
      namespace.IsSymbolPartOfNamespace(
        'aaa.bbb.foo',
        'aaa.bbb.foo'))


if __name__ == '__main__':
    unittest.main()



