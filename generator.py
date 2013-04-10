from xml.dom import minidom

def GenerateDocs(namespace_map):

  content = {}

  for namespace, symbols in namespace_map.iteritems():
    filepath = '%s.html' % namespace
    doc = _GenerateDocument(namespace, symbols)
    xml_str = doc.documentElement.toprettyxml(indent='  ')
    content[filepath] = xml_str
  
  return content

def _MakeTextNode(content):
  text = minidom.Text()
  text.data = content
  return text

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
  for symbol in sorted_symbols:
    header = minidom.Element('h2')
    header.appendChild(_MakeTextNode(symbol.identifier))
    node_list.append(header)

    comment = minidom.Element('p')
    comment.appendChild(_MakeTextNode(symbol.comment.text))
    node_list.append(comment)


  return node_list


                       
    
  

  

  
