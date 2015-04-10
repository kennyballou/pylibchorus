#!/usr/bin/env python
'''PyLibChorus -- Python Chorus API Library'''

import logging
from pylibchorus.chorus_client import login
from pylibchorus.chorus_client import logout
from pylibchorus.chorus_client import check_login_status

LOG = logging.getLogger(__name__)

#pylint: disable=R0903
class ChorusSession(object):
    '''Chorus User Session Object'''

    def __init__(self, config):
        self.config = config
        self.sid = None
        self.cookies = None

    def __enter__(self):
        '''create session and return sid and cookies'''

        LOG.debug("Opening Chorus Session")
        post = login(
            self.config.get('alpine', 'username'),
            self.config.get('alpine', 'password'),
            self)
        json = post.json()

        self.sid = json['response']['session_id']
        self.cookies = post.cookies
        return self

    def __exit__(self, _type, _value, _traceback):
        '''Close chorus session'''
        LOG.debug("Closing Chorus Session")
        logout(self)
