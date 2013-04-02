import scanner

class Source(object):
  def __init__(self, script, provides, requires, comments, path=None):
    self.script = script
    self.provides = provides
    self.requires = requires
    self.comments = comments
    self.path = path

class Symbol(object):
  def __init__(self, identifier, start, end):
    self.identifier = identifier
    self.start = start
    self.end = end

class Comment(object):
  def __init__(self, symbol, text, start, end):
    self.symbol = symbol
    self.text = text
    self.start = start
    self.end = end
    

def ScanScript(script, path=None):
  provides = set(scanner.YieldProvides(script))
  requires = set(scanner.YieldRequires(script))

  pairs = scanner.ExtractDocumentedSymbols(script)

  comments = set()
  for comment_match, identifier_match in pairs:
    identifier = scanner.StripWhitespace(identifier_match.group())
    symbol = Symbol(identifier, identifier_match.start(), identifier_match.end())

    comment_text = scanner.ExtractTextFromJsDocComment(comment_match.group())
    comment = Comment(symbol, comment_text, comment_match.start(), comment_match.end())
    comments.add(comment)

  return Source(script, provides, requires, comments, path)
    
    
