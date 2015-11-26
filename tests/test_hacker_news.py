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
