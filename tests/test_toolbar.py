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

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from pygments.token import Token

from hncli.haxor import Haxor
from hncli.toolbar import Toolbar


class ToolbarTest(unittest.TestCase):

    def setUp(self):
        self.haxor = Haxor()
        self.toolbar = Toolbar(self.haxor.get_fuzzy_match)

    def test_toolbar_on(self):
        self.haxor.set_fuzzy_match(True)
        expected = [
            (Token.Toolbar.On, ' [F2] Fuzzy: ON '),
            (Token.Toolbar, ' [F10] Exit ')]
        assert expected == self.toolbar.handler(None)

    def test_toolbar_off(self):
        self.haxor.set_fuzzy_match(False)
        expected = [
            (Token.Toolbar.Off, ' [F2] Fuzzy: OFF '),
            (Token.Toolbar, ' [F10] Exit ')]
        assert expected == self.toolbar.handler(None)
