# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='daliea',
    version='0.0.1',
    description='Evolutionary algorithms applied to visual arts',
    long_description=readme,
    author='Bruno Morgado',
    author_email='jb.morgado@gmail.com',
    url='https://github.com/jbmorgado/daliea',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

