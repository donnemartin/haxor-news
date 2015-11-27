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
from html2text import HTML2Text
import requests
from tabulate import tabulate

from .haxor.haxor import HackerNewsApi

class HackerNews(object):
    """Encapsulates Hacker News.

    Attributes:
        * COMMENT_INDENT: A string representing the indent amount for comments.
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_INDEX: A string representing the last index used.
        * hacker_news_api: An instance of HackerNews.
        * item_ids: A list containing the last set of ids the user has seen,
            which allows the user to quickly access an item with the
            gh view [#] [-u/--url] command.
        * TIP: A string that lets the user know about the hn view command.
        * URL_POST: A string that represents a Hacker News post minus the
            post id.
    """

    COMMENT_INDENT = '    '
    CONFIG = '.hncliconfig'
    CONFIG_SECTION = 'hncli'
    CONFIG_INDEX = 'item_ids'
    TIP = 'Tip: View the page or comments in your terminal with the ' \
          'following command:\n' \
          '    hn view [#] [-c/--comments]'
    URL_POST = 'https://news.ycombinator.com/item?id='

    def __init__(self):
        """Initializes HackerNews.

        Args:
            * None.

        Returns:
            None.
        """
        self.hacker_news_api = HackerNewsApi()
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

    def pretty_date_time(self, date_time):
        """Prints a pretty datetime similar to what's seen on Hacker News.

        Gets a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc.

        Adapted from: http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python

        Args:
            * date_time: An instance of datetime.

        Returns:
            A string that represents the pretty datetime.
        """
        from datetime import datetime
        now = datetime.now()
        if type(date_time) is int:
            diff = now - datetime.fromtimestamp(date_time)
        elif isinstance(date_time,datetime):
            diff = now - date_time
        elif not date_time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days
        if day_diff < 0:
            return ''
        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return "1 minute ago"
            if second_diff < 3600:
                return str(second_diff // 60) + " minutes ago"
            if second_diff < 7200:
                return "1 hour ago"
            if second_diff < 86400:
                return str(second_diff // 3600) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff // 7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff // 30) + " months ago"
        return str(day_diff // 365) + " years ago"

    def print_comments(self, item, regex_query='', depth=0):
        """Recursively print comments and subcomments for the given item.

        Args:
            * item: An instance of haxor.Item.
            * regex_query: A string that specifies the regex query to match.
            * depth: The current recursion depth, used to indent the comment.

        Returns:
            None.
        """
        comment_ids = item.kids
        if item.text is not None:
            print_comment = True
            if regex_query and not self.regex_match(item, regex_query):
                print_comment = False
            if print_comment:
                self.print_formatted_comment(item, depth)
        if not comment_ids:
            return
        for comment_id in comment_ids:
            comment = self.hacker_news_api.get_item(comment_id)
            depth += 1
            self.print_comments(comment, regex_query=regex_query, depth=depth)
            depth -= 1

    def print_formatted_comment(self, item, depth):
        """Formats and prints a given item's comment.

        Args:
            * item: An instance of haxor.Item.
            * depth: The current recursion depth, used to indent the comment.

        Returns:
            None.
        """
        indent = self.COMMENT_INDENT * depth
        click.secho(
            '\n' + indent + item.by + ' - ' + \
            str(self.pretty_date_time(item.submission_time)),
            fg='yellow')
        html_to_text = HTML2Text()
        html_to_text.body_width = 0
        markdown = html_to_text.handle(item.text)
        markdown = re.sub('\n\n', '\n\n' + indent, markdown)
        wrapped_markdown = click.wrap_text(
            text=markdown,
            initial_indent=indent,
            subsequent_indent=indent)
        click.echo(wrapped_markdown)

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
            item = self.hacker_news_api.get_item(item_id)
            if item.title:
                table.append([rank, item.title, item.score, item.descendants])
                self.item_ids.append(item.item_id)
                rank += 1
        self.save_item_ids()
        self.print_table(table, headers=['#', 'Title', 'Score', 'Comments'])
        click.secho(str(self.TIP), fg='blue')

    def print_table(self, table, headers):
        """Prints the table and headers with tabulate.

        Args:
            * table: A collection of items to print as rows with tabulate.
            * headers: A collection of column headers to print with tabulate.

        Returns:
            None.
        """
        click.echo(tabulate(table, headers, tablefmt='grid'))

    def save_item_ids(self):
        """Saves the current set of item ids to ~/.hncliconfig.

        Args:
            * None

        Returns:
            None.
        """
        config = self._config(self.CONFIG)
        parser = configparser.RawConfigParser()
        parser.add_section(self.CONFIG_SECTION)
        parser.set(self.CONFIG_SECTION, self.CONFIG_INDEX, self.item_ids)
        parser.write(open(config, 'w+'))

    def view(self, index, comments_query, comments):
        """Views the given index in a browser.

        Loads item ids from ~/.hncliconfig and stores them in self.item_ids.
        If url is True, opens a browser with the url based on the given index.
        Else, displays the post's comments.

        Args:
            * index: An int that specifies the index to open in a browser.
            * comments_query: A string that specifies the regex query to match.
            * comments: A boolean that determines whether to view the comments
                or a simplified version of the post url.

        Returns:
            None.
        """
        config = self._config(self.CONFIG)
        parser = configparser.RawConfigParser()
        try:
            parser.readfp(open(config))
            items_ids = parser.get(self.CONFIG_SECTION,
                                   self.CONFIG_INDEX)
            items_ids = items_ids.strip()
            excludes = ['[', ']', "'"]
            for exclude in excludes:
                items_ids = items_ids.replace(exclude, '')
            self.item_ids = items_ids.split(', ')
            item = self.hacker_news_api.get_item(self.item_ids[index])
            if comments:
                comments_url = self.URL_POST + str(item.item_id)
                click.secho('Fetching Comments from ' + comments_url, fg='blue')
                self.print_comments(item, regex_query=comments_query)
            else:
                click.secho('Opening ' + item.url + '...', fg='blue')
                response = requests.get(item.url)
                html_to_text = HTML2Text()
                html_to_text.ignore_links = True
                click.echo_via_pager(html_to_text.handle(response.text))
        except Exception as e:
            click.secho('Error: ' + str(e), fg='red')
