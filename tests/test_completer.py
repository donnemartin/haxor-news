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

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import mock
from tests.compat import unittest

from prompt_toolkit.document import Document

from haxor_news.completions import ARG_POST_LIMIT, ARG_HIRING_REGEX_QUERY, \
    ARG_VIEW_POST_INDEX, ARG_USER_ID, COMMAND, SUBCOMMAND_VIEW, \
    OPTIONS_HIRING, OPTIONS_USER, OPTIONS_VIEW, OPTION_BROWSER, \
    OPTIONS_FREELANCE
from haxor_news.completer import Completer
from haxor_news.utils import TextUtils


class CompleterTest(unittest.TestCase):

    def setUp(self):
        self.completer = Completer(fuzzy_match=False,
                                   text_utils=TextUtils())
        self.completer_event = self.create_completer_event()

    def create_completer_event(self):
        return mock.Mock()

    def _get_completions(self, command):
        position = len(command)
        result = set(self.completer.get_completions(
            Document(text=command, cursor_position=position),
            self.completer_event))
        return result

    def verify_completions(self, commands, expected):
        result = set()
        for command in commands:
            # Call the AWS CLI autocompleter
            result.update(self._get_completions(command))
        result_texts = []
        for item in result:
            # Each result item is a Completion object,
            # we are only interested in the text portion
            result_texts.append(item.text)
        assert result_texts
        if len(expected) == 1:
            assert expected[0] in result_texts
        else:
            for item in expected:
                assert item in result_texts

    def test_blank(self):
        text = ''
        expected = set([])
        result = self._get_completions(text)
        assert result == expected

    def test_no_completions(self):
        text = 'foo'
        expected = set([])
        result = self._get_completions(text)
        assert result == expected

    def test_command(self):
        text = ['h']
        expected = [COMMAND]
        self.verify_completions(text, expected)

    def test_subcommand(self):
        text = ['hn as']
        expected = ['ask']
        self.verify_completions(text, expected)

    def test_arg_freelance(self):
        text = ['hn freelance ']
        expected = [ARG_HIRING_REGEX_QUERY]
        self.verify_completions(text, expected)

    def test_arg_hiring(self):
        text = ['hn hiring ']
        expected = [ARG_HIRING_REGEX_QUERY]
        self.verify_completions(text, expected)

    def test_arg_limit(self):
        text = ['hn top ']
        expected = [ARG_POST_LIMIT]
        self.verify_completions(text, expected)

    def test_arg_user(self):
        text = ['hn user ']
        expected = [ARG_USER_ID]
        self.verify_completions(text, expected)

    def test_arg_view(self):
        text = ['hn view ']
        expected = [ARG_VIEW_POST_INDEX]
        self.verify_completions(text, expected)

    def test_option_freelance(self):
        text = ['hn freelance "" ']
        expected = OPTIONS_FREELANCE
        self.verify_completions(text, expected)

    def test_option_hiring(self):
        text = ['hn hiring "" ']
        expected = OPTIONS_HIRING
        self.verify_completions(text, expected)

    def test_option_user(self):
        text = ['hn user "" ']
        expected = OPTIONS_USER
        self.verify_completions(text, expected)

    def test_option_view(self):
        text = ['hn view 0 ']
        expected = OPTIONS_VIEW
        self.verify_completions(text, expected)

    def test_completing_option(self):
        text = ['hn view 0 -']
        expected = OPTIONS_VIEW
        self.verify_completions(text, expected)

    def test_multiple_options(self):
        text = ['hn view 0 -c --brow']
        expected = [OPTION_BROWSER]
        self.verify_completions(text, expected)

    def test_fuzzy(self):
        text = ['hn vw']
        expected = [SUBCOMMAND_VIEW]
        self.completer.fuzzy_match = True
        self.verify_completions(text, expected)
