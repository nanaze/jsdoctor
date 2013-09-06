#!/usr/bin/env python

"""Process a JSON file tree."""

import os
import json
import logging
import sys

def main():
  logging.basicConfig(level=logging.INFO)
  input = sys.stdin.read()
  obj = json.loads(input)
  ProcessJsonTree(obj)

def ProcessJsonTree(json_obj):
  pass

if __name__ == '__main__':
  main()
