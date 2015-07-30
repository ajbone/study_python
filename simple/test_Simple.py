# -*- coding: iso-8859-15 -*-
"""Simple FunkLoad test

$Id$
"""
import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data

class Simple(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def setUp(self):
        """Setting up test."""
        data=None
        self.server_url = self.conf_get('main', 'url')
        self.server_params = self.conf_get('main','data')
        print self.server_params
    def test_simple(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin test ---------------------------------------------
        #nb_time = self.conf_getInt('test_simple', 'nb_time')
        #for i in range(nb_time):
        req = self.post(server_url,Data('text/json', self.server_params),description='Get URL')
        # end test -----------------------------------------------
        print req.body


if __name__ in ('main', '__main__'):
    unittest.main()
