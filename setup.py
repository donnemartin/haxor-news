from onion.__init__ import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    description='Hacker News lulz from the command line.',
    author='Donne Martin',
    url='https://github.com/donnemartin/hacker-news-onion',
    download_url='https://github.com/donnemartin/hacker-news-onion/archive/master.zip',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=[
        'click>=5.1',
    ],
    extras_require={
        'testing': [
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'onion = onion.onion:OnionCli.cli'
    },
    packages=find_packages(),
    scripts=[],
    name='onion',
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
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
