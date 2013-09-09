#!/usr/bin/env python

"""Process a JSON file tree."""

import os
import json
import logging
import sys
import esprima

def main():
  logging.basicConfig(level=logging.INFO)
  input = sys.stdin.read()
  obj = json.loads(input)
  ProcessJsonTree(obj)

  sys.stdout.write(json.dumps(obj))

def ProcessJsonTree(json_obj):

  result = dict()
  
  for path, source in json_obj.iteritems():
    logging.info('Parsing path %s', path)

    ast_json = esprima.parse(source)
    ast = json.loads(ast_json)
    
    if path in result:
      raise Exception('Path %s defined twice' % path)

    result[path] = {
      'source': source,
      'ast': ast
    }

  return result

if __name__ == '__main__':
  main()
