#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys
import re
import subprocess

dir_path = sys.argv[1] + "\\GIS_edited\\"
name = sys.argv[2]
state = sys.argv[3]

#dir_path = "S:\\Projects\\1940Census\\StLouis\\GIS_edited\\"
#name = "StLouis"
#state = "MO"

####WORKS    arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", "'Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_1930_stgrid.shp' 'Primary Table'", "'Feature ID' FID VISIBLE NONE;'*From Left' LFROMADD VISIBLE NONE;'*To Left' LTOADD VISIBLE NONE;'*From Right' RFROMADD VISIBLE NONE;'*To Right' RTOADD VISIBLE NONE;'Prefix Direction' <None> VISIBLE NONE;'Prefix Type' <None> VISIBLE NONE;'*Street Name' FULLNAME VISIBLE NONE;'Suffix Type' <None> VISIBLE NONE;'Suffix Direction' <None> VISIBLE NONE;'Left City or Place' CITY VISIBLE NONE;'Right City or Place' CITY VISIBLE NONE;'Left ZIP Code' <None> VISIBLE NONE;'Right ZIP Code' <None> VISIBLE NONE;'Left State' state VISIBLE NONE;'Right State' state VISIBLE NONE;'Left Street ID' <None> VISIBLE NONE;'Right Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;'Max Y value for extent' <None> VISIBLE NONE;'Left parity' <None> VISIBLE NONE;'Right parity' <None> VISIBLE NONE;'Left Additional Field' <None> VISIBLE NONE;'Right Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE", "Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_addloc","")

# overwrite output
arcpy.env.overwriteOutput=True

#Create Paths to be used throughout Process
reference_data = dir_path + name + state + "_1940_stgrid_edit_Uns2.shp 'Primary Table'"
grid = dir_path + name + state + "_1940_stgrid_edit.shp"
#grid = dir_path + name + "_1930_Added_Directions.shp"
grid_uns =  dir_path + name + state + "_1940_stgrid_edit_Uns.shp"
grid_uns2 =  dir_path + name + state + "_1940_stgrid_edit_Uns2.shp"
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

#arcpy.DeleteField_management(split_grid,['FID_StLoui'])

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

arcpy.CopyFeatures_management(grid_uns,grid_uns2)

def change_ns(name_type,first_n,fids_n,fids_s):
	cursor = arcpy.UpdateCursor(grid_uns2)
	for row in cursor:
		fid = row.getValue('JOIN_FID')
		st_name = row.getValue('FULLNAME')
		if (st_name == name_type and fid >= first_n and fid not in fids_s) or fid in fids_n:
			row.setValue('FULLNAME','N '+name_type)
		if (st_name == name_type and fid < first_n and fid not in fids_n) or fid in fids_s:
			row.setValue('FULLNAME','S '+name_type)
		cursor.updateRow(row)
		del(row)
	del(cursor)

