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
import os
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from hncli.hacker_news import HackerNews


class HackerNewsTest(unittest.TestCase):

    def setUp(self):
        self.hacker_news = HackerNews()

    def jobs(self, limit=2):
        self.hacker_news.print_items(
            message='Fetching Latest Headlines...',
            item_ids=self.hacker_news.hacker_news_api.job_stories(limit))

    def test_config(self):
        expected = os.path.join(os.path.abspath(os.environ.get('HOME', '')),
                                self.hacker_news.CONFIG)
        assert self.hacker_news._config(self.hacker_news.CONFIG) == expected

    @mock.patch('hncli.hacker_news.click')
    def test_print_comments(self, mock_click):
        query = 'command line'
        post_id = '10251896'
        post = self.hacker_news.hacker_news_api.get_item(post_id)
        self.hacker_news.print_comments(post, query)
        mock_click.secho.assert_called_with(
            '\n' + self.hacker_news.COMMENT_INDENT + \
            u'amjith - 2015-09-21 16:13:13',
            fg='blue')

    @mock.patch('hncli.hacker_news.click')
    def test_print_items(self, mock_click):
        self.hacker_news.item_ids = []
        limit = 3
        self.jobs(limit)
        assert len(self.hacker_news.item_ids) == limit
        mock_click.secho.assert_called_with(self.hacker_news.TIP, fg='blue')

    @mock.patch('hncli.hacker_news.click')
    def test_view(self, mock_click):
        limit = 3
        self.jobs(limit)
        index = 0
        query = ''
        comments = False
        self.hacker_news.view(index, query, comments)
        item_id = self.hacker_news.item_ids[index]
        item = self.hacker_news.hacker_news_api.get_item(item_id)
        message = 'Opening ' + item.url + '...'
        assert mock.call(message, fg='blue') in mock_click.secho.mock_calls
        assert mock_click.echo_via_pager.mock_calls
