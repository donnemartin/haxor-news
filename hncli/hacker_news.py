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
import random
import re
import webbrowser
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import click
from tabulate import tabulate

from haxor.haxor import HackerNewsApi

class HackerNews(object):
    """Encapsulates Hacker News.

    Attributes:
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_INDEX: A string representing the last index used.
        * hacker_news: An instance of HackerNews.
        * item_ids: A list containing the last set of ids the user has seen,
            which allows the user to quickly access an item with the
            gh view [#] [-u/--url] command.
    """

    CONFIG = '.hncliconfig'
    CONFIG_SECTION = 'hncli'
    CONFIG_INDEX = 'item_ids'

    def __init__(self):
        """Initializes HackerNews.

        Args:
            * None.

        Returns:
            None.
        """
        self.hacker_news = HackerNewsApi()
        self.item_ids = []

    def _config(self, config_file_name):
        """Gets the config file path.

        Args:
            * config_file_name: A String that represents the config file name.

        Returns:
            A string that represents the hn config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def print_comments(self, item, regex_query='', depth=0):
        comment_ids = item.kids
        if item.text is not None:
            print_comment = True
            if regex_query:
                match = re.search(regex_query, item.text)
                if not match:
                    print_comment = False
            if print_comment:
                indent = '  ' * depth
                click.secho(
                    indent + item.by + ' - ' + str(item.submission_time),
                    fg='blue')
                click.echo(indent + item.text + '\n')
        if not comment_ids:
            return
        for comment_id in comment_ids:
            comment = self.hacker_news.get_item(comment_id)
            depth += 1
            self.print_comments(comment, regex_query=regex_query, depth=depth)
            depth -= 1

    def print_items(self, message, item_ids):
        """Prints the items and headers with tabulate.

        Args:
            * message: A string to print out to the user before outputting
                the results.
            * item_ids: A collection of items to print as rows with tabulate.
                Can be a list or dictionary.

        Returns:
            None.
        """
        click.secho(message, fg='blue')
        rank = 0
        table = []
        for item_id in item_ids:
            item = self.hacker_news.get_item(item_id)
            if item.title:
                table.append([rank, item.title, item.score, item.descendants])
                self.item_ids.append(item.item_id)
                rank += 1
        self.save_item_ids()
        self.print_table(table, headers=['#', 'Title', 'Score', 'Comments'])
        click.secho('Tip: View comments in your terminal or the url in your' \
                    ' browser with the following command:\n' \
                    '    hn view [#] [-u/--url]',
                    fg='blue')
