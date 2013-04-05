import scanner
import namespace
import logging
import jsdoc
import flags
import re

class Source(object):
  def __init__(self, script, path=None):
    self.script = script
    self.path = path
    
    self.provides = set()
    self.requires = set()
    self.symbols = set()
    self.filecomment = None

  def __str__(self):
    source_string = super(Source, self).__str__()

    if self.path:
      source_string += ' ' + self.path

    return source_string

class Symbol(object):
  def __init__(self, identifier, start, end):
    self.identifier = identifier
    self.start = start
    self.end = end
    self.source = None
    self.comment = None
    self.namespace = None

  def __str__(self):
    symbol_string = super(Symbol, self).__str__()

    symbol_string += ' ' + self.identifier

    if self.source:
      symbol_string += ' ' + str(self.source)

    return symbol_string

class Comment(object):
  def __init__(self, text, start, end):
    self.text = text
    self.start = start
    self.end = end
    
    self.description_sections, self.flags = _GetDescriptionAndFlags(text)
    
class Flag(object):
  def __init__(self, name, text):

    assert name in flags.ALL_FLAGS, 'Unrecognized flag: ' + name
    
    self.name = name
    self.text = text

def _GetDescriptionAndFlags(text):
  description_sections, flag_pairs = jsdoc.ProcessComment(text)
  flags = [Flag(name, text) for name, text in flag_pairs]
  return description_sections, flags

def _IsSymbolPartOfProvidedNamespaces(symbol, provided_namespaces):
  for ns in provided_namespaces:
    if namespace.IsSymbolPartOfNamespace(symbol, ns):
      return True
  return False

def _IsIgnorableIdentifier(identifier_match):

  # Find the first non-whitespace character after the identifier.
  regex = re.compile('[\S]')
  match = regex.search(identifier_match.string, pos=identifier_match.end())
  if match:
    first_character = match.group()
    if first_character in ['(', '[']:
      # This is a method call or a bracket-notation property access. Ignore.
      return True

  return False

class NamespaceNotFoundError(Exception):
  pass
  
# TODO(nanaze): In the future this could farm out to a formal parser like
# Esprima to correctly identify comments. Regexing seems to work OK for now.

def _YieldSymbols(match_pairs, provided_namespaces):
  for comment_match, identifier_match in match_pairs:
    comment_text = scanner.ExtractTextFromJsDocComment(comment_match.group())
    comment = Comment(comment_text, comment_match.start(), comment_match.end())

    if not identifier_match:
      assert not source.filecomment, '@fileoverview comment made more than once' 
      source.filecomment = comment
      continue

    if _IsIgnorableIdentifier(identifier_match):
      # This is JsDoc on a method call, most likely a type cast of a return value.
      # Ignore.
      continue

    if identifier_match.group() == '(':
      # This comment targeted a parenthetical and can be ignored.
      continue

    # TODO(nanaze): Identify scoped variables and expand identifiers.
    identifier = scanner.StripWhitespace(identifier_match.group())

    if identifier.startswith('this.'):
      logging.info('Skipping identifer. Ignoring "this." properties for now. ' + identifier)
      continue

    # Ignore symbols that are not part of the provided namespace.
    if not _IsSymbolPartOfProvidedNamespaces(identifier, provided_namespaces):
      logging.info('Skipping identifer. Not part of provided namespace. ' + identifier)
      continue

    symbol = Symbol(identifier, identifier_match.start(), identifier_match.end())
    symbol.comment = comment

    # Identify the namespace for this symbol.
    closest_namespace = namespace.GetClosestNamespaceForSymbol(
        identifier, provided_namespaces)

    if not closest_namespace:
      raise NamespaceNotFoundError('No namespace found ' + identifier)

    symbol.namespace = closest_namespace
    
    yield symbol
  

def ScanScript(script, path=None):

  source = Source(script, path)
  source.provides.update(set(scanner.YieldProvides(script)))
  source.requires.update(set(scanner.YieldRequires(script)))

  match_pairs = scanner.ExtractDocumentedSymbols(script)
  for symbol in _YieldSymbols(match_pairs, source.provides):
    symbol.source = source
    source.symbols.add(symbol)

  return source


    
    
