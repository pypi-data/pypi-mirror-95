#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='py-wikimarkup',
    version='2.1.1',
    packages=find_packages(),
    description='A basic MediaWiki markup parser.',
    long_description=open('README.rst').read(),
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://www.github.com/dgilman/py-wikimarkup/',
    classifiers=[
       'Development Status :: 6 - Mature',
       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
       'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.5',
    zip_safe=False,
    include_package_data=True,
    install_requires=['bleach>=3.0.0,<4.0.0', 'unidecode>=1.2.0,<2.0.0'],
    package_data = { '': ['README.rst'] },
)
