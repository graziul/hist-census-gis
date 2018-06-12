"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
 	name='histcensusgis',
 	version='1.0.0a82',
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
 	'shapely',
 	'fiona',
 	'pyproj',
 	'geopandas',
 	'fuzzyset',
 	'paramiko',
 	'unicodecsv',
 	'dbf'],
 	package_data={
 	'':['*.pickle','*.R']
 	},
 	url='http://www.github.com/graziul/hist-census-gis',
  	zip_safe=False,
  	)