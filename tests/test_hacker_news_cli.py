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

from hncli.hacker_news import HackerNews
from hncli.hacker_news_cli import HackerNewsCli


class HackerNewsCliTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.hacker_news_cli = HackerNewsCli()
        self.limit = 10
        self.user = 'foo'
        self.dummy = 'foo'

    def test_cli(self):
        result = self.runner.invoke(self.hacker_news_cli.cli)
        assert result.exit_code == 0

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    def test_ask(self, mock_print_items):
        self.hn.ask(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message(self.hn.MSG_ASK),
            item_ids=self.hn.hacker_news_api.ask_stories(self.limit))

    @mock.patch('hncli.hacker_news.HackerNews.print_comments')
    @mock.patch('hncli.hacker_news.HackerNews.print_item_not_found')
    def test_comments(self, mock_print_item_not_found, mock_print_comments):
        self.hn.comments(self.valid_id, regex_query=self.query)
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        mock_print_comments.assert_called_with(item, regex_query=self.query)
        self.hn.comments(self.invalid_id, regex_query=self.query)
        mock_print_item_not_found.assert_called_with(self.invalid_id)

    @mock.patch('hncli.hacker_news.HackerNews.print_comments')
    @mock.patch('hncli.hacker_news.HackerNews.print_item_not_found')
    def test_hiring(self, mock_print_item_not_found, mock_print_comments):
        self.hn.hiring(self.query, post_id=self.valid_id)
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        mock_print_comments.assert_called_with(item, self.query)
        self.hn.hiring(self.query, post_id=self.invalid_id)
        mock_print_item_not_found.assert_called_with(self.invalid_id)
