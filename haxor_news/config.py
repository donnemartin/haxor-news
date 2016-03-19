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
import urllib

import click
from .compat import configparser


class Config(object):
    """Hacker News config.

    Attributes:
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_CLR_XXX: A string representing the ansi color to use to
            highlight the specified item.
        * CONFIG_IDS: A string representing the last list of seen post ids.
        * CONFIG_CACHE: A string representing the list of seen comments.
        * CONFIG_HIRING_ID: A string representing the monthly freelancer
            post id.
        * CONFIG_FREELANCE_ID: A string representing the monthly who's hiring
            post id.
        * CONFIG_SHOW_TIP: A boolean that determines whether to show the tip.
        * freelance_id: An int representing the monthly freelancer post id.
        * hiring_id: An int representing the monthly who's hiring post id.
        * item_cache: A list of seen comment ids.
            TODO: Look into an OrderedSet for improved lookup performance
            http://code.activestate.com/recipes/576694/
        * item_ids: A list containing the last set of ids the user has seen,
            which allows the user to quickly access an item with the
            gh view [#] [-u/--url] command.
        * MAX_ITEM_CACHE_SIZE: An int representing the maximum number of
            seen comment ids.
    """

    CONFIG = '.haxornewsconfig'
    CONFIG_CLR_BOLD = 'clr_bold'
    CONFIG_CLR_CODE = 'clr_code'
    CONFIG_CLR_GENERAL = 'clr_general'
    CONFIG_CLR_HEADER = 'clr_header'
    CONFIG_CLR_LINK = 'clr_link'
    CONFIG_CLR_LIST = 'clr_list'
    CONFIG_CLR_NUM_COMMENTS = 'clr_num_comments'
    CONFIG_CLR_NUM_POINTS = 'clr_num_points'
    CONFIG_CLR_TAG = 'clr_tag'
    CONFIG_CLR_TIME = 'clr_time'
    CONFIG_CLR_TITLE = 'clr_title'
    CONFIG_CLR_TOOLTIP = 'clr_tooltip'
    CONFIG_CLR_USER = 'clr_user'
    CONFIG_CLR_VIEW_LINK = 'clr_view_link'
    CONFIG_CLR_VIEW_INDEX = 'clr_view_index'
    CONFIG_SECTION = 'haxor-news'
    CONFIG_IDS = 'item_ids'
    CONFIG_CACHE = 'item_cache'
    CONFIG_HIRING_ID = 'hiring_id'
    CONFIG_FREELANCE_ID = 'freelance_id'
    CONFIG_SHOW_TIP = 'show_tip'
    MAX_ITEM_CACHE_SIZE = 20000

    def __init__(self):
        """Initializes Config.

        Args:
            * None.

        Returns:
            None.
        """
        self.item_ids = []
        self.item_cache = self.load_cache(self.CONFIG_CACHE)
        self.hiring_id, self.freelance_id = \
            self.load_hiring_and_freelance_ids()
        self.load_colors()
        try:
            self.show_tip = self.load_cache(self.CONFIG_SHOW_TIP)
            if self.show_tip is None:
                self.show_tip = True
        except configparser.NoOptionError:
            self.show_tip = True

    def clear_item_cache(self):
        """Clears the item cache.

        Args:
            * None.

        Returns:
            None.
        """
        self.item_ids = self.load_cache(self.CONFIG_IDS)
        self.item_cache = []
        self.save_cache()

    def get_config_path(self, config_file_name):
        """Gets the config file path.

        Args:
            * config_file_name: A String that represents the config file name.

        Returns:
            A string that represents the hn config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def load_cache(self, section):
        """Loads the item ids and the item cache from ~/.haxornewsconfig.

        Args:
            * section: A string representing the section to load.

        Returns:
            A list of caches.
        """
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        try:
            with open(config_file_path) as config_file:
                parser.readfp(config_file)
                return self.load_section(parser, section)
        except IOError:
            # There might not be a cache yet, just silently return.
            return None

    def load_color(self, config, default):
        try:
            color = self.load_cache(config)[0].lower()
            if color == 'none':
                color = None
            # Check if the user input a valid color.
            # If invalid, this will throw a TypeError
            dummy = click.style('', fg=color)
        except TypeError:
            return default
        return color

    def load_colors(self):
        self.clr_bold = self.load_color(
            config=self.CONFIG_CLR_BOLD,
            default='cyan')
        self.clr_code = self.load_color(
            config=self.CONFIG_CLR_CODE,
            default='cyan')
        self.clr_general = self.load_color(
            config=self.CONFIG_CLR_GENERAL,
            default=None)
        self.clr_header = self.load_color(
            config=self.CONFIG_CLR_HEADER,
            default='yellow')
        self.clr_link = self.load_color(
            config=self.CONFIG_CLR_LINK,
            default='green')
        self.clr_list = self.load_color(
            config=self.CONFIG_CLR_LIST,
            default='cyan')
        self.clr_num_comments = self.load_color(
            config=self.CONFIG_CLR_NUM_COMMENTS,
            default='green')
        self.clr_num_points = self.load_color(
            config=self.CONFIG_CLR_NUM_POINTS,
            default='green')
        self.clr_tag = self.load_color(
            config=self.CONFIG_CLR_TAG,
            default='cyan')
        self.clr_time = self.load_color(
            config=self.CONFIG_CLR_TIME,
            default='yellow')
        self.clr_title = self.load_color(
            config=self.CONFIG_CLR_TITLE,
            default=None)
        self.clr_tooltip = self.load_color(
            config=self.CONFIG_CLR_TOOLTIP,
            default=None)
        self.clr_user = self.load_color(
            config=self.CONFIG_CLR_USER,
            default='cyan')
        self.clr_view_link = self.load_color(
            config=self.CONFIG_CLR_VIEW_LINK,
            default='magenta')
        self.clr_view_index = self.load_color(
            config=self.CONFIG_CLR_VIEW_INDEX,
            default='magenta')

    def load_hiring_and_freelance_ids(self):
        """Loads the latest who's hiring and freelancer post ids.

        The latest ids are updated monthly on the repo and are then cached.
        If fetching the latest ids from the repo fails, the cache is checked.
        If fetching the cache fails, the default ids set during installation
        are used.

        Args:
            * None.

        Returns:
            None.
        """
        try:
            url = 'https://raw.githubusercontent.com/donnemartin/donnemartin.github.io/master/tmp/settings.py'  # NOQA
            file_name = 'downloaded_settings.py'
            urllib.request.urlretrieve(url, file_name)
            with open(file_name, 'r') as f:
                for line in f:
                    if line.startswith('who_is_hiring_post_id'):
                        hiring_id = line.split(' = ')[1].strip('\n')
                    if line.startswith('freelancer_post_id'):
                        freelance_id = line.split(' = ')[1].strip('\n')
        except:
            try:
                hiring_id = self.load_cache(self.CONFIG_HIRING_ID)
                freelance_id = self.load_cache(self.CONFIG_FREELANCE_ID)
            except configparser.NoOptionError:
                hiring_id = who_is_hiring_post_id
                freelance_id = freelancer_post_id
        return hiring_id, freelance_id

    def load_section(self, parser, section):
        """Loads the given section from ~/.haxornewsconfig.

        Args:
            * parser: An instance of ConfigParser.RawConfigParser.
            * section: A string representing the section to load

        Returns:
            A list containing a string of elements.

        Raises:
            Exception: An error occurred reading from the parser.
        """
        items_ids = parser.get(self.CONFIG_SECTION, section)
        items_ids = items_ids.strip()
        excludes = ['[', ']', "'"]
        for exclude in excludes:
            items_ids = items_ids.replace(exclude, '')
        return items_ids.split(', ')

    def save_cache(self):
        """Saves the current set of item ids and cache to ~/.haxornewsconfig.

        Args:
            * None

        Returns:
            None.
        """
        if self.item_cache is not None and \
                len(self.item_cache) > self.MAX_ITEM_CACHE_SIZE:
            self.item_cache = self.item_cache[-self.MAX_ITEM_CACHE_SIZE//2:]
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        parser.add_section(self.CONFIG_SECTION)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_IDS,
                   self.item_ids)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CACHE,
                   self.item_cache)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_HIRING_ID,
                   self.hiring_id)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_FREELANCE_ID,
                   self.freelance_id)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_SHOW_TIP,
                   self.show_tip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_BOLD,
                   self.clr_bold)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_CODE,
                   self.clr_code)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_GENERAL,
                   self.clr_general)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_HEADER,
                   self.clr_header)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_LINK,
                   self.clr_link)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_LIST,
                   self.clr_list)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_NUM_COMMENTS,
                   self.clr_num_comments)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_NUM_POINTS,
                   self.clr_num_points)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TAG,
                   self.clr_tag)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TIME,
                   self.clr_time)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TITLE,
                   self.clr_title)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TOOLTIP,
                   self.clr_tooltip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_USER,
                   self.clr_user)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_VIEW_LINK,
                   self.clr_view_link)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_VIEW_INDEX,
                   self.clr_view_index)
        config_file = open(config_file_path, 'w+')
        parser.write(config_file)
        config_file.close()
