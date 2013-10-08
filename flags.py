import re

BASE_FLAGS = frozenset([
    '@provideGoog'
    ])

JSDOC_FLAGS = frozenset([
    '@suppress'
    ])

FILE_FLAGS = frozenset([
    '@author',
    '@fileoverview',
    '@see',
    '@license',
    '@visibility'
    ])

FUNCTION_FLAGS = frozenset([
    '@param',
    '@return',
    '@template',
    '@deprecated',
    '@throws',
    '@see',
    '@override',
    ])

VISIBILITY_FLAGS = frozenset([
    # Everything public by default
    '@protected',
    '@private'
    ])

INSTANTIABLE_FLAGS = frozenset([
    '@constructor',
    '@extends',
    '@implements',
    '@see',
    ])

TYPEDEF_FLAGS = frozenset([
    '@typedef'
    ])

PROPERTY_FLAGS = frozenset([
    '@const',
    '@define',    
    '@enum',
    '@struct',
    '@type',
    '@inheritDoc',
    '@export'
    ])

INTERFACE_FLAGS = frozenset([
    '@interface',
    '@extends'
    ])

COMPILER_FLAGS = frozenset([
    '@nocompile',
    '@preserveTry',    
    ])

# TODO(nanaze): File.
MISC_FLAGS = frozenset([
    '@desc', 
    '@supported',
    '@hidden',
    '@final',
    '@idGenerator',
    '@this'    
    ])

all_flags = set()
all_flags.update(MISC_FLAGS)
all_flags.update(BASE_FLAGS)
all_flags.update(COMPILER_FLAGS)
all_flags.update(JSDOC_FLAGS)
all_flags.update(FILE_FLAGS)
all_flags.update(FUNCTION_FLAGS)
all_flags.update(INTERFACE_FLAGS)
all_flags.update(INSTANTIABLE_FLAGS)
all_flags.update(PROPERTY_FLAGS)
all_flags.update(TYPEDEF_FLAGS)
all_flags.update(VISIBILITY_FLAGS)

ALL_FLAGS = frozenset(all_flags)


def ParseParameterDescription(desc):
  match = re.match(r'^\s*\{(?P<type>.*?)\}\s+(?P<name>\w+)(?P<desc>.*)$', desc, re.DOTALL | re.MULTILINE)
  if not match:
    raise ValueError('Could not parse flag description: %s' % desc)
  return (match.group('name').strip(),
          match.group('type').strip(),
          match.group('desc').strip())

def ParseReturnDescription(desc):
  match = re.match(r'^\s*{(?P<type>.*?)\}(?P<desc>.*)$', desc, re.DOTALL | re.MULTILINE)
  if not match:
    raise ValueError('Could not parse flag description: %s' % desc)
  return (match.group('type').strip(),
          match.group('desc').strip())

PUBLIC = 'public'
PROTECTED = 'protected'
PRIVATE = 'private'

def GetVisibility(flags):
  """Returns one of PUBLIC, PROTECTED, or PRIVATE."""

  flag_names = [flag.name for flag in flags]
  if '@private' in flag_names:
    return PRIVATE

  if '@protected' in flag_names:
    return PROTECTED

  return PUBLIC

def GetSymbolType(flags):
  for flag in flags:
    if flag.name in ['@type', '@const', '@protected', '@private']:
      flag_type = MaybeParseTypeFromDescription(flag.text)
      if flag_type:
        return flag_type
          
def MaybeParseTypeFromDescription(desc):
  match = re.match(r'^\s*{(?P<type>.*?)}', desc, re.DOTALL | re.MULTILINE)
  if match:
    return match.group('type')

    
          
