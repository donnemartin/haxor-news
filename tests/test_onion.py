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

from click.testing import CliRunner

from onion.lulz import lulz
from onion.onion import Onion
from onion.onion_cli import OnionCli
from data import expected_lol_troll, expected_partial_lol_troll


class OnionTest(unittest.TestCase):

    def setUp(self):
        self.onion = Onion()

    def test_onion_config(self):
        expected = os.path.join(os.path.abspath(os.environ.get('HOME', '')),
                                self.onion.CONFIG)
        assert self.onion._onion_config(self.onion.CONFIG) == expected

    def test_generate_lol_troll(self):
        lol_troll = self.onion.generate_lol_troll(lol_index=len(lulz)-1,
                                                  troll_index=0)
        assert lol_troll == expected_lol_troll

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

    def test_onion_cli(self):
        runner = CliRunner()
        onion_cli = OnionCli()
        result = runner.invoke(onion_cli.cli)
        assert result.exit_code == 0

    def test_onion_cli_headline(self):
        runner = CliRunner()
        onion_cli = OnionCli()
        headline = str(len(lulz)-1)
        result = runner.invoke(onion_cli.cli, [headline])
        assert expected_partial_lol_troll in result.output
        assert result.exit_code == 0

    def test_onion_cli_headline_error(self):
        runner = CliRunner()
        onion_cli = OnionCli()
        result = runner.invoke(onion_cli.cli, ['foo'])
        expected = u'Expected int arg from 0 to ' + str(len(lulz))
        assert expected in result.output
        assert result.exit_code == 0
