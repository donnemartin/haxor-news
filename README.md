[![Build Status](https://travis-ci.org/donnemartin/saws.svg?branch=master)](https://travis-ci.org/donnemartin/saws) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/saws.svg)](https://codecov.io/github/donnemartin/saws/saws) [![PyPI version](https://badge.fury.io/py/onion.svg)](http://badge.fury.io/py/onion)

hacker-news-onion
=================

> ***A Hacker's Finest News Source***  *-[@HackerNewsOnion](#credits)*

## Today's Top Headlines

![Imgur](http://i.imgur.com/aU569Yv.png)
![Imgur](http://i.imgur.com/ZVpRdxH.png)
![Imgur](http://i.imgur.com/2Kv6UxC.png)
![Imgur](http://i.imgur.com/8ZGDRYq.png)
![Imgur](http://i.imgur.com/e1nuqdC.png)
![Imgur](http://i.imgur.com/opoRJ79.png)
![Imgur](http://i.imgur.com/gTlWaVI.png)
![Imgur](http://i.imgur.com/9JazvbL.png)
![Imgur](http://i.imgur.com/jlIfzoT.png)
![Imgur](http://i.imgur.com/OnVaQVp.png)

> ![Imgur](http://i.imgur.com/KUMg4Si.png)

## Installing Onion

[![PyPI version](https://badge.fury.io/py/onion.svg)](http://badge.fury.io/py/onion) [![PyPI](https://img.shields.io/pypi/pyversions/onion.svg)](https://pypi.python.org/pypi/onion/)

Install `onion` from [PyPI](https://pypi.python.org/pypi/onion):

    $ pip install onion

## Using Onion

Cycle through the top 40+ headlines:

    $ onion

Specific headline:

    $ onion [#]

RNG:

    $ onion -r

## Contributing to Onion

[![Build Status](https://travis-ci.org/donnemartin/saws.svg?branch=master)](https://travis-ci.org/donnemartin/saws) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/saws.svg)](https://codecov.io/github/donnemartin/saws/saws) [![Documentation Status](https://readthedocs.org/projects/saws/badge/?version=latest)](http://saws.readthedocs.org/en/latest/?badge=latest)

For bug reports or requests [submit an issue](https://github.com/donnemartin/saws/issues).

    $ git clone https://github.com/donnemartin/hacker-news-onion.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ onion

Run tests:

    $ tox

## Credits

* [@HackerNewsOnion](https://twitter.com/HackerNewsOnion)
* [click](https://github.com/mitsuhiko/click) by [mitsuhiko](https://github.com/mitsuhiko)
* [img2txt](https://github.com/hit9/img2txt) by [hit9](https://github.com/hit9)
