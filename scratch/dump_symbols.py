import source

import sys

def main():
  assert len(sys.argv) > 1
  paths = sys.argv[1:]

  for path in paths:
    print 'Symbols in path', path
    with open(path) as f:
      script = f.read()

    s = source.ScanScript(script)

    for comment in s.comments:
      identifier = comment.symbol.identifier
      print identifier


if __name__ == '__main__':
  main()
