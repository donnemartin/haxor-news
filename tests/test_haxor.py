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
import platform

from tests.compat import unittest

from haxor_news.haxor import Haxor


class HaxorTest(unittest.TestCase):

    def setUp(self):
        self.haxor = Haxor()

    def test_add_comment_pagination(self):
        text = 'hn view 1'
        result = self.haxor._add_comment_pagination(text)
        assert result == text
        text = 'hn view 1 -c'
        result = self.haxor._add_comment_pagination(text)
        if platform.system() == 'Windows':
            assert result == text + self.haxor.PAGINATE_CMD_WIN
        else:
            assert result == text + self.haxor.PAGINATE_CMD
        text = 'hn view 1 -c -b'
        result = self.haxor._add_comment_pagination(text)
        assert result == text

    @mock.patch('haxor_news.haxor.subprocess.call')
    def test_run_command(self, mock_subprocess_call):
        document = mock.Mock()
        document.text = 'hn view 1 -c'
        self.haxor.run_command(document)
        mock_subprocess_call.assert_called_with('hn view 1 -c | less -r',
                                                shell=True)
        document.text = 'hn view 1'
        self.haxor.run_command(document)
        mock_subprocess_call.assert_called_with('hn view 1',
                                                shell=True)
