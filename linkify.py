import re

_WEB_URL_RE = re.compile('https?://[^\s]*')

def _ReplaceWebUrl(url_match):
  url = url_match.group(0)
  link = '<a href="%s">%s</a>' % (url, url)
  return link

def LinkifyWebUrls(content):
  return _WEB_URL_RE.sub(_ReplaceWebUrl, content)

_SYMBOL_RE = re.compile('(\w+(?:\.\w+)*)(#\w+)?')

def _ReplaceSymbol(match, symbols):
  full_match = match.group(0)
  symbol_portion = match.group(1)
  hash_portion = match.group(2)

  if symbol_portion in symbols:
    href = '%s.html' % symbol_portion

    if hash_portion:
      href + hash_portion

    return '<a href="%s">%s</a>' % (href, full_match)

  return full_match

def LinkifySymbols(content, symbols):
  return _SYMBOL_RE.sub(
      lambda match: _ReplaceSymbol(match, symbols),
      content)
