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

import os
import platform
import subprocess
import sys
import traceback
import webbrowser

import click
from prompt_toolkit import AbortAction, Application, CommandLineInterface
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Always, HasFocus, IsDone
from prompt_toolkit.interface import AcceptAction
from prompt_toolkit.layout.processors import \
    HighlightMatchingBracketProcessor, ConditionalProcessor
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding.input_processor import KeyPress
from prompt_toolkit.keys import Keys
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .__init__ import __version__
from .completer import Completer
from .hacker_news_cli import HackerNewsCli
from .keys import KeyManager
from .style import StyleFactory
from .toolbar import Toolbar
from .utils import TextUtils


class Haxor(object):
    """Encapsulates the Hacker News CLI.

    Attributes:
        * key_manager: An instance of KeyManager.
        * theme: A string representing the lexer theme.
    """

    def __init__(self):
        """Inits Saws.

        Args:
            * None.

        Returns:
            None.
        """
        self.cli = None
        self.key_manager = None
        self.color = False
        self.theme = 'vim'
        self.hacker_news_cli = HackerNewsCli()
        self.text_utils = TextUtils()
        self.completer = Completer(fuzzy_match=False,
                                   text_utils=self.text_utils)
        self._create_cli()

    def set_fuzzy_match(self, fuzzy_match):
        """Setter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * fuzzy_match: A boolean that represents the fuzzy flag.

        Returns:
            None.
        """
        self.completer.fuzzy_match = fuzzy_match

    def get_fuzzy_match(self):
        """Getter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the fuzzy flag.
        """
        return self.completer.fuzzy_match

    def _create_cli(self):
        """Creates the prompt_toolkit's CommandLineInterface.

        Args:
            * None.

        Returns:
            None.
        """
        history = FileHistory(os.path.expanduser('~/.hnclihistory'))
        toolbar = Toolbar(self.get_fuzzy_match)
        layout = create_default_layout(
            message=u'haxor> ',
            reserve_space_for_menu=True,
            get_bottom_toolbar_tokens=toolbar.handler,
        )
        cli_buffer = Buffer(
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            completer=self.completer,
            complete_while_typing=Always(),
            accept_action=AcceptAction.RETURN_DOCUMENT)
        self.key_manager = KeyManager(
            self.set_fuzzy_match,
            self.get_fuzzy_match)
        style_factory = StyleFactory(self.theme)
        application = Application(
            mouse_support=False,
            style=style_factory.style,
            layout=layout,
            buffer=cli_buffer,
            key_bindings_registry=self.key_manager.manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            on_abort=AbortAction.RETRY,
            ignore_case=True)
        eventloop = create_eventloop()
        self.cli = CommandLineInterface(
            application=application,
            eventloop=eventloop)

    def run_cli(self):
        """Runs the main loop.

        Args:
            * None.

        Returns:
            None.
        """
        click.echo('Version: ' + __version__)
        click.echo('Syntax: hn <command> [params] [options]')
        while True:
            document = self.cli.run()
            try:
                subprocess.call(document.text, shell=True)
                click.echo('')
            except Exception as e:
                click.secho(e, fg='red')
