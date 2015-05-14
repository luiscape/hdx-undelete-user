#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
import requests

from config.config import LoadConfig
from utilities.prompt_format import item


def GetUserInformation(user_id, hdx_key, verbose=True):
  '''Fetch user information from HDX.'''
  
  #
  # Make request.
  #
  u = 'http://data.hdx.rwlabs.org/api/action/user_show?id=' + user_id
  headers = { 'Authorization': hdx_key }
  
  try:
    if verbose:
      print '%s Fetching user information from HDX.' % item('prompt_bullet')
    r = requests.get(u, headers=headers)

  except Exception as e:
    print '%s Could not make request to HDX.' % item('prompt_error')
    if verbose:
      print e
    return False

  user_data = r.json()
  
  #
  # Checking if the user data exists.
  #
  if user_data['success'] is False:
    print '%s User data could not be collected. Please check user id.' % item('prompt_error')
    if verbose:
      print '%s%s %s' % (item('prompt_dash').decode('utf-8'), item('prompt_bullet').decode('utf-8'), user_data['error']['message'])

    return False

  else:
    if verbose:
      print '%s User data collected successfully.' % item('prompt_bullet')
    return user_data


def UndeleteUser(user_id, verbose=True):
  '''Undelete an user from HDX by user_id.'''
  
  print '%s Undeleting user `%s`.' % (item('prompt_bullet'), user_id)

  #
  # Load configuration.
  # 
  hdx_key = LoadConfig()['hdx_key']
  
  #
  # Update parameters.
  #
  u = 'https://data.hdx.rwlabs.org/api/action/user_update'
  headers = { 'Authorization': hdx_key, 'content-type': 'application/json' }

  #
  # Collect data and change delete status.
  #
  payload = GetUserInformation(user_id=user_id, hdx_key=hdx_key)['result']

  #
  # Check if state is deleted.
  #
  if payload['state'] != 'deleted':
    print '%s User `%s` does not need to be undeleted.' % (item('prompt_warn'), user_id)
    return False
  
  else:
    payload['state'] = 'active'

    #
    # Making POST request.
    #
    try:

      #
      # Check if the connection with HDX works.
      #
      r = requests.post(u, headers=headers, data=json.dumps(payload))
      if r.status_code != requests.codes.ok:
        print '%s Failed to undelete user `%s`.' % (item('prompt_error'), user_id)
        if verbose:
          print '%s%s %s' % (item('prompt_dash').decode('utf-8'), item('prompt_bullet').decode('utf-8'), r.json()['error']['message'])

        return False
      
      #
      # Check if user has been undeleted.
      #
      else:
        if GetUserInformation(user_id=user_id, hdx_key=hdx_key, verbose=False)['result']['state'] == 'active':
          print '%s User `%s` undeleted successfully.' % (item('prompt_success'), user_id)
          return True

        else:
          print '%s Could not undelete user `%s`.' % (item('prompt_error'), user_id)
          return False


    except Exception as e:
      print '%s Could not connect to HDX.' % item('prompt_error')
      if verbose:
        print e
      return False
