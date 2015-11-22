# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import print_function
from __future__ import division

import os
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from onion.lulz import lulz
from onion.onion import Onion


class OnionTest(unittest.TestCase):

    def setUp(self):
        self.onion = Onion()

    def test_onion_config(self):
        expected = os.path.join(os.path.abspath(os.environ.get('HOME', '')),
                                self.onion.CONFIG)
        assert self.onion._onion_config(self.onion.CONFIG) == expected

    def save_and_generate_index(self, lol_index):
        self.onion.last_index = lol_index
        self.onion.save_last_index()
        return self.onion.generate_next_index()

    def test_save_and_generate_index(self):
        lol_index = 0
        next_lol_index = self.save_and_generate_index(lol_index)
        assert lol_index + 1 == next_lol_index
        lol_index = len(lulz) - 1
        next_lol_index = self.save_and_generate_index(lol_index)
        assert next_lol_index == 0

    def test_generate_next_index_default_index(self):
        default_index = 0
        self.onion.CONFIG = 'foo bar'
        next_lol_index = self.onion.generate_next_index(default_index)
        assert next_lol_index == 0

    def test_random_index(self):
        len_lulz = len(lulz)
        lol_index = self.onion.random_index(len_lulz-1)
        assert lol_index >= 0 and lol_index < len_lulz

    def test_repeat(self):
        expected = '-----'
        result = self.onion.repeat('-', 5)
        assert result == expected
