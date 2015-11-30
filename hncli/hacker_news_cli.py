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
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn ask
            hn ask 5

        Returns:
            None.
        """
        hacker_news.ask(limit)

    @cli.command()
    @click.argument('post_id')
    @click.argument('regex_query', required=False, default='')
    @pass_hacker_news
    def comments(hacker_news, post_id, regex_query):
        """Views the comments for the given post_id.

        Args:
            * hacker_news: An instance of Hacker News.
            * post_id: A string representing the post's id.
            * regex_query: A string that specifies the regex query to match.
                Optional, defaults to ''.

        Example(s):
            hn comments 10492086
            hn comments 10492086 "Python"
            hn comments 10492086 "(?i)case insensitive match"
            hn comments 10492086 "(?i)(Python|Django)" > comments.txt

        Returns:
            None.
        """
        hacker_news.comments(post_id, regex_query)

    @cli.command()
    @click.argument('regex_query', required=False)
    @click.option('-i', '--id_post', required=False,
                  default=who_is_hiring_post_id)
    @pass_hacker_news
    def hiring(hacker_news, regex_query, id_post):
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
            * regex_query: A string that specifies the regex query to match.
            * id_post: A string that specifies the who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of hncli.

        Example(s):
            hn hiring
            hn hiring "Python"
            hn hiring "(?i)Python|JavaScript"  # (?i) case insensitive
            hn hiring "(?i)Python|JavaScript" -i 8394339  # search post 8394339
            hn hiring "(?i)(Python|JavaScript).*(rockstar)" > rockstars.txt

        Returns:
            None.
        """
        hacker_news.hiring(regex_query, id_post)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def jobs(hacker_news, limit):
        """Displays job posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn jobs
            hn jobs 15

        Returns:
            None.
        """
        hacker_news.jobs(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def new(hacker_news, limit):
        """Displays the latest posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn new
            hn new 20

        Returns:
            None.
        """
        hacker_news.new(limit)

    @cli.command()
    @click.argument('limit', required=False, default=50)
    @pass_hacker_news
    def onion(hacker_news, limit):
        """Displays onions.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 50.

        Example(s):
            hn onion
            hn onion 10

        Returns:
            None.
        """
        hacker_news.onion(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def show(hacker_news, limit):
        """Displays Show HN posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn show
            hn show 5

        Returns:
            None.
        """
        hacker_news.show(limit)

    @cli.command()
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def top(hacker_news, limit):
        """Displays the top posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn top
            hn top 20

        Returns:
            None.
        """
        hacker_news.top(limit)

    @cli.command()
    @click.argument('user_id')
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def user(hacker_news, user_id, limit):
        """Displays basic user info and submitted posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * user_id: A string representing the user id.
            * limit: A int that specifies the number of submissions to show.
                Optional, defaults to 10.

        Example(s):
            hn user tptacek
            hn user patio11

        Returns:
            None.
        """
        user = hacker_news.hacker_news_api.get_user(user_id)
        table = [[user_id, str(user.created), str(user.karma)]]
        hacker_news.print_table(table, headers=['User Id', 'Created', 'Karma'])
        hacker_news.print_items('User submissions:', user.submitted[0:limit])

    @cli.command()
    @click.argument('index')
    @click.argument('comments_query', required=False, default='')
    @click.option('-c', '--comments', is_flag=True)
    @click.option('-cr', '--comments_recent', is_flag=True)
    @click.option('-b', '--browser', is_flag=True)
    @pass_hacker_news
    def view(hacker_news, index, comments_query,
             comments, comments_recent, browser):
        """Views the given index comments or url.

        This method is meant to be called after a command that outputs a
        table of posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * index: A int that specifies the index of a post just shown within
                a table.  For example, calling hn top will list the latest posts
                with indices for each row.  Calling hn view [index] will view
                the comments of the given post.
            * comments_query: A string that specifies the regex query to match.
                This automatically sets comments to True.
            * comments: A boolean that determines whether to view the comments
                or a simplified version of the post url.
            * comments_recent: A boolean that determines whether to view only
                 recently comments (posted within the past 59 minutes or less)
            * browser: A boolean that determines whether to view the url
                 in a browser.

        Example(s):
            hn top
            hn view 3
            hn view 3 -c | less
            hn view 3 -c > comments.txt
            hn view 3 --browser
            hn view 3 -b -c
            hn view 3 "(?i)case insensitive match" --comments
            hn view 3 "(?i)programmer" --comments
            hn view 3 "(?i)programmer" --comments | less

        Returns:
            None.
        """
        if comments_query:
            comments = True
        if comments_recent:
            query_recent = 'minutes ago'
            if not comments_query:
                comments_query = query_recent
            else:
                comments_query += '' + query_recent
            comments = True
        hacker_news.view(int(index), comments_query, comments, browser)
