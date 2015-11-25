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

import mock
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from click.testing import CliRunner

from hncli.onions import onions
from hncli.hacker_news_cli import HackerNewsCli


class HackerNewsCliTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.hacker_news_cli = HackerNewsCli()

    def assert_print_output(self, message, count, output, assert_tip=True):
        assert message in output
        assert '|   ' + str(count-1) + ' |' in output
        if assert_tip:
            assert 'Tip: View comments in your terminal' in output

    def test_hacker_news_cli(self):
        result = self.runner.invoke(self.hacker_news_cli.cli)
        assert result.exit_code == 0

    def test_ask(self):
        limit = 1
        result = self.runner.invoke(self.hacker_news_cli.cli, ['ask'])
        self.assert_print_output('Ask HN', limit, result.output)
        assert result.exit_code == 0

    def test_hiring(self):
        query = 'command line'
        post_id = '10251896'
        result = self.runner.invoke(self.hacker_news_cli.cli,
                                    ['hiring', query, post_id])
        assert query in result.output
        assert result.exit_code == 0

    def test_jobs(self):
        limit = 2
        result = self.runner.invoke(self.hacker_news_cli.cli,
                                    ['jobs', str(limit)])
        self.assert_print_output('Job', limit, result.output)
        assert result.exit_code == 0

    def test_new(self):
        limit = 3
        result = self.runner.invoke(self.hacker_news_cli.cli,
                                    ['new', str(limit)])
        self.assert_print_output('Latest', limit, result.output)
        assert result.exit_code == 0
