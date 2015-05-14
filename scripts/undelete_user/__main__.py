#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from undelete import UndeleteUser
from utilities.prompt_format import item

class ArgumentsError(Exception):
    pass

def FetchSystemArguments():
  '''Fetching arguments from the command line interface.'''
  
  #
  # Checking that all arguments have been provided.
  # 
  if len(sys.argv) <= 1:
    print '%s Please provide an HDX user id.' % item('prompt_error')
    raise ArgumentsError('No arguments provided')

  arguments = {
    'user_id': sys.argv[1]
  }
  
  #
  # Checking if no arguments are None.
  # 
  for argument in arguments:

    if argument is None:
      print '%s Argument %s is empty. That argument is necessary.' % (item('prompt_error'), argument.keys())
      raise ArgumentsError('No arguments provided')

  return arguments


if __name__ == '__main__':
  user_id = FetchSystemArguments()['user_id']
  UndeleteUser(user_id=user_id)