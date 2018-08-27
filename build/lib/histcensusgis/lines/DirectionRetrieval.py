
#
# Name:			DirectionRetrieval.py
#
# Author(s):	Chris Graziul and Amory Kisch 
#
# Purpose:		Re-add street directions lost when creating 1940 street grids from contemporary Tiger/LINE street grids
#
# Usage:		To be run as batch with CityInfo.csv as input			
#
# File types:	Edited street grid shapefiles
#				Tiger/LINE street grid shapefiles
#


from __future__ import print_function
import time
# NOTE: Geopandas MUST be loaded before arcpy to avoid collisions in function naming
import geopandas as gpd
import arcpy
import os
import sys
import re
import pysal as ps
import pandas as pd
import numpy as np
import multiprocessing
from blocknum.blocknum import *
from microclean.STstandardize import *

arcpy.env.overwriteOutput = True

# Paths
dir_path = "S:/Users/Chris/"
stedit_path = "S:/Projects/1940Census/StreetGridsStdName/"
tiger2012_path = "S:/Projects/1940Census/County Shapefiles/"
sj_path = "S:/Projects/1940Census/DirAdd/"

# Get city list
city_info_csv = tiger2012_path + 'CityInfo.csv'
city_info_df = pd.read_csv(city_info_csv, dtype={'fips':str})

# Create city dictionary {CityState:CountyFIPS}
city_info_list = city_info_df.values.tolist()
city_fips_dict = {i[0].replace(' ','')+i[1]:i[3] for i in city_info_list}

# Function to fix blank street names
def fix_blank_names(stedit, contemp1, contemp2):
	# If student edited grid has no street name, fill it in 
	if stedit == "":
		if contemp1 == "":
			return contemp2
		else:
			return contemp1
	else:
		return stedit
			
# Function to add direction
# Note: If edited NAME+TYPE is same as contemp NAME+TYPE, check if edited DIR is same as contemp DIR
def add_dir(dir_e, dir_t1, dir_t2, st_e, st_t1, st_t2):
	if st_e == st_t1:
		if dir_e != "" and dir_t1 != "" and dir_e != dir_t1:
			return '', 1
		if dir_e == "" and dir_t1 != "":
			return dir_t1, 0
		else:
			return '', 0
	if st_e == st_t2:
		if dir_e != "" and dir_t2 != "" and dir_e != dir_t2:
			return '', 1
		if dir_e == "" and dir_t2 != "":
			return dir_t2, 0
		else:
			return '', 0
	else:
		return '', 0

