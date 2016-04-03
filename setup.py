from haxor_news.__init__ import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    description=('View and filter Hacker News from the command line: '
                 'Posts, comments, and linked web content.'),
    author='Donne Martin',
    url='https://github.com/donnemartin/haxor-news',
    download_url='https://pypi.python.org/pypi/haxor-news',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=[
        'click>=5.1',
        'colorama>=0.3.3',
        'requests>=2.4.3',
        'pygments>=2.0.2',
        'prompt-toolkit==0.52',
        'six>=1.9.0',
    ],
    extras_require={
        'testing': [
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': [
            'haxor-news = haxor_news.main:cli',
            'hn = haxor_news.main_cli:cli'
        ]
    },
    packages=find_packages(),
    scripts=[],
    name='haxor-news',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
