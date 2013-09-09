"""Wrappers around esprima"""

import StringIO
import os
import subprocess
import logging
import codecs


def GetParseInputPath():
  dir = os.path.dirname(__file__)
  return os.path.join(dir, 'node/parseinput.js')

def _CreateEsprimaProcess():
  logging.info('Starting Esprima parsing...')
  proc = subprocess.Popen(
      [GetParseInputPath()],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE)
  return proc
  

def MultiParse(sources, num_threads):
  pass

def parse(source):
  proc = _CreateEsprimaProcess()

  encoded_source, unused_length = codecs.getencoder('utf8')(source)
  out, err = proc.communicate(encoded_source)

  if proc.returncode != 0:
    logging.error('Error while parsing.')
    logging.error(err)
    raise Exception('Esprima parsing failed.')

  return out

  

