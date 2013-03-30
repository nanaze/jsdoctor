import re

def FindJsDocComments(script):
  return re.finditer('/\*\*.*?\*/', script, re.DOTALL)

