# -*- coding: utf-8 -*-

#
# All the functions for performing block numbering (includes many things)
#

from histcensusgis.microdata.misc import load_cleaned_microdata
from histcensusgis.lines.street import *
from histcensusgis.points.geocode import *
from histcensusgis.s4utils.IOutils import *
from multiprocessing import Pool
import histcensusgis
import arcpy
import sys
import subprocess
import random
import re
arcpy.env.overwriteOutput = True

#
# Misc functions
#

# Fix grid and get physical blocks
def get_pblks(city_info, paths, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD'], geocode_file=None):
	
	"""
	Creates physical blocks after re-running grid fixing function

	Parameters
	----------
	city_info : list
		List containing city name (e.g. "Hartford"), state abbreviation (e.g. "CT"), and decade (e.g. 1930)
	paths : list 
		List of file paths for R code, Python scripts, and data files
	hn_ranges : list (Optional)
		List of string variables naming min/max from/to for house number ranges in street grid

	Returns
	-------
	1. "Fixed" street grid (if it doesn't exist already)
	2. Shapefile containing physical blocks based on "fixed" street grid

	"""

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# overwrite output
	arcpy.env.overwriteOutput=True

	print("The script has started to work and is running the 'street' function")

	problem_segments = process_raw_grid(city_info, geo_path, hn_ranges)
	print("The script has finished executing the 'street' function and has now started executing 'physical_blocks' function")

	create_pblks(city_info, geo_path)
	print("The script has finished executing the 'physical_blocks' function and has now started executing 'geocode' function")

# Creates physical blocks shapefile 
def create_pblks(city_info, geo_path):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')

	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	split_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Split.shp"
	grid_uns2 = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"

	if not os.path.isfile(split_grid) or not os.path.isfile(grid_uns2):
		print("Processing raw stgrid for %s" %decade)
		_ = process_raw_grid(city_info, geo_path)

	#Create Physical Blocks# #####
	arcpy.FeatureToPolygon_management(split_grid, pblk_shp)
	#Add a Physical Block ID
	expression="!FID! + 1"
	arcpy.AddField_management(pblk_shp, "pblk_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(pblk_shp, "pblk_id", expression, "PYTHON_9.3")

# Attach physical block IDs to geocoded points 
def attach_pblk_id(city_info, geo_path, points_shp):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Files
	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	pblk_points_shp = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"

	#Attach Pblk ids to points
	arcpy.SpatialJoin_analysis(points_shp, 
		pblk_shp, 
		pblk_points_shp, 
		"JOIN_ONE_TO_MANY", 
		"KEEP_ALL", 
		"#", 
		"INTERSECT")
	print("The script has finished executing the 'SpatialJoin' tool")

#
# Block numbering functions
# 

# Identifies block numbers and can be run independently (R script)
# NOTE: Assigns block numbers using microdata blocks. Examines proportion of cases that geocode 
# onto the same physical block and decides  
def identify_blocks_geocode(city_info, paths):

	city_name, _, decade = city_info
	city_name = city_name.replace(' ','')

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Ensure files exist for Matt's block algorithm
	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	pblk_points_shp = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"
	#if not os.path.isfile(pblk_points_shp) or not os.path.isfile(pblk_shp):
	check_matt_dependencies(city_info, paths)

	print("Identifying " + str(decade) + " blocks\n")
	package_path = os.path.dirname(histcensusgis.__file__)
	t = subprocess.call([r_path,'--vanilla',package_path+'/polygons/Identify 1930 Blocks.R',dir_path,city_name,str(decade)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying " + str(decade) + " blocks for "+city_name+"\n")
	else:
		print("OK!\n")

# Uses block descriptions from microdata to fill in block numbers
def identify_blocks_microdata(city_info, paths, micro_street_var='st_best_guess', v=7):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	block_shp = geo_path + city_name + "_" + str(decade) + "_block_geo.shp"
	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	grid_shp = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	pblk_grid_shp = geo_path + city_name + state_abbr + "_" + str(decade) + "_Pblk_Grid_SJ.shp"
	block_guess_shp = geo_path + city_name + "_" + str(decade) + "_block_guess.shp"
	pblk_grid_dict_file = geo_path + city_name + "_pblk_grid_dict.pkl"
	pblk_st_dict_file = geo_path + city_name + "_pblk_st_dict.pkl"

	print("Getting block description guesses\n")

	#
	# Step 1: Create "block descriptions" using microdata
	#

	#Load data
	start = time.time()
	
	df_pre = load_cleaned_microdata(city_info, dir_path)
	df_pre = df_pre[['ed','block',micro_street_var]]

	end = time.time()
	run_time = round(float(end-start)/60, 1)
	print("Finished loading microdata (took " + str(run_time) + " minutes)")

	#TO DO: Clean up block numbers
	df_pre = df_pre[df_pre['block'].notnull() & df_pre['ed'].notnull()]
	df_pre['ed_int'] = df_pre['ed'].astype(int)
	df_pre['ed_block'] = df_pre['ed_int'].astype(str) + '-' + df_pre['block'].astype(str)
	#del df_pre['ed']
	#del df_pre['block']

	#Get number of physical blocks
	num_physical_blocks = int(arcpy.GetCount_management(block_shp).getOutput(0))
	#Get number of microdata blocks
	num_micro_blocks = len(df_pre.groupby(['block','ed']).groups)

	#Create {Census block:streets} dict from microdata 
	df = df_pre.groupby(['ed_block',micro_street_var]).size().to_frame('st_addresses').reset_index()
	block_num_addresses_dict = df.groupby('ed_block').sum().to_dict().values()[0]
	df['block_addresses'] = df.apply(lambda x: block_num_addresses_dict[x['ed_block']],axis=1)
	df['prop_block'] = df['st_addresses']/df['block_addresses']
	micro_blocks_dict = {group:streets[micro_street_var].values.tolist() for group, streets in df.groupby('ed_block')}
		#TO DO: Remove blocks defined by a single street (too indeterminate)???
	print("Finished building microdata block-street dictionary")

	#
	# Step 1.5: Spatial join stgrid to pblk to get {pblk_id:[FULLNAME]} and {pblk_id:[grid_id]}
	#

	start = time.time()

	field_mapSJ = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
	FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
	grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (pblk_shp, grid_shp, grid_shp)
	arcpy.SpatialJoin_analysis(target_features=pblk_shp, join_features=grid_shp, out_feature_class=pblk_grid_shp, 
		join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
		match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
	df_pblk_grid = load_shp(pblk_grid_shp.replace(".shp",".dbf"))
	
	# Group by pblk_id to create some dictionaries
	df_grouped = df_pblk_grid.groupby('pblk_id')
	# pblk_st_dict is used here as empiric census block descriptions
	pblk_st_dict = {pblk:list(set(grid_list['FULLNAME'].tolist())) for pblk, grid_list in df_grouped}
	# Exclude certain street names "City Limits"
	exclude_list = ['City Limits']
	pblk_st_dict = {k:[i for i in v if i not in exclude_list] for k,v in pblk_st_dict.items()}
	# This dictionary is used in RenumberGrid.py to match empiric house number ranges to grid segments based on block number
	pblk_grid_dict = {pblk:list(set(grid_list['grid_id'].tolist())) for pblk, grid_list in df_grouped}
	pickle.dump(pblk_grid_dict,open(pblk_grid_dict_file,'wb'))

	end = time.time()
	run_time = round(float(end-start)/60, 1)
	print("Finished overlaying physical blocks and street grid (took " + str(run_time) + " minutes)"+"\n")

	#
	# Step 2: Now use empiric block descriptions to try to label physical blocks 
	#

	#Get block numbers already labeled in Step 1 (strict criteria)
	def extract_step1_labels(fields):
		labels_step1 = []
		pblks_labeled1 = []
		for field in fields:
			with arcpy.da.SearchCursor(block_shp,['pblk_id',field]) as cursor:
				for row in cursor:
					if row[1] != ' ' and row[1] != '0' and row[1] != 0:
						labels_step1.append(row[1])
						pblks_labeled1.append(row[0])
		num_labels_step1 = len(labels_step1)
		per_micro_blocks = round(100*float(num_labels_step1)/num_micro_blocks, 1)
		print("Physical blocks labeled in Step 1: "+str(num_labels_step1)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")
		return labels_step1, [int(i) for i in pblks_labeled1], num_labels_step1

	#This step determines which ED-blocks to consider labeled based on prior numbering efforts
	fields = ['MBID','MBID2']
	labels_step1, pblks_labeled_step1, num_labeled_step1 = extract_step1_labels(fields)

	#Look for block description matches


	def check_block(temp):
		map_block, map_streets = temp
		map_streets = [x if x!=None else '' for x in map_streets]
		map_streets_no_dir = map(lambda x : re.sub('^[NSEW]+ ','',x), map_streets)
		matches = []
		for micro_block, microdata_streets in unknown_micro_blocks_dict.items():
			u = [i.decode('utf-8') for i in microdata_streets]
			num_matching_streets = len((set(map_streets)|set(map_streets_no_dir)).intersection(set(u)))
			prop_matching_map = float(num_matching_streets)/len(map_streets)
			if prop_matching_map >= thresh:
				matches.append(micro_block)	
		temp_match_dict = {}
		temp_match_dict[map_block] = matches
		return temp_match_dict

	def match_using_block_desc(pblks_labeled):
		start = time.time()
		#Ensure that physical block (1) has not been labeled already and (2) intersects streets with names
		temp_pblk_st_dict = {k:v for k,v in pblk_st_dict.items() if (int(k) not in pblks_labeled) and (len(v) > 0)}
		#Use multiprocessing to compare street lists for matching blocks
		if 'win' in sys.platform:
			pool_results=[]
			for i in temp_pblk_st_dict.items():
				pool_results.append(check_block(i))
		else:
			pool = Pool(4)
			pool_results = pool.map(check_block,temp_pblk_st_dict.items())
			pool.close()
		#Convert list of dictionaries into one dictionary, as long as there is only one microdata block guess
		temp_match_dict = {k:v[0] for d in pool_results for k,v in d.items() if len(v)==1}
		temp_pblks_labeled, temp_labels = zip(*temp_match_dict.items())
		num_matches = len(temp_match_dict)
		per_micro_blocks = round(100*float(num_matches)/num_micro_blocks, 1)
		end = time.time()
		run_time = round(float(end-start)/60, 1)
		print("Matches based on block description: "+str(num_matches)+" ("+str(per_micro_blocks)+r"% of microdata blocks)")
		print("Matching took "+str(run_time)+" minutes to complete\n")
		return temp_match_dict, list(temp_pblks_labeled), list(temp_labels), num_matches

	thresh = 1
	unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1}
	exact_match_dict, pblks_labeled_exact, labels_exact, num_exact_matches = match_using_block_desc(pblks_labeled_step1)

	thresh = 0.75
	unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1+labels_exact}
	good_match_dict, pblks_labeled_good, labels_good, num_good_matches = match_using_block_desc(pblks_labeled_step1+pblks_labeled_exact)

	num_labeled_step2 = num_exact_matches+num_good_matches
	per_micro_blocks = round(100*float(num_labeled_step2)/num_micro_blocks, 1)
	print("\n"+"Physical blocks labeled by Step 2: "+str(num_labeled_step2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")

	num_labeled_steps1and2 = num_labeled_step1+num_labeled_step2
	per_micro_blocks = round(100*float(num_labeled_steps1and2)/num_micro_blocks, 1)
	print("Physical blocks labeled by Step 1 and Step 2: "+str(num_labeled_steps1and2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")

	#Add labels 

	pblks = pblk_st_dict.keys()
	for block in pblks:
		if block not in exact_match_dict.keys():
			exact_match_dict[block] = ''
		if block not in good_match_dict.keys():
			good_match_dict[block] = ''		

	arcpy.CopyFeatures_management(block_shp, block_guess_shp)
	arcpy.AddField_management(block_guess_shp,'blockdesc','TEXT')
	arcpy.AddField_management(block_guess_shp,'blockdesc2','TEXT')

	cursor = arcpy.UpdateCursor(block_guess_shp)
	for row in cursor:
		pblk_id = row.getValue('pblk_id')
		row.setValue('blockdesc',exact_match_dict[int(pblk_id)])
		row.setValue('blockdesc2',good_match_dict[int(pblk_id)])
		cursor.updateRow(row)
	del(cursor)

#
# OCR related functions (not currently used) 
#

# Uses OCR and ED map images to fill in block numbers 
def run_ocr(city_info, paths, script_path):
	city_name, _, _ = city_info
	r_path, file_path = paths
	print("Runing Matlab script\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
	if t != 0:
		print("Error running Matlab OCR script for "+city_name+"\n")
	else:
		print("OK!\n")

# Incorporates OCR block data
def integrate_ocr(city_info, paths, script_path, file_name):
	city_name, _, _ = city_info
	r_path, file_path = paths
	print("Integrating OCR block numbering results\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/MapOCRintegration.py",file_path,city_name,file_name])
	if t != 0:
		print("Error integrating OCR block numbering results for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Functions for flagging our confidence in block number guesses
#

# Sets confidence in block number based on multpiel sources
def set_blocknum_confidence(city_info, paths, has_ocr=False):

	city_name, state_abbr, decade = city_info
	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	# Load
	block_guess_shp = geo_path + city_name + "_" + str(decade) + "_block_guess.shp"
	df = load_shp(block_guess_shp)
	relevant_vars = ['MBID','MBID2','MBID3','blockdesc','blockdesc2']
	df[relevant_vars] = df[relevant_vars].astype(str).replace('None','')

	# Reduce OCR variables to fewest possible
	if has_ocr:
		vars_to_compress = []
		df_to_compress = df[vars_to_compress]
		list_to_compress = df_to_compress.values.tolist()
		list_compressed = [list(set(i)) for i in list_to_compress]
		for i in list_compressed:
			if '' in i:
				i.remove('')
		df_compressed = pd.DataFrame.from_records(list_compressed)
		min_num_vars = len(df_compressed.columns)
		for i in range(1,min_num_vars+1):
			df['ocr%s' % (str(i))] = df_compressed[[i-1]]

	# Run confidence setting algorithm 
	for i in range(1,7):
		df['auto_bn'], df['auto_bnc'] = zip(*df.apply(lambda x: get_auto_blocknum(x,i), axis=1))

	print(100*df['auto_bnc'].value_counts(normalize=True))

	save_shp(df, block_guess_shp)


# Function to set block confidence based on which method(s) provided a block number
def get_auto_blocknum(x,conf,min_num_vars=None):

	# Confidence 1: Matt's strict (100% of people are in block)
	#				Matt's loose (criteria 2 or 3) and Chris's strict (100% of streets match) agree
	if conf == 1:
		if x['MBID'] != '':
			return [x['MBID'], conf]
		if x['MBID2'] == x['blockdesc'] and x['MBID2'] != '':
			return [x['MBID2'], conf]
		if x['MBID3'] == x['blockdesc'] and x['MBID3'] != '':
			return [x['MBID3'], conf]				
		else:
			return ['', '']

	# Confidence 2: Matt's loose and Chris's loose (75% of streets match) agree
	#
	if conf == 2:
		if x['auto_bnc'] == '':
			if x['MBID2'] == x['blockdesc2'] and x['MBID2'] != '':
				return [x['MBID2'], conf]	
			if x['MBID3'] == x['blockdesc2'] and x['MBID3'] != '':
				return [x['MBID3'], conf]	
			else:		
				return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 3: Matt's loose
	#				Chris's strict and one of Chris's OCR agree
	if conf == 3:
		if x['auto_bnc'] == '':
			if x['MBID2'] != '':
				return [x['MBID2'], conf]	
			elif x['MBID3'] != '':
				return [x['MBID3'], conf]	
			if min_num_vars != None:		
				for i in range(1,min_num_vars+1):
					if x['blockdesc'] == x['ocr%s' % (str(i))] and x['blockdesc'] != '':
						return [x['blockdesc'], conf]	
			else:
				return ['','']					
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 4: Chris's strict 
	#				Chris's loose and one of Chris's OCR agree
	if conf == 4:
		if x['auto_bnc'] == '':
			if x['blockdesc'] != '':
				return [x['blockdesc'], conf]				
			if min_num_vars != None:		
				for i in range(1,min_num_vars+1):
					if x['blockdesc2'] == x['ocr%s' % (str(i))] and x['blockdesc2'] != '':
						return [x['blockdesc2'], conf]	
			else:
				return ['','']											
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 5: Chris's loose 
	#
	if conf == 5:
		if x['auto_bnc'] == '':
			if x['blockdesc2'] != '':
				return [x['blockdesc2'], conf]	
			else:
				return ['','']							
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 6: At least two of Chris's OCR agree
	#
	if conf == 6:
		if x['auto_bnc'] == '':
			if min_num_vars != None and min_num_vars > 1:
				guess = ''
				for i in range(1,min_num_vars+1):
					for j in range(1,min_num_vars+1):
						if i != j and x['ocr%s' % (str(i))] == x['ocr%s' % (str(j))] and x['ocr%s' % (str(i))] != '':
							guess = [x['ocr%s' % (str(i))], conf]
				if guess != '':
					return [guess, conf]
				else:
					return ['','']
			else:
				return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()

	# Confidence 7: List of OCR guesses
	#
	if conf == 7:
		if x['auto_bnc'] == '' and min_num_vars != None:
			if min_num_vars > 1:
				guesses = [] 
				for i in range(1,min_num_vars+1):
					guesses.append(x['ocr%s' % (str(i))])
				guesses = list(set(guesses))
				if len(guesses) > 1:
					return [', '.join(guesses), conf]
				if len(guesses) == 1 & guesses[0] != '':
					return [guesses[0], conf]
				else:
					return ['','']
			if min_num_vars == 1:
				if x['ocr1'] != None:
					return [x['ocr1'], conf]
				else:		
					return ['','']
		else:
			return x[['auto_bn','auto_bnc']].tolist()
	else:
		return ['','']

#
# FixDirAndBlockNumsUsingMap.py
#

# Use ED map and street grid to fix microdata street directions
def fix_micro_dir_using_ed_map(city_info, paths, df_micro=None, micro_street_var='st_best_guess', grid_street_var='FULLNAME', hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Files
	grid_shp = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	ed_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_guess.shp'
	grid_ed_intersect_shp = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_ED_intersect.shp"

	# Load files
	df_grid = load_shp(grid_shp, hn_ranges)
	if type(df_micro) != pd.core.frame.DataFrame:
		df_micro = load_cleaned_microdata(city_info, dir_path)
	try:
		df_micro.rename(columns={'DIR':'dir'},inplace=True)
	except:
		pass
	df_micro[[micro_street_var,'dir']] = df_micro[[micro_street_var,'dir']].astype(str).replace('nan','')
	df_micro[micro_street_var+'_old'] = df_micro[micro_street_var]

	def get_dir(st):
		_, DIR, _, _ = standardize_street(st)
		return DIR

	df_grid.loc[:,('DIR')] = df_grid.apply(lambda x: get_dir(x[grid_street_var]), axis=1)
	save_shp(df_grid, grid_shp)

	arcpy.Intersect_analysis(in_features=[grid_shp, ed_shp], 
		out_feature_class=grid_ed_intersect_shp, 
		join_attributes="ALL")

	# Get the spatial join dbf and extract some info
	df_intersect = load_shp(grid_ed_intersect_shp, hn_ranges)
	if 'ed' in df_intersect.columns.values:
		ed_var = 'ed'
		df_dir_ed = df_intersect[['DIR',ed_var]].drop_duplicates()
		df_dir_ed = df_dir_ed[df_dir_ed[ed_var]!=0]
	elif 'ed_guess' in df_intersect.columns.values:
		ed_var = 'ed_guess'
		df_dir_ed[ed_var] = df_dir_ed[ed_var].astype(int) 
		df_dir_ed = df_intersect[['DIR',ed_var]].drop_duplicates()
		df_dir_ed = df_dir_ed[df_dir_ed[ed_var]!=0]
	elif 'aggr_ed' in df_intersect.columns.values:
		ed_var = 'aggr_ed'
		df_dir_ed = df_intersect[['DIR',ed_var]].drop_duplicates()
		df_dir_ed = df_dir_ed[df_dir_ed[ed_var]!='']
	df_dir_ed = df_dir_ed[df_dir_ed['DIR']!='']
	eds = df_dir_ed[ed_var].drop_duplicates().tolist()

	# Create dictionary of {ED:list(DIRs)}
	ed_dir_dict = {}
	ed_grouped = df_dir_ed.groupby([ed_var])
	for ed, group in ed_grouped:
		ed_dir_dict[ed] = group['DIR'].tolist()

	## I feel like this could be simplified significantly

	# Create dictionary of {street_var:list(DIRs)} and delete any that have combination of N/S and E/W
	df_name_dir = df_micro[[micro_street_var,'dir']]
	df_name_dir.loc[:,('st')], df_name_dir.loc[:,('dir')], df_name_dir.loc[:,('name')], df_name_dir.loc[:,('type')] = zip(*df_name_dir.apply(lambda x: standardize_street(x[micro_street_var]), axis=1))
	df_name_dir.loc[:,('st')] = (df_name_dir['name'] + ' ' + df_name_dir['type']).str.strip()
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

	df_micro.loc[:,('dir')], df_micro.loc[:,(micro_street_var)] = zip(*df_micro.apply(lambda x: prepend_dir(x['ed'], x[micro_street_var+'_old']), axis=1))	

	# Check how many streets had DIRs pre-pended
	df_micro['changed_Dir'] = df_micro[micro_street_var] != df_micro[micro_street_var+'_old']
	print("Number of cases with DIR prepended: "+str(df_micro['changed_Dir'].sum())+" of "+str(len(df_micro))+" ("+'{:.1%}'.format(float(df_micro['changed_Dir'].sum())/len(df_micro))+") of cases")

	return df_micro

# Use ED map and 
def fix_micro_blocks_using_ed_map(city_info, paths, df_micro=None, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Paths

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/" 

	# File names

	rand_post = str(random.randint(1,100001))
	ed_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_guess.shp'
	temp = geo_path + "temp"+rand_post+".shp"
	add_locator_contemp = geo_path + city_name + "_addloc_" + str(decade)
	resid_add_dbf = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.dbf"
	resid_add_csv = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.csv"
	address_fields_contemp="Street address; City city; State state"
	points_shp = geo_path + city_name + "_" + str(decade) + "_Points.shp"
	points_resid_shp = geo_path + city_name + "_" + str(decade) + "_ResidPoints.shp"
	resid_ed_intersect_shp = geo_path + city_name + "_" + str(decade) + "_resid_ed_intersect.shp"
	inrighted_shp = geo_path + city_name + "_" + str(decade) + "_ResidPoints_inRightED.shp"
	correct_ed_intersect_shp = geo_path + city_name + "_" + str(decade) + "_correct_ed_intersect.shp"
	ed_block_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_block_guess.shp'

	# Obtain residuals
	#arcpy.MakeFeatureLayer_management(points, "geocodelyr")
	#arcpy.SelectLayerByAttribute_management("geocodelyr", "NEW_SELECTION", """ "Status" <> 'M' """)
	#arcpy.CopyFeatures_management("geocodelyr",temp)
	df_points = load_shp(points_shp, hn_ranges)
	df = df_points[df_points['Status']!='M']
	# ERROR: LOST INDEX SOMEWHERE ALONG THE WAY
	if 'ed' in df.columns.values:
		ed_var = 'ed'
	elif 'ed_guess' in df.columns.values:
		ed_var = 'ed_guess'
	elif 'aggr_ed' in df.columns.values:
		ed_Var = 'aggr_ed'
	resid_vars = ['index',ed_var,'fullname','state','city','address']
	df_resid = df[resid_vars]
	if os.path.isfile(resid_add_csv):
		os.remove(resid_add_csv)
	df_resid.to_csv(resid_add_csv)
	if os.path.isfile(resid_add_csv.replace('.csv','.dbf')):
		os.remove(resid_add_csv.replace('.csv','.dbf'))
	arcpy.TableToTable_conversion(resid_add_csv, '/'.join(resid_add_dbf.split('/')[:-1]), resid_add_dbf.split('/')[-1])
	temp_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith("temp"+rand_post)]
	for f in temp_files:
		if os.path.isfile(f):
			os.remove(f)

	# Geocode residuals using street grid with contemporary HN ranges
	arcpy.GeocodeAddresses_geocoding(resid_add_dbf, add_locator_contemp, address_fields_contemp, points_resid_shp)

	# Intersect geocoded points with ED map
	arcpy.Intersect_analysis([ed_shp, points_resid_shp], resid_ed_intersect_shp)

	# Identify points in the correct ED
	arcpy.MakeFeatureLayer_management(resid_ed_intersect_shp, "geocodelyr1")
	if ed_var=='ed':
		sql_exp=""" 'ed' = 'ed_1' """
		arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", "[ed]==[ed_1]")
	elif ed_var=='ed_guess':
		sql_exp=""" 'ed_guess' = 'ed' """
		arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", sql_exp)
	elif ed_var=='aggr_ed':
		sql_exp=""" 'aggr_ed' = 'ed' """
		arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", sql_exp)

	arcpy.CopyFeatures_management("geocodelyr1",inrighted_shp)

	# Intersect points in the correct ED with block map
	arcpy.Intersect_analysis([ed_block_shp, inrighted_shp], correct_ed_intersect_shp)

	# Get correct block number based on block map and geocoded in correct ED
	df_correct_ed = load_shp(correct_ed_intersect_shp, hn_ranges)
	df_correct_ed['block'] = df_correct_ed['am_bn'].str.split('-').str[1:].str.join('-')
	fix_block_dict = df_correct_ed[['index','block']].set_index('index')['block'].to_dict()

	# Replace microdata block number with block map block number
	if type(df_micro) != pd.core.frame.DataFrame:
		df_micro = load_cleaned_microdata(city_info, dir_path)
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

#
# Functions for intersecting ED map with street grids and uploading to Rhea/CS1 Unix server
#

'''
def intersect_ed_stgrid(ed_year, map_type):

def upload_to_unix(file_path, file_name, target_path, user, pw):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.load_system_host_keys
	#ssh.load_host_keys('C:/Users/cgraziul')
	ssh.connect('rhea.pstc.brown.edu',username=user,password=pw)
	sftp = ssh.open_sftp()
	map_files = [x for x in os.listdir(file_path) if x.split('.')[0]==file_name]
	#Try to find directory, create it if it doesn't exist
	try:
		sftp.listdir(target_path)
	except IOError:
		sftp.mkdir(target_path)
	for item in map_files:
		file_name = '%s/%s' % (target_path, item)
		if os.path.isfile(os.path.join(file_path, item)):
			#Try to remove old file if it exist
			try: 
				sftp.remove(file_name)
			except IOError:
				pass
			sftp.put(os.path.join(file_path, item), file_name)
	sftp.close()
	ssh.close()

def upload_ed_stgrid(ed_year, map_type, user, pw):
	file_path = 
	file_name = 
	upload_to_unix(file_path, file_name, targeT_path, user, pw)

	for map_type in ['1940','Contemp']:
		ed_year = 1940
		upload_ed_stgrid(ed_year, map_type, XX, YY)
'''
