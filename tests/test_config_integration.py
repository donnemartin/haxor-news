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
from tests.compat import unittest

from haxor_news.hacker_news import HackerNews
from haxor_news.settings import freelancer_post_id, who_is_hiring_post_id
from tests.mock_hacker_news_api import MockHackerNewsApi


class ConfigTestIntegration(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()
        self.hn.hacker_news_api = MockHackerNewsApi()
        self.limit = len(self.hn.hacker_news_api.items)

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
