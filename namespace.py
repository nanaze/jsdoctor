def GetNamespaceParts(namespace):
  return namespace.split('.')

def IsSymbolPartOfNamespace(symbol, namespace):
  namespace_parts = GetNamespaceParts(namespace)
  symbol_parts = GetNamespaceParts(symbol)

  return (
    namespace_parts ==
    symbol_parts[0:len(namespace_parts)])
