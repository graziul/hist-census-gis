"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
 	name='histcensusgis',
 	version='1.0.0a5',
 	description='Tools for cleaning and geocoding full count census data (1900-1940)',
 	author='Historical GIS Project, Spatial Structures in the Social Sciences, Brown University',
 	author_email='christopher_graziul@brown.edu',
 	classifiers=['Development Status :: 3 - Alpha',
 		'License :: OSI Approved :: MIT License',
 		'Programming Language :: Python :: 2.7'],
 	packages=find_packages(['histcensusgis']),
 	install_requires=[
 	'pysal',
 	'openpyxl',
 	'geopandas',
 	'fuzzyset',
 	'paramiko',
 	'unicodecsv'],
 	package_data={
 	'':['*.pickle']
 	},
 	url='http://www.github.com/graziul/hist-census-gis'
 	)