if name == "StLouis":

	#
	# Broadway St splits N/S at Market St,  is first N Broadway St
	#

	first_n = 6637
	fids_n = []
	fids_s = []

	change_ns("Broadway St",first_n,fids_n,fids_s)

	#
	# Grand Ave splits N/S at Laclede Ave,  is first N Grand Ave (becomes Grand Blvd in contemporary)
	#

	# Issue with "Grand Kingshighway St" - should be changed to "Grand Ave" prior to anything else
	first_n = 7785
	fids_n = []
	fids_s = []

	change_ns("Grand Ave",first_n,fids_n,fids_s)

	#
	# Garrison Ave splits N/S at Laclede Ave

	first_n = 7575
	fids_n = []
	fids_s = []

	change_ns("Garrison Ave",first_n,fids_n,fids_s)

	#
	# Sarah St splits N/S at Forest Park Ave

	first_n = 7946
	fids_n = []
	fids_s = []

	change_ns("Sarah St",first_n,fids_n,fids_s)

	#
	# Ewing Ave splits N/S at Market Ave

	first_n = 7394
	fids_n = []
	fids_s = []

	change_ns("Ewing Ave",first_n,fids_n,fids_s)

	#
	# Boyle Ave splits N/S at Forest Park Blvd
	#

	first_n = 8042
	fids_n = []
	fids_s = []

	change_ns("Boyle Ave",first_n,fids_n,fids_s)

	#
	# Compton Ave splits N/S at Olive St
	#

	first_n = 7889
	fids_n = []
	fids_s = []

	change_ns("Compton Ave",first_n,fids_n,fids_s)


	#
	# For numbered streets, Market St. splits N/S
	#

	# 2nd St
	first_n = 6531
	fids_n = []
	fids_s = []

	change_ns("2nd St",first_n,fids_n,fids_s)

	# 3rd St
	first_n = 6564
	fids_n = []
	fids_s = []

	change_ns("3rd St",first_n,fids_n,fids_s)

	# 4th St
	first_n = 6604
	fids_n = []
	fids_s = []

	change_ns("4th St",first_n,fids_n,fids_s)

	# 5th St
	first_n = 6564
	fids_n = []
	fids_s = []

	change_ns("5th St",first_n,fids_n,fids_s)

	# 6th St
	first_n = 6669
	fids_n = []
	fids_s = []

	change_ns("6th St",first_n,fids_n,fids_s)

	# 7th St
	first_n = 6706
	fids_n = []
	fids_s = []

	change_ns("7th St",first_n,fids_n,fids_s)

	# 8th St
	first_n = 6741
	fids_n = []
	fids_s = []

	change_ns("8th St",first_n,fids_n,fids_s)

	# 9th St
	first_n = 6770
	fids_n = []
	fids_s = []

	change_ns("9th St",first_n,fids_n,fids_s)

	# 10th St
	first_n = 6810
	fids_n = []
	fids_s = []

	change_ns("10th St",first_n,fids_n,fids_s)

	# 11th st
	first_n = 6843
	fids_n = []
	fids_s = []

	change_ns("11th St",first_n,fids_n,fids_s)

	# 12th St (becomes 12th Blvd at Market, unsure what to do)
	#first_n = -1
	#fids_n = []
	#fids_s = []

	#change_ns("12th St",first_n,fids_n,fids_s)

	# 13th St
	first_n = 6934
	fids_n = []
	fids_s = []

	change_ns("13th St",first_n,fids_n,fids_s)

	# 14th St
	first_n = 6974
	fids_n = []
	fids_s = []

	change_ns("14th St",first_n,fids_n,fids_s)

	# 15th St
	first_n = 7014
	fids_n = []
	fids_s = []

	change_ns("15th St",first_n,fids_n,fids_s)

	# 16th St
	first_n = 7056
	fids_n = []
	fids_s = []

	change_ns("16th St",first_n,fids_n,fids_s)

	# 17th St
	first_n = 7088
	fids_n = []
	fids_s = []

	change_ns("17th St",first_n,fids_n,fids_s)

	# 18th St
	first_n = 7127
	fids_n = []
	fids_s = []

	change_ns("18th St",first_n,fids_n,fids_s)

	# 19th St
	first_n = 7275
	fids_n = []
	fids_s = []

	change_ns("18th St",first_n,fids_n,fids_s)

	# 20th St
	first_n = 7198
	fids_n = []
	fids_s = []

	change_ns("20th St",first_n,fids_n,fids_s)

	# 21st St
	first_n = 7251
	fids_n = []
	fids_s = []

	change_ns("20th St",first_n,fids_n,fids_s)

	# 22nd St
	first_n = 7286
	fids_n = []
	fids_s = []

	change_ns("22nd St",first_n,fids_n,fids_s)

	# 23rd St
	first_n = 7331
	fids_n = []
	fids_s = []

	change_ns("23rd St",first_n,fids_n,fids_s)

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
