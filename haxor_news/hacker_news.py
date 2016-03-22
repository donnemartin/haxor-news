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

import platform
import re
import sys
import webbrowser

import click
from .compat import HTMLParser
from .compat import urlparse
import requests

from .config import Config
from .lib.haxor.haxor import HackerNewsApi, HTTPError, InvalidItemID, \
    InvalidUserID
from .lib.html2text.html2text import HTML2Text
from .lib.pretty_date_time import pretty_date_time
from .onions import onions


class HackerNews(object):
    """Encapsulates Hacker News.

    Attributes:
        * COMMENT_INDENT: A string representing the indent amount for comments.
        * COMMENT_UNSEEN: A string representing the adornment for unseen
            comments.
        * config: An instance of haxor_news.Config.
        * html: An instance of html or HTMLParser.
        * MAX_LIST_INDEX: An int representing the maximum 1-based index value
            hn view will use to match item_ids.  Any value larger than
            MAX_LIST_INDEX will result in hn view treating that index as an
            actual post id.
        * MAX_SNIPPET_LENGTH: An int representing the max length of a comment
            snippet shown when filtering comments.
        * MSG_ASK: A string representing the message displayed when the
            command hn ask is executed.
        * MSG_BEST: A string representing the message displayed when the
            command hn best is executed.
        * MSG_ITEM_NOT_FOUND: A string representing the message displayed when
            the given item is not found.
        * MSG_JOBS: A string representing the message displayed when the
            command hn jobs is executed.
        * MSG_NEW: A string representing the message displayed when the
            command hn new is executed.
        * MSG_ONION: A string representing the message displayed when the
            command hn onion is executed.
        * MSG_SHOW: A string representing the message displayed when the
            command hn show is executed.
        * MSG_TOP: A string representing the message displayed when the
            command hn top is executed.
        * MSG_SUBMISSIONS: A string representing the message displayed for
            repositories when the command hn user is executed.
        * hacker_news_api: An instance of HackerNews.
        * html_to_text: An instance of HTML2Text.
        * QUERY_RECENT: A string representing the query to show recent comments.
        * QUERY_UNSEEN: A string representing the query to show unseen comments.
        * TIP0, TIP1, TIP2, TIP3: Strings that lets the user know about the
            hn view command.
        * URL_POST: A string that represents a Hacker News post minus the
            post id.
    """

    COMMENT_INDENT = '  '
    COMMENT_UNSEEN = ' [!]'
    MAX_LIST_INDEX = 1000
    MAX_SNIPPET_LENGTH = 60
    MSG_ASK = 'Ask HN'
    MSG_BEST = 'Best'
    MSG_ITEM_NOT_FOUND = 'Item with id {0} not found.'
    MSG_JOBS = 'Jobs'
    MSG_NEW = 'Latest'
    MSG_ONION = 'Top Onion'
    MSG_SHOW = 'Show HN'
    MSG_TOP = 'Top'
    MSG_SUBMISSIONS = 'User submissions:'
    QUERY_RECENT = 'seconds ago|minutes ago'
    QUERY_UNSEEN = '\[!\]'
    TIP0 = '  Tip: View the page or comments for '
    TIP1 = ' with the following command:\n'
    TIP2 = '    hn view [#] '
    TIP3 = 'optional: [-c] [-cr] [-cu] [-cq "regex"] [-ch] [-b] [--help]'
    URL_POST = 'https://news.ycombinator.com/item?id='

    def __init__(self):
        """Initializes HackerNews.

        Args:
            * None.

        Returns:
            None.
        """
        self.hacker_news_api = HackerNewsApi()
        try:
            self.html = HTMLParser.HTMLParser()
        except:
            self.html = HTMLParser
        self.config = Config()
        self.html_to_text = None
        self._init_html_to_text()

    def _init_html_to_text(self):
        """Initializes HTML2Text.

        Args:
            * None.

        Returns:
            None.
        """
        self.html_to_text = HTML2Text()
        self.html_to_text.body_width = 0
        self.html_to_text.ignore_images = False
        self.html_to_text.ignore_emphasis = False
        self.html_to_text.ignore_links = False
        self.html_to_text.skip_internal_links = False
        self.html_to_text.inline_links = False
        self.html_to_text.links_each_paragraph = False

    def ask(self, limit):
        """Displays Ask HN posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_ASK),
            item_ids=self.hacker_news_api.ask_stories(limit))

    def best(self, limit):
        """Displays best posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_BEST),
            item_ids=self.hacker_news_api.best_stories(limit))

    def format_markdown(self, text):
        """Adds color to the input markdown using click.style.

        Args:
            * text: A string that represents the markdown text.

        Returns:
            A string that has been colorized.
        """
        pattern_url_name = r'[^]]*'
        pattern_url_link = r'[^)]+'
        pattern_url = r'([!]*\[{0}]\(\s*{1}\s*\))'.format(
            pattern_url_name,
            pattern_url_link)
        regex_url = re.compile(pattern_url)
        text = regex_url.sub(click.style(r'\1', fg=self.config.clr_link), text)
        pattern_url_ref_name = r'[^]]*'
        pattern_url_ref_link = r'[^]]+'
        pattern_url_ref = r'([!]*\[{0}]\[\s*{1}\s*\])'.format(
            pattern_url_ref_name,
            pattern_url_ref_link)
        regex_url_ref = re.compile(pattern_url_ref)
        text = regex_url_ref.sub(click.style(r'\1', fg=self.config.clr_link),
                                 text)
        regex_list = re.compile(r'(  \*.*)')
        text = regex_list.sub(click.style(r'\1', fg=self.config.clr_list),
                              text)
        regex_header = re.compile(r'(#+) (.*)')
        text = regex_header.sub(click.style(r'\2', fg=self.config.clr_header),
                                text)
        regex_bold = re.compile(r'(\*\*|__)(.*?)\1')
        text = regex_bold.sub(click.style(r'\2', fg=self.config.clr_bold),
                              text)
        regex_code = re.compile(r'(`)(.*?)\1')
        text = regex_code.sub(click.style(r'\1\2\1', fg=self.config.clr_code),
                              text)
        text = re.sub(r'(\s*\r?\n\s*){2,}', r'\n\n', text)
        return text

    def headlines_message(self, message):
        """Creates the "Fetching [message] Headlines..." string.

        Args:
            * message: A string that represents the message.

        Returns:
            A string: "Fetching [message] Headlines..."
        """
        return 'Fetching {0} Headlines...'.format(message)

    def hiring_and_freelance(self, regex_query, post_id):
        """Displays comments matching the monthly who is hiring post.

        Searches the monthly Hacker News who is hiring post for comments
        matching the given regex_query.  Defaults to searching the latest
        post based on your installed version of haxor-news.

        Args:
            * regex_query: A string that specifies the regex query to match.
            * post_id: An int that specifies the who is hiring post id.
                Optional, defaults to the latest post based on your installed
                version of haxor-news.

        Returns:
            None.
        """
        try:
            item = self.hacker_news_api.get_item(post_id)
            self.print_comments(item,
                                regex_query,
                                comments_hide_non_matching=True)
            self.config.save_cache()
        except InvalidItemID:
            self.print_item_not_found(post_id)
        except IOError:
            sys.stderr.close()

    def jobs(self, limit):
        """Displays job posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_JOBS),
            item_ids=self.hacker_news_api.job_stories(limit))

    def new(self, limit):
        """Displays the latest posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_NEW),
            item_ids=self.hacker_news_api.new_stories(limit))

    def onion(self, limit):
        """Displays onions.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 50.

        Returns:
            None.
        """
        click.secho('\n' + self.headlines_message(self.MSG_ONION) + '\n',
                    fg=self.config.clr_title)
        index = 1
        for onion in onions[0:limit]:
            formatted_index_title = self.format_index_title(index, onion)
            click.echo(formatted_index_title)
            index += 1
        click.echo('')

    def print_comment(self, item, regex_query='',
                      comments_hide_non_matching=False, depth=0):
        """Prints the comments for the given item.

        Args:
            * item: An instance of haxor.Item.
            * regex_query: A string that specifies the regex query to match.
            * comments_hide_non_matching: A bool that determines whether to
                hide comments that don't match (False) or truncate them (True).
            * depth: The current recursion depth, used to indent the comment.

        Returns:
            None.
        """
        if item.text is not None:
            header_color = 'yellow'
            header_color_highlight = 'magenta'
            header_adornment = ''
            if self.config.item_cache is not None and \
                    str(item.item_id) not in self.config.item_cache:
                header_adornment = self.COMMENT_UNSEEN
                self.config.item_cache.append(item.item_id)
            show_comment = True
            if regex_query is not None:
                if self.match_comment_unseen(regex_query, header_adornment) or \
                        self.match_regex(item, regex_query):
                    header_color = header_color_highlight
                else:
                    show_comment = False
            formatted_heading, formatted_comment = self.format_comment(
                item, depth, header_color, header_adornment)
            if show_comment:
                click.echo(formatted_heading, color=True)
                click.echo(formatted_comment, color=True)
            elif comments_hide_non_matching:
                click.secho('.', nl=False)
            else:
                click.echo(formatted_heading, color=True)
                num_chars = len(formatted_comment)
                if num_chars > self.MAX_SNIPPET_LENGTH:
                    num_chars = self.MAX_SNIPPET_LENGTH
                click.echo(formatted_comment[0:num_chars] + ' [...]',
                           color=True)

    def print_comments(self, item, regex_query='',
                       comments_hide_non_matching=False, depth=0):
        """Recursively print comments and subcomments for the given item.

        Args:
            * item: An instance of haxor.Item.
            * regex_query: A string that specifies the regex query to match.
            * comments_hide_non_matching: A bool that determines whether to
                hide comments that don't match (False) or truncate them (True).
            * depth: The current recursion depth, used to indent the comment.

        Returns:
            None.
        """
        self.print_comment(item, regex_query, comments_hide_non_matching, depth)
        comment_ids = item.kids
        if not comment_ids:
            return
        for comment_id in comment_ids:
            try:
                comment = self.hacker_news_api.get_item(comment_id)
                depth += 1
                self.print_comments(
                    comment,
                    regex_query=regex_query,
                    comments_hide_non_matching=comments_hide_non_matching,
                    depth=depth)
                depth -= 1
            except (InvalidItemID, HTTPError):
                click.echo('')
                self.print_item_not_found(comment_id)

    def format_comment(self, item, depth, header_color, header_adornment):
        """Formats a given item's comment.

        Args:
            * item: An instance of haxor.Item.
            * depth: An int that represents the current recursion depth,
                used to indent the comment.
            * header_color: A string that represents the header color.
            * header_adornment: A string that the header adornment, if present.

        Returns:
            A tuple of the following:
                * A string representing the formatted comment header.
                * A string representing the formatted comment.
        """
        indent = self.COMMENT_INDENT * depth
        formatted_heading = click.style(
            '\n' + indent + item.by + ' - ' +
            str(pretty_date_time(item.submission_time)) + header_adornment,
            fg=header_color)
        unescaped_text = self.html.unescape(item.text)
        regex_paragraph = re.compile(r'<p>')
        unescaped_text = regex_paragraph.sub(click.style(
            '\n\n' + indent), unescaped_text)
        regex_url = re.compile(r'(<a href=(".*") .*</a>)')
        unescaped_text = regex_url.sub(click.style(
            r'\2', fg=self.config.clr_link), unescaped_text)
        regex_tag = re.compile(r'(<(.*)>.*?<\/\2>)')
        unescaped_text = regex_tag.sub(click.style(
            r'\1', fg=self.config.clr_tag), unescaped_text)
        formatted_comment = click.wrap_text(
            text=unescaped_text,
            initial_indent=indent,
            subsequent_indent=indent)
        return formatted_heading, formatted_comment

    def format_index_title(self, index, title):
        """Formats and item's index and title.

        Args:
            * index: An int that specifies the index for the given item.
            * title: A string that represents the item's title.

        Returns:
            A string representation of the formatted index and title.
        """
        space = '  ' if index < 10 else ' '
        formatted_index_title = click.style('  ' + str(index) + '.' + space,
                                            fg=self.config.clr_view_index)
        formatted_index_title += click.style(title + ' ',
                                             fg=self.config.clr_title)
        return formatted_index_title

    def format_item(self, item, index):
        """Formats an item.

        Args:
            * item: An instance of haxor.Item.
            * index: An int that specifies the index for the given item,
                used with the hn view [index] commend.

        Returns:
            A string representing the formatted item.
        """
        formatted_item = self.format_index_title(index, item.title)
        if item.url is not None:
            netloc = urlparse(item.url).netloc
            netloc = re.sub('www.', '', netloc)
            formatted_item += click.style('(' + netloc + ')',
                                          fg=self.config.clr_view_link)
        formatted_item += '\n'
        formatted_item += click.style('        ' + str(item.score) + ' points ',
                                      fg=self.config.clr_num_points)
        formatted_item += click.style('by ' + item.by + ' ',
                                      fg=self.config.clr_user)
        formatted_item += click.style(
            str(pretty_date_time(item.submission_time)) + ' ',
            self.config.clr_time)
        num_comments = str(item.descendants) if item.descendants else '0'
        formatted_item += click.style('| ' + num_comments + ' comments',
                                      fg=self.config.clr_num_comments)
        self.config.item_ids.append(item.item_id)
        return formatted_item

    def print_item_not_found(self, item_id):
        """Prints a message the given item id was not found.

        Long description.

        Args:
            * item_id: An int representing the item id.

        Returns:
            None.
        """
        click.secho(self.MSG_ITEM_NOT_FOUND.format(item_id), fg='red')

    def print_items(self, message, item_ids):
        """Prints the items.

        Args:
            * message: A string to print out to the user before outputting
                the results.
            * item_ids: A collection of items to print.
                Can be a list or dictionary.

        Returns:
            None.
        """
        self.config.item_ids = []
        index = 1
        for item_id in item_ids:
            try:
                item = self.hacker_news_api.get_item(item_id)
                if item.title:
                    formatted_item = self.format_item(item, index)
                    click.echo(formatted_item)
                    index += 1
            except InvalidItemID:
                self.print_item_not_found(item_id)
        self.config.save_cache()
        if self.config.show_tip:
            click.secho(self.tip_view(str(index-1)))

    def tip_view(self, max_index):
        """Creates the tip about the view command.

        Args:
            * max_index: A string that represents the index upper bound.

        Returns:
            A string representation of the formatted tip.
        """
        tip = click.style(self.TIP0, fg=self.config.clr_tooltip)
        tip += click.style('1 through ', fg=self.config.clr_view_index)
        tip += click.style(str(max_index), fg=self.config.clr_view_index)
        tip += click.style(self.TIP1, fg=self.config.clr_tooltip)
        tip += click.style(self.TIP2, fg=self.config.clr_view_index)
        tip += click.style(self.TIP3 + '\n', fg=self.config.clr_tooltip)
        return tip

    def url_contents(self, url):
        """Gets the formatted contents of the given item's url.

        Converts the HTML to text using HTML2Text, colors it, then displays
            the output in a pager.

        Args:
            * url: A string representing the url.

        Returns:
            A string representation of the formatted url contents.
        """
        raw_response = requests.get(url)
        contents = self.html_to_text.handle(raw_response.text)
        contents = self.format_markdown(contents)
        contents = click.style(
            'Viewing ' + url + '\n\n', fg=self.config.clr_general) + contents
        return contents

    def match_comment_unseen(self, regex_query, header_adornment):
        """Determines if a comment is unseen based on the query and header.

        Args:
            * regex_query: A string that specifies the regex query to match.
            * header_adornment: A string that represents the header adornment,
                if present.

        Returns:
            A boolean that specifies if there is a match found.
        """
        if regex_query == self.QUERY_UNSEEN and \
                header_adornment == self.COMMENT_UNSEEN:
            return True
        else:
            return False

    def match_regex(self, item, regex_query):
        """Determines if there is a match with the given regex_query.

        Args:
            * item: An instance of haxor.Item.
            * regex_query: A string that specifies the regex query to match.

        Returns:
            A boolean that specifies whether there is a match.
        """
        match_time = re.search(
            regex_query,
            str(pretty_date_time(item.submission_time)))
        match_user = re.search(regex_query, item.by)
        match_text = re.search(regex_query, item.text)
        if not match_text and not match_user and not match_time:
            return False
        else:
            return True

    def show(self, limit):
        """Displays Show HN posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_SHOW),
            item_ids=self.hacker_news_api.show_stories(limit))

    def top(self, limit):
        """Displays the top posts.

        Args:
            * limit: A int that specifies the number of items to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        self.print_items(
            message=self.headlines_message(self.MSG_TOP),
            item_ids=self.hacker_news_api.top_stories(limit))

    def user(self, user_id, submission_limit):
        """Displays basic user info and submitted posts.

        Args:
            * user_id: A string representing the user id.
            * submission_limit: A int that specifies the number of
                submissions to show.
                Optional, defaults to 10.

        Returns:
            None.
        """
        try:
            user = self.hacker_news_api.get_user(user_id)
            click.secho('\nUser Id: ', nl=False, fg=self.config.clr_general)
            click.secho(user_id, fg=self.config.clr_user)
            click.secho('Created: ', nl=False, fg=self.config.clr_general)
            click.secho(str(user.created), fg=self.config.clr_user)
            click.secho('Karma: ', nl=False, fg=self.config.clr_general)
            click.secho(str(user.karma), fg=self.config.clr_user)
            self.print_items(self.MSG_SUBMISSIONS,
                             user.submitted[0:submission_limit])
        except InvalidUserID:
            self.print_item_not_found(user_id)

    def view(self, index, comments_query, comments,
             comments_hide_non_matching, browser):
        """Views the given index in a browser.

        Uses ids from ~/.haxornewsconfig stored in self.config.item_ids.
        If url is True, opens a browser with the url based on the given index.
        Else, displays the post's comments.

        Args:
            * index: An int that specifies the index to open in a browser.
            * comments_query: A string that specifies the regex query to match.
            * comments: A boolean that determines whether to view the comments
                or a simplified version of the post url.
            * comments_hide_non_matching: A bool that determines whether to
                hide comments that don't match (False) or truncate them (True).
            * browser: A boolean that determines whether to view the url
                 in a browser.

        Returns:
            None.
        """
        if self.config.item_ids is None:
            click.secho('There are no posts indexed, run a command such as '
                        'hn top first',
                        fg='red')
            return
        item_id = index
        if index < self.MAX_LIST_INDEX:
            try:
                item_id = self.config.item_ids[index-1]
            except IndexError:
                self.print_item_not_found(item_id)
                return
        try:
            item = self.hacker_news_api.get_item(item_id)
        except InvalidItemID:
            self.print_item_not_found(self.config.item_ids[index-1])
            return
        if not comments and item.url is None:
            click.secho('\nNo url associated with post.',
                        nl=False,
                        fg=self.config.clr_general)
            comments = True
        if comments:
            comments_url = self.URL_POST + str(item.item_id)
            click.secho('\nFetching Comments from ' + comments_url,
                        fg=self.config.clr_general)
            if browser:
                webbrowser.open(comments_url)
            else:
                try:
                    self.print_comments(
                        item,
                        regex_query=comments_query,
                        comments_hide_non_matching=comments_hide_non_matching)
                    click.echo('')
                except IOError:
                    sys.stderr.close()
                self.config.save_cache()
        else:
            click.secho('\nOpening ' + item.url + '...',
                        fg=self.config.clr_general)
            if browser:
                webbrowser.open(item.url)
            else:
                contents = self.url_contents(item.url)
                if platform.system() == 'Windows':
                    try:
                        click.echo(contents)
                    except IOError:
                        sys.stderr.close()
                else:
                    click.echo_via_pager(contents)
            click.echo('')

    def view_setup(self, index, comments_regex_query, comments,
                   comments_recent, comments_unseen,
                   comments_hide_non_matching, clear_cache, browser):
        """Sets up the call to views the given index comments or url.

        This method is meant to be called after a command that outputs a
        table of posts.

        Args:
            * index: A int that specifies the index of a post just shown within
                a table.  For example, calling hn top will list the latest posts
                with indices for each row.  Calling hn view [index] will view
                the comments of the given post.
            * comments_regex_query: A string that specifies the regex query
                to match.  This automatically sets comments to True.
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

        Returns:
            None.
        """
        if comments_regex_query is not None:
            comments = True
        if comments_recent:
            comments_regex_query = self.QUERY_RECENT
            comments = True
        if comments_unseen:
            comments_regex_query = self.QUERY_UNSEEN
            comments = True
        if clear_cache:
            self.config.clear_item_cache()
        self.view(int(index),
                  comments_regex_query,
                  comments,
                  comments_hide_non_matching,
                  browser)
