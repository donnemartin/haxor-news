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

    def __init__(self, color_cfg):
        """Initializes ToolBar.

        Args:
            * color_cfg: A boolean that spedifies whether to color the output.

        Returns:
            None
        """
        self.handler = self._create_toolbar_handler(color_cfg)

    def _create_toolbar_handler(self, color_cfg):
        """Creates the toolbar handler.

        Args:
            * color_cfg: A boolean that spedifies whether to color the output.

        Returns:
            A callable get_toolbar_items.
        """
        assert callable(color_cfg)

        def get_toolbar_items(_):
            """Returns bottom menu items.

            Args:
                * _: An instance of prompt_toolkit's Cli (not used).

            Returns:
                A list of Token.Toolbar.
            """
            if color_cfg():
                color_token = Token.Toolbar.On
                color = 'ON'
            else:
                color_token = Token.Toolbar.Off
                color = 'OFF'
            return [
                (color_token, ' [F2] Color: {0} '.format(color)),
                (Token.Toolbar, ' [F5] Refresh '),
                (Token.Toolbar, ' [F10] Exit ')
            ]

        return get_toolbar_items
