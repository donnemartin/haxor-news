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

    def test_headlines_message(self):
        message = 'foo'
        headlines_message = self.hn.headlines_message(message)
        assert message in headlines_message

    @mock.patch('hncli.hacker_news.HackerNews.print_comments')
    @mock.patch('hncli.hacker_news.HackerNews.print_item_not_found')
    def test_hiring(self, mock_print_item_not_found, mock_print_comments):
        self.hn.hiring(self.query, post_id=self.valid_id)
        item = self.hn.hacker_news_api.get_item(self.valid_id)
        mock_print_comments.assert_called_with(item, self.query)
        self.hn.hiring(self.query, post_id=self.invalid_id)
        mock_print_item_not_found.assert_called_with(self.invalid_id)

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    def test_jobs(self, mock_print_items):
        self.hn.jobs(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message(self.hn.MSG_JOBS),
            item_ids=self.hn.hacker_news_api.ask_stories(self.limit))

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    def test_new(self, mock_print_items):
        self.hn.new(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message(self.hn.MSG_NEW),
            item_ids=self.hn.hacker_news_api.new_stories(self.limit))

    @mock.patch('hncli.hacker_news.HackerNews.print_index_title')
    @mock.patch('hncli.hacker_news.click')
    def test_onion(self, mock_click, mock_print_index_title):
        self.hn.onion(self.limit)
        assert len(mock_print_index_title.mock_calls) == self.limit
        assert mock_click.mock_calls

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    def test_show(self, mock_print_items):
        self.hn.show(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message(self.hn.MSG_SHOW),
            item_ids=self.hn.hacker_news_api.show_stories(self.limit))

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    def test_top(self, mock_print_items):
        self.hn.top(self.limit)
        mock_print_items.assert_called_with(
            message=self.hn.headlines_message(self.hn.MSG_TOP),
            item_ids=self.hn.hacker_news_api.top_stories(self.limit))

    @mock.patch('hncli.hacker_news.HackerNews.print_items')
    @mock.patch('hncli.hacker_news.click')
    @mock.patch('hncli.hacker_news.HackerNews.print_item_not_found')
    def test_user(self, mock_print_item_not_found,
                  mock_click, mock_print_items):
        user_id = 'foo'
        self.hn.user(user_id, self.limit)
        user = self.hn.hacker_news_api.get_user(user_id)
        mock_print_items.assert_called_with(
            self.hn.MSG_SUBMISSIONS, user.submitted[0:self.limit])
        assert mock_click.mock_calls
        self.hn.user(self.invalid_id, self.limit)
        mock_print_item_not_found.assert_called_with(self.invalid_id)
