#!/usr/bin/env python2
import json
import os
import requests
from panda3d.core import *

username = os.environ['ttjUsername']
password = os.environ['ttjPassword']
distribution = ConfigVariableString('distribution', 'dev').getValue()

accountServerEndpoint = ConfigVariableString(
    'account-server-endpoint',
    'https://toontownjourney.com/api/').getValue()
request = requests.post(
    accountServerEndpoint + 'login/',
    data={'n': username, 'p': password, 'dist': distribution})

try:
    response = json.loads(request.text)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if not response['success']:
        print response['reason']
    else:
        os.environ['TTJ_PLAYCOOKIE'] = response['token']

        # Start the game:
        import toontown.toonbase.ClientStart
