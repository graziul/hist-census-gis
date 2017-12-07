#
#	FixDirAndBlockNumsUsingMap.py
#
#	Purpose: Pre-pend street direction to street without direction if one of two conditions:
#				(a) Other streets in ED exist and have *ONE* direction
#				(b) Same street has opposite direction elsewhere in the city (E -> W)
#
#			 Fix block numbers in microdata using contemporary geocode and ED map
#				(a) Geocode on contemporary map
#				(b) Intersect points 
#
#	Requires: 	(1) Clean street grid (_diradd.shp)
#				(2) Microdata (either _AutoClean.dta or _StudAuto.dta)
#				(3) Completed ED map 

import arcpy
import pysal as ps
import pandas as pd
import subprocess
import sys
import re
import os
from blocknum.blocknum import *
# overwrite output
arcpy.env.overwriteOutput=True

city = 'StLouis'
state = 'MO'
street_var = 'st_best_guess'
geocode_file = ""

different_geocode = False
if geocode_file != "":
	different_geocode = True

# Paths

dir_path = "S:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr
r_path = "C:/Program Files/R/R-3.4.2/bin/Rscript"
script_path = "C:/Users/cgraziul/Documents/GitHub/hist-census-gis"

paths = [r_path, script_path, dir_path]

# Files

grid_1930 = "S:/Projects/1940Census/DirAdd/" + city + state + "_1940_stgrid_diradd.shp"
grid = dir_path + "/GIS_edited/" + city + state + "_1940_stgrid_diradd.shp"
ed_1930 = dir_path + "/GIS_edited/" + city + "_1930_block_ED_checked.shp"
grid_ed_SJ = dir_path + "/GIS_edited/" + city + state + "_1930_grid_edSJ.shp"
microdata_file = dir_path + "/StataFiles_Other/1930/" + city + state + "_StudAuto.dta"
add_locator_old = dir_path + "/GIS_edited/" + city + "_addlocOld"
addresses = dir_path + "/GIS_edited/" + city + "_1930_Addresses.csv"
address_fields_old="Street address; City CITY; State STATE; ZIP <None>"
points30 = dir_path + "/GIS_edited/" + city + "_1930_Points_updated.shp"

#
# Step 1: Fix DIR in microdata using ED map
#

