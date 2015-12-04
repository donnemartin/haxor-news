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

import re
import sys
import traceback

import click
from prompt_toolkit.completion import Completer
from six.moves import cStringIO

from .completions import ARG_POST_LIMIT, ARG_HIRING_REGEX_QUERY, \
    ARG_VIEW_POST_INDEX, ARG_USER_ID, COMMAND, SUBCOMMAND_HIRING, \
    SUBCOMMAND_USER, SUBCOMMAND_VIEW, OPTIONS_HIRING, OPTIONS_USER, \
    OPTIONS_VIEW, SUB_COMMANDS
from .utils import TextUtils


class Completer(Completer):
    """Completer hncli.

    Attributes:
        * None
    """

    def __init__(self):
        """Initializes Completer.

        Args:
            * None.

        Returns:
            None.
        """
        self.text_utils = TextUtils()

    def completing_command(self, words, word_before_cursor):
        if len(words) == 1 and word_before_cursor != '':
            return True
        else:
            return False

    def completing_sub_command(self, words, word_before_cursor):
        if (len(words) == 1 and word_before_cursor == '') \
            or (len(words) == 2 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_arg(self, words, word_before_cursor):
        if (len(words) == 2 and word_before_cursor == '') \
            or (len(words) == 3 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_sub_command_option(self, option, words, word_before_cursor):
        if option in words and \
            (words[-2] == option or \
                self.completing_option(option, words)):
            return True
        else:
            return False

    def completing_option(self, option, words):
        # Example: Return True for: hn view 0 --comm
        if len(words) > 3:
            if words[-3] == option:
                return True
        return False

    def generate_arg(self, words, word_before_cursor):
        if COMMAND not in words:
            return []
        elif SUBCOMMAND_HIRING in words:
            return [ARG_HIRING_REGEX_QUERY]
        elif SUBCOMMAND_USER in words:
            return [ARG_USER_ID]
        elif SUBCOMMAND_VIEW in words:
            return [ARG_VIEW_POST_INDEX]
        else:
            return [ARG_POST_LIMIT]
        return []

    def get_completions(self, document, _):
        """Get completions for the current scope.

        Args:
            * document: An instance of prompt_toolkit's Document.
            * _: An instance of prompt_toolkit's CompleteEvent (not used).

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if self.completing_command(
            words, word_before_cursor):
            commands = [COMMAND]
        else:
            if self.completing_sub_command(words, word_before_cursor):
                commands = SUB_COMMANDS
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.generate_arg(words, word_before_cursor)
                elif self.completing_sub_command_option(
                    SUBCOMMAND_HIRING, words, word_before_cursor):
                    commands = OPTIONS_HIRING
                elif self.completing_sub_command_option(
                    SUBCOMMAND_USER, words, word_before_cursor):
                    commands = OPTIONS_USER
                elif self.completing_sub_command_option(
                    SUBCOMMAND_VIEW, words, word_before_cursor):
                    commands = OPTIONS_VIEW
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=False)
        return completions