# Function to do the work
def fix_dir(city, hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD']):

	# Load files
	#citystate = city[0]
	#fips = city[1]

	citystate=city
	fips=city_fips_dict[citystate]
	# Log stuff
	#sys.stdout = open(stedit_path + "/logs/DirRet_%s.log" % (citystate),'wb')

	# Filenames
	stedit_shp_file = stedit_path + citystate + "_1940_stgrid_edit.shp"
	stedit_pol_shp_file = stedit_path + citystate + "_1940_stgrid_pol.shp"
	stedit_pol_diss_shp_file = stedit_path + citystate + "_1940_stgrid_pol_diss.shp"
	stedit_pol_diss_buff_shp_file = stedit_path + citystate + "_1940_stgrid_pol_diss_buff.shp"
	tiger2012_shp_file = tiger2012_path + citystate + "_2012_tigerline.shp"
	tiger2012_clip_shp_file = tiger2012_path + citystate + "_2012_tigerline_clip.shp"
	sj_file = sj_path + citystate + "_Spatial_Join.shp"
	sj2_file = sj_path + citystate + "_Spatial_Join2.shp"
	buff_file = sj_path + citystate + "_1940_60ft_BUFF.shp"
	diradd_file = sj_path + citystate + "_1940_stgrid_diradd.shp"
	gaps_file = stedit_path + citystate + "_gaps.shp"
	temp_file = stedit_path + citystate + "_temp.shp"

	print("\nWorking on %s\n" % (citystate))

	# Create copy of edited 1940 street grid (for/while/try/except needed due to processing hiccups)
	try:
		arcpy.DeleteFeatures_management(stedit_shp_file)
	except:
		pass
	print("Trying to load 1940 street grid for %s" % (citystate))		
	for attempt in range(3):
		try:
			if citystate == "StLouisMO":
				arcpy.CopyFeatures_management("S:/Projects/1940Census/StLouis/GIS_edited/StLouisMO_1930_stgrid_edit.shp", 
					stedit_shp_file)
			else:
				arcpy.CopyFeatures_management("S:/Projects/1940Census/StreetGrids/" + citystate + "_1940_stgrid_edit.shp", 
					stedit_shp_file)
			# Have to remove char from num (and convert None to either '' or 0)
			df_stedit_temp = load_shp(stedit_shp_file, hn_ranges)
			# If Kansas City, MO need to rename street variable
			if citystate == "KansasCityMO":
				df_stedit_temp = df_stedit_temp.rename(columns={'stndrdName': 'FULLNAME'})
			save_shp(df_stedit_temp, stedit_shp_file)
		except:
			continue
		else:
			break
	else: 
		print("Error loading 1940 street grid for %s" % (citystate))
		return ['','','','','',''], {}

	# Create copy of TigerLINE 2012 street grid
	try:
		arcpy.DeleteFeatures_management(tiger2012_shp_file)
	except:
		pass
	arcpy.CopyFeatures_management("S:/Projects/1940Census/County Shapefiles/raw/tl_2012_" + fips + "_edges.shp", 
		tiger2012_shp_file)

	# Clip TigerLINE 2012 file to match 1940 street grid (Lisa)
	arcpy.FeatureToPolygon_management(in_features=stedit_shp_file, 
		out_feature_class=stedit_pol_shp_file, 
		attributes="ATTRIBUTES")
	arcpy.Dissolve_management(in_features=stedit_pol_shp_file, 
		out_feature_class=stedit_pol_diss_shp_file, 
		dissolve_field="Id", 
		multi_part="MULTI_PART", 
		unsplit_lines="DISSOLVE_LINES")
	arcpy.Buffer_analysis(in_features=stedit_pol_diss_shp_file, 
		out_feature_class=stedit_pol_diss_buff_shp_file, 
		buffer_distance_or_field="1000 Feet", 
		line_side="FULL", 
		line_end_type="ROUND", 
		dissolve_option="NONE", 
		method="PLANAR")
	arcpy.Clip_analysis(in_features=tiger2012_shp_file, 
		clip_features=stedit_pol_diss_buff_shp_file, 
		out_feature_class=tiger2012_clip_shp_file)

	# Load attibute data for files
	df_stedit = load_shp(stedit_shp_file, hn_ranges)
	df_tiger2012 = load_shp(tiger2012_clip_shp_file, hn_ranges)

	# Determine number of DIR in TigerLINE 2012
	df_tiger2012['FULLSTD'], df_tiger2012['DIR'], df_tiger2012['NAME'], df_tiger2012['TYPE'] = zip(*df_tiger2012.apply(lambda x: standardize_street(x['FULLNAME']), axis=1))
	tiger2012_dir_counts_dict = df_tiger2012['DIR'].value_counts().to_dict()

	# Drop all extraneous variables
	df_stedit['FULLEDIT'] = df_stedit['FULLNAME']
	df_stedit['OrigStE'] = df_stedit['FULLNAME']
	keep_vars_stedit = ['geometry','FULLEDIT','LFROMADD','LTOADD','RFROMADD','RTOADD','OrigStE']
	df_stedit = df_stedit[keep_vars_stedit]
	
	df_tiger2012['FULL2012'] = df_tiger2012['FULLNAME']
	df_tiger2012['OrigStT'] = df_tiger2012['FULLNAME']
	keep_vars_tiger2012 = ['geometry','FULL2012','OrigStT']
	df_tiger2012 = df_tiger2012[keep_vars_tiger2012]

	# Write .shp
	save_shp(df_stedit, stedit_shp_file)
	save_shp(df_tiger2012, tiger2012_clip_shp_file)

	# Create copies of original FID (text) variable
	arcpy.AddField_management(stedit_shp_file, "FIDCOPYE", "TEXT", 50, "", "","", "", "")
	arcpy.AddField_management(tiger2012_clip_shp_file, "FIDCOPYT", "TEXT", 50, "", "","", "", "")

	arcpy.CalculateField_management(in_table=stedit_shp_file, 
		field="FIDCOPYE", 
		expression="!FID!", 
		expression_type="PYTHON") 
	arcpy.CalculateField_management(in_table=tiger2012_clip_shp_file,
		field="FIDCOPYT", 
		expression="!FID!", 
		expression_type="PYTHON") 

	# Process: Spatial Join (for/while/try/except needed due to processing hiccups)
	print("Trying to perform spatial joins for %s" % (citystate))		
	for attempt in range(0,3):
		try:
			# Spatial join - ARE_IDENTICAL_TO
			arcpy.SpatialJoin_analysis(target_features=stedit_shp_file, 
				join_features=tiger2012_clip_shp_file, 
				out_feature_class=sj_file, 
				join_operation="JOIN_ONE_TO_ONE", 
				join_type="KEEP_ALL", 
				field_mapping="""FULLEDIT "FULLEDIT" true true false 254 Text 0 0 ,First,#,%s,FULLEDIT,-1,-1;
				LFROMADD "LFROMADD" true true false 10 Long 0 10 ,First,#,%s,LFROMADD,-1,-1;
				LTOADD "LTOADD" true true false 10 Long 0 10 ,First,#,%s,LTOADD,-1,-1;
				RFROMADD "RFROMADD" true true false 10 Long 0 10 ,First,#,%s,RFROMADD,-1,-1;
				RTOADD "RTOADD" true true false 10 Long 0 10 ,First,#,%s,RTOADD,-1,-1;
				OrigStE "OrigStE" true true false 254 Text 0 0 ,First,#,%s,OrigStE,-1,-1;
				FIDCOPYE "FIDCOPYE" true true false 254 Text 0 0 ,First,#,%s,FIDCOPYE,-1,-1;
				FULL2012 "FULL2012" true true false 254 Text 0 0 ,First,#,%s,FULL2012,-1,-1;
				OrigStT "OrigStT" true true false 254 Text 0 0 ,First,#,%s,OrigStT,-1,-1;
				FIDCOPYT "FIDCOPYT" true true false 254 Text 0 0 ,First,#,%s,FIDCOPYT,-1,-1""" % (stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, tiger2012_clip_shp_file, tiger2012_clip_shp_file, tiger2012_clip_shp_file), 
				match_option="ARE_IDENTICAL_TO")
			# Create Buffer
			arcpy.Buffer_analysis(in_features=sj_file, 
				out_feature_class=buff_file, 
				buffer_distance_or_field="60 Feet", 
				line_side="FULL", 
				line_end_type="ROUND", 
				dissolve_option="NONE", 
				method="PLANAR")
			# Spatial join - CONTAINS
			arcpy.SpatialJoin_analysis(target_features=buff_file, 
				join_features=tiger2012_clip_shp_file, 
				out_feature_class=sj2_file, 
				join_operation="JOIN_ONE_TO_ONE", 
				join_type="KEEP_ALL", 
				match_option="CONTAINS")
		except:
			continue
		else:
			break
	else: 
		print("Error performing spatial joins for %s" % (citystate))
		return ['','','','','',''], {}

	# Load final street grid data and create vars for comparison
	df_sj2 = load_shp(sj2_file, hn_ranges)  

	df_sj2['FULLSTD_e'], df_sj2['DIR_e'], df_sj2['NAME_e'], df_sj2['TYPE_e'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULLEDIT']), axis=1))
	df_sj2['FULLSTD_t1'], df_sj2['DIR_t1'], df_sj2['NAME_t1'], df_sj2['TYPE_t1'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULL2012']), axis=1))
	df_sj2['FULLSTD_t2'], df_sj2['DIR_t2'], df_sj2['NAME_t2'], df_sj2['TYPE_t2'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULL2012_1']), axis=1))

	df_sj2['st_e'] = df_sj2['NAME_e'] + ' ' + df_sj2['TYPE_e']
	df_sj2['st_e'] = df_sj2['st_e'].str.rstrip()
	df_sj2['st_t1'] = df_sj2['NAME_t1'] + ' ' + df_sj2['TYPE_t1']
	df_sj2['st_t1'] = df_sj2['st_t1'].str.rstrip()
	df_sj2['st_t2'] = df_sj2['NAME_t2'] + ' ' + df_sj2['TYPE_t2']
	df_sj2['st_t2'] = df_sj2['st_t2'].str.rstrip()

	# Fix blank street names - wasn't producing intended results, leaving code for documentation
 	#df_sj2['FULLSTD'] = df_sj2.apply(lambda x: fix_blank_names(x['FULLSTD_e'], x['FULLSTD_t1'], x['FULLSTD_t2']), axis=1)

	# Add DIR if called for
	df_sj2['DIR_fix'], df_sj2['DIR_mismatch'] = zip(*df_sj2.apply(lambda x: add_dir(x['DIR_e'], x['DIR_t1'], x['DIR_t2'], x['st_e'], x['st_t1'], x['st_t2']), axis=1))

	# Rereate FULLNAME based on fixed DIR
	def make_fullname(dir_e, dir_fix, st_e):
		if dir_e != '':
			return dir_e + ' ' + st_e
		if dir_e == '' and dir_fix != '':
			return dir_fix + ' ' + st_e
		if dir_e == '' and dir_fix == '':
			return st_e
	df_sj2['FULLNAME'] = df_sj2.apply(lambda x: make_fullname(x['DIR_e'],x['DIR_fix'],x['st_e']), axis=1)

	# Create DF to merge with 1940 edited street grid
	df_tomerge = df_sj2[['FIDCOPYE','DIR_e','DIR_fix','FULLNAME']]

	# Merge streets with fixed DIR and 1940 edited street grid
	df_stedit = load_shp(stedit_shp_file, hn_ranges) 
	df = df_stedit.merge(df_tomerge, how='left', on='FIDCOPYE')
	save_shp(df, temp_file) 

	# Fix gaps
	print("Trying to create gaps file for %s" % (citystate))		
	for attempt in range(3):
		try:
			arcpy.SpatialJoin_analysis(target_features=temp_file,
				join_features=temp_file, 
				out_feature_class=gaps_file, 
				join_operation="JOIN_ONE_TO_MANY", 
				join_type="KEEP_ALL", 
				field_mapping="""FIDCOPYE "FIDCOPYE" true true false 100 Text 0 0 ,First,#,%s,FIDCOPYE,-1,-1;
				FULLNAME "FULLNAME" true true false 100 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
				FULLNAME_1 "FULLNAME_1" true true false 100 Text 0 0 ,First,#,%s,FULLNAME,-1,-1""" % (temp_file, temp_file, temp_file), 
				match_option="INTERSECT")
		except:
			continue
		else:
			break
	else: 
		print("Error creating gaps file for %s" % (citystate))
		return ['','','','','',''], {}

	def list_append_unique(LIST, item) :
		if(not item in LIST) :
			LIST.append(item)
		return LIST

	def make_nametype(st_list):
		NAME, TYPE = st_list
		nametype = NAME + ' ' + TYPE
		return nametype.rstrip()

	df_gaps = load_shp(gaps_file, hn_ranges)
	# Make dictionary for FID to TARGET FID
	fid_dict = {target_fid:df_group['FULLNAME'].tolist() for target_fid, df_group in df_gaps.groupby('TARGET_FID')}
 #	for target_fid, df_group in df_diradd.groupby('TARGET_FID'):
 #		fid_dict[target_fid] = df_group['FULLNAME'].tolist()
	# run through FIDs from original Target file	
	def fill_gap(curFID, fullname):
		_, st_dir, st_name, st_type = standardize_street(fullname)
		# st=FULLNAME of segment identified by curFID #we can either retrieve this from original Target, or it is the record from TargetSJ where TARGET_FID == JOIN_FID == curFID
		nametype = make_nametype([st_name, st_type])
		#select records where TARGET_FID == curFID # this gives us all streets that intersected with segment identified by curFID
		intersect_list = fid_dict[int(curFID)]
		same_name_list = filter(lambda x: make_nametype(standardize_street(x)[2:])==nametype, intersect_list)
		dir_list = []
		for st in same_name_list :
			list_append_unique(dir_list, standardize_street(st)[1])
		if (len(dir_list)==1) and st_dir == '':
			return same_name_list[0]
		else :
			#multiple different directions, no change
			return fullname

	arcpy.CopyFeatures_management(temp_file, diradd_file)
	df_diradd = load_shp(diradd_file, hn_ranges) 	

	# Try to fix gaps
	df_diradd['FULLNAMEda'] = df_diradd.apply(lambda x: fill_gap(x['FIDCOPYE'], x['FULLNAME']), axis=1)
	# Do things if any gaps are fixed
	if sum(df_diradd['FULLNAMEda'] == df_diradd['FULLNAME']) < len(df_diradd):

		def note_gap_dir_fixes(st,dir_fix):
			_, st_dir, _, _ = standardize_street(st)
			if dir_fix == "" and st_dir != "":
				return st_dir
			else:
				return dir_fix

		num_missing_before = len(df_diradd[df_diradd['DIR_e']!=df_diradd['DIR_fix']])
		df_diradd['DIR_fix'] = df_diradd.apply(lambda x: note_gap_dir_fixes(x['FULLNAMEda'], x['DIR_fix']), axis=1)
		num_missing_after = len(df_diradd[df_diradd['DIR_e']!=df_diradd['DIR_fix']])
		num_gaps_filled = num_missing_before - num_missing_after
		df_diradd['FULLNAMEgp'] = df_diradd['FULLNAME']
		df_diradd['FULLNAME'] = df_diradd['FULLNAMEda']
		save_shp(df_diradd, diradd_file)
		print("Filled " + str(num_gaps_filled) + " gaps in " + citystate)

	del df_diradd['FULLNAMEda']

	# Cleanup shapefiles
	arcpy.Delete_management(stedit_pol_shp_file)
	arcpy.Delete_management(stedit_pol_diss_shp_file)
	arcpy.Delete_management(stedit_pol_diss_buff_shp_file)
	arcpy.Delete_management(tiger2012_shp_file)
	arcpy.Delete_management(buff_file)
	arcpy.Delete_management(sj_file)
	arcpy.Delete_management(sj2_file)
	arcpy.Delete_management(gaps_file)
	arcpy.Delete_management(temp_file)

	# Count changes
	stgrid_dir_counts_dict = df_sj2['DIR_e'].value_counts().to_dict()
	fixed_dir_counts_dict = df_diradd['DIR_fix'].value_counts().to_dict()

	num_stseg = sum(stgrid_dir_counts_dict.values())
	num_dirs_stedit = num_stseg - stgrid_dir_counts_dict['']
	num_dirs_added = stgrid_dir_counts_dict[''] - fixed_dir_counts_dict[''] 

	num_tiger = sum(tiger2012_dir_counts_dict.values()) 
	num_dirs_tiger = num_tiger - tiger2012_dir_counts_dict['']

	info_dict = {'tiger2012':tiger2012_dir_counts_dict,
		'stedit':stgrid_dir_counts_dict,
		'diradd':fixed_dir_counts_dict}

	info = [citystate, num_stseg, num_dirs_stedit, num_dirs_added, num_tiger, num_dirs_tiger]

	print("\nFinished %s, %s DIR mismatches" % (citystate, str(df_sj2['DIR_mismatch'].sum())))

	return info, info_dict 


'''
# This iterates sequentially as opposed to parallel processing
temp_dict = {}
temp = []
start_total = time.time()
for i in city_fips_dict.items():
	info, info_dict = fix_dir(i)
	temp.append(info)
	temp_dict[i[0]] = info_dict
temp = [i for i in temp if i != ['', '', '', '', '', '']]
end_total = time.time()

total_time = round(float(end_total-start_total)/60,1)
print("Total processing time: %s\n" % (total_time))

'''

'''
# This uses parallel processing rather than iterating sequentially
if __name__ == "__main__":
	pool = multiprocessing.Pool(processes=8, maxtasksperchild=1)
	temp = pool.map(fix_dir, city_fips_dict.items())
	pool.close()

	# pd.DataFrame.from_dict(info_dict)

	# Build dashboard for decade and save
	city_state = ['City']
	tiger_names = ['num_tiger','num_dirs_tiger']
	stedit_names = ['num_stedit','num_dirs_stedit','num_dirs_added']

	sp = ['']
	names = city_state + stedit_names + tiger_names 
	df = pd.DataFrame(temp,columns=names)

	dfnum = df.ix[:,0:5].sort_values(by='num_dirs_stedit').reset_index()

	dashboard = pd.concat([dfnum],axis=1)
	del dashboard['index']

	csv_file = sj_path + '/DirAddSummary2018_03_16.csv' 
	dashboard.to_csv(csv_file, index=False)
'''