import re

def FindJsDocComments(script):
  return re.finditer('/\*\*.*?\*/', script, re.DOTALL)

def FindNextIdentifer(script, pos=0):
  identifier_regex = re.compile('(?:\w+\s*\.\s*)*\w+')
  return identifier_regex.search(script, pos=pos)

def StripWhitespace(original_string):
  return re.sub('\s*', '', original_string)

