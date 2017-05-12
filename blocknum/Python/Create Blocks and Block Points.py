#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys
import re

dir_path = sys.argv[1] + "\\GIS_edited\\"
name = sys.argv[2]
state = sys.argv[3]

####WORKS    arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", "'Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_1930_stgrid.shp' 'Primary Table'", "'Feature ID' FID VISIBLE NONE;'*From Left' LFROMADD VISIBLE NONE;'*To Left' LTOADD VISIBLE NONE;'*From Right' RFROMADD VISIBLE NONE;'*To Right' RTOADD VISIBLE NONE;'Prefix Direction' <None> VISIBLE NONE;'Prefix Type' <None> VISIBLE NONE;'*Street Name' FULLNAME VISIBLE NONE;'Suffix Type' <None> VISIBLE NONE;'Suffix Direction' <None> VISIBLE NONE;'Left City or Place' CITY VISIBLE NONE;'Right City or Place' CITY VISIBLE NONE;'Left ZIP Code' <None> VISIBLE NONE;'Right ZIP Code' <None> VISIBLE NONE;'Left State' state VISIBLE NONE;'Right State' state VISIBLE NONE;'Left Street ID' <None> VISIBLE NONE;'Right Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;'Max Y value for extent' <None> VISIBLE NONE;'Left parity' <None> VISIBLE NONE;'Right parity' <None> VISIBLE NONE;'Left Additional Field' <None> VISIBLE NONE;'Right Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE", "Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_addloc","")

# overwrite output
arcpy.env.overwriteOutput=True

#Create Paths to be used throughout Process
reference_data = "'S:\\Projects\\1940Census\\StreetGrids\\" + name + state + "_1940_stgrid_edit.shp' 'Primary Table'"
grid = "S:\\Projects\\1940Census\\StreetGrids\\" + name + state + "_1940_stgrid_edit.shp"
dissolve_grid = dir_path + name + "_1930_stgrid_Dissolve.shp"
split_grid = dir_path + name + "_1930_stgrid_Split.shp"
pblocks = dir_path + name + "_1930_Pblk.shp"
field_map="'Feature ID' FID VISIBLE NONE; \
'*From Left' LFROMADD VISIBLE NONE; \
'*To Left' LTOADD VISIBLE NONE; \
'*From Right' RFROMADD VISIBLE NONE; \
'*To Right' RTOADD VISIBLE NONE; \
'Prefix Direction' <None> VISIBLE NONE; \
'Prefix Type' <None> VISIBLE NONE; \
'*Street Name' FULLNAME VISIBLE NONE; \
'Suffix Type' '' VISIBLE NONE; \
'Suffix Direction' <None> VISIBLE NONE; \
'Left City or Place' CITY VISIBLE NONE; \
'Right City or Place' CITY VISIBLE NONE; \
'Left ZIP Code' <None> VISIBLE NONE; \
'Right ZIP Code' <None> VISIBLE NONE; \
'Left State' STATE VISIBLE NONE; \
'Right State' STATE VISIBLE NONE; \
'Left Street ID' <None> VISIBLE NONE; \
'Right Street ID' <None> VISIBLE NONE; \
'Display X' <None> VISIBLE NONE; \
'Display Y' <None> VISIBLE NONE; \
'Min X value for extent' <None> VISIBLE NONE; \
'Max X value for extent' <None> VISIBLE NONE; \
'Min Y value for extent' <None> VISIBLE NONE; \
'Max Y value for extent' <None> VISIBLE NONE; \
'Left parity' <None> VISIBLE NONE; \
'Right parity' <None> VISIBLE NONE; \
'Left Additional Field' <None> VISIBLE NONE; \
'Right Additional Field' <None> VISIBLE NONE; \
'Altname JoinID' <None> VISIBLE NONE"
add_locator = dir_path + name + "_addloc"
#'_1930_Addresses.csv' originates from 'Create 1930 and 1940 Address Files.R' code
addresses = dir_path + name + "_1930_Addresses.csv"
address_fields="Street address; City city; State state; ZIP <None>"
points30 = dir_path + name + "_1930_Points.shp"
pblk_points = dir_path + name + "_1930_Pblk_Points.shp"
temp = dir_path + name + "_temp.shp"

#Check CITY and STATE, standardized and add if it doens't exist yet
fields_raw = arcpy.ListFields(grid)
fields = [i.name for i in fields_raw]

r_city = re.compile('[Cc][Ii][Tt][Yy]')
has_city = filter(r_city.match,fields)

def add_city(grid, name):
	arcpy.AddField_management(grid,'CITY','TEXT')
	cur = arcpy.UpdateCursor(grid)
	for row in cur:
		row.setValue('CITY',name)
		cur.updateRow(row)
	del cur

if len(has_city) == 0:
	add_city(grid, name)
if len(has_city) == 1:
	if has_city[0] != 'CITY':
		arcpy.DeleteField_management(grid, has_city[0])
		add_city(grid, name)

r_state = re.compile('[Ss][Tt][Aa][Tt][Ee]')
has_state = filter(r_state.match,fields)

def add_state(grid, state):
	arcpy.AddField_management(grid,'STATE','TEXT')
	cur = arcpy.UpdateCursor(grid)
	for row in cur:
		row.setValue('STATE',state)
		cur.updateRow(row)
	del cur

if len(has_state) == 0:
	add_state(grid, state)
if len(has_state) == 1:
	if has_state[0] != 'STATE':
		arcpy.DeleteField_management(grid, has_state[0])
		add_state(grid, state)

#Make sure address locator doesn't already exist - if it does, delete it
add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(name+"_addloc")]
for f in add_loc_files:
	if os.path.isfile(f):
		os.remove(f)

print "Working On: " + name + " Creating Physical Blocks"
##### #Create Physical Blocks# #####
#First Dissolve St_Grid lines
arcpy.Dissolve_management(grid, dissolve_grid, "FULLNAME")
#Second Split Lines at Intersections
arcpy.FeatureToLine_management(dissolve_grid, split_grid)
#Third Create Physical Blocks using Feature to Polygon
arcpy.FeatureToPolygon_management(split_grid, pblocks)
#Finally Add a Physical Block ID
expression="!FID! + 1"
arcpy.AddField_management(pblocks, "pblk_id", "LONG", 4, "", "","", "", "")
arcpy.CalculateField_management(pblocks, "pblk_id", expression, "PYTHON_9.3")

print "Working On: " + name + " Geocode\n"
##### #Geocode Points# #####
#Create Address Locator
arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", in_reference_data=reference_data, in_field_map=field_map, out_address_locator=add_locator, config_keyword="")
#Geocode Points
arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
#Attach Pblk ids to points
arcpy.SpatialJoin_analysis(points30, pblocks, pblk_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")

