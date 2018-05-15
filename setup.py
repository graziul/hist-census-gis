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
 	name='hist-census-gis',
 	version='1.0.0a1',
 	description='Tools for cleaning and geocoding full count census data (1900-1940)',
 	author='Historical GIS Project, Spatial Structures in the Social Sciences, Brown University',
 	author_email='christopher_graziul@brown.edu',
 	classifiers=['Development Status:: 3 - Alpha',
 		'License :: OSI Approved :: MIT License',
 		'Programming Language :: Python :: 2.7'],
 	packages=find_packages(exclude=['+deprecated+']),
 	install_requires=[
 		'pandas',
 		'termcolor',
 		'colorama',
 		'pickle',
 		'pysal',
 		'openpyxl',
 		'geopandas',
 		'fuzzyset',
 		'fnmatch',
 		'paramiko',
 		'shutil',
 		'unicodecsv'],
 	package_data={
 		'microdata':['sm_ed_st_dict.pickle',
 			'sm_ed_st_dict1900.pickle',
 			'sm_ed_st_dict1910.pickle',
 			'sm_ed_st_dict1930.pickle',
 			'sm_ed_st_dict1940.pickle',
 			'sm_st_ed_dict1900.pickle',
 			'sm_st_ed_dict1910.pickle',
 			'sm_st_ed_dict1930.pickle',
 			'sm_st_ed_dict1940.pickle',
 			'sm_web_abbr.pickle']
 		}
 	)