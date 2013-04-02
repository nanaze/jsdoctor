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
  
def main():
  logging.basicConfig(
      level=logging.INFO,
      format='%(levelname)s:%(module)s:%(lineno)d: %(message)s')

  paths = sys.argv[1:]
  paths = [path for path in paths if _ShouldScanPath(path)]
  sources = [_ScanPath(path) for path in paths]

  for s in sources:
    for symbol in s.symbols:
      print symbol.identifier
  
if __name__ == '__main__':
  main()
