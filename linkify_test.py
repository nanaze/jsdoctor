import linkify
import unittest

class LinkifyTestCase(unittest.TestCase):
  def testWebRegEx(self):
    match = linkify._WEB_URL_RE.search('aaa http://google.com bbb')
    self.assertEquals('http://google.com', match.group(0))

  def testLinkifyWebUrls(self):
    self.assertEquals(
      'aaa <a href="http://google.com">http://google.com</a> bbb',
      linkify.LinkifyWebUrls('aaa http://google.com bbb'))

if __name__ == '__main__':
    unittest.main()



