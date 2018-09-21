"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools.command.install import install as _install
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib
import subprocess
import sys

setup(
 	name='histcensusgis',
 	version='1.0.0a127',
 	description='Tools for cleaning and geocoding full count census data (1900-1940)',
 	author='Historical GIS Project, Spatial Structures in the Social Sciences, Brown University',
 	author_email='christopher_graziul@brown.edu',
 	classifiers=['Development Status :: 3 - Alpha',
 		'License :: OSI Approved :: MIT License',
 		'Programming Language :: Python :: 2.7'],
 	packages=find_packages(exclude=['+deprecated+']),
 	install_requires=[
 	'Cython',
 	'pysal',
 	'openpyxl',
 	'pandas',
 	'xlrd',
 	'fiona',
 	'pyproj',
 	'geopandas',
 	'fuzzyset',
 	'paramiko',
 	'unicodecsv',
 	'dbf',
 	'argparse',
 	'fuzzywuzzy',
 	'netcdf4'],
 	package_data={
 	'':['*.pickle','*.R']
 	},
 	scripts=['histcensusgis/RunClean.py'],
	url='http://www.github.com/graziul/hist-census-gis',
  	zip_safe=True,
  	)
