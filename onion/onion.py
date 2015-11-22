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
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser


class Onion(object):
    """Encapsulates Hacker News Onion.

    Attributes:
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_INDEX: A string representing the last index used.
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
        pass

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
