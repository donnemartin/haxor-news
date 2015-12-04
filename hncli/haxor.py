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
import click
import os
import platform
import subprocess
import sys
import traceback
import webbrowser
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
from .completer import Completer
# from .lexer import CommandLexer
# from .config import Config
from .style import StyleFactory
from .keys import KeyManager
from .toolbar import Toolbar
from .hacker_news_cli import HackerNewsCli
from .utils import TextUtils
# from .commands import AwsCommands
from .__init__ import __version__


class Haxor(object):
    """Encapsulates the Hacker News CLI.

    Attributes:
        * key_manager: An instance of KeyManager.
        * theme: A string representing the lexer theme.
    """

    def __init__(self, refresh_resources=True):
        """Inits Saws.

        Args:
            * refresh_resources: A boolean that determines whether to
                refresh resources.

        Returns:
            None.
        """
        self.cli = None
        self.key_manager = None
        self.color = False
        self.theme = 'vim'
        self.hacker_news_cli = HackerNewsCli()
        self.text_utils = TextUtils()
        # self.all_commands = AwsCommands().all_commands
        # self.commands = \
        #     self.all_commands[AwsCommands.CommandType.COMMANDS.value]
        # self.sub_commands = \
        #     self.all_commands[AwsCommands.CommandType.SUB_COMMANDS.value]
        self.completer = Completer()
        # if refresh_resources:
        #     self.completer.refresh_resources_and_options()
        self._create_cli()

    def set_color(self, color):
        """Setter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the color flag.

        Returns:
            None.
        """
        self.color = color

    def get_color(self):
        """Getter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the color flag.
        """
        return self.color

    def refresh_resources_and_options(self):
        """Convenience function to refresh resources and options for completion.

        Used by prompt_toolkit's KeyBindingManager.

        Args:
            * None.

        Returns:
            None.
        """
        pass

    def _create_cli(self):
        """Creates the prompt_toolkit's CommandLineInterface.

        Args:
            * None.

        Returns:
            None.
        """
        history = FileHistory(os.path.expanduser('~/.hnclihistory'))
        toolbar = Toolbar(self.get_color)
        layout = create_default_layout(
            message='haxor> ',
            reserve_space_for_menu=True,
            # lexer=CommandLexer,
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
            self.set_color,
            self.get_color,
            self.refresh_resources_and_options)
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

    def _process_command(self, args):
        """Executes the gh command.

        Calls the dispatch to execute the command.
        If no command is given, it lists all available commands.
        Prints the rate limit if it starts to get low.

        Args:
            * args: A list of user supplied args.

        Returns:
            None.
        """
        old_sys_args = list(sys.argv)
        if args:
            # GitHubCli uses click, which looks for args in sys.argv.
            # Update sys.argv with our arguments before sending the command
            # off to GitHubCli.
            # TODO: Determine if there is a cleaner way to do this.
            sys.argv.extend(args)
        try:
            # Send the command to GitHubCli.
            self.hacker_news_cli.cli()
        except:
            # TODO: After every cli call the following exception is thrown:
            #   AttributeError: 'module' object has no
            #       attribute '__xonsh_env__'
            # Suppressing this exception does also silence helpful errors
            # during debugging, so disable this try/except block during dev
            # until this problem is fixed.
            pass
        if args:
            # Restore sys.argv to its original state.
            sys.argv = old_sys_args

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
            self.cli.start_completion(select_first=False)
            try:
                text = document.text
                text = text.strip('\n')
                text = text.strip()
                args = self.text_utils.get_tokens(text)
                if len(args) > 0 and args[0].lower() == 'hn':
                    self._process_command(args[1:])
                else:
                    subprocess.call(document.text, shell=True)
                    click.echo('')
            except Exception as e:
                click.secho(e, fg='red')