def fix_micro_dir_using_ed_map(city, state, street_var):

	grid_1930 = "S:/Projects/1940Census/DirAdd/" + city + state + "_1940_stgrid_diradd.shp"
	grid = dir_path + "/GIS_edited/" + city + state + "_1940_stgrid_diradd.shp"
	ed_1930 = dir_path + "/GIS_edited/" + city + "_1930_block_ED_checked.shp"
	grid_ed_SJ = dir_path + "/GIS_edited/" + city + state + "_1930_grid_edSJ.shp"
	microdata_file = dir_path + "/StataFiles_Other/1930/" + city + state + "_StudAuto.dta"

	# Make sure not working on actual grid
	arcpy.CopyFeatures_management(grid_1930,grid)

	# Load files
	df_grid = dbf2DF(grid.replace('.shp','.dbf'))
	df_micro = load_large_dta(microdata_file)
	#df_micro = df_micro[['ed','block','hn',street_var,'dir','name','type','checked_st']]
	df_micro[street_var+'_old'] = df_micro[street_var]
	#df_micro_backup = df_micro

	def get_dir(st):
		_, DIR, _, _ = standardize_street(st)
		return DIR

	df_grid['DIR'] = df_grid.apply(lambda x: get_dir(x['FULLNAME']), axis=1)
	grid_path = "/".join(grid.split("/")[:-1]) + "/"
	grid_filename = grid.split("/")[-1]
	save_dbf(df_grid, grid_filename, grid_path)

	arcpy.SpatialJoin_analysis(target_features=grid, 
		join_features=ed_1930, 
		out_feature_class=grid_ed_SJ, 
		join_operation="JOIN_ONE_TO_MANY", 
		join_type="KEEP_ALL", 
		match_option="SHARE_A_LINE_SEGMENT_WITH")

	# Get the spatial join dbf and extract some info
	df_sj = dbf2DF(grid_ed_SJ.replace('.shp','.dbf'))
	df_dir_ed = df_sj[['DIR','ed']].drop_duplicates()
	df_dir_ed = df_dir_ed[df_dir_ed['DIR']!='']
	df_dir_ed = df_dir_ed[df_dir_ed['ed']!=0]
	eds = df_dir_ed['ed'].drop_duplicates().tolist()

	# Create dictionary of {ED:list(DIRs)}
	ed_dir_dict = {}
	ed_grouped = df_dir_ed.groupby(['ed'])
	for ed, group in ed_grouped:
		ed_dir_dict[ed] = group['DIR'].tolist()

	## I feel like this could be simplified significantly

	# Create dictionary of {street_var:list(DIRs)} and delete any that have combination of N/S and E/W
	df_name_dir = df_micro[[street_var,'dir']]
	df_name_dir['st'], df_name_dir['dir'], df_name_dir['name'], df_name_dir['type'] = zip(*df_name_dir.apply(lambda x: standardize_street(x[street_var]), axis=1))
	df_name_dir['st'] = (df_name_dir['name'] + ' ' + df_name_dir['type']).str.strip()
	df_name_dir = df_name_dir.drop_duplicates(['dir','st'])
	df_name_dir = df_name_dir.loc[df_name_dir['dir']!='']

	# Create dictionary of microdata streets and DIRs
	micro_st_dir_dict = {}
	st_grouped = df_name_dir.groupby(['st'])
	for st, group in st_grouped:
		micro_st_dir_dict[st] = group['dir'].tolist()
	def check_st_dirs(dirs):
		if type(dirs) is not list:
			return True
		if ('N' in dirs or 'S' in dirs) and 'W' not in dirs and 'E' not in dirs:
			return True
		if ('E' in dirs or 'W' in dirs) and 'N' not in dirs and 'S' not in dirs:
			return True
		else:
			return False
	micro_st_dir_dict = {k:v for k,v in micro_st_dir_dict.items() if check_st_dirs(v)}

	# Pre-pend DIR to select streets
	def prepend_dir(ED, street_var):
		_, DIR, NAME, TYPE = standardize_street(street_var)
		#If DIR exists, return current values
		if DIR != '':
			return DIR, street_var
		else:
			try:
				st = (NAME + ' ' + TYPE).strip()
				micro_st_dirs = micro_st_dir_dict[st]
				ed_dirs = ed_dir_dict[ED]
			#	print([st, micro_st_dirs, ed_dirs])
				#If ED has single DIR, see if street has same DIR
				if len(ed_dirs) == 1 and ed_dirs == micro_st_dirs:
					new_DIR = ed_dirs[0]
					new_street = (new_DIR + ' ' + NAME + ' ' + TYPE).strip()
			#		print(new_street)
					return new_DIR, new_street
				#If street has single DIR, see if it's in the ED
				if len(micro_st_dirs) == 1 and micro_st_dirs in ed_dirs:
					new_DIR = micro_st_dirs[0]
					new_street = (new_DIR + ' ' + NAME + ' ' + TYPE).strip()
			#		print(new_street)
					return new_DIR, new_street
				#If ED has multiple DIRs, see if 
		#		if len(ed_dirs) > 1 and micro_st_dirs:
		#		if len(micro_st_dirs) > 1 and set(micro):
				else:
					return DIR, street_var
			except:
				return DIR, street_var

	df_micro['dir'], df_micro[street_var] = zip(*df_micro.apply(lambda x: prepend_dir(x['ed'], x[street_var+'_old']), axis=1))	

	# Check how many streets had DIRs pre-pended
	df_micro['changed_Dir'] = df_micro[street_var] != df_micro[street_var+'_old']
	print("Number of cases with DIR prepended: "+str(df_micro['changed_Dir'].sum())+" of "+str(len(df_micro))+" ( "+'{:.1%}'.format(float(df_micro['changed_Dir'].sum())/len(df_micro))+" ) of cases")

	return df_micro

df_micro = fix_micro_dir_using_ed_map(city, state, street_var)

#
# Step 2: Write addresses to file
#

create_1930_addresses(city, state, microdata_file, paths)

#
# Step 3: Run Create Blocks and Block Points.py to get 1930 geocode
#

create_blocks_and_block_points(city, state, paths)

#
# Step 4: Fix block nums in microdata using ED map
#

