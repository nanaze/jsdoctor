import re

def FindJsDocComments(script):
  return re.finditer('/\*\*.*?\*/', script, re.DOTALL)

def FindIdentiferForComment(comment_match):
  end_index = comment_match.end()
  identifier_regex = re.compile('(?:\w+\s*\.\s*)*\w+')
  script = comment_match.string
  return identifier_regex.search(script, comment_match.end())

