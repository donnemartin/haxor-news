Installation
============

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

## Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential issues with dependencies or permissions.

If you are a Windows user or if you would like more details on `virtualenv`, check out this [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install `virtualenv` and `virtualenvwrapper`:

    pip install virtualenv
    pip install virtualenvwrapper
    export WORKON_HOME=~/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

Create a `haxor-news` `virtualenv` and install `haxor-news`:

    mkvirtualenv haxor-news
    pip install haxor-news

If you want to activate the `haxor-news` `virtualenv` again later, run:

    workon haxor-news

## Mac OS X 10.11 El Capitan Users

There is a known issue with Apple and its included python package dependencies (more info at https://github.com/pypa/pip/issues/3165). We are investigating ways to fix this issue but in the meantime, to install haxor-news, you can run:

    $ sudo pip install haxor-news --upgrade --ignore-installed six
  
## Nix/NixOS installation

Nix is a package manager default to the NixOS distribution, but it can also be used on any Linux distribution. In order to install `haxor-news` with it run:

    $ nix-env -i haxor-news
