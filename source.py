import scanner

class Source(object):
  def __init__(self, script, path=None):
    self.script = script
    self.path = path
    
    self.provides = set()
    self.requires = set()
    self.symbols = set()


class Symbol(object):
  def __init__(self, identifier, start, end):
    self.identifier = identifier
    self.start = start
    self.end = end
    self.source = None
    self.comment = None

class Comment(object):
  def __init__(self, symbol, text, start, end):
    self.symbol = symbol
    self.text = text
    self.start = start
    self.end = end
    
    

def ScanScript(script, path=None):

  source = Source(script, path)
  source.provides.update(set(scanner.YieldProvides(script)))
  source.requires.update(set(scanner.YieldRequires(script)))

  pairs = scanner.ExtractDocumentedSymbols(script)

  for comment_match, identifier_match in pairs:

    # TODO(nanaze): Identify scoped variables and expand identifiers.
    identifier = scanner.StripWhitespace(identifier_match.group())
    symbol = Symbol(identifier, identifier_match.start(), identifier_match.end())

    comment_text = scanner.ExtractTextFromJsDocComment(comment_match.group())
    comment = Comment(symbol, comment_text, comment_match.start(), comment_match.end())
    symbol.source = source
    symbol.comment = comment
    source.symbols.add(symbol)

  return source


    
    