def fix_micro_blocks_using_ed_map(city, state, paths):

	# Paths

	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/" 

	# File names

	ed_map = geo_path + city + "_1930_ED.shp"
	temp = geo_path + "temp.shp"
	add_locator_contemp = geo_path + city + "_addloc"
	resid_add_dbf = geo_path + city + "_1930_Addresses_residual.dbf"
	resid_add_csv = geo_path + city + "_1930_Addresses_residual.csv"
	address_fields_contemp="Street address; City city; State state"
	points30_resid = geo_path + city + "_1930_ResidPoints.shp"
	intersect_resid_ed = geo_path + city + "_1930_intersect_resid_ed.shp"
	inrighted = geo_path + "_1930_ResidPoints_inRightED.shp"
	intersect_correct_ed = geo_path + city + "_1930_intersect_correct_ed.shp"
	block_shp_file = geo_path + city + "_1930_block_ED_checked.shp"
	microdata_file = dir_path + "/StataFiles_other/1930/"  + city + state + "_StudAuto.dta"

	# Obtain residuals
	arcpy.MakeFeatureLayer_management(points30, "geocodelyr")
	arcpy.SelectLayerByAttribute_management("geocodelyr", "NEW_SELECTION", """ "Status" <> 'M' """)
	arcpy.CopyFeatures_management("geocodelyr",temp)
	df = dbf2DF(temp.replace('.shp','.dbf'))
	resid_vars = ['index','ed','fullname','state','city','address']
	df_resid = df[resid_vars]
	if os.path.isfile(resid_add_csv):
		os.remove(resid_add_csv)
	df_resid.to_csv(resid_add_csv)
	if os.path.isfile(resid_add_csv.replace('.csv','.dbf')):
		os.remove(resid_add_csv.replace('.csv','.dbf'))
	arcpy.TableToTable_conversion(resid_add_csv,geo_path,city + "_1930_Addresses_residual.dbf")
	temp_files = [geo_path+'\\'+x for x in os.listdir(geo_path) if x.startswith("temp")]
	for f in temp_files:
	    if os.path.isfile(f):
	        os.remove(f)

	# Geocode residuals using street grid with contemporary HN ranges
	arcpy.GeocodeAddresses_geocoding(resid_add_dbf, add_locator_contemp, address_fields_contemp, points30_resid)

	# Intersect geocoded points with ED map
	arcpy.Intersect_analysis([ed_map, points30_resid], intersect_resid_ed)

	# Identify points in the correct ED
	arcpy.MakeFeatureLayer_management(intersect_resid_ed, "geocodelyr1")
	arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", """ "ed" = "ed_1" """)
	arcpy.CopyFeatures_management("geocodelyr1",inrighted)

	# Intersect points in the correct ED with block map
	arcpy.Intersect_analysis([block_shp_file, inrighted], intersect_correct_ed)

	# Get correct block number based on block map and geocoded in correct ED
	df_correct_ed = dbf2DF(intersect_correct_ed.replace('.shp','.dbf'))
	df_correct_ed['block'] = df_correct_ed['am_bn'].str.split('-').str[1:].str.join('-')
	fix_block_dict = df_correct_ed[['index','block']].set_index('index')['block'].to_dict()

	# Replace microdata block number with block map block number
	df_micro = load_large_dta(microdata_file)
	df_micro['block_old'] = df_micro['block']

	def fix_block(index, block):
		try:
			fix_block = fix_block_dict[index]
			return fix_block
		except:
			return block

	df_micro['block'] = df_micro[['index','block_old']].apply(lambda x: fix_block(x['index'], x['block_old']), axis=1)
	df_micro['changed_Block'] = df_micro['block'] != df_micro['block_old']

	print("Number of blocks changed: "+str(df_micro['changed_Block'].sum())+" of "+str(len(df_micro))+" ("+'{:.1%}'.format(float(df_micro['changed_Block'].sum())/len(df_micro))+") of cases")

	return df_micro

df_micro = fix_micro_blocks_using_ed_map(city, state, paths)

file_name_students = dir_path + '/StataFiles_Other/1930/%s%s_StudAutoDirBlockFixed.csv' % (city, state)
df_micro.to_csv(file_name_students)

# Convert manually to .dta


