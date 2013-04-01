import parser

import sys

def main():
  assert len(sys.argv) > 1
  paths = sys.argv[1:]
  print paths

  for path in paths:
    with open(path) as f:
      script = f.read()
      for comment, symbol in parser.ExtractDocumentedSymbols(script):
        print 'symbol', symbol.GetSymbol()
        print 'comment', comment.GetText()


if __name__ == '__main__':
  main()
