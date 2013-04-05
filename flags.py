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
    '@license'
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
    '@inheritDoc'
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

