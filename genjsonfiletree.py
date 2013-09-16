#!/usr/bin/env python

"""Scans a directory tree for .js files and builds a JSON representation.

Scans a directory tree for .js files, and puts the contents into a single JSON 
object map of path to content.

Ouput is written to stdout.

Usage:

$ genjsonfiletree.py

Scans the current directory.

$ genjsonfiletree.py path/to/dir

Scans the given directory.
"""

import os
import json
import logging
import sys

def _YieldPaths(root):
  for dir_root, dirs, files in os.walk(root):
    for file_path in files:
      abspath = os.path.join(dir_root, file_path)
      relpath = os.path.relpath(abspath, root)

      yield relpath, abspath

def _YieldJsPaths(root):
  for relpath, abspath in _YieldPaths(root):
    _, ext = os.path.splitext(abspath)
    if ext == '.js':
      yield relpath, abspath

def ScanTree(tree_root):
  tree = dict()

  for relpath, abspath in _YieldJsPaths(tree_root):
    logging.info('Reading file: %s', relpath)
    with open(abspath) as f:
      tree[relpath] = f.read()

  return tree

def main():
  logging.basicConfig(level=logging.INFO)
  
  if len(sys.argv) == 1:
    logging.info('Path not specified. Using current directory as path.')
    dir_root = os.getcwd()
    
  elif len(sys.argv) == 2:
    dir_root = sys.argv[1]

  else:
    sys.exit(__doc__)
  
  logging.info('Scanning tree. Path: "%s"', dir_root)

  tree = ScanTree(dir_root)
  resulting_json = json.dumps(tree)
  sys.stdout.write(resulting_json)
  sys.stdout.flush()
  

if __name__ == '__main__':
  main()
