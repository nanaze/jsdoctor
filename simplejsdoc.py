#!/usr/bin/env python

import logging
import sys
import os
import source

def _ScanPath(path):
  logging.info('Scanning source %s' % path)
  with open(path) as f:
    script = f.read()
  return source.ScanScript(script, path)

def _ShouldScanPath(path):
  _, filename = os.path.split(path)

  if not filename.endswith('.js'):
    return False

  if filename == 'deps.js':
    return False

  if filename.endswith('_test.js'):
    return False

  return True

_IGNORED_IDENTIFIERS = frozenset([
  'goog.provide',
  'goog.require',
  'goog.setTestOnly'
  ])

def _GetSymbolsFromSources(sources):
  for s in sources:
    for symbol in s.symbols:
      yield symbol

# TODO(nanaze): Make this a flag
_DUPLICATE_SYMBOL_IS_ERROR = False

def _MakeSymbolMap(symbols):
  symbol_map = {}

  for symbol in symbols:
    identifier = symbol.identifier

    if identifier in _IGNORED_IDENTIFIERS:
      continue

    if identifier.startswith('this.'):
      logging.info('Skipping "this" identifier ' + identifier)
      continue

    if identifier in symbol_map:
      duplicate_symbol = symbol_map[identifier]
      msg = 'Symbol duplicated\n%s\n%s' % (symbol, duplicate_symbol)
      
      if _DUPLICATE_SYMBOL_IS_ERROR:
        raise DuplicateSymbolError(msg)
      else:
        logging.warning(msg)
      continue

    symbol_map[identifier] = symbol
  
  return symbol_map

class DuplicateSymbolError(Exception):
  pass

def main():
  logging.basicConfig(
      level=logging.INFO,
      format='%(levelname)s:%(module)s:%(lineno)d: %(message)s')

  paths = sys.argv[1:]
  paths = [path for path in paths if _ShouldScanPath(path)]

  # This can be parallelized if needed.
  sources = [_ScanPath(path) for path in paths]
  symbols = _GetSymbolsFromSources(sources)
  symbol_map = _MakeSymbolMap(symbols)

  keys = symbol_map.keys()
  keys.sort()
  for key in keys:
    symbol = symbol_map[key]
    print symbol.identifier
    print symbol.comment.text
    
  
  
if __name__ == '__main__':
  main()
