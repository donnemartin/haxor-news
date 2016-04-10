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
from tests.compat import unittest

from haxor_news.hacker_news import HackerNews
from haxor_news.settings import freelancer_post_id, who_is_hiring_post_id
from tests.mock_hacker_news_api import MockHackerNewsApi


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()
        self.hn.hacker_news_api = MockHackerNewsApi()
        self.limit = len(self.hn.hacker_news_api.items)
        self.valid_id = 0
        self.invalid_id = 9000
        self.query = 'foo'

    def test_config(self):
        expected = os.path.join(os.path.abspath(os.environ.get('HOME', '')),
                                self.hn.config.CONFIG)
        assert self.hn.config.get_config_path(self.hn.config.CONFIG) == expected

    @mock.patch('haxor_news.config.Config.save_cache')
    def test_clear_item_cache(self, mock_save_cache):
        item_ids = self.hn.config.item_ids
        self.hn.config.clear_item_cache()
        assert self.hn.config.item_ids == item_ids
        assert self.hn.config.item_cache == []
        mock_save_cache.assert_called_with()

    def test_load_hiring_and_freelance_ids(self):
        self.hn.config.load_hiring_and_freelance_ids()
        assert self.hn.config.hiring_id != who_is_hiring_post_id
        assert self.hn.config.freelance_id != freelancer_post_id

    def test_load_hiring_and_freelance_ids_invalid_url(self):
        self.hn.config.load_hiring_and_freelance_ids(url='https://example.com')
        assert self.hn.config.hiring_id == who_is_hiring_post_id
        assert self.hn.config.freelance_id == freelancer_post_id
        os.remove('./downloaded_settings.py')

    def test_load_hiring_and_freelance_ids_from_cache_or_defaults(self):
        self.hn.config.load_hiring_and_freelance_ids_from_cache_or_defaults()
        assert self.hn.config.hiring_id == who_is_hiring_post_id
        assert self.hn.config.freelance_id == freelancer_post_id

    def test_save_and_load_item_ids(self):
        self.hn.config.item_ids = [0, 1, 2]
        self.hn.config.item_cache = [3, 4, 5]
        self.hn.config.save_cache()
        item_ids = self.hn.config.item_ids
        assert item_ids == [0, 1, 2]
        item_cache = self.hn.config.item_cache
        assert item_cache == [3, 4, 5]

    @mock.patch('haxor_news.hacker_news.HackerNews.view')
    @mock.patch('haxor_news.config.Config.clear_item_cache')
    def test_view_comment_clear_cache(self, mock_clear_item_cache, mock_view):
        index = 0
        comments = False
        comments_recent = False
        comments_unseen = True
        comments_hide_non_matching = False
        comments_clear_cache = True
        browser = False
        self.hn.view_setup(
            index, self.query, comments, comments_recent,
            comments_unseen, comments_hide_non_matching,
            comments_clear_cache, browser)
        comments_expected = True
        mock_clear_item_cache.assert_called_with()
        mock_view.assert_called_with(
            index, self.hn.QUERY_UNSEEN, comments_expected,
            comments_hide_non_matching, browser)
