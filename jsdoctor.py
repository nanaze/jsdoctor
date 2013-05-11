#!/usr/bin/env python

import collections
import logging
import sys
import os
import multiprocessing
import source
import argparse
import generator
import StringIO
import tarfile


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

class JsDoctorError(Exception):
  pass

class DuplicateSymbolError(JsDoctorError):
  pass


def _MakeNamespaceMap(symbols):
  namespace_map = collections.defaultdict(set)
  for symbol in symbols:
    namespace_map[symbol.namespace].add(symbol)
  return namespace_map

def _ScanContent(content_pair):
  path, content = content_pair
  return source.ScanScript(content, path)
  
def _ScanContentInParallel(content_map):
  pool = multiprocessing.Pool(20 * multiprocessing.cpu_count())
  return pool.imap(_ScanContent, content_map.iteritems())

def _MakeContentMap(paths):
  content_map = dict()
  for path in paths:
    if path in content_map:
      raise JsDoctorError('Path already added: %s', path)

    with open(path) as f:
      content = f.read()
      
    content_map[path] = content

  return content_map

def _ParseArgs():
  parser = argparse.ArgumentParser(description='Generates HTML docs for JsDoc')
  parser.add_argument('--tar', help='Path to tar file', required=True)
  parser.add_argument('files', help='Paths to files', nargs='*')
  return parser.parse_args()

def main():
  logging.basicConfig(
      level=logging.INFO,
      format='%(levelname)s:%(module)s:%(lineno)d: %(message)s')

  result = _ParseArgs()
  tar_path = result.tar
  
  paths = result.files
  paths = [path for path in paths if _ShouldScanPath(path)]

  logging.info('Found %s paths.', len(paths))
  logging.info('Reading file contents.')
  content_map = _MakeContentMap(paths)

  sources = _ScanContentInParallel(content_map)
  symbols = _GetSymbolsFromSources(sources)

  # This could instead be just a dupe check
  symbol_map = _MakeSymbolMap(symbols)

  symbols = symbol_map.values()
  
  namespace_map = _MakeNamespaceMap(symbols)

  logging.info('Writing to tar: %s', tar_path)
  with tarfile.open(name=tar_path, mode='w') as tar:
    for path, content in generator.GenerateDocs(namespace_map):
      logging.info('Writing doc to tar: %s', path)
      # Add each path to the tar
      info = tarfile.TarInfo(name=path)
      info.size = len(content)
      buf = StringIO.StringIO(content)
      tar.addfile(info, buf)
  logging.info('Tar written to %s', tar_path)

    
if __name__ == '__main__':
  main()
