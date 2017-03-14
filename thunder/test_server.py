#!/usr/bin/env python
#coding: utf-8

import os
import sys
import unittest

sys.path.insert(0, '..')

import server
from server import QueryBroker, MediaWise, Hash, Query

class TestServer(unittest.TestCase):

    def test_send_broker_task(self):
        url = 'http://www.baidu.com/someplace/video.mp4'
        url_hash = Hash(url=url)
        url_data = {
            'location': url,
            'hash': url_hash.value
        }
        thunder_client = 'unittest-Thunder-Client-ID'
        mime_type = 'video/mp4'
        QueryBroker.push(thunder_client, mime_type,
                         url_hash.protocol, url_hash.value,
                         url=url_data)

    def test_hash(self):
        url = 'http://www.baidu.com/dl/some.mp4'
        url_hash = Hash(url=url)

        self.assertEqual(url_hash.protocol, 'http')
        self.assertEqual(url_hash.value, '76709133b1bcd884611186bdefcdbe2e235ef104')


    def test_init(self): pass
    def test_auth(self):
        server.APIKEY = 'test-key'
        key_right = 'test-key'
        key_wrong = 'wrong-key'
        
        
    def test_wrap_error(self): pass
    def test_wrap_result(self): pass
    def test_http_request(self): pass
    def test_query_mediawise(self):
        self.assertEqual(MediaWise.query('a'), (True, True))
        self.assertEqual(MediaWise.query('abc'), (None, None))
        
    def test_push_querybroker(self): pass
    def test_GET(self): pass
    def test_POST(self): pass


if __name__ == '__main__':
    unittest.main()
