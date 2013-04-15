from xml.dom import minidom

import symboltypes

def GenerateDocs(namespace_map):
  for namespace, symbols in namespace_map.iteritems():
    filepath = '%s.html' % namespace
    doc = _GenerateDocument(namespace, symbols)
    content = doc.documentElement.toprettyxml(indent='  ')
    yield filepath, content


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

def _GetSymbolsOfType(symbols, type):
  return [symbol for symbol in symbols if symbol.type == type]

def _GenerateDocument(namespace, symbols):
  doc = minidom.getDOMImplementation().createDocument(None, 'html', None)

  body =  doc.createElement('body')
  doc.documentElement.appendChild(body)
  
  for elem in _GenerateContent(namespace, symbols):
   body.appendChild(elem)
    
  return doc

def _GenerateContent(namespace, symbols):

  node_list = minidom.NodeList()

  sorted_symbols = sorted(symbols, key= lambda symbol: symbol.identifier)

  # Constructor
  constructor_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.CONSTRUCTOR)

  if constructor_symbols:
    node_list.append(_MakeElement('h2', 'Constructor'))

    for symbol in constructor_symbols:
      node_list.append(_MakeElement('h3', symbol.identifier))
      for section in symbol.comment.description_sections:
        node_list.append(_MakeElement('p', section))

  # Interface
  interface_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.INTERFACE)
        
  if interface_symbols:
    node_list.append(_MakeElement('h2', 'Interface'))

    for symbol in interface_symbols:
      node_list.append(_MakeElement('h3', symbol.identifier))
      for section in symbol.comment.description_sections:
        node_list.append(_MakeElement('p', section))        

  return node_list


                       
    
  

  

  
