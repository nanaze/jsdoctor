import re

def ProcessComment(comment_text):
  descriptions = []
  flags = []

  for section_text in _YieldSections(comment_text):
    description, section_flags = _ProcessCommentSection(section_text)

    if description:
      descriptions.append(description)

    flags.extend(section_flags)

  return descriptions, flags
    

def _ProcessCommentSection(section_text):
  
  remaining_text = section_text
  flags = []
  
  matches = list(_MatchFlags(section_text))
  matches.reverse()

  # A flag is itself and whatever text appears behind it (until the next flag
  # or the end of a section).
  for flag_match in matches:

    flag_name = flag_match.group('flag')
    flag_text = remaining_text[flag_match.end():].strip()
      
    flags.insert(0, (flag_name, flag_text))
    
    remaining_text = remaining_text[0:flag_match.start()]

  # The description is whatever wasn't part of a flag.
  description = remaining_text.strip()

  return description, flags
      

  
def _MatchFlags(text):
  return re.finditer(r'(?:\s|\A)(?P<flag>@\w+)\b', text)
  
def _YieldSections(comment_text):
  # 
  assert '\r' not in comment_text, 'Non-UNIX strings not supported for now'
  parts = comment_text.split('\n\n')

  for part in parts:
    part = part.strip()

    # skip empty strings
    if part:
      yield part
