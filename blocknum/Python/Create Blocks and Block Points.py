#
# Name:			Create Blocks and Block Points.py
#
# Author(s):	Matt Martinez (adapted for AssignBlockNums.py by Chris Graziul)
#
# Purpose:		Use street grid and microdata to create blocks and perform initial geocode
#
# Usage:		python "Create Blocks and Block Points.py" [path] [city_name] [state abbreviation] 					
#
# File types:	Edited street grid shapefiles
#				StudAuto microdata files
#

import arcpy
import os
import sys
import re
import subprocess

dir_path = sys.argv[1] + "\\GIS_edited\\"
name = sys.argv[2]
state = sys.argv[3]
#start_from = sys.argv[4]

# overwrite output
arcpy.env.overwriteOutput=True

#THIS IS AN ONGOING ISSUE: WHICH VERSION TO START FROM? PAY CLOSE ATTENTION!
#if int(start_from) = 1940:
grid_1940 = "S:\\Projects\\1940Census\\DirAdd\\" + name + state + "_1940_stgrid_diradd.shp"
grid = dir_path + name + state + "_1940_stgrid_edit.shp"
arcpy.CopyFeatures_management(grid_1940, grid)
#if int(start_from) = 1930:

#Create Paths to be used throughout Process
reference_data = dir_path + name + state + "_1930_stgrid_edit_Uns2.shp 'Primary Table'"
grid_uns =  dir_path + name + state + "_1930_stgrid_edit_Uns.shp"
grid_uns2 =  dir_path + name + state + "_1930_stgrid_edit_Uns2.shp"
dissolve_grid = dir_path + name + "_1930_stgrid_Dissolve.shp"
split_grid = dir_path + name + "_1930_stgrid_Split.shp"
pblocks = dir_path + name + "_1930_Pblk.shp"
add_locator = dir_path + name + "_addloc"
#'_1930_Addresses.csv' originates from 'Create 1930 and 1940 Address Files.R' code
addresses = dir_path + name + "_1930_Addresses.csv"
address_fields="Street address; City city; State state; ZIP <None>"
points30 = dir_path + name + "_1930_Points.shp"
pblk_points = dir_path + name + "_1930_Pblk_Points.shp"
temp = dir_path + name + "_temp.shp"

field_map="'Feature ID' FID VISIBLE NONE; \
'*From Left' MIN_LFROMA VISIBLE NONE; \
'*To Left' MAX_LTOADD VISIBLE NONE; \
'*From Right' MIN_RFROMA VISIBLE NONE; \
'*To Right' MAX_RTOADD VISIBLE NONE; \
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

#arcpy.AddField_management(grid, 'FULLNAME', 'TEXT')
#arcpy.CalculateField_management(grid, "FULLNAME","!Strt_Fx!", "PYTHON_9.3")

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
#Unsplit lines before creating address locator (more involved than expected)

#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MIN replace with big number
codeblock_min = """def replace(x):
	if x == ' ':
		return 999999
	else:
		return x"""

fieldName = "LFROMADD"
expression = "replace(!LFROMADD!)"
arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

fieldName = "RFROMADD"
expression = "replace(!RFROMADD!)"
arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MAX replace with small number
codeblock_max = """def replace(x):
	if x == ' ':
		return -1
	else:
		return x"""

fieldName = "LTOADD"
expression = "replace(!LTOADD!)"
arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

fieldName = "RTOADD"
expression = "replace(!RTOADD!)"
arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

