from xml.dom import minidom

import html5lib

import symboltypes
import flags
import linkify

def GenerateDocs(namespace_map):
  for namespace, symbols in namespace_map.iteritems():
    filepath = '%s.html' % namespace
    doc = _GenerateDocument(namespace, symbols)
    content = doc.documentElement.toxml('utf-8')
    yield filepath, content

def _ProcessString(content):
  content = linkify.LinkifyWebUrls(content)
  return html5lib.parseFragment(content, treebuilder='dom')

def _MakeTextNode(content):
  text = minidom.Text()
  text.data = content
  return text

def _MakeHeader(content=None):
  return _MakeElement('h2', content)

def _MakeElement(tagname, content=None):
  element = minidom.Element(tagname)

  if content:
    element.appendChild(_MakeTextNode(content))
  
  return element

def _IsStatic(symbol):
  return bool(symbol.static)

def _IsNotStatic(symbol):
  return not _IsStatic(symbol)

def _GetSymbolsOfType(symbols, type):
  return [symbol for symbol in symbols if symbol.type == type]

def _GenerateDocument(namespace, symbols):
  doc = minidom.getDOMImplementation().createDocument(None, 'html', None)

  body =  doc.createElement('body')
  doc.documentElement.appendChild(body)
  
  for elem in _GenerateContent(namespace, symbols):
   body.appendChild(elem)
    
  return doc

def _AddSymbolDescriptions(node_list, symbols):
  for symbol in symbols:
    node_list.append(_MakeElement('h3', symbol.identifier))
    for section in symbol.comment.description_sections:
      elem = _ProcessString(section)
      p = _MakeElement('p')
      node_list.append(p)
      p.appendChild(elem)
    node_list.append(_MakeElement('hr'))

def _MakeLink(text, href):
  a = _MakeElement('a', text)
  a.setAttribute('href', href)
  return a

def _YieldParamFlags(flags):
  for flag in flags:
    if flag.name == '@param':
      yield flag

def _GetParamString(flag):
  assert flag.name == '@param'
  name, type, _ = flags.ParseParameterDescription(flag.text)
  return '{%s} %s' % (type, name)

def _GetReturnFlag(flags):
  return_flags = filter(lambda flag: flag.name == '@return', flags)
  assert(len(return_flags) <= 1, 'There should not be more than one @return flag.')

  if return_flags:
    return return_flags[0]

def _GetReturnString(flag):
  assert flag.name == '@return'
  type, _ = flags.ParseReturnDescription(flag.text)
  return '{%s}' % type
  
def _MakeFunctionCodeElement(name, function):
  code = _MakeElement('code')
  code.appendChild(_MakeLink(name, '#' + name))

  param_flags = list(_YieldParamFlags(function.comment.flags))
  param_strings = [_GetParamString(flag) for flag in param_flags]
  param_line = ', '.join(param_strings)

  text_node = _MakeTextNode('(%s)' % param_line)
  code.appendChild(text_node)
  
  return_flag = _GetReturnFlag(function.comment.flags)
  if return_flag:
    code.appendChild(_MakeTextNode(' : '))
    code.appendChild(_MakeTextNode(_GetReturnString(return_flag)))
  return code
  
def _MakeFunctionSummary(name, function):
  container = _MakeElement('p')
  code = _MakeFunctionCodeElement(name, function)
  container.appendChild(code)  

  if function.comment.description_sections:
    desc = function.comment.description_sections[0]
    container.appendChild(_MakeElement('br'))
    container.appendChild(_ProcessString(desc))

  return container

