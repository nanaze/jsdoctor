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

def _GetCpuCount():
  if sys.platform == 'darwin':
    return int(subprocess.check_output(['sysctl', '-n', 'hw.logicalcpu']))

  if sys.platform == 'linux':
    return os.sysconf('SC_NPROCESSORS_ONLN')

  raise NotImplementedError(
      '_GetCpuCount not implemented for platform %s' % sys.platform)

def MultiParse(sources, num_threads=None):
  if num_threads is None:
    num_threads = _GetCpuCount() * 3
  


def parse(source):
  proc = _CreateEsprimaProcess()

  encoded_source, unused_length = codecs.getencoder('utf8')(source)
  out, err = proc.communicate(encoded_source)

  if proc.returncode != 0:
    logging.error('Error while parsing.')
    logging.error(err)
    raise Exception('Esprima parsing failed.')

  return out

  

