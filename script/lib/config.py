#!/usr/bin/env python

import errno
import os
import platform
import sys


BASE_URL = os.getenv('LIBCHROMIUMCONTENT_MIRROR') or \
    'http://github-janky-artifacts.s3.amazonaws.com/libchromiumcontent'
LIBCHROMIUMCONTENT_COMMIT = '42200d8ec0b77c7491d3a09611c23eb771e0862d'

PLATFORM = {
  'cygwin': 'win32',
  'darwin': 'darwin',
  'linux2': 'linux',
  'win32': 'win32',
}[sys.platform]

verbose_mode = False


def get_target_arch():
  try:
    target_arch_path = os.path.join(__file__, '..', '..', '..', 'vendor',
                                    'brightray', 'vendor', 'download',
                                    'libchromiumcontent', '.target_arch')
    with open(os.path.normpath(target_arch_path)) as f:
      return f.read().strip()
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise

  if PLATFORM == 'win32':
    return 'ia32'
  else:
    return 'x64'


def get_chromedriver_version():
  return 'v2.15'


def s3_config():
  config = (os.environ.get('ATOM_SHELL_S3_BUCKET', ''),
            os.environ.get('ATOM_SHELL_S3_ACCESS_KEY', ''),
            os.environ.get('ATOM_SHELL_S3_SECRET_KEY', ''))
  message = ('Error: Please set the $ATOM_SHELL_S3_BUCKET, '
             '$ATOM_SHELL_S3_ACCESS_KEY, and '
             '$ATOM_SHELL_S3_SECRET_KEY environment variables')
  assert all(len(c) for c in config), message
  return config


def enable_verbose_mode():
  print 'Running in verbose mode'
  global verbose_mode
  verbose_mode = True


def is_verbose_mode():
  return verbose_mode
