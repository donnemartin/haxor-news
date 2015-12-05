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
from pygments.token import Token


class Toolbar(object):
    """Encapsulates the bottom toolbar.

    Attributes:
        * handler: A callable get_toolbar_items.
    """

    def __init__(self, fuzzy_cfg):
        """Initializes ToolBar.

        Args:
            * fuzzy_cfg: A boolean that spedifies whether to do fuzzy matching.

        Returns:
            None
        """
        self.handler = self._create_toolbar_handler(fuzzy_cfg)

    def _create_toolbar_handler(self, fuzzy_cfg):
        """Creates the toolbar handler.

        Args:
            * fuzzy_cfg: A boolean that spedifies whether to do fuzzy matching.

        Returns:
            A callable get_toolbar_items.
        """
        assert callable(fuzzy_cfg)

        def get_toolbar_items(_):
            """Returns bottom menu items.

            Args:
                * _: An instance of prompt_toolkit's Cli (not used).

            Returns:
                A list of Token.Toolbar.
            """
            if fuzzy_cfg():
                fuzzy_token = Token.Toolbar.On
                fuzzy = 'ON'
            else:
                fuzzy_token = Token.Toolbar.Off
                fuzzy = 'OFF'
            return [
                (fuzzy_token, ' [F2] Fuzzy: {0} '.format(fuzzy)),
                (Token.Toolbar, ' [F10] Exit ')
            ]

        return get_toolbar_items
