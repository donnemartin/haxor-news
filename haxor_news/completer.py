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

from prompt_toolkit.completion import Completer

from .completions import ARG_POST_LIMIT, ARG_HIRING_REGEX_QUERY, \
    ARG_VIEW_POST_INDEX, ARG_USER_ID, COMMAND, SUBCOMMAND_HIRING, \
    SUBCOMMAND_USER, SUBCOMMAND_VIEW, OPTIONS_HIRING, OPTIONS_USER, \
    OPTIONS_VIEW, SUBCOMMANDS, SUBCOMMAND_FREELANCE, OPTIONS_FREELANCE


class Completer(Completer):
    """Completer haxor-news.

    Attributes:
        * text_utils: An instance of TextUtils.
        * fuzzy_match: A boolean that determines whether to use fuzzy matching.
    """

    def __init__(self, fuzzy_match, text_utils):
        """Initializes Completer.

        Args:
            * text_utils: An instance of TextUtils.
            * fuzzy_match: A boolean that determines whether to use
                fuzzy matching.

        Returns:
            None.
        """
        self.fuzzy_match = fuzzy_match
        self.text_utils = text_utils

    def completing_command(self, words, word_before_cursor):
        """Determines if we are currently completing the hn command.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A boolean that specifies whether we are currently completing the
                hn command.
        """
        if len(words) == 1 and word_before_cursor != '':
            return True
        else:
            return False

    def completing_subcommand(self, words, word_before_cursor):
        """Determines if we are currently completing a subcommand.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A boolean that specifies whether we are currently completing a
                subcommand.
        """
        if (len(words) == 1 and word_before_cursor == '') \
                or (len(words) == 2 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_arg(self, words, word_before_cursor):
        """Determines if we are currently completing an arg.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A boolean that specifies whether we are currently completing an arg.
        """
        if (len(words) == 2 and word_before_cursor == '') \
                or (len(words) == 3 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_subcommand_option(self, option, words, word_before_cursor):
        """Determines if we are currently completing an option.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A boolean that specifies whether we are currently completing an
                option.
        """
        if option in words and \
            (words[-2] == option or
                self.completing_subcommand_option_util(option, words)):
            return True
        else:
            return False

    def completing_subcommand_option_util(self, option, words):
        """Determines if we are currently completing an option.

        Called by completing_subcommand_option as a utility method.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A boolean that specifies whether we are currently completing an
                option.
        """
        # Example: Return True for: hn view 0 --comm
        if len(words) > 3:
            # if words[-3] == option:
            if option in words:
                return True
        return False

    def arg_completions(self, words, word_before_cursor):
        """Generates arguments completions based on the input.

        Args:
            * words: A list of words repsenting the input text.
            * word_before_cursor: A string that represents the current word
                 before the cursor, which might be one or more blank spaces.

        Returns:
            A list of completions.
        """
        if COMMAND not in words:
            return []
        elif SUBCOMMAND_FREELANCE in words:
            return [ARG_HIRING_REGEX_QUERY]
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
        if self.completing_command(words, word_before_cursor):
            commands = [COMMAND]
        else:
            if self.completing_subcommand(words, word_before_cursor):
                commands = SUBCOMMANDS
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.arg_completions(words, word_before_cursor)
                elif self.completing_subcommand_option(
                        SUBCOMMAND_FREELANCE, words, word_before_cursor):
                    commands = OPTIONS_FREELANCE
                elif self.completing_subcommand_option(
                        SUBCOMMAND_HIRING, words, word_before_cursor):
                    commands = OPTIONS_HIRING
                elif self.completing_subcommand_option(
                        SUBCOMMAND_USER, words, word_before_cursor):
                    commands = OPTIONS_USER
                elif self.completing_subcommand_option(
                        SUBCOMMAND_VIEW, words, word_before_cursor):
                    commands = OPTIONS_VIEW
                else:
                    commands = []
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match)
        return completions
