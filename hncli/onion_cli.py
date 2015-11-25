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

import click

from .lulz import lulz
from .onion import Onion


class OnionCli(object):
    """Encapsulates the OnionCli.

    Attributes:
        * None.
    """

    @click.command()
    @click.argument('headline', required=False)
    @click.option('-r', '--random', is_flag=True)
    def cli(headline, random):
        """Main entry point for OnionCli.

        Args:
            * headline: An int that determines the index of the lol to display.
            * random: A bool that determines whether to display a random lol.
                If false, cycles through lols from start to end, then repeats.

        Returns:
            None.
        """
        onion = Onion()
        len_lulz = len(lulz)
        lol_index = None
        if random:
            lol_index = onion.random_index(len_lulz-1)
        else:
            if headline is not None:
                try:
                    lol_index = int(headline)
                except ValueError:
                    click.secho('Expected int arg from 0 to ' +
                                str(len(lulz)),
                                fg='red')
                    return
            else:
                lol_index = onion.generate_next_index()
        lol_troll = onion.generate_lol_troll(lol_index)
        click.echo(lol_troll)
        click.echo(str(onion.last_index) + '/' + str(len_lulz-1))
        if not random:
            onion.save_last_index()
