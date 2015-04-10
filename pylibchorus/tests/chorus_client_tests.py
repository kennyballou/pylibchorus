#!/usr/bin/env python
'''Chorus Client Test Cases'''

import logging
from pylibchorus.chorus_client import _login_
from pylibchorus.chorus_client import _logout_
from pylibchorus.chorus_client import _check_login_
from pylibchorus.chorus_client import _create_workfile_
import unittest

LOG = logging.getLogger(__name__)

def check_request_structure(testcase, request_obj):
    '''Test the request structure is correct'''
    testcase.assertIsNotNone(request_obj)
    testcase.assertIn('data', request_obj)
    testcase.assertIn('headers', request_obj)
    testcase.assertIn('params', request_obj)
    testcase.assertIn('cookies', request_obj)
    testcase.assertIn('url', request_obj)
    testcase.assertIn('method', request_obj)
    check_header(testcase, request_obj['headers'])

def check_header(testcase, header):
    '''Test the header object conforms to the what the API requires'''
    testcase.assertIsNotNone(header)
    testcase.assertIn('content-type', header)
    testcase.assertEquals(header['content-type'],
                          'application/x-www-form-urlencoded')

def check_params(testcase, params, expected_sid):
    '''Check the params object contains the correct session_id'''
    testcase.assertIsNotNone(params)
    testcase.assertIn('session_id', params)
    testcase.assertEqual(params['session_id'], expected_sid)

class ChorusSessionTests(unittest.TestCase):
    '''ChorusSession Test Case'''

    def test_login_returns_request_data(self):
        '''Test _login_ returns request data'''
        actual = _login_('chorusadmin', 'secret')
        check_request_structure(self, actual)
        self.assertIsNotNone(actual['data'])
        self.assertIsNotNone(actual['headers'])
        self.assertIsNotNone(actual['params'])
        self.assertIsNone(actual['cookies'])
        self.assertIsNotNone(actual['url'])
        self.assertIsNotNone(actual['method'])
        data = actual['data']
        self.assertIn('username', data)
        self.assertIn('password', data)
        self.assertEquals(data['username'], 'chorusadmin')
        self.assertEquals(data['password'], 'secret')
        check_header(self, actual['headers'])
        params = actual['params']
        self.assertIn('session_id', params)
        self.assertEquals(params['session_id'], '')
        self.assertEquals('/sessions?session_id=', actual['url'])
        self.assertEquals('POST', actual['method'])


    #pylint: disable=C0103
    def test_logout_returns_request_data(self):
        '''Test _logout_ returns correct request data'''
        sid = 'foobar'
        cookies = {'session_id', sid}
        actual = _logout_(sid, cookies)
        check_request_structure(self, actual)
        self.assertIsNone(actual['data'])
        self.assertIsNotNone(actual['headers'])
        self.assertIsNotNone(actual['params'])
        self.assertIsNotNone(actual['cookies'])
        self.assertIsNotNone(actual['url'])
        self.assertIsNotNone(actual['method'])
        headers = actual['headers']
        self.assertIn('content-type', headers)
        self.assertEquals('application/x-www-form-urlencoded',
                          headers['content-type'])
        params = actual['params']
        self.assertIn('session_id', params)
        self.assertEquals(sid, params['session_id'])
        self.assertEquals(cookies, actual['cookies'])
        self.assertEquals('/sessions', actual['url'])
        self.assertEquals('DELETE', actual['method'])

    #pylint: disable=C0103
    def test_check_login_returns_request_data(self):
        '''Test _check_login_ returns correct request data'''
        sid = 'foobar'
        cookies = {'session_id': sid}
        actual = _check_login_(sid, cookies)
        check_request_structure(self, actual)
        self.assertIsNone(actual['data'])
        self.assertIsNotNone(actual['headers'])
        self.assertIsNone(actual['params'])
        self.assertIsNotNone(actual['cookies'])
        self.assertIsNotNone(actual['url'])
        self.assertIsNotNone(actual['method'])
        check_header(self, actual['headers'])
        self.assertEquals(cookies, actual['cookies'])
        self.assertEquals('/sessions', actual['url'])
        self.assertEquals('GET', actual['method'])

    #pylint: disable=C0103
    def test_create_workfile_returns_request_data(self):
        '''Test _create_workfile_ returns correct request data'''
        workspace_id = 1
        workfile_name = 'foo'
        sid = 'foobar'
        cookies = {'session_id': sid}
        actual = _create_workfile_(workspace_id, workfile_name, sid, cookies)
        check_request_structure(self, actual)
        self.assertIsNotNone(actual['data'])
        self.assertIsNotNone(actual['headers'])
        self.assertIsNotNone(actual['params'])
        self.assertIsNotNone(actual['cookies'])
        self.assertIsNotNone(actual['url'])
        self.assertIsNotNone(actual['method'])
        data = actual['data']
        self.assertIn('workspace_id', data)
        self.assertIn('file_name', data)
        self.assertEquals(workspace_id, data['workspace_id'])
        self.assertEquals(workfile_name, data['file_name'])
        check_header(self, actual['headers'])
        check_params(self, actual['params'], sid)
        self.assertEquals(cookies, actual['cookies'])
        self.assertEquals('/workspaces/%d/workfiles' % workspace_id,
                          actual['url'])
        self.assertEquals('POST', actual['method'])
