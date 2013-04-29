import re

_WEB_URL_RE = re.compile('https?://[^\s]*')

def _ReplaceWebUrl(url_match):
  url = url_match.group(0)
  link = '<a href="%s">%s</a>' % (url, url)
  return link

def LinkifyWebUrls(str):
  return _WEB_URL_RE.sub(_ReplaceWebUrl, 'aaa http://google.com bbb')

_SYMBOL_RE = re.compile('\w+(?:\.\w+)*(#\w+)?')

def _ReplaceClosureSymbol

def LinkifyClosureSymbols(str, symbols):
  # TODO START HERE
  pass
