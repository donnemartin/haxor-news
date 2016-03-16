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

from tests.compat import unittest

from prompt_toolkit.key_binding.input_processor import KeyPress
from prompt_toolkit.keys import Keys

from haxor_news.haxor import Haxor


class KeysTest(unittest.TestCase):

    def setUp(self):
        self.haxor = Haxor()
        self.registry = self.haxor.key_manager.manager.registry
        self.processor = self.haxor.cli.input_processor

    def test_F2(self):
        # orig_paginate = self.haxor.paginate_comments
        self.processor.feed_key(KeyPress(Keys.F2, ''))
        # assert orig_paginate != self.haxor.paginate_comments

    def test_F10(self):
        with self.assertRaises(EOFError):
            self.processor.feed_key(KeyPress(Keys.F10, ''))
