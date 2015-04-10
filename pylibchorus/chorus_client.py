#!/usr/bin/env python
'''Alpine/Chorus Client API Module'''

import logging
import requests

LOG = logging.Logger(name=__name__)

CONTENT_TYPE = 'application/x-www-form-urlencoded'
JSON_CONTENT_TYPE = 'application/json'

def login(username, password, session):
    '''POST login request to chorus server'''
    return _perform_http_method_(
        session.config.get('alpine', 'host'), _login_(username, password))

def logout(session):
    '''DELETE login request to chorus server'''
    return _perform_http_method_(
        session.config.get('alpine', 'host'),
        _logout_(session.sid, session.cookies))

def check_login_status(session):
    '''GET login request to chorus server'''
    return _perform_http_method_(
        session.config.get('alpine', 'host'),
        _check_login_(session.sid, session.cookies))

def _get_url_(host, endpoint=""):
    '''Return the host and path for the chorus instance'''
    return "http://%s/%s" % (host, endpoint)

def _perform_http_method_(host, request_data):
    '''Perform IO operation to Chorus Server using request_data object'''
    methods = {'GET': requests.get,
               'POST': requests.post,
               'DELETE': requests.delete,}
    method = methods[request_data['method']]
    response = method(_get_url_(host, request_data['url']),
                      params=request_data['params'],
                      headers=request_data['headers'],
                      cookies=request_data['cookies'],
                      data=request_data['data'])
    LOG.info("Request: %s status code: %d",
             request_data['url'],
             response.status_code)
    return response

def _login_(username, password):
    '''Create Request Data for ChorusSession'''
    return {
        'data': {
            'username': username,
            'password': password,
        },
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'params': {
            'session_id': '',
        },
        'cookies': None,
        'url': '/sessions?session_id=',
        'method': 'POST',
    }

def _check_login_(_, cookies):
    '''Create request data for check login check'''
    return {
        'data': None,
        'params': None,
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'cookies': cookies,
        'url': '/sessions',
        'method': 'GET',
    }

def _logout_(sid, cookies):
    '''Create request data for ChorusSession'''
    return {
        'data': None,
        'headers': {
            'content-type': CONTENT_TYPE,
        },
        'params': {
            'session_id': sid,
        },
        'cookies': cookies,
        'url': '/sessions',
        'method': 'DELETE',
    }
