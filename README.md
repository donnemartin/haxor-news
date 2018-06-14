![Imgur](http://i.imgur.com/C4mkc3L.gif)

[![Build Status](https://travis-ci.org/donnemartin/haxor-news.svg?branch=master)](https://travis-ci.org/donnemartin/haxor-news)

[![PyPI version](https://badge.fury.io/py/haxor-news.svg)](http://badge.fury.io/py/haxor-news) [![PyPI](https://img.shields.io/pypi/pyversions/haxor-news.svg)](https://pypi.python.org/pypi/haxor-news/) [![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

haxor-news
=================

> *Coworker who sees me looking at something in a browser: "Glad you're not busy; I need you to do this, this, this..."*
>
> *Coworker who sees me staring intently at a command prompt: Backs away, slowly...*
>
> *-[Source](https://www.reddit.com/user/foxingworth)*

Check out the `haxor-news` discussion in this [Hacker News post](https://news.ycombinator.com/item?id=11518596).

`haxor-news` brings Hacker News to the terminal, allowing you to **view**/**filter** the following without leaving your command line:

* Posts
* Post Comments
* Post Linked Web Content
* Monthly Hiring and Freelancers Posts
* User Info
* Onions

`haxor-news` helps you **filter the large number of comments that popular posts generate**.

* Want to expand only previously **unseen comments**?
    * `-cu/--comments_unseen`
* How about **recent comments** posted in the past 60 minutes?
    * `-cr/--comments_recent`
* Filter comments matching a **regex query**?
    * `-cq/--comments_query [query]`

![Imgur](http://i.imgur.com/4psj3nE.png)

Job hunting or just curious what's out there?  **Filter the monthly who's hiring and freelancers post**:

    $ hn hiring "(?i)(Node|JavaScript).*(remote)" > remote_web_jobs.txt

Combine `haxor-news` with pipes, redirects, and other command line utilities.  Output to pagers, write to files, automate with cron, etc.

`haxor-news` comes with a handy **optional auto-completer with interactive help**:

![Imgur](http://i.imgur.com/seKUiur.png)

## TODO

* [Vote on posts and comments](https://github.com/donnemartin/haxor-news/issues/)
* [Submit posts and comments](https://github.com/donnemartin/haxor-news/issues/19)
* [Search posts and comments](https://github.com/donnemartin/haxor-news/issues/20)

## Index

### General

* [Syntax](#syntax)
* [Auto-Completer and Interactive Help](#auto-completer-and-interactive-help)
* [Customizable Highlighting](#customizable-highlighting)
* [Commands](#commands)

### Features

* [View Posts](#view-posts)
* [View a Post's Linked Web Content](#view-a-posts-linked-web-content)
* [View and Filter a Post's Comments](#view-and-filter-a-posts-comments)
    * [View All Comments](#view-all-comments)
    * [Filter on Unseen Comments](#filter-on-unseen-comments)
    * [Filter on Recent Comments](#filter-on-recent-comments)
    * [Filter with Regex](#filter-with-regex)
    * [Hide Non-Matching Comments](#hide-non-matching-comments)
* [View and Filter the Monthly Hiring Post](#filter-the-monthly-hiring-post)
* [View and Filter the Monthly Freelancer Post](#filter-the-monthly-hiring-post)
* [Combine With Pipes and Redirects](#combine-with-pipes-and-redirects)
* [View User Info](#view-user-info)
* [View Onions](#view-onions)
* [View Results in a Browser](#view-in-a-browser)
* [Windows Support](#windows-support)

### Installation and Tests

* [Installation](#installation)
    * [Pip Installation](#pip-installation)
    * [Virtual Environment Installation](#virtual-environment-installation)
    * [Supported Python Versions](#supported-python-versions)
    * [Supported Platforms](#supported-platforms)
* [Developer Installation](#developer-installation)
    * [Continuous Integration](#continuous-integration)
    * [Dependencies Management](#dependencies-management)
    * [Unit Tests and Code Coverage](#unit-tests-and-code-coverage)
    * [Documentation](#documentation)

### Misc

* [Contributing](#contributing)
* [Credits](#credits)
* [Contact Info](#contact-info)
* [License](#license)

## Syntax

Usage:

    $ hn <command> [params] [options]

## Auto-Completer and Interactive Help

Optionally, you can enable fish-style completions and an auto-completion menu with interactive help:

    $ haxor-news

If available, the auto-completer also automatically displays comments through a pager.

Within the auto-completer, the same syntax applies:

    haxor> hn <command> [params] [options]

![Imgur](http://i.imgur.com/L2rzgb3.png)

![Imgur](http://i.imgur.com/FL2pyC0.png)

## Customizable Highlighting

You can control the ansi colors used for highlighting by updating your `~/.haxornewsconfig` file.

Color options include:

```
'black', 'red', 'green', 'yellow',
'blue', 'magenta', 'cyan', 'white'
```

For no color, set the value(s) to `None`.

![Imgur](http://i.imgur.com/lzoRxfW.png)

## Commands

![Imgur](http://i.imgur.com/oqvUbj8.png)

## View Posts

View the Top, Best, Show, Show, Ask, Jobs, New, and Onion posts.

Usage:

    $ hn [command] [limit]  # post limit default: 10

Examples:

    $ hn top
    $ hn show 20

![Imgur](http://i.imgur.com/tjGPszv.png)

## View a Post's Linked Web Content

After viewing a list of posts, you can view a post's linked web content by referencing the post `#`.

The HTML contents of the post's link are **formatted for easy-viewing within your terminal**.  If available, the formatted output is sent to a pager.

See the [View in a Browser](#view-in-a-browser) section to view the contents in a browser instead.

Usage:

    $ hn view [#]

Example:

    $ hn view 1
    $ hn view 8

![Imgur](http://i.imgur.com/FoTCPAp.png)

## View and Filter a Post's Comments

### View All Comments

After viewing a list of posts, you can view a post's comments by referencing the post `#`.

Examples:

    $ hn view 8 -c
    $ hn view 8 --comments > comments.txt

#### Paged Comments

If running with the auto-completer, comments are automatically paginated.  To get the same pagination without the auto-completer, append `| less -r`:

    $ hn view 8 -c | less -r

![Imgur](http://i.imgur.com/t32ITvN.png)

### Filter on Unseen Comments

Filter comments to expand only those you have not yet seen.  Unseen comments are denoted with a `[!]` and are fully expanded.

Seen comments will be truncated with [...] and will be shown to help provide context to unseen comments.

Examples:

    $ hn view 8 -cu
    $ hn view 8 --comments_unseen | less -r

![Imgur](http://i.imgur.com/tCVpSIs.png)

### Filter on Recent Comments

Filter comments to expand only those **posted within the past 60 minutes**.

Older comments will be truncated with [...] and will be shown to help provide context to recent comments.

Examples:

    $ hn view 8 -cr | less -r
    $ hn view 8 --comments_recent

![Imgur](http://i.imgur.com/diOjxIr.png)

### Filter with Regex

Filter comments based on a given regular expression query.

Examples:

    $ hn view 2 -cq "(?i)programmer" | less -r
    $ hn view 2 --comments_regex_query "(?i)programmer" > programmer.txt

*Case insensitive regex: `(?i)`*

![Imgur](http://i.imgur.com/SlKtIpS.png)

### Hide Non-Matching Comments

When filtering comments for unseen, recent, or with regex, non-matching comments are collapsed to provide context.  To instead hide non-matching comments, pass the `-ch\--comments_hide` flag.  Hidden comments will be displayed as `.`.

Example:

    $ hn view 8 -cu -ch | less -r

![Imgur](http://i.imgur.com/qPopK7X.png)

## Filter the Monthly Hiring Post

Hacker News hosts a monthly hiring post where employers post the latest job openings.

Usage:

    $ hn hiring [regex filter]

Examples:

    $ hn hiring ""
    $ hn hiring "(?i)JavaScript|Node"
    $ hn hiring "(?i)(Node|JavaScript).*(remote)" > remote_jobs.txt

*Case insensitive regex: `(?i)`*

![Imgur](http://i.imgur.com/Lwz8iwG.png)

To search a different monthly hiring post other than the latest, use the hiring post id.

Usage:

    $ hn hiring [regex filter] [post id]

## Filter the Freelancers Post

Hacker News hosts a monthly freelancers post where employers and freelancers post availabilities.

Usage:

    $ hn freelancer [regex filter]

Examples:

    $ hn freelancer ""
    $ hn freelancer "(?i)JavaScript|Node"
    $ hn freelancer "(?i)(Node|JavaScript).*(remote)" > remote_jobs.txt

*Case insensitive regex: `(?i)`*

![Imgur](http://i.imgur.com/TnBDFGk.png)

To search a different monthly hiring post other than the latest, use the hiring post id.

Usage:

    $ hn freelancer [regex filter] [post id]

## Combine With Pipes and Redirects

Output to pagers, write to files, automate with cron, etc.

Examples:

    $ hn view 1 -c | less
    $ hn freelancer "(?i)(Node|JavaScript).*(remote)" > remote_jobs.txt

![Imgur](http://i.imgur.com/x2aj7SM.png)

## View User Info

Usage:

    $ hn user [user id]

![Imgur](http://i.imgur.com/oTALQQI.png)

## View Onions

Usage:

    $ hn onion [limit]  # post limit default: all

![Imgur](http://i.imgur.com/MubWRNG.png)

## View in a Browser

View the linked web content or comments in your default browser instead of your terminal.

Usage:

    $ hn <command> [params] [options] -b
    $ hn <command> [params] [options] --browser

## Windows Support

`haxor-news` has been tested on Windows 10.

### Pager Support

Pager support on Windows is more limited as discussed in the following [ticket](https://github.com/donnemartin/haxor-news/issues/16).  Users can direct output to a pager with the `| more` command:

    $ hn view 1 -c | more

### Config File

On Windows, the `.haxornewsconfig` file can be found in `%userprofile%`.  For example:

    C:\Users\dmartin\.haxornewsconfig

### `cmder` and `conemu`

Although you can use the standard Windows command prompt, you'll probably have a better experience with either [cmder](https://github.com/cmderdev/cmder) or [conemu](https://github.com/Maximus5/ConEmu).

## Installation

### Pip Installation

[![PyPI version](https://badge.fury.io/py/haxor-news.svg)](http://badge.fury.io/py/haxor-news) [![PyPI](https://img.shields.io/pypi/pyversions/haxor-news.svg)](https://pypi.python.org/pypi/haxor-news/)

`haxor-news` is hosted on [PyPI](https://pypi.python.org/pypi/haxor-news).  The following command will install `haxor-news`:

    $ pip install haxor-news

You can also install the latest `haxor-news` from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/donnemartin/haxor-news.git

If you are not installing in a virtualenv, run with `sudo`:

    $ sudo pip install haxor-news

Once installed, run the optional `haxor-news` auto-completer with interactive help:

    $ haxor-news

Run commands:

    $ hn <command> [params] [options]

### Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential issues with dependencies or permissions.

To view `haxor-news` `virtualenv` installation instructions, click [here](https://github.com/donnemartin/haxor-news/blob/master/INSTALLATION.md).

### Mac OS X 10.11 El Capitan Users

There is a known issue with Apple and its included python package dependencies (more info at https://github.com/pypa/pip/issues/3165). We are investigating ways to fix this issue but in the meantime, to install haxor-news, you can run:

    $ sudo pip install haxor-news --upgrade --ignore-installed six

### Supported Python Versions

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

### Supported Platforms

* Mac OS X
    * Tested on OS X 10.10
* Linux, Unix
    * Tested on Ubuntu 14.04 LTS
* Windows
    * Tested on Windows 10

## Developer Installation

If you're interested in contributing to `haxor-news`, run the following commands:

    $ git clone https://github.com/donnemartin/haxor-news.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ haxor-news
    $ hn <command> [params] [options]

### Continuous Integration

[![Build Status](https://travis-ci.org/donnemartin/haxor-news.svg?branch=master)](https://travis-ci.org/donnemartin/haxor-news)

Continuous integration details are available on [Travis CI](https://travis-ci.org/donnemartin/haxor-news).

### Unit Tests and Code Coverage

Run unit tests in your active Python environment:

    $ python tests/run_tests.py

Run unit tests with [tox](https://pypi.python.org/pypi/tox) on multiple Python environments:

    $ tox

### Documentation

Source code documentation will soon be available on [Readthedocs.org](https://readthedocs.org/).  Check out the [source docstrings](https://github.com/donnemartin/haxor-news/blob/master/haxor_news/hacker_news_cli.py).

Run the following to build the docs:

    $ scripts/update_docs.sh

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/donnemartin/haxor-news/blob/master/CONTRIBUTING.md) for details on how to:

* Submit issues
* Submit pull requests

## Credits

* [click](https://github.com/pallets/click) by [mitsuhiko](https://github.com/mitsuhiko)
* [haxor](https://github.com/avinassh/haxor) by [avinassh](https://github.com/avinassh)
* [html2text](https://github.com/aaronsw/html2text) by [aaronsw](https://github.com/aaronsw)
* [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) by [jonathanslenders](https://github.com/jonathanslenders)
* [requests](https://github.com/kennethreitz/requests) by [kennethreitz](https://github.com/kennethreitz)

## Contact Info

Feel free to contact me to discuss any issues, questions, or comments.

My contact info can be found on my [GitHub page](https://github.com/donnemartin).

## License

*I am providing code and resources in this repository to you under an open source license.  Because this is my personal repository, the license you receive to my code and resources is from me and not my employer (Facebook).*

[![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

    Copyright 2015 Donne Martin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
