[![Build Status](https://magnum.travis-ci.com/donnemartin/hacker-news-onion.svg?token=HyQMZpiZXhiL2dftcC67)](https://magnum.travis-ci.com/donnemartin/hacker-news-onion) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/hacker-news-onion.svg)](https://codecov.io/github/donnemartin/hacker-news-onion/hacker-news-onion) [![PyPI version](https://badge.fury.io/py/onion.svg)](http://badge.fury.io/py/onion)

hacker-news-onion
=================

> ***A Hacker's Finest News Source***  *-[@HackerNewsOnion](#credits)*
>
> ![Imgur](http://i.imgur.com/01kNvP4.png)

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

## Installing Onion

[![PyPI version](https://badge.fury.io/py/onion.svg)](http://badge.fury.io/py/onion) [![PyPI](https://img.shields.io/pypi/pyversions/onion.svg)](https://pypi.python.org/pypi/onion/)

Install `onion` from [PyPI](https://pypi.python.org/pypi/onion):

    $ pip install onion

## Using Onion

Cycle through the top 40 headlines:

    $ onion

Specific headline:

    $ onion [#]

RNG:

    $ onion -r

## Contributing to Onion

[![Build Status](https://magnum.travis-ci.com/donnemartin/hacker-news-onion.svg?token=HyQMZpiZXhiL2dftcC67)](https://magnum.travis-ci.com/donnemartin/hacker-news-onion) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/hacker-news-onion.svg)](https://codecov.io/github/donnemartin/hacker-news-onion/hacker-news-onion)

For bug reports or requests [submit an issue](https://github.com/donnemartin/hacker-news-onion/issues).

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
