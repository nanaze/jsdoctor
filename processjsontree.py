#!/usr/bin/env python

"""Process a JSON file tree."""

import os
import json
import logging
import sys
import esprima


def ProcessJsonTree(json_obj):

  items = json_obj.items()
  paths = [pair[0] for pair in items]
  sources = [pair[1] for pair in items]

  logging.info('Parsing sources...')
  asts = esprima.MultiParse(sources)

  source_count = len(items)
  assert (len(paths) == source_count and
          len(sources) == source_count and
          len(asts) == source_count)

  results = zip(paths, sources, asts)

  result = dict()
  for path, source, ast in results:
    result[path] = {
      'source': source,
      'ast': ast
    }
  
  return result

def main():

  logging.basicConfig(level=logging.INFO)
  input = sys.stdin.read()
  obj = json.loads(input)
  result = ProcessJsonTree(obj)
  sys.stdout.write(json.dumps(result))

if __name__ == '__main__':
  main()
