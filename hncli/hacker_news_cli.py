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
    @click.argument('limit', required=False, default=10)
    @pass_hacker_news
    def best(hacker_news, limit):
        """Displays the best posts of the past few days.

        Args:
            * hacker_news: An instance of Hacker News.
            * limit: A string that specifies the number of items to show.
                Optional, defaults to 10.

        Example(s):
            hn best
            hn best 20

        Returns:
            None.
        """
        hacker_news.best(limit)

    @cli.command()
    @click.argument('regex_query', required=False)
    @click.option('-i', '--id_post', required=False, default=0)
    @pass_hacker_news
    def freelance(hacker_news, regex_query, id_post):
        """Displays comments from the seeking freelancer posts.

        Searches the monthly Hacker News seeking freelancer post for comments
        matching the given regex_query.  Defaults to searching the latest
        post.

        You can search any post by providing a freelancer_post_id:
            Example: https://news.ycombinator.com/item?id=10492087
            freelancer_post_id = 10492087

        Args:
            * hacker_news: An instance of Hacker News.
            * regex_query: A string that specifies the regex query to match.
            * id_post: A string that specifies the who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of hncli.

        Example(s):
            hn freelance
            hn freelance "Python"
            hn freelance "(?i)Python|JavaScript"  # (?i) case insensitive
            hn freelance "(?i)Python" -i 8394339  # search post 8394339
            hn freelance "(?i)(Python|JavaScript).*(rockstar)" > rockstars.txt

        Returns:
            None.
        """
        if id_post == 0:
            id_post = hacker_news.freelance_id
        hacker_news.hiring_and_freelance(regex_query, id_post)

    @cli.command()
    @click.argument('regex_query', required=False)
    @click.option('-i', '--id_post', required=False, default=0)
    @pass_hacker_news
    def hiring(hacker_news, regex_query, id_post):
        """Displays comments from the who is hiring posts.

        Searches the monthly Hacker News who is hiring post for comments
        matching the given regex_query.  Defaults to searching the latest
        post.

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
        if id_post == 0:
            id_post = hacker_news.hiring_id
        hacker_news.hiring_and_freelance(regex_query, id_post)

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
        """Displays the top recent posts.

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
    @click.option('-l', '--limit', required=False, default=10)
    @pass_hacker_news
    def user(hacker_news, user_id, limit):
        """Displays basic user info and submitted posts.

        Args:
            * hacker_news: An instance of Hacker News.
            * user_id: A string representing the user id.
            * limit: A string that specifies the number of posts to show.Optional, defaults to 10.

        Example(s):
            hn user tptacek
            hn user patio11

        Returns:
            None.
        """
        hacker_news.user(user_id, limit)

    @cli.command()
    @click.argument('index')
    @click.option('-cq', '--comments_regex_query', required=False, default=None)
    @click.option('-c', '--comments', is_flag=True)
    @click.option('-cr', '--comments_recent', is_flag=True)
    @click.option('-cu', '--comments_unseen', is_flag=True)
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-cc', '--clear_cache', is_flag=True)
    @click.option('-ch', '--comments_hide_non_matching', is_flag=True)
    @pass_hacker_news
    def view(hacker_news, index, comments_regex_query, comments,
             comments_recent, comments_unseen,
             comments_hide_non_matching, clear_cache, browser):
        """Views the post index or id, hn view --help.

        Args:
            * hacker_news: An instance of Hacker News.
            * index: A string that specifies either:
                    1) the index of a post just shown within a list of posts or
                    2) the actual post id
                For example, calling `hn top` will list the top posts with
                1-based indices for each post:
                  1. Post foo
                  2. Post bar
                  3. Post baz
                A subsequent call to `hn view 1` will view 'Post foo'.
                Providing an index larger than MAX_LIST_INDEX (1000) will
                result in hn view treating index as an actual post id.
            * comments_regex_query: A string that specifies the regex query
                to match.  Passing this option automatically sets comments
                to True.
            * comments: A boolean that determines whether to view the comments
                or a simplified version of the post url.
            * comments_recent: A boolean that determines whether to view only
                recently comments (posted within the past 59 minutes or less)
            * comments_unseen: A boolean that determines whether to view only
                comments that you have not yet seen.
            * comments_hide_non_matching: A bool that determines whether to
                hide comments that don't match (False) or truncate them (True).
            * clear_cache: A boolean that clears the comment cache before
                running the view command.
            * browser: A boolean that determines whether to view the url
                in a browser.

        Example(s):
            hn top
            hn view 3
            hn view 3 -c | less
            hn view 3 -c > comments.txt
            hn view 3 -cr
            hn view 3 --comments_recent
            hn view 3 -cu
            hn view 3 --comments_unseen
            hn view 3 -cu -ch
            hn view 3 --comments_unseen --comments_hide_non_matching
            hn view 3 --browser
            hn view 3 -b -c
            hn view 3 -comments -clear_cache
            hn view 3 "(?i)case insensitive match" --comments
            hn view 3 "(?i)programmer" --comments
            hn view 3 "(?i)programmer" --comments | less
            hn view 10492086
            hn view 10492086 "Python"
            hn view 10492086 "(?i)case insensitive match"
            hn view 10492086 "(?i)(Python|Django)" > comments.txt

        Returns:
            None.
        """
        try:
            post_index = int(index)
        except ValueError:
            click.secho('Error: Expected an integer post index', fg='red')
        else:
            hacker_news.view_setup(post_index,
                                   comments_regex_query,
                                   comments,
                                   comments_recent,
                                   comments_unseen,
                                   comments_hide_non_matching,
                                   clear_cache,
                                   browser)
