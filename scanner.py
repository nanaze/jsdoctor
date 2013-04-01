import re

class Symbol(object):
  def __init__(self, match):
    self.match = match

  def GetSymbol(self):
    return StripWhitespace(self.match.group())

class JsDoc(object):
  def __init__(self, match):
    self.match = match

  def GetComment(self):
    return self.match.group()

  def GetText(self):
    return ExtractTextFromJsDocComment(self.GetComment())

class NoIdentifierError(Exception):
  pass

_BASE_REGEX_STRING = '^\s*goog\.%s\(\s*[\'"](.+)[\'"]\s*\)'
_PROVIDE_REGEX = re.compile(_BASE_REGEX_STRING % 'provide')
_REQUIRES_REGEX = re.compile(_BASE_REGEX_STRING % 'require')

def YieldProvides(source):
  for line in source.splitlines():
    match = _PROVIDE_REGEX.match(line)
    if match:
      yield match.group(1)

def YieldRequires(source):
  for line in source.splitlines():
    match = _REQUIRES_REGEX.match(line)
    if match:
      yield match.group(1)
  
  

def ExtractDocumentedSymbols(script):

  for comment_match in FindJsDocComments(script):
    jsdoc = JsDoc(comment_match)

    identifier = FindNextIdentifer(script, comment_match.end())
    if not identifier:
      raise NoIdentiferFoundError(
        'Found no identifier for comment: ' + jsdoc.GetComment())

    symbol = Symbol(identifier)
    yield jsdoc, symbol
    
  
def FindJsDocComments(script):
  return re.finditer('/\*\*.*?\*/', script, re.DOTALL)

def FindNextIdentifer(script, pos=0):
  identifier_regex = re.compile('(?:\w+\s*\.\s*)*\w+')
  return identifier_regex.search(script, pos=pos)

def StripWhitespace(original_string):
  return re.sub('\s*', '', original_string)

def ExtractTextFromJsDocComment(comment):
  comment = comment.strip()

  # Strip the leading "/**"
  assert comment.startswith('/**')
  comment = comment[3:]

  assert comment.endswith('*/')
  comment = comment[:-2]

  comment = comment.strip()
  lines = comment.splitlines(True)

  output_lines = []
  for line in lines:
    line = line.lstrip()
    if line.startswith('*'):
      line = line[1:]
      while line.startswith(' '):
        line = line[1:]
      output_lines.append(line)
  
  return ''.join(output_lines)

