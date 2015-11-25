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

from .hacker_news import HackerNews
from .onions import onions
from .settings import who_is_hiring_post_id


pass_hacker_news = click.make_pass_decorator(HackerNews)


class HackerNewsCli(object):
    """Encapsulates the HackerNewsCli.

    Attributes:
        * None.
    """

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for HackerNewsCli.

        Args:
            * ctx: An instance of click.core.Context that stores an instance
                 of HackerNews.

        Returns:
            None.
        """
        # Create a HackerNews object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_hacker_news decorator.
        ctx.obj = HackerNews()

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def ask(hacker_news, limit):
        """Displays Ask HN posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn ask
            hn ask 5
            hn ask | grep foo

        Returns:
            None.
        """
        hacker_news.print_items(
            message='Fetching Ask HN Headlines...',
            item_ids=hacker_news.hacker_news.ask_stories(limit))

    @cli.command()
    @click.argument('regex_query')
    @click.argument('who_is_hiring_post_id', required=False, default=10492086)
    @pass_hacker_news
    def hiring(hacker_news, regex_query, who_is_hiring_post_id):
        """Displays comments matching the monthly who is hiring post.

        Searches the monthly Hacker News who is hiring post for comments
        matching the given regex_query.  Defaults to searching the latest
        post based on your installed version of hncli.  Update to the latest
        version of hncli to get the latest who is hiring post by:

            pip install --upgrade hncli

        TODO: Provide a more dynamic way of getting the latest who is hiring
        post id.

        You can search any post by providing a who_is_hiring_post_id:
            Example: https://news.ycombinator.com/item?id=10492086
            who_is_hiring_post_id = 10492086

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.
            * who_is_hiring_post_id: An int that specifies the who is hiring
                post id.  Optional, defaults to the latest post based on your
                installed version of hncli.

        Example(s):
            hn hiring "Python"
            hn hiring "[Pp]ython|[Rr]uby"
            hn hiring "([Pp]ython|[Rr]uby).*([Rr]ock.star)"
            hn hiring "([Pp]ython|[Rr]uby).*([Rr]ock.star)" > results.txt
            hn hiring "([Pp]ython|[Rr]uby).*([Rr]ock.star)" 8394339

        Returns:
            None.
        """
        who_is_hiring = hacker_news.hacker_news.get_item(who_is_hiring_post_id)
        hacker_news.print_comments(who_is_hiring, regex_query=regex_query)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def jobs(hacker_news, limit):
        """Displays job posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn jobs
            hn jobs 15
            hn jobs | grep Python

        Returns:
            None.
        """
        hacker_news.print_items(
            message='Fetching Job Headlines...',
            item_ids=hacker_news.hacker_news.job_stories(limit))

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def new(hacker_news, limit):
        """Displays the latest posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn new
            hn new 20
            hn new | grep foo

        Returns:
            None.
        """
        hacker_news.print_items(
            message='Fetching Latest Headlines...',
            item_ids=hacker_news.hacker_news.new_stories(limit))

    @cli.command()
    @click.argument('limit', required=False, default=50)
    @pass_hacker_news
    def onion(hacker_news, limit):
        """Displays onions.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 50.

        Example(s):
            hn onion
            hn onion 10

        Returns:
            None.
        """
        click.secho('Fetching Top Onion Headlines...', fg='blue')
        rank = 0
        table = []
        for onion in onions[0:limit]:
            table.append([rank, onion])
            rank += 1
        hacker_news.print_table(table, headers=['#', 'Title'])

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def show(hacker_news, limit):
        """Displays Show HN posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn show
            hn show 5
            hn show | grep foo

        Returns:
            None.
        """
        hacker_news.print_items(
            message='Fetching Show HN Headlines...',
            item_ids=hacker_news.hacker_news.show_stories(limit))

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def top(hacker_news, limit):
        """Displays the top posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn top
            hn top 20
            hn top | grep foo

        Returns:
            None.
        """
        hacker_news.print_items(
            message='Fetching Top Headlines...',
            item_ids=hacker_news.hacker_news.top_stories(limit))