def _AddFunctionDescription(node_list, function):

  header = _MakeElement('h2', function.identifier)
  header.setAttribute('id', function.identifier)
  node_list.append(header)

  # Draw function signature
  param_flags = list(_YieldParamFlags(function.comment.flags))

  function_interface = ''
  function_interface += flags.GetVisibility(function.comment.flags) + ' '
  function_interface += '%s(' % function.identifier

  # Draw parameters
  if param_flags:
    for index, flag in enumerate(param_flags):
      function_interface += '\n  %s' % _GetParamString(flag)

      # If this is not the last parameter, draw a comma.
      if index != (len(param_flags) - 1):
        function_interface += ','
      else:
        function_interface += '\n'
        
  function_interface += ')'

  # Draw return
  return_flag = _GetReturnFlag(function.comment.flags)
  if return_flag:
    function_interface += ' : ' + _GetReturnString(return_flag)

  node_list.append(_MakeElement('pre', function_interface))

  # Parameter list
  if param_flags:
    node_list.append(_MakeElement('h4', 'Parameters:'))
    
    param_list = _MakeElement('dl')
    node_list.append(param_list)
    for flag in param_flags:
      name, type, desc = flags.ParseParameterDescription(flag.text)
      term = _MakeElement('dt', name)
      param_list.appendChild(term)

      definition = _MakeElement('dd')
    
      code_type = _MakeElement('code', '{%s}' % type)
      definition.appendChild(code_type)
      definition.appendChild(_MakeTextNode(' '))
      definition.appendChild(_ProcessString(flag.text))
      term.appendChild(definition)

  if return_flag:
    node_list.append(_MakeElement('h4', 'Returns:'))
    return_paragraph = _MakeElement('p')
    node_list.append(return_paragraph)

    type, desc = flags.ParseReturnDescription(return_flag.text)
    code_type = _MakeElement('code', '{%s}' % type)
    return_paragraph.appendChild(code_type)
    return_paragraph.appendChild(_MakeTextNode(' '))
    return_paragraph.appendChild(_ProcessString(desc))
    
    

  # Add description paragraphs
  for section in function.comment.description_sections:
    section_paragraph = _MakeElement('p')
    section_paragraph.appendChild(_ProcessString(section))
    node_list.append(section_paragraph)

def _GenerateContent(namespace, symbols):

  node_list = minidom.NodeList()

  node_list.append(_MakeElement('h1', namespace))

  sorted_symbols = sorted(symbols, key= lambda symbol: symbol.identifier)

  # Constructor
  constructor_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.CONSTRUCTOR)

  if constructor_symbols:
    node_list.append(_MakeElement('h2', 'Constructor'))
    _AddSymbolDescriptions(node_list, constructor_symbols)

  # Interface
  interface_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.INTERFACE)
        
  if interface_symbols:
    node_list.append(_MakeElement('h2', 'Interface'))
    _AddSymbolDescriptions(node_list, interface_symbols)

  instance_methods = filter(_IsNotStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.FUNCTION))

  instance_properties = filter(_IsNotStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.PROPERTY))

  static_functions = filter(_IsStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.FUNCTION))

  if instance_methods:
    node_list.append(_MakeElement('h2', 'Method summary'))
    for method in instance_methods:
      node_list.append(_MakeFunctionSummary(method.property, method))

  if static_functions:
    node_list.append(_MakeElement('h2', 'Static method summary'))
    for function in static_functions:
      node_list.append(_MakeFunctionSummary(function.identifier, function))      

  # Enumerations
  enum_symbols = _GetSymbolsOfType(
     sorted_symbols, symboltypes.ENUM)
  
  if enum_symbols:
    node_list.append(_MakeElement('h2', 'Enumerations'))
    _AddSymbolDescriptions(node_list, enum_symbols)

  if instance_methods:
    node_list.append(_MakeElement('h2', 'Instance methods'))
    for method in instance_methods:
      _AddFunctionDescription(node_list, method)
      node_list.append(_MakeElement('hr'))

  if instance_properties:
    node_list.append(_MakeElement('h2', 'Instance properties'))
    _AddSymbolDescriptions(node_list, instance_properties)      

  if static_functions:
    node_list.append(_MakeElement('h2', 'Static methods'))
    for function in static_functions:
      _AddFunctionDescription(node_list, function)
      node_list.append(_MakeElement('hr'))

  static_properties = filter(_IsStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.PROPERTY))
  if static_properties:
    node_list.append(_MakeElement('h2', 'Static properties'))
    _AddSymbolDescriptions(node_list, static_properties)      

  return node_list


                       
    
  

  

  