#Spatial join split_grid to grid to get unique seg_id for split segments
field_map_spatjoin = """FULLNAME \"FULLNAME\" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
LFROMADD \"LFROMADD\" true true false 80 Text 0 0 ,First,#,%s,LFROMADD,-1,-1; 
LTOADD \"LTOADD\" true true false 80 Text 0 0 ,First,#,%s,LTOADD,-1,-1; 
RFROMADD \"RFROMADD\" true true false 80 Text 0 0 ,First,#,%s,RFROMADD,-1,-1; 
RTOADD \"RTOADD\" true true false 80 Text 0 0 ,First,#,%s,RTOADD,-1,-1; 
NEWSS \"NEWSS\" true true false 9 Long 0 9 ,First,#,%s,NEWSS,-1,-1; 
NAMEREV \"NAMEREV\" true true false 9 Long 0 9 ,First,#,%s,NAMEREV,-1,-1; 
Shape_Leng \"Shape_Leng\" true true false 24 Double 15 23 ,First,#,%s,Shape_Leng,-1,-1; 
NEWSS30 \"NEWSS30\" true true false 24 Double 15 23 ,First,#,%s,NEWSS30,-1,-1; 
NAMEREV30 \"NAMEREV30\" true true false 24 Double 15 23 ,First,#,%s,NAMEREV30,-1,-1; 
CITY \"CITY\" true true false 254 Text 0 0 ,First,#,%s,CITY,-1,-1; 
STATE \"STATE\" true true false 254 Text 0 0 ,First,#,%s,STATE,-1,-1; 
FID_StLoui \"FID_StLoui\" true true false 10 Long 0 10 ,First,#,%s,FID_StLoui,-1,-1; 
FULLNAME_1 \"FULLNAME_1\" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1; 
Seg_ID \"Seg_ID\" true true false 10 Long 0 10 ,First,#,%s,Seg_ID,-1,-1""" % (grid, grid, grid, grid, grid, grid, grid, grid, grid, grid, grid, grid, split_grid, split_grid, split_grid)
arcpy.SpatialJoin_analysis(target_features=grid, join_features=split_grid, out_feature_class=temp, 
	join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_map_spatjoin,
	match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")

#Dissolve on seg_id to unsplit street segments
arcpy.Dissolve_management(in_features=temp, out_feature_class=grid_uns, dissolve_field="FULLNAME;JOIN_FID;city;state", statistics_fields="LFROMADD MIN;LTOADD MAX;RFROMADD MIN;RTOADD MAX", multi_part="MULTI_PART", unsplit_lines="UNSPLIT_LINES")

#Blank out the big/small numbers now that aggregation is done
codeblock = """def replace(x):
	if x == "999999" or x == "-1":
		return ' '
	else:
		return x"""

fieldName = "MIN_LFROMA"
expression = "replace(!MIN_LFROMA!)"
arcpy.CalculateField_management(grid_uns, fieldName, expression, "PYTHON", codeblock)

fieldName = "MIN_RFROMA"
expression = "replace(!MIN_RFROMA!)"
arcpy.CalculateField_management(grid_uns, fieldName, expression, "PYTHON", codeblock)

fieldName = "MAX_LTOADD"
expression = "replace(!MAX_LTOADD!)"
arcpy.CalculateField_management(grid_uns, fieldName, expression, "PYTHON", codeblock)

fieldName = "MAX_RTOADD"
expression = "replace(!MAX_RTOADD!)"
arcpy.CalculateField_management(grid_uns, fieldName, expression, "PYTHON", codeblock)

#Fix grid problems (OFFLOAD TO SEPARATE SCRIPT)

#Create a copy in case names need changing
arcpy.CopyFeatures_management(grid_uns,grid_uns2)
#Add a unique, static identifier (so ranges can be changed later)
expression="!FID! + 1"
arcpy.AddField_management(grid_uns2, "grid_id", "LONG", 4, "", "","", "", "")
arcpy.CalculateField_management(grid_uns2, "grid_id", expression, "PYTHON_9.3")

#Make sure address locator doesn't already exist - if it does, delete it
add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(name+"_addloc")]
for f in add_loc_files:
	if os.path.isfile(f):
		os.remove(f)

#Create Address Locator
arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", in_reference_data=reference_data, in_field_map=field_map, out_address_locator=add_locator, config_keyword="")
#Geocode Points
arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
#Attach Pblk ids to points
arcpy.SpatialJoin_analysis(points30, pblocks, pblk_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
