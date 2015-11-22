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
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

from .lulz import lulz


class Onion(object):
    """Encapsulates Hacker News Onion.

    Attributes:
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_INDEX: A string representing the last index used.
        * last_index: An int that specifies the last lol index displayed.
    """

    CONFIG = '.onionconfig'
    CONFIG_SECTION = 'onion'
    CONFIG_INDEX = 'index'

    def __init__(self):
        """Initializes Onion.

        Args:
            * None.

        Returns:
            None.
        """
        self.last_index = None

    def _onion_config(self, config_file_name):
        """Gets the config file path.

        Args:
            * config_file_name: A String that represents the config file name.

        Returns:
            A string that represents the github config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def generate_next_index(self, default_index=0):
        """Generates the next valid lol index.

        Avoids showing the same lol when cycling incrementally without flag -r.
        Reads the config file if it exists for the last shown lol index.
        If found, increments that index and returns it, cycling to 0 if the
        last lol index was previously shown.
        If not found, returns the value specified in default_index.

        Args:
            * default_index: An int that represents the next index if the
                config file does not yet exist.

        Returns:
            An int that represents the next valid lol index.
        """
        config = self._onion_config(self.CONFIG)
        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            parser = configparser.RawConfigParser()
            parser.readfp(open(config))
            self.last_index = int(parser.get(self.CONFIG_SECTION,
                                             self.CONFIG_INDEX))
            if self.last_index >= len(lulz) - 1:
                self.last_index = 0
            else:
                self.last_index += 1
            return self.last_index
        else:
            # Either the file didn't exist or we didn't have the correct
            # permissions
            return default_index

    def random_index(self, upper):
        """Gets a random index from 0 to the input upper.

        Args:
            * upper: An int that specifies the upper bound, inclusive.

        Returns:
            A random int from the range 0 to the upper bound, inclusive.
        """
        return random.randint(0, upper)

    def repeat(self, string, iterations):
        """Builds a string by repeating the input string iterations times.

        Yay for Python one liner list comprehensions.

        Args:
            * string: A string to repeat.
            * iterations: An int that determines number of times to repeat
                the input string.

        Returns:
            A string of input string repeated iterations times.
        """
        return ''.join([string for i in range(iterations)])

    def save_last_index(self):
        """Saves the last shown lol index to the config file.

        Args:
            * None.

        Returns:
            None.
        """
        config = self._onion_config(self.CONFIG)
        parser = configparser.RawConfigParser()
        parser.add_section(self.CONFIG_SECTION)
        parser.set(self.CONFIG_SECTION, self.CONFIG_INDEX, self.last_index)
        parser.write(open(config, 'w+'))
