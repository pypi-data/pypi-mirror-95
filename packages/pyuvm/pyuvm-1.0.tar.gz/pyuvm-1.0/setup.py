# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyuvm',
    version='1.0',
    description='Python Implementation of Universal Verification Methodology',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Ray Salemi',
    author_email='ray@raysalemi.com',
    url='https://github.com/pyuvm/pyuvm',
    license='Apache License',
    packages=find_packages(exclude=('tests', 'docs', 'examples', 'scratch'))
)

