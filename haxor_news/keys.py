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
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


class KeyManager(object):
    """Creates a Key Manager.

    Attributes:
        * manager: An instance of a prompt_toolkit's KeyBindingManager.
    """

    def __init__(self, set_paginate_comments, get_paginate_comments):
        """Initializes KeyManager.

        Args:
            * set_paginate_comments: A function setting the paginate comments
                config.
            * get_paginate_comments: A function setting the paginate comments
                config.

        Returns:
            None.
        """
        self.manager = None
        self._create_key_manager(set_paginate_comments, get_paginate_comments)

    def _create_key_manager(self, set_paginate_comments, get_paginate_comments):
        """Creates and initializes the keybinding manager.

        Args:
            * set_paginate_comments: A function setting the paginate comments
                config.
            * get_paginate_comments: A function setting the paginate comments
                config.

        Returns:
            A KeyBindingManager.
        """
        assert callable(set_paginate_comments)
        assert callable(get_paginate_comments)
        self.manager = KeyBindingManager(
            enable_search=True,
            enable_abort_and_exit_bindings=True,
            enable_system_bindings=True,
            enable_auto_suggest_bindings=True)

        @self.manager.registry.add_binding(Keys.F2)
        def handle_f2(_):
            """Enables/Disables paginate comments mode.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            set_paginate_comments(not get_paginate_comments())

        @self.manager.registry.add_binding(Keys.F10)
        def handle_f10(_):
            """Quits when the `F10` key is pressed.

            Args:
                * _: An instance of prompt_toolkit's Event (not used).

            Returns:
                None.
            """
            raise EOFError

        @self.manager.registry.add_binding(Keys.ControlSpace)
        def handle_ctrl_space(event):
            """Initializes autocompletion at the cursor.

            If the autocompletion menu is not showing, display it with the
            appropriate completions for the context.

            If the menu is showing, select the next completion.

            Args:
                * event: An instance of prompt_toolkit's Event.

            Returns:
                None.
            """
            b = event.cli.current_buffer
            if b.complete_state:
                b.complete_next()
            else:
                event.cli.start_completion(select_first=False)
