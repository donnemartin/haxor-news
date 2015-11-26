from hncli.__init__ import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    description='A Hacker News command line interface (CLI).',
    author='Donne Martin',
    url='https://github.com/donnemartin/hncli',
    download_url='https://pypi.python.org/pypi/hncli',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=[
        'click>=5.1',
        'colorama>=0.3.3',
        'html2text',
        'requests>=2.4.3',
        'tabulate>=0.7.5',
    ],
    extras_require={
        'testing': [
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'hn = hncli.hacker_news_cli:HackerNewsCli.cli'
    },
    packages=find_packages(),
    scripts=[],
    name='hncli',
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
