haxor-news
=================

View and filter Hacker News posts, comments, and linked web content without leaving the command line.  Comes with auto-completion and interactive help.

> *Coworker who sees me looking at something in a browser: "Glad you're not busy; I need you to do this, this, this..."*
>
> *Coworker who sees me staring intently at a command prompt: Backs away, slowly...*
>
> *-[Source](https://www.reddit.com/user/foxingworth)*

## Index

### General

* [Syntax](#syntax)
* [Commands](#commands)
* [Auto-Completion and Interactive Help](#auto-completion-and-interactive-help)

### Features

* [View Posts](#view-posts)
* [View a Post's Linked Web Content in a Terminal](#view-a-posts-linked-web-content-in-a-terminal)
* [View and Filter a Post's Comments](#view-and-filter-a-posts-comments)
    * [View All Comments](#view-all-comments)
    * [View Only Unseen Comments](#view-only-unseen-comments)
    * [View Only Recent Comments](#view-only-recent-comments)
    * [Filter Post Comments with Regex](#filter-post-comments-with-regex)
* [View and Filter the Monthly Hiring Post](#filter-the-monthly-hiring-post)
* [View and Filter the Monthly Freelancer Post](#filter-the-monthly-hiring-post)
* [View User Info](#view-user-info)
* [View Onions](#view-onions)
* [View in a Browser](#viewing-results-in-a-browser)
* [TODO]()
    * [Submit Posts and Comments]()
    * [Search Posts and Comments]()
    * [Customize Color Scheme]()

## Installation

### Pip Installation

[![PyPI version](https://badge.fury.io/py/saws.svg)](http://badge.fury.io/py/saws) [![PyPI](https://img.shields.io/pypi/pyversions/saws.svg)](https://pypi.python.org/pypi/saws/)

`hncli` is hosted on [PyPI](https://pypi.python.org/pypi/hncli).  The following command will install `hncli`:

    $ pip install hncli

You can also install the latest `hncli` from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/donnemartin/hacker-news-cli.git

If you are not installing in a virtualenv, run with `sudo`:

    $ sudo pip install hncli

Once installed, run `hncli`:

    $ hn [command] [options]

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
    * Tested on Windows 7 and 10

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/donnemartin/hacker-news-cli/blob/master/CONTRIBUTING.md) for details on how to:

* Submit issues
* Submit pull requests

## Contact Info

Feel free to contact me with any issues, questions, or comments.

* Email: [donne.martin@gmail.com](mailto:donne.martin@gmail.com)
* Twitter: [donne_martin](https://twitter.com/donne_martin)
* GitHub: [donnemartin](https://github.com/donnemartin)
* LinkedIn: [donnemartin](https://www.linkedin.com/in/donnemartin)
* Website: [donnemartin.com](http://donnemartin.com)

## License

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
