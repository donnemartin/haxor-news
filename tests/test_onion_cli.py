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

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from click.testing import CliRunner

from onion.lulz import lulz
from onion.onion_cli import OnionCli
from data import expected_partial_lol_troll


class OnionCliTest(unittest.TestCase):

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

    def test_onion_cli_random(self):
        runner = CliRunner()
        onion_cli = OnionCli()
        result = runner.invoke(onion_cli.cli, ['-r'])
        assert result.exit_code == 0
