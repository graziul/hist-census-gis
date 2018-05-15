# Import the ESRI library of tools into Python
import arcpy
import os
import pysal as ps
import pandas as pd
from blocknum.blocknum import *
from geocoding.GeocodeFunctions import *
import random

# All Python to overwrite any ESRI output files (e.g., shapefiles)
arcpy.env.overwriteOutput=True

# City info
city = "Albany"
state = "NY"

# Paths
dir_path = "S:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr
r_path = "C:/Program Files/R/R-3.4.2/bin/Rscript"
script_path = "C:/Users/cgraziul/Documents/GitHub/hist-census-gis"
paths = [r_path, script_path, dir_path]
geo_path = dir_path + "/GIS_edited/"

# Files
grid_uns2 =  geo_path + city + state + "_1930_stgrid_edit_Uns2.shp"
points30 = geo_path + city + "_1930_Points.shp"

# House number range variables (must be [LF, LT, RF, RT])
hn_ranges = ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD']

try:
	microdata_file = dir_path + "/StataFiles_Other/1930/" + city + state + "_StudAuto.dta"
	df = load_large_dta(microdata_file)
except:
	print("No Student + AutoClean file")
df.loc[:,('index')] = df.index

# Import and "fix up" the street grid (creates _Uns2.shp)
problem_segments = street(geo_path=geo_path, 
	city_name=city, 
	state_abbr=state, 
	hn_ranges=hn_ranges)

# Create 1930 addresses
create_1930_addresses(city_name=city, 
	state_abbr=state, 
	paths=paths, 
	df=df)

# Perform initial geocode
initial_geocode(geo_path=geo_path, 
	city_name=city, 
	state_abbr=state, 
	hn_ranges=hn_ranges)

# Get streets in microdata but not in grid
df_points30 = dbf2DF(points30)
df_ungeocoded = df_points30[df_points30['Ref_ID']==-1]
df_grid = dbf2DF(grid_uns2)

get_st_in_micro_not_grid(geo_path=geo_path, 
	df_ungeocoded=df_ungeocoded, 
	df_grid=df_grid, 
	city_name=city, 
	state_abbr=state)

