#
# All the functions for performing block numbering (includes many things)
#

import arcpy
import os
import copy
import sys
import re
import time
import pickle
import random
import fnmatch
from multiprocessing.dummy import Pool 
from _functools import partial
from operator import itemgetter
import pandas as pd
import pysal as ps
import numpy as np
import subprocess
import fuzzyset
import math
import paramiko
#import win32api, win32con
from shutil import copyfile
from microclean.STstandardize import *

#
# Helper functions
#

# Helper functions

# Function to load large Stata files
def load_large_dta(fname):

	reader = pd.read_stata(fname, iterator=True)
	df = pd.DataFrame()

	try:
		chunk = reader.get_chunk(100*1000)
		while len(chunk) > 0:
			df = df.append(chunk, ignore_index=True)
			chunk = reader.get_chunk(100*1000)
			print '.',
			sys.stdout.flush()
	except (StopIteration, KeyboardInterrupt):
		pass

	print '\nloaded {} rows\n'.format(len(df))

	# Convert objects to categories to save memory
	for col in df.columns:
		# Downcast int 
		if df[col].dtype == 'int':
			df.loc[:,col] = df[col].apply(pd.to_numeric,downcast='signed')
		# Downcast float 
		if df[col].dtype == 'float':
			df.loc[:,col] = df[col].apply(pd.to_numeric,downcast='float')
	
	return df

# Function to reads in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=False):
	dbfile = dbfile.replace('.shp','.dbf')
	db = ps.open(dbfile) #Pysal to open DBF
	d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
	#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
	pandasDF = pd.DataFrame(d) #Convert to Pandas DF
	if upper == True: #Make columns uppercase if wanted 
		pandasDF.columns = map(str.upper, db.header) 
	db.close() 
	return pandasDF

# Function to save Pandas DF as DBF file 
def save_dbf(df, shapefile, dir_path):
	os.chdir(dir_path)
	shapefile_name = shapefile
	def get_rand_part():
		rand_post = str(random.randint(1,999999999999999))
		rand_part = "temp_for_shp"+rand_post
		return rand_part
	rand_part = get_rand_part()
	for f in os.listdir('.'):
		if fnmatch.fnmatch(f, '*'+rand_part+'.*'):
			rand_part = get_rand_part()
	csv_file = rand_part + ".csv"
	df.to_csv(csv_file,index=False)
	try:
		os.remove("schema.ini")
	except:
		pass
	arcpy.TableToTable_conversion(csv_file,dir_path,rand_part+".dbf")
	os.remove(shapefile_name.replace('.shp','.dbf'))
	os.remove(csv_file)
	os.rename(rand_part+".dbf",shapefile_name.replace('.shp','.dbf'))
	#os.remove(rand_part+".dbf.xml")
	#os.remove(rand_part+".cpg")

#
# Functions for calling R scripts 
#

# Identifies EDs and can be run independently
def identify_eds(city_name, paths, decade):
	r_path, script_path, file_path = paths
	print("Identifying " + str(decade) + " EDs\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Identify 1930 EDs.R',file_path,city_name,str(decade)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying " + str(decade) + " EDs for "+city_name+"\n")
	else:
		print("OK!\n")

# Returns a list of streets for students to add
def analyzing_microdata_and_grid(city_name, state_abbr, paths, decade):
	print("Analyzing microdata and grids\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Analyzing Microdata and Grid.R',file_path,city_name,state_abbr, str(decade)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error analyzing microdata and grid for "+city_name+"\n")
	else:
		print("OK!\n")

# Adds new streets and ranges based on Steve Morse webpage that may or may not exist
def add_ranges_to_new_grid(city_name, state_abbr, file_name, paths):
	r_path, script_path, file_path = paths
	print("Adding ranges to new grid\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Add Ranges to New Grid.R',file_path,city_name,file_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error adding ranges to new grid for "+city_name+"\n")
	else:
		print("OK!\n")

# Identifies block numbers and can be run independently
def identify_blocks_geocode(city_name, paths, decade):
	r_path, script_path, file_path = paths
	print("Identifying " + str(decade) + " blocks\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Identify 1930 Blocks.R',file_path,city_name,str(decade)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying " + str(decade) + " blocks for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Functions for calling Python scripts (code/functions should get pulled into here)
#

# Uses block descriptions from microdata to fill in block numbers
def identify_blocks_microdata(city_name, state_abbr, micro_street_var, paths, decade, v=7):

	r_path, script_path, dir_path = paths

	geo_path = dir_path + "/GIS_edited/"

	block_file = geo_path + city_name + "_" + str(decade) + "_Block_Choice_Map.shp"
	pblk_file = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	stgrid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	pblk_grid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_Pblk_Grid_SJ.shp"
	out_file = geo_path + city_name + "_" + str(decade) + "_Block_Choice_Map2.shp"
	pblk_grid_dict_file = geo_path + city_name + "_pblk_grid_dict.pkl"
	pblk_st_dict_file = geo_path + city_name + "_pblk_st_dict.pkl"
	microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAuto.dta"
	microdata_file2 = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_AutoCleanedV" + str(v) + ".csv"

	print("Getting block description guesses\n")

	#
	# Step 1: Create "block descriptions" using microdata
	#

	#Load data
	start = time.time()
	
	try:
		df_pre = load_large_dta(microdata_file)
	except:
		df_pre = pd.read_csv(microdata_file2)
	df_pre = df_pre[['ed','block',street]]

	end = time.time()
	run_time = round(float(end-start)/60, 1)
	print("Finished loading microdata (took " + str(run_time) + " minutes)", 'cyan')

	#TO DO: Clean up block numbers
	df_pre = df_pre[df_pre['block'].notnull() & df_pre['ed'].notnull()]
	df_pre['ed_int'] = df_pre['ed'].astype(int)
	df_pre['ed_block'] = df_pre['ed_int'].astype(str) + '-' + df_pre['block'].astype(str)
	#del df_pre['ed']
	#del df_pre['block']

	#Get number of physical blocks
	num_physical_blocks = int(arcpy.GetCount_management(block_file).getOutput(0))
	#Get number of microdata blocks
	num_micro_blocks = len(df_pre['block'].unique())

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
	grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (pblk_file, stgrid_file, stgrid_file)
	arcpy.SpatialJoin_analysis(target_features=pblk_file, join_features=stgrid_file, out_feature_class=pblk_grid_file, 
		join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
		match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
	df_pblk_grid = dbf2DF(pblk_grid_file.replace(".shp",".dbf"))

	# Group by pblk_id to create some dictionaries
	df_grouped = df_pblk_grid.groupby('pblk_id')
	# This dictionary is used here as empiric census block descriptions
	pblk_st_dict = {pblk:list(set(grid_list['FULLNAME'].tolist())) for pblk, grid_list in df_grouped}
		#Exclude certain street names "City Limits"
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
			with arcpy.da.SearchCursor(block_file,['pblk_id',field]) as cursor:
				for row in cursor:
					if row[1] != ' ':
						labels_step1.append(row[1])
						pblks_labeled1.append(row[0])
		num_labels_step1 = len(labels_step1)
		per_micro_blocks = round(100*float(num_labels_step1)/num_micro_blocks, 1)
		print("Physical blocks labeled in Step 1: "+str(num_labels_step1)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")
		return labels_step1, pblks_labeled1, num_labels_step1

	#This step determines which ED-blocks to consider labeled based on prior numbering efforts
	fields = ['MBID','MBID2']
	labels_step1, pblks_labeled_step1, num_labeled_step1 = extract_step1_labels(fields)

	#Look for block description matches

	def check_block(temp):
		map_block, map_streets = temp
		matches = []
		for micro_block, microdata_streets in unknown_micro_blocks_dict.items():
			u = [i.decode('utf-8') for i in microdata_streets]
			num_matching_streets = len(set(map_streets).intersection(set(u)))
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

	arcpy.CopyFeatures_management(block_file,out_file)
	arcpy.AddField_management(out_file,'blockdesc','TEXT')
	arcpy.AddField_management(out_file,'blockdesc2','TEXT')

	cursor = arcpy.UpdateCursor(out_file)
	for row in cursor:
		pblk_id = row.getValue('pblk_id')
		row.setValue('blockdesc',exact_match_dict[int(pblk_id)])
		row.setValue('blockdesc2',good_match_dict[int(pblk_id)])
		cursor.updateRow(row)
	del(cursor)

# Uses OCR and ED map images to fill in block numbers (not generally used)
def run_ocr(city_name, paths):
	r_path, script_path, file_path = paths
	print("Runing Matlab script\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
	if t != 0:
		print("Error running Matlab OCR script for "+city_name+"\n")
	else:
		print("OK!\n")

# Incorporates OCR block data
def integrate_ocr(city_name, file_name, paths):
	r_path, script_path, file_path = paths
	print("Integrating OCR block numbering results\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/MapOCRintegration.py",file_path,city_name,file_name])
	if t != 0:
		print("Error integrating OCR block numbering results for "+city_name+"\n")
	else:
		print("OK!\n")

# Sets confidence in block number based on multpiel sources
def set_blocknum_confidence(city_name, paths):
	r_path, script_path, file_path = paths
	print("Setting confidence\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/SetConfidence.py",file_path,city_name])
	if t != 0:
		print("Error setting confidence for for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Create 1930 Address.R (ported to Python)
#

# This function replaces Matt's R script but produces exactly the same file
def create_addresses(city_name, state_abbr, paths, decade, v=7, df=None):
	r_path, script_path, dir_path = paths
	# Load microdata file if not passed to function
	if type(df) == 'NoneType' or df == None:
		try:
			microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAuto.dta"
			df = load_large_dta(microdata_file)
		except:
			microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_AutoCleanedV" + str(v) + ".csv"
			df = pd.read_csv(microdata_file)
	df.columns = map(str.lower, df.columns)
	# Set index variable
	df['index'] = df.index
	if decade == 1930:
		# Change name of 'block' to 'Mblk' (useful for later somehow? Matt did it)
		df.loc[:,('mblk')] = df['block']
	elif decade == 1940:
		df['mblk'] = ''
	# Choose the best available street name variable (st_best_guess includes student cleaning)
	# NOTE: When student cleaning is unavailable we should probably fill in overall_match_bool==FALSE
	#	    with street_precleanedHN, but this has not been done yet to my knowledge.
	if 'st_best_guess' in df.columns.values:
		street_var = 'st_best_guess'
	elif 'overall_match' in df.columns.values:
		street_var = 'overall_match'
	# Change '.' to blank string
	df.loc[:,'fullname'] = df[street_var]
	df.loc[df['fullname']=='.','fullname'] = ''
	# Make sure we found a street name variable
	if 'fullname' not in df.columns.values:
		print("No street name variable selected")
		raise
	
	# Select variables for file
	# Create ED-block
	if decade == 1930:
		vars_of_interest = ['index','fullname', 'ed','type','Mblk','hn','ed_block']
		df[:,('ed_int')] = df['ed'].astype(int)
		df[:,('ed_block')] = df['ed_int'].astype(str) + '-' + df['mblk'].astype(str)
		del df_add['ed_int']
	elif decade == 1940:
		vars_of_interest = ['index','fullname', 'ed','type','hn']

	df_add = df.loc[:,vars_of_interest]

	# Change missing and 0 to blank string
	df_add.loc[(np.isnan(df_add['hn']))|(df_add['hn']==0),'hn'] = '-1'
	df_add.loc[:,'hn'] = df_add['hn'].astype(int)
	df_add.loc[:,'hn'] = df_add['hn'].astype(str).str.replace('-1','')
	df_add.loc[:,'city'] = city_name
	df_add.loc[:,'state'] = state_abbr
	df_add.loc[:,'address'] = (df_add['hn'] + " " + df_add['fullname']).str.strip()
	# Save address file	
	addresses = dir_path + "/GIS_edited/" + city_name + "_" + str(decade) + "_Addresses.csv"
	df_add.to_csv(addresses, index=False)

#
# Create Blocks and Block Points.py
#

# Head script calling individual functions
def create_blocks_and_block_points(city_name, state_abbr, paths, decade, geocode_file=None):
	
	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	hn_ranges = ['MIN_LFROMA', 'MIN_RFROMA', 'MAX_LTOADD', 'MAX_RTOADD']

	different_geocode = False
	if geocode_file != None:
		different_geocode = True

	# overwrite output
	arcpy.env.overwriteOutput=True

	print("The script has started to work and is running the 'street' function")

	problem_segments = street(geo_path, city_name, state_abbr, hn_ranges, decade)
	print("The script has finished executing the 'street' function and has now started executing 'physical_blocks' function")

	physical_blocks(geo_path, city_name, decade)
	print("The script has finished executing the 'physical_blocks' function and has now started executing 'geocode' function")

	initial_geocode(geo_path, city_name, state_abbr, hn_ranges, decade)
	print("The script has finished executing the 'geocode' function and has now started excuting 'attach_pblk_id'")

	if different_geocode:
		points = geocode_file
		print("Different geocode")
	else:
		points = geo_path + city_name + "_" + str(decade) + "_Points.shp"

	attach_pblk_id(geo_path, city_name, points, decade)
	print("The script has finished executing the 'attach_pblk_id' function and the entire script is complete")

# Code to import and "fix up" the street grid (calls Amory's code below)
def street(geo_path, city_name, state_abbr, hn_ranges, decade):

	min_l, max_l, min_r, max_r = hn_ranges

	rand_post = str(random.randint(1,100001))

	# Function to save Pandas DF as DBF file 
	def save_dbf_st(df, shapefile_name, field_map = None):
		file_temp = shapefile_name.split('/')[-1]
		csv_file = geo_path + "/temp_for_dbf"+rand_post+".csv"
		df.to_csv(csv_file,index=False)
		try:
			os.remove(geo_path + "/schema.ini")
		except:
			pass

		# Add a specific field mapping for a special case
		if field_map:
			file = csv_file
			field_map = """FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
			CITY "CITY" true true false 30 Text 0 0 ,First,#,%s,CITY,-1,-1;
			STATE "STATE" true true false 30 Text 0 0 ,First,#,%s,STATE,-1,-1;
			%s "%s" true true false 10 Text 0 0 ,First,#,%s,%s,-1,-1;
			%s "%s" true true false 10 Text 0 0 ,First,#,%s,%s,-1,-1;
			%s "%s" true true false 10 Text 0 0 ,First,#,%s,%s,-1,-1;
			%s "%s" true true false 10 Text 0 0 ,First,#,%s,%s,-1,-1;
			grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (file, file, file, 
				min_l, min_l, file, min_l,
				max_l, max_l, file, max_l,
				min_r, min_r, file, min_r,
				max_r, max_r, file, max_r,				
				file)
		else:
			field_map = None

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=geo_path, 
			out_name="temp_for_shp"+rand_post+".dbf",
			field_mapping=field_map)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		os.remove(csv_file)
		os.rename(geo_path+"/temp_for_shp"+rand_post+".dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(geo_path+"/temp_for_shp"+rand_post+".dbf.xml")
		os.remove(geo_path+"/temp_for_shp"+rand_post+".cpg")

	#Create Paths to be used throughout Process
	#
	#NOTE: By defualt we are starting with 1940 cleaned grids then saving them as 19X0 grids!	
	grid = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit.shp"
	grid_orig = "S:/Projects/1940Census/DirAdd/" + city_name + state_abbr + "_1940_stgrid_diradd.shp"
	dissolve_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Dissolve.shp"
	temp = geo_path + city_name + "_temp"+rand_post+".shp"
	split_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Split.shp"
	grid_uns =  geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns.shp"
	grid_uns2 =  geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"

	#Create copy of "diradd" file to use as grid
	if not os.path.isfile(grid):
		if not os.path.isfile(grid_orig):
			print("%s%s_1940_stgrid_diradd.shp not found" % (city_name, state_abbr))
		else:
			arcpy.CopyFeatures_management(grid_orig, grid)

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

	#First Dissolve to create split_grid (no multi-part segments, split at intersections)
	arcpy.Dissolve_management(grid, split_grid, 
		multi_part="SINGLE_PART", 
		unsplit_lines="DISSOLVE_LINES")

	#Add a unique, static identifier (so ranges can be changed later)
	expression="!FID! + 1"
	arcpy.AddField_management(split_grid, "grid_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(split_grid, "grid_id", expression, "PYTHON_9.3")

	#Intersect with grid
	temp = geo_path + "temp_step"+rand_post+".shp"
	arcpy.CopyFeatures_management(grid, temp)
	arcpy.Intersect_analysis([temp, split_grid], grid)
	arcpy.DeleteFeatures_management(temp)
	#arcpy.DeleteFeatures_management(split_grid)

	#Second Dissolve St_Grid lines
	arcpy.Dissolve_management(in_features=grid, 
		out_feature_class=grid_uns, 
		dissolve_field="grid_id", 
		statistics_fields="LFROMADD MIN;LTOADD MAX;RFROMADD MIN;RTOADD MAX", 
		unsplit_lines="UNSPLIT_LINES")

	#Get the longest street name from multi-part segments
	df_grid = dbf2DF(grid)
	longest_name_dict = {}
	problem_segments = {}
	for grid_id, group in df_grid.groupby(['grid_id']):
		max_chars = group['FULLNAME'].str.len().max()
		longest_name = group.loc[group['FULLNAME'].str.len()==max_chars,'FULLNAME'].drop_duplicates().tolist()
		if len(longest_name) > 1:
			problem_segments[grid_id] = longest_name
		# Always returns first entry in longest name (a list of names equal in length to max_chars)
		longest_name_dict[grid_id] = longest_name[0]

	#Assign longest street name by grid_id (also add city and state for geolocator)
	df_grid_uns = dbf2DF(grid_uns)
	df_grid_uns.loc[:,'CITY'] = city_name
	df_grid_uns.loc[:,'STATE'] = state_abbr
	df_grid_uns.loc[:,'FULLNAME'] = df_grid_uns.apply(lambda x: longest_name_dict[x['grid_id']], axis=1)

	#Blank out the big/small numbers now that aggregation is done

	# Function to blank out big/small numbers
	def replace_nums(x):
		if x == "999999" or x == "-1":
			return ' '
		else:
			return x

	for field in hn_ranges:
		df_grid_uns[field] = df_grid_uns[field].astype(str)
		df_grid_uns[field] = df_grid_uns.apply(lambda x: replace_nums(x[field]), axis=1)

	save_dbf_st(df_grid_uns, grid_uns, field_map=True)

	#Add a unique, static identifier (so ranges can be changed later)
	arcpy.DeleteField_management(grid_uns, "grid_id")
	expression="!FID! + 1"
	arcpy.AddField_management(grid_uns, "grid_id", "LONG", 10, "", "","", "", "")
	arcpy.CalculateField_management(grid_uns, "grid_id", expression, "PYTHON_9.3")

	#Fix duplicate address ranges
	t = fix_dup_address_ranges(grid_uns,hn_ranges)
	print(t)

	return problem_segments

# Amory's code for fixing duplicate address ranges
def fix_dup_address_ranges(shp,hn_ranges,debug_flag=False):
	# Set range names
	LFROMADD, LTOADD, RFROMADD, RTOADD = hn_ranges
	# Set OBJECTID (grid_id is FID+1)
	OBJECTID = "grid_id" 
	# Calculate starting and ending coordinates and length for each line segment
	arcpy.AddGeometryAttributes_management(shp, "LENGTH_GEODESIC;LINE_START_MID_END")

	data = []

	fields = arcpy.ListFields(shp)
	field_names = [field.name for field in fields]

	for row in arcpy.SearchCursor(shp):
		data.append([row.getValue(field.name) for field in fields])

	df = pd.DataFrame(data, columns=field_names)

	grouped = df.groupby(["FULLNAME",LFROMADD,LTOADD,RFROMADD,RTOADD])
	
	df["IN_FID"] = grouped.grouper.group_info[0]

	#There is no simple way to assign _n of each group to a variable in the dataframe
	# so use Chris Graziul's dict workaround.
	foo = {}
	#create dict: keys: group IDs ; values: number of items in group
	for g, d in grouped:
		foo[g] = d[OBJECTID].count()
	df['size'] = df.apply(lambda x : foo[x["FULLNAME"],x[LFROMADD],x[LTOADD],x[RFROMADD],x[RTOADD]], axis=1)

	df = df[[OBJECTID,LFROMADD,LTOADD,RFROMADD,RTOADD,"IN_FID","LENGTH_GEO","size","START_X","END_X","START_Y","END_Y"]]

	addresses = open('new_addresses.csv', 'wt') #this is deprecated, although topo errors are still output here.
	addresses.write("fid,l_f_add,l_t_add,r_f_add,r_t_add,short_segment\n")

	df = df.sort_values('IN_FID')

	for col in df:
		df[col] = df[col].astype(str)
	DList = df.values.tolist()

	TopoErrors = []

	ind = 0

	#master list for corrected data
	Data = []

	#input data should be in format :
	#fid;l_f_add;l_t_add;r_f_add;r_t_add;in_fid;new_length;num_identical;start_x;end_x;start_y;end_y

	appInd = 0

	while ind < len(DList):
		if(appInd != ind):
			print("len of Data: %sind: %s" % (appInd,ind))
		feat_seq = DList[ind][5] # actually in_fid, as feat_seq was unreliable.
		feat_num = int(DList[ind][7]) # number of features
		feat_list = DList[ind : ind+feat_num] #list of features that comprised the original feature
		if feat_num > 1:
			##find beginning segment##
			start_segment = False
			i=0
			topology_error = False
			while start_segment == False and i<feat_num:
				start_segment = True
				start = (DList[ind+i][8]+" "+DList[ind+i][10]).strip()
				for feat in feat_list:
					end = (feat[9]+" "+feat[11]).strip()
					if end == start:
						start_segment = False
						i= i +1
						#print "found a connexion. i is now %d",i
						break
			if start_segment==False : #could not find a start segment
				#print "PANIC"
				#probably topology or parsing error; or we are dealing with a circular street segment
				#pretend that the first segment in the input order is the start segment
				i=0
			##put feat list in order of street direction##
			o_feat_list = []
			o_feat_list.append(DList[ind+i])
			order_num = 1
			end = (o_feat_list[0][9]+" "+o_feat_list[0][11]).strip()
			feat_length = float(o_feat_list[0][6])
			while order_num < feat_num:
				for j,feat in enumerate(feat_list):
					start = (feat[8]+" "+feat[10]).strip()
					if start == end:
						end = (feat[9]+" "+feat[11]).strip()
						order_num= order_num + 1
						feat_length = feat_length + float(feat[6])
						o_feat_list.append(feat)
						break
					if j==feat_num-1:
	#					print ("topological error (there is a gap)~~~~~~~~~~~~~~!!!!!!!!!!!!!!~~~~~~~~~~~~~~")
						TopoErrors.append(DList[ind+order_num])
						topology_error = True
						order_num= order_num + 1
			if topology_error==False:
				try:
					LFAdd = int(o_feat_list[0][1])
				except ValueError:
					LFAdd = 0
				try:
					LTAdd = int(o_feat_list[0][2])
				except ValueError:
					LTAdd = 0
				try:
					RFAdd = int(o_feat_list[0][3])
				except ValueError:
					RFAdd = 0
				try:
					RTAdd = int(o_feat_list[0][4])
				except ValueError:
					RTAdd = 0
				if debug_flag:
					addresses.write("feat_seq: "+str(feat_seq)+", name: "+o_feat_list[0][5]+", num segments: "+str(feat_num)+", add range: "+str(LFAdd)+"-"+str(LTAdd)+" "+str(RFAdd)+"-"+str(RTAdd)+"\n")

				RRange = (RTAdd - RFAdd)
				LRange = (LTAdd - LFAdd)
				ORange = RRange
				OLange = LRange
				RDir, LDir = 0,0 #Dir: direction addresses are going in.

				final_feat_list = []
				for feat in o_feat_list:
					if round(abs((float(feat[6])/feat_length)*LRange)) < 2 and LRange!= 0 and round(abs((float(feat[6])/feat_length)*RRange)) < 2 and RRange!= 0:
						#if feat is too short to contain even a single address (on either side) in its range...
						feat[1]=feat[2]=feat[3]=feat[4]=0
						feat_num = feat_num - 1
						feat_length = feat_length - float(feat[6])
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+",1")
						if debug_flag:
							addresses.write(" length is "+feat[6]+"/"+str(feat_length)+" which WAS too short\n")
						else:
							addresses.write("\n")
					else:
						final_feat_list.append(feat)

				o_feat_list = final_feat_list

				ShortRange = False
				if RRange!=0:
					RDir = RRange/abs(RRange)
				if LRange!=0:
					LDir = LRange/abs(LRange)
				if abs(RRange)>2*feat_num : #if address range is NOT too small in comparison to number of segments
					RRange -= 2*(feat_num-1)*RDir #account for the hidden extra 2 address range each time we change segments
				else:
					ShortRange = True
					if debug_flag:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				if abs(LRange)>2*feat_num:
					LRange -= 2*(feat_num-1)*LDir
				else:
					ShortRange = True
					if debug_flag:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				assignedLength = 0

				for j, feat in enumerate(o_feat_list):
					segmentLength = float(feat[6])
					assignedLength+=segmentLength
					tooShort = False
					if debug_flag:
						addresses.write(str(int(round(((segmentLength/feat_length)*LRange)/2)*2))+" is more than 2. RRange is "+str(RRange)+"\n")
					if j == 0:
						feat[1] = LFAdd
						feat[3] = RFAdd
					else:
						feat[1] = int(o_feat_list[j-1][2])+2*LDir
						feat[3] = int(o_feat_list[j-1][4])+2*RDir
	#				print "left range",round(((segmentLength/feat_length)*LRange)/2)*2
					if j == feat_num-1:
						feat[2] = LTAdd
						feat[4] = RTAdd
					else:
						feat[2] = feat[1] + int(round(((segmentLength/feat_length)*LRange)/2)*2)
						feat[4] = feat[3] + int(round(((segmentLength/feat_length)*RRange)/2)*2)
						if feat[2] > LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2) and LDir>0 or LDir<0 and feat[2] < LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2):
							feat[2] = LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2)
							if debug_flag:
								addresses.write("HAD TO ADJUST on LEFT\n")
						if feat[4] > RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2) and RDir>0 or RDir<0 and feat[4] < RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2):
							if debug_flag:
								addresses.write("HAD TO ADJUST on RIGHT\n")
							feat[4] = RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2)
					if RRange == 0:
						feat[3] = feat[4] = RFAdd
					if LRange == 0:
						feat[1] = feat[2] = LFAdd

					if debug_flag:
						if LDir > 0 and (feat[1] > LTAdd or feat[2] > LTAdd) or LDir < 0 and (feat[1] < LTAdd or feat[2] < LTAdd) or RDir > 0 and (feat[3] > RTAdd or feat[4] > RTAdd) or RDir < 0 and (feat[3] < RTAdd or feat[4] < RTAdd):
							addresses.write("THIS SHOULD NOT HAPPEN!\n")
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+" length is "+feat[6]+"/"+str(feat_length)+" which was NOT too short\n")
					else:
						#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
						Data.append(feat)
						appInd =appInd+1

			else : #if topo error
				for feat in feat_list:
					Data.append(feat) #add just the fid of all segments to Data if topo error
					appInd =appInd+1

		else : #if feature was not split
			feat = DList[ind]
			#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
			Data.append(feat)
			appInd =appInd+1

		ind+=feat_num

	Data.sort(key=itemgetter(0)) #sort both by OBJECTID (both are text so the sorting is weird but consistently so!)
	newShp = os.path.splitext(shp)[0]+"2.shp"
	#have to create a new FID field because Arc won't let you sort on fields of type Object ID
	arcpy.AddField_management(in_table = shp, field_name="FID_str", field_type="TEXT", field_precision="", field_scale="", field_length="", field_alias="",
		field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
	arcpy.CalculateField_management(in_table = shp, field="FID_str", expression="!"+OBJECTID+"!", expression_type="PYTHON_9.3", code_block="")
	arcpy.Sort_management(shp, newShp, [["FID_str", "ASCENDING"]])

	with arcpy.da.UpdateCursor(newShp,[LFROMADD,LTOADD,RFROMADD,RTOADD]) as cursor:
		for i,row in enumerate(cursor):
			if Data[i][1] == 0:
				row[0] = ''
			else:
				row[0] = Data[i][1]
			if Data[i][2] == 0:
				row[1] = ''
			else:
				row[1] = Data[i][2]
			if Data[i][3] == 0:
				row[2] = ''
			else:
				row[2] = Data[i][3]
			if Data[i][4] == 0:
				row [3] = ''
			else:
				row[3] = Data[i][4]
			cursor.updateRow(row)
	addresses.write("Topology Errors. Must be fixed and re-run script or re-address manually.\n")

	for err in TopoErrors:
		addresses.write(str(err[0])+"\n")
	addresses.close()

	return "\nFixed duplicate address ranges"

# Creates physical blocks shapefile 
def physical_blocks(geo_path, city_name, decade):

	pblocks = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	split_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Split.shp"

	#if int(start_from) = 1930:
	#arcpy.AddField_management(grid, 'FULLNAME', 'TEXT')
	#arcpy.CalculateField_management(grid, "FULLNAME","!Strt_Fx!", "PYTHON_9.3")

	#Create Physical Blocks# #####
	arcpy.FeatureToPolygon_management(split_grid, pblocks)
	#Add a Physical Block ID
	expression="!FID! + 1"
	arcpy.AddField_management(pblocks, "pblk_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(pblocks, "pblk_id", expression, "PYTHON_9.3")

# Performs initial geocode on contemporary grid
def initial_geocode(geo_path, city_name, state_abbr, hn_ranges, decade):

	min_l, max_l, min_r, max_r = hn_ranges

	# Files
	add_locator = geo_path + city_name + "_addloc_" + str(decade)
	addresses = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	address_fields="Street address; City city; State state"
	points = geo_path + city_name + "_" + str(decade) + "_Points.shp"
	reference_data = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp 'Primary Table'"

	# Fix addresses for use in geocoding
	arcpy.CreateFileGDB_management(geo_path,"temp.gdb")
	df_addresses_csv = pd.read_csv(addresses)
	df_addresses_dbf = df_addresses_csv.replace(np.nan,'',regex=True)
	x = np.array(np.rec.fromrecords(df_addresses_dbf.values))
	names = df_addresses_dbf.dtypes.index.tolist()
	x.dtype.names = tuple(names)
	arcpy.da.NumPyArrayToTable(x,geo_path + "temp.gdb/" + city_name + "_" + str(decade) + "_Addresses")
	arcpy.env.workspace = geo_path + "temp.gdb"

	field_map="'Feature ID' FID VISIBLE NONE; \
	'*From Left' %s VISIBLE NONE; \
	'*To Left' %s  VISIBLE NONE; \
	'*From Right' %s  VISIBLE NONE; \
	'*To Right' %s  VISIBLE NONE; \
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
	'Altname JoinID' <None> VISIBLE NONE" % (min_l, max_l, min_r, max_r)

	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith(city_name+"_addloc")]
	for f in add_loc_files:
			 if os.path.isfile(f):
				 os.remove(f)

	print("The script is executing the 'CreateAddressLocator' tool")
	#Create Address Locator
	arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", 
		in_reference_data=reference_data, 
		in_field_map=field_map, 
		out_address_locator=add_locator, 
		config_keyword="")
	print("The script has finished executing the 'CreateAddressLocator' tool and has begun executing the 'GeocodeAddress' tool")
	#Geocode Points
	arcpy.GeocodeAddresses_geocoding(in_table=city_name + "_" + str(decade) + "_Addresses", 
		address_locator=add_locator, 
		in_address_fields=address_fields, 
		out_feature_class=points)
	#Delete temporary.gdb
	arcpy.Delete_management(geo_path + "temp.gdb/" + city_name + "_" + str(decade) + "_Addresses")
	arcpy.Delete_management(geo_path + "temp.gdb")
	print("The script has finished executing the 'GeocodeAddress' tool and has begun executing the 'SpatialJoin' tool")

# Attach physical block IDs to geocoded points 
def attach_pblk_id(geo_path, city_name, points, decade):
	# Files
	pblk_points = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"
	pblocks = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	#Attach Pblk ids to points
	arcpy.SpatialJoin_analysis(points, pblocks, pblk_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
	print("The script has finished executing the 'SpatialJoin' tool")

#
# RenumberGrid.py
#

# Renumber grid using microdata
def renumber_grid(city_name, state_abbr, paths, decade, df=None, geocode=False):

	#Paths
	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	#Files
	microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAutoDirBlockFixed.dta"
	stgrid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	out_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_renumbered.shp"
	block_shp_file = geo_path + city_name + "_" + str(decade) + "_block_ED_checked.shp"
	block_dbf_file = block_shp_file.replace(".shp",".dbf")
	addresses = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	points = geo_path + city_name + "_" + str(decade) + "_Points_updated.shp"
	pblk_file = block_shp_file #Note: This is the manually edited block file
	pblk_grid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_Pblk_Grid_SJ2.shp"
	add_locator = geo_path + city_name + "_addlocOld" 

	# Load
	df_grid = dbf2DF(stgrid_file.replace(".shp",".dbf"),upper=False)
	df_block = dbf2DF(block_dbf_file,upper=False)
	if df is None:
		df_micro = load_large_dta(microdata_file)
	else:
		df_micro = df

	if 'st_best_guess' in df_micro.columns.values:
		micro_street_var = 'st_best_guess'
	else:
		micro_street_var = 'overall_match'
	try:
		block = 'block'
		vars_of_interest = ['ed','hn',micro_street_var,block]
		df_micro = df_micro[vars_of_interest]
	except:
		block = 'block_old'
		vars_of_interest = ['ed','hn',micro_street_var,block]
		df_micro = df_micro[vars_of_interest]
	df_micro = df_micro.dropna(how='any')
	df_micro['hn'] = df_micro['hn'].astype(int)

	#Create ED-block variable (standardized against block map)
	#Turn ED=0 into blank 
	df_micro['ed1'] = df_micro['ed'].astype(str).replace('0','')

	df_micro['block1'] = df_micro[block].str.replace(' ','-')
	df_micro['block1'] = df_micro['block1'].str.replace('and','-')
	df_micro['block1'] = df_micro['block1'].str.replace('.','-')
	df_micro['block1'] = df_micro['block1'].replace('-+','-',regex=True)

	df_micro['edblock'] = df_micro['ed1'] + '-' + df_micro['block1']
	df_micro['edblock'] = df_micro['edblock'].replace('^-|-$','',regex=True)
	df_micro.loc[df_micro[block]=='','edblock'] = ''
	df_micro.loc[df_micro['ed']==0,'edblock'] = ''

	def get_cray_z_scores(arr) :
		debug = False
		if not None in arr :
			inc_arr = np.unique(arr) #returns sorted array of unique values
			if(len(inc_arr)>=2) :
				if debug : print("uniques: "+str(inc_arr))
				median = np.median(inc_arr,axis=0)
				diff = np.abs(inc_arr - median)
				med_abs_deviation = np.median(diff)
				mean_abs_deviation = np.mean(diff)
				meanified_z_score = diff / (1.253314 * mean_abs_deviation)

				if med_abs_deviation == 0 :
						modified_z_score = diff / (1.253314 * mean_abs_deviation)
				else :
						modified_z_score = diff / (1.4826 * med_abs_deviation)
				if debug : print ("MedAD Zs: "+str(modified_z_score))
				if debug : print("MeanAD Zs: "+str(meanified_z_score))
				if debug : print ("Results: "+str(meanified_z_score * modified_z_score > 16))

				return dict(zip(inc_arr, meanified_z_score * modified_z_score > 16))    
		try:
			return {inc_arr[0]:False}
		except:
			pass

	# Get house number ranges for block-street combinations from microdata
	df_micro_byblkst = df_micro.groupby(['edblock',micro_street_var])
	blkst_hn_dict = {}
	bad_blkst = []
	for group, group_data in df_micro_byblkst:
		try:
			cray_dict = get_cray_z_scores(group_data['hn'])
			hn_range = [k for k,v in cray_dict.items() if not v]
			blkst_hn_dict[group] = {'min_hn':min(hn_range), 'max_hn':max(hn_range)}
		except:
			bad_blkst.append(group)

	# Get dictionaries {pblk_id:edblock} and {pblk_id:ed} 
	bn_var = 'am_bn'
	temp = df_block.loc[df_block[bn_var]!='',[bn_var,'ed','pblk_id']]
	pblk_edblock_dict = temp.set_index('pblk_id')[bn_var].to_dict()
	pblk_ed_dict = temp.set_index('pblk_id')['ed'].to_dict()

	# Intersect block map and stgrid (needs to be manual block map because dissolved pblks)
	field_mapSJ = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
	ed "ed" true true false 10 Long 0 10 ,First,#,%s,ed,-1,-1;
	FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
	grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (block_shp_file, block_shp_file, stgrid_file, stgrid_file)
	arcpy.Intersect_analysis (in_features=[block_shp_file, stgrid_file], 
		out_feature_class=pblk_grid_file, 
		join_attributes="ALL")
	# Used spatial join before, but results in fewer cases (some streets not on block boundaries?)
	#arcpy.SpatialJoin_analysis(target_features=block_shp_file, join_features=stgrid_file, out_feature_class=pblk_grid_file, 
	#	join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
	#	match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
	df_pblk_grid = dbf2DF(pblk_grid_file.replace(".shp",".dbf"),upper=False)

	# Create dictionary linking grid_id to pblk_id
	grid_pblk_dict = {}
	grouped_grid = df_pblk_grid.groupby(['grid_id'])
	for grid_id, pblk_df in grouped_grid:
		grid_pblk_dict[grid_id] = pblk_df['pblk_id'].tolist()

	# Create dictionary linking grid_id to fullname
	# OLd WORKING: grid_fullname_dict = df_pblk_grid.set_index('grid_id').to_dict()['FULLNAME']
	grid_fullname_dict = df_grid.set_index('grid_id').to_dict()['FULLNAME']

	# Create dictionary linking grid_id to list of edblocks it intersects
	grid_edblock_dict = {grid_id:[pblk_edblock_dict[int(pblk_id)] for pblk_id in pblk_id_list] for grid_id, pblk_id_list in grid_pblk_dict.items()}

	# Create dictionary linking grid_id to min/max HN and ED
	grid_hn_dict = {}
	for grid_id, edblock_list in grid_edblock_dict.items():
		try:
			min_hn = max([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['min_hn'] for i in edblock_list])
			max_hn = min([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['max_hn'] for i in edblock_list])
			eds = [i.split("-")[0] for i in edblock_list] 
			grid_hn_dict[grid_id] = {'min_hn':min_hn, 'max_hn':max_hn, 'ed':max(set(eds), key=eds.count)}
		except:
			pass

	#Create copy of st_grid to work on 
	arcpy.CopyFeatures_management(stgrid_file,out_file)

	#Add ED field
	arcpy.AddField_management(out_file, "ed", "TEXT", 5, "", "","", "", "")

	#Delete contemporary ranges and recreate HN range attributes
	arcpy.DeleteField_management(out_file, ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD'])
	arcpy.AddField_management(out_file, "MIN_LFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_LTOADD", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MIN_RFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_RTOADD", "TEXT", 5, "", "","", "", "")

	#Add HN ranges and ED based on grid_id
	cursor = arcpy.UpdateCursor(out_file)
	for row in cursor:
		grid_id = row.getValue('grid_id')
		st_name = row.getValue('FULLNAME')
		try:
			hn_range = range(grid_hn_dict[grid_id]['min_hn'],grid_hn_dict[grid_id]['max_hn']+1)
			evensList = [x for x in hn_range if x % 2 == 0]
			oddsList = [x for x in hn_range if x % 2 != 0]
			row.setValue('MIN_LFROMA', min(evensList))
			row.setValue('MAX_LTOADD', max(evensList))
			row.setValue('MIN_RFROMA', min(oddsList))
			row.setValue('MAX_RTOADD', max(oddsList))
			row.setValue('ed', int(grid_hn_dict[grid_id]['ed']))
		except:
			pass
		cursor.updateRow(row)
	del(cursor)

	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith(city_name+"_addlocOld.")]
	for f in add_loc_files:
		if os.path.isfile(f):
			os.remove(f)

	if geocode:

		#Recreate Address Locator
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
		address_fields= "Street address; City city; State state"
		arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", 
			in_reference_data=out_file, 
			in_field_map=field_map, 
			out_address_locator=add_locator, 
			config_keyword="")

		#Geocode Points
		arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points)

#
# consecutive_segments.py
#

def find_consecutive_segments(grid_shp, grid_street_var, debug_flag=False):

	fields = arcpy.ListFields(grid_shp)

	for f in fields :
		if f.type == "OID" :
			fid_var = f.name

	#This should be the new standard for segment IDs:
	fid_var = "grid_id"

	field_names = [x.name for x in fields]

	# Version of Dict_append that only accepts unique v(alues) for each k(ey)
	def Dict_append_unique(Dict, k, v) :
		if not k in Dict :
			Dict[k] = [v]
		else :
			if not v in Dict[k] :
				Dict[k].append(v)
				
	def Dict_append_flexible(Dict, k, v) :
		if not k in Dict :
			Dict[k] = v
		else :
			Dict[k] = [Dict[k]]
			Dict[k].append(v)

	#Return all unique values of field found in table
	def unique_values(table, field):
		with arcpy.da.SearchCursor(table, [field]) as search_cursor:
			return sorted({row[0] for row in search_cursor})

	#Returns just the NAME and TYPE components of the street phrase, if any#
	def remove_st_dir(st) :
		if (st == None or st == '' or st == ' ' or st == -1) or not (isinstance(st, str) or isinstance(st, unicode)) :
			return "" #.shp files do not support NULL !!!
		else :
			DIR = re.search("^[NSEW]+ ",st)
			if(DIR) :
				DIR = DIR.group(0)
				st = re.sub("^"+DIR, "",st)
				DIR = DIR.strip()
			st = st.strip()
			return st

	#function to make sure fids aren't accidentally looping through nexts
	#returns True if there is no loop. fnd = fid_next_dict
	def test_fid_loop(fnd,fid) :
		n = fid
		for i in range(0,len(fnd.keys())+1) :
			
			try :
				n = fnd[n]
			except KeyError :
				return True
			except TypeError :
				pass #BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD
			if n == fid :
				return False
		if debug_flag: print("ran out of fids?")
		return False

	#returns a tuple of lists comprising all discrete runs of consequent FIDs. fnd = fid_next_dict
	def find_fid_runs(fnd) :
		run_starts = [x for x in fnd.keys() if not x in fnd.values()]
		runs = ()
		if len(run_starts) == 0 :
			if debug_flag: print("FIDS ARE A LOOP AND WE CAN TELL FROM TRYING TO FIND RUNS!")
		for f in run_starts :
			runs += (fid_run_recurse(fnd, f),)
		return runs
	#recursion function called by find_fid_runs
	def fid_run_recurse(fnd, fid) :
		#if fid == None :
		#    return []
		try :
			next_fid = fnd[fid]
		except KeyError :
			return [fid]
		except TypeError :
			return [fid]
		else :
			return [fid]+fid_run_recurse(fnd,next_fid)

	#given a graph in the form of a dict: node -> [child_nodes]
	#return a list containing the nodes of the longest possible path
	#from a start node to an end 
	def longest_path(G) :
		keys = G.keys()
		values = []
		for v in G.values() :
			if isinstance(v,list) :
				values += v
			else :
				values.append(v)
		starts = set([x for x in keys if not x in values])
		ends = set([x for x in values if not x in keys])
		Gd = dict(G)
		#create new dict structure with entries for child vertices (v) and whether
		#current node is "discovered" (d)
		for k in Gd.keys() :
			if not isinstance(Gd[k],list) :
				Gd[k] = [Gd[k]]
			Gd[k] = {'v':Gd[k],'d':False}
		for e in ends :
			Gd[e] = {'v':[],'d':False}
		paths = []
		for s in starts :
			paths.append(depth_first_search(dict(Gd),s))
		return max(paths,key=len)
	#recursive search function called by longest_path
	def depth_first_search(G,v) :
		Gd = copy.deepcopy(G)
		#create an entirely new data structure in memory so that nodes' "discovered" 
		#values do not propagate backward to parent nodes!
		Gd[v]['d'] = True
		longest_subpath = []
		subpaths = []
		for n in Gd[v]['v'] :
			if not Gd[n]['d'] :
				subpaths.append(depth_first_search(Gd,n))
		if not subpaths == [] :
			longest_subpath = max(subpaths,key=len)
		return [v]+longest_subpath

	def fill_addr_gaps(grid_shp) :
		pass
		#Chris is working on this...

	# converts a stname -> [fid_sequence] dict into a fid -> [prev_fid, next_fid] dict
	def flatten_seq_dict(name_sequence_dict) :
		fid_prevnext_dict = {}
		for name, seq in name_sequence_dict.items() :
			for ind, fid in enumerate(seq) :
				if ind == 0 :
					prev_fid = None
				else :
					prev_fid = seq[ind-1]
				if ind == len(seq) - 1 :
					next_fid = None
				else :
					next_fid = seq[ind+1]
				fid_prevnext_dict[fid] = [prev_fid,next_fid]
		return fid_prevnext_dict

	#assumes that name_sequence_dict was created with ignore_dir = True
	def consec_to_arc(grid_shp,name_sequence_dict,exact_next_dict) :
		fid_prevnext_dict = flatten_seq_dict(name_sequence_dict)
		#try : arcpy.AddField_management (grid_shp, "flipLine", "SHORT"); except : pass
		with arcpy.da.UpdateCursor(grid_shp, [fid_var,"consecPrev","consecNext","exact_Prev",
										  "exact_Next"]) as up_cursor:
			for row in up_cursor :
				fid = row[0]
				try :
					prev_next = fid_prevnext_dict[fid]
				except KeyError :
					continue
				if debug_flag: print("row: "+str(row))
				row[1] = prev_next[0]
				row[2] = prev_next[1]
				try :
					if debug_flag: print("prev_next: "+str(prev_next))
					row[3] = exact_next_dict[prev_next[0]] == fid
				except KeyError :
					row[3] = False
				try :
					row[4] = exact_next_dict[fid] == prev_next[1]
				except KeyError :
					row[4] = False
				up_cursor.updateRow(row)

	#have to pass in a .shp
	#include_non_exact: True or False
	#logic: organize streets one stname at a time
	#       first find exactly consequent segments
	#       then, separately, decide about inexact consequent segments

	#ignore_dir determines whether streets with only differing directions are considered
	#the same street for purposes of determining consecutive-ness:
	def get_consecutive(grid_shp,include_non_exact = True,ignore_dir = True) :

		debug = True
		
		arcpy.AddGeometryAttributes_management(grid_shp, "LINE_START_MID_END")
		try :
			arcpy.AddField_management (grid_shp, "consecPrev", "TEXT")
			arcpy.AddField_management (grid_shp, "consecNext", "TEXT")
			arcpy.AddField_management (grid_shp, "exact_Prev", "SHORT")
			arcpy.AddField_management (grid_shp, "exact_Next", "SHORT")
		except :
			pass #just for debugging, as any .shp having this done will not have these fields
		fields = arcpy.ListFields(grid_shp)
		field_names = [x.name for x in fields]
		name_sequence_dict = {} #dict: st_name -> sequential list of FIDs for all segments with st_name
		name_sequence_spur_dict = {} #same format as name_sequence_dict, but comprising spurs and other segments that connect to main sequence
		#how do we account for two different groups of segs with same name when include_non_exact is False?
		exact_next_dict = {}
		if debug_flag: print("field_names"+str(field_names))
		if ignore_dir :
			arcpy.AddField_management (grid_shp, "name_type", "TEXT")
			with arcpy.da.UpdateCursor(grid_shp, [grid_street_var,"name_type"]) as up_cursor:
				for row in up_cursor :
					row[1] = remove_st_dir(row[0])
					up_cursor.updateRow(row)
			unique_names = unique_values(grid_shp,"name_type")
			name_var = "name_type"
		else :
			unique_names = unique_values(grid_shp,grid_street_var)
			name_var = grid_street_var
		
		for name in unique_names :
			fid_coord_dict = {}
			if name != " " and name != "City Limits" :
				name_grid_shp = name+"_lyr"
				name = name.replace("'","''") #replace apostrophe in name with two apostrophes (SQL-specific syntax)
				arcpy.MakeFeatureLayer_management(grid_shp,name_grid_shp,name_var+" = '"+name+"'")
				num_name_segments = int(arcpy.GetCount_management(name_grid_shp).getOutput(0))
				if debug_flag: 
					print("examining "+str(num_name_segments)+" segments named "+name)
				if num_name_segments > 1 : #if more than 1 st segment with name
					next_fid_list = []#fids that should be considered for next of another segment
					all_fid_list = []
					with arcpy.da.SearchCursor(name_grid_shp, [fid_var,'START_X', 'START_Y', 'END_X', 'END_Y']) as s_cursor :
						for row in s_cursor :
							#populate dict of fid -> coordinates_dict
							all_fid_list.append(row[0])
							next_fid_list.append(row[0])
							fid_coord_dict[row[0]] = {}
							fid_coord_dict[row[0]]['START_X'] = row[1]
							fid_coord_dict[row[0]]['START_Y'] = row[2]
							fid_coord_dict[row[0]]['END_X'] = row[3]
							fid_coord_dict[row[0]]['END_Y'] = row[4]
					with arcpy.da.UpdateCursor(name_grid_shp, [fid_var,"consecPrev","consecNext",
														   "exact_Prev","exact_Next",grid_street_var]) as up_cursor:
						next_fid_linked_list = {} #dict: fid -> fid of next segment(s)
						prev_fid_linked_list = {} #dict: fid -> fid of prev segment
						coord_diff_start = {} #keeps track of the segment that is spatially closest to cur_seg
						coord_diff_end = {}#for purposes of tracking down inexact next and prev segments
						singleton_segments = ()
						found_cyclic_loop = False
						fork_segs = [] #not used
						merge_segs = []#not used
						fid_fullname_dict = {}
						for row in up_cursor :
							cur_fid = row[0]
							cur_seg = fid_coord_dict[cur_fid]
							startx = round(cur_seg['START_X'],6) # Assuming units=decimal degrees,
							starty = round(cur_seg['START_Y'],6) #this rounds to roughly the
							endx = round(cur_seg['END_X'],6) # nearest inch.
							endy = round(cur_seg['END_Y'],6) # i.e. negligible (but necessary. Because Arc.)
							coord_diff_start[cur_fid] = []
							coord_diff_end[cur_fid] = []
							fid_fullname_dict[cur_fid] = row[5]
							found_exact_prev = False
							found_exact_next = False
							next_fid_candidates = []
							prev_fid_candidates = []
							for fid, seg in fid_coord_dict.items() :
								if not cur_fid == fid :#no segment can be the next or prev of itself...
									if round(seg['END_X'],6) == startx and round(seg['END_Y'],6) == starty : #found exact prev
										found_exact_prev = True
										prev_fid_candidates.append(fid)
									#print("cur_fid - endx: "+str(endx)+" endy:   "+str(endy)+" ("+str(fid)+")")
									#print("fid -  START_X: "+str(seg['START_X'])+" START_Y: "+str(seg['START_Y']))
									if round(seg['START_X'],6) == endx and round(seg['START_Y'],6) == endy : #found exact next
										if found_exact_next :
											### cur_fid is the last segment before a fork:
											###            \ /
											###             |  <- cur_fid
											###             ^
											if debug_flag:print(str(cur_fid)+" has multiple exact nexts!")
											fork_segs.append(cur_fid)#not used
										found_exact_next = True
										try :
											next_fid_list.remove(fid)
										except ValueError :
											### cur_fid is the last segment before a merge:
											###             ^
											###             |
											###            / \  <- cur_fid
											if debug_flag:print("an exact next is already the exact next of something else")
											merge_segs.append(fid)#not used
											
										next_fid_candidates.append(fid)
									#record distance of start and end coordinates relative to start and end of cur_seg:
									end_end_diff = math.sqrt((seg['END_X'] - endx)**2 + (seg['END_Y'] - endy)**2)
									end_start_diff = math.sqrt((seg['START_X'] - endx)**2 + (seg['START_Y'] - endy)**2)
									coord_diff_end[cur_fid].append((min(end_end_diff,end_start_diff), fid))
									start_end_diff = math.sqrt((seg['END_X'] - startx)**2 + (seg['END_Y'] - starty)**2)
									start_start_diff = math.sqrt((seg['START_X'] - startx)**2 + (seg['START_Y'] - starty)**2)
									coord_diff_start[cur_fid].append((min(start_end_diff,start_start_diff), fid))
							if not found_exact_prev and not found_exact_next :
								singleton_segments += ([cur_fid],)
							else :
								if len(prev_fid_candidates) == 1 :
									prev_fid_linked_list[cur_fid] = prev_fid_candidates[0]
								if len(prev_fid_candidates) > 1 :
									prev_fid_linked_list[cur_fid] = prev_fid_candidates
								if len(next_fid_candidates) == 1 :
									next_fid_linked_list[cur_fid] = next_fid_candidates[0]
								if len(next_fid_candidates) > 1 :
									next_fid_linked_list[cur_fid] = next_fid_candidates
							
							
						if test_fid_loop(next_fid_linked_list,fid) :
							pass
						else :
							if debug_flag: 
								print("Cyclic Loop detected.")
								print("Name of segments: "+name)
								print("FIDs of segments: "+str(all_fid_list))
							found_cyclic_loop = True
							#TODO: store this info somewhere?

						cur_longest_path = []
						
						if not found_cyclic_loop :
							if not next_fid_linked_list == {} :
								#PROBLEM:#PROBLEM:#PROBLEM: 
								#PROBLEM:#PROBLEM:#PROBLEM: test_fid_loop does not support lists in next_fid_linked_list
								#PROBLEM:#PROBLEM:#PROBLEM:
								#PROBLEM:#PROBLEM:#PROBLEM: CURRENTLY THIS IS BEING SILENCED WITH AN except TypeError!!!!
								#PROBLEM:#PROBLEM:#PROBLEM: instead, should change longest_path to detect cycles
								#PROBLEM:#PROBLEM:#PROBLEM:
								cur_longest_path = longest_path(next_fid_linked_list)
								if debug_flag:
									print("next_fid_linked_list is: "+str(next_fid_linked_list))
									print("longest path is: "+str(cur_longest_path))
									print("FIDs not in longest path: "+str([x for x in all_fid_list if not x in cur_longest_path]))

								#modify next_fid_linked_list to conform to longest_path
								for k,v in dict(next_fid_linked_list).items() :
									if k in cur_longest_path :
										if isinstance(v,list) :
											next_fid_linked_list[k] = cur_longest_path[cur_longest_path.index(k)+1]

							else :
								if debug_flag: print("no exact consecutive segments exist for "+name)

							street_is_too_messed_up = False
							for k, v in next_fid_linked_list.items() :
								if isinstance(v, list) :
									if debug_flag:
										print("There is a fork on a non-central path for the street "+name)
										print("This is not currently supported. Goodbye.")
									street_is_too_messed_up = True
									break
							if street_is_too_messed_up :
								continue

							exact_next_dict = dict(copy.deepcopy(next_fid_linked_list), **exact_next_dict)
							
							#determine if segments that do not have an exact next/prev should have an inexact next/prev:
							#start segment is somewhere in next_fid_list
							#first, break down entire sequence of street segments into contiguous runs:
							#then create a dict of possible connections (which will include end segment->start segment. we do not want this.)

							runs = find_fid_runs(next_fid_linked_list)
							runs += singleton_segments

							if debug_flag: print("runs: "+str(runs))

							#set aside runs that are spurs/forks of cur_longest_path
							#they will not be considered as candidates for inexact next/prev
							for run in tuple(runs) :
								if not run == cur_longest_path :
									longest_path_overlap = [x for x in run if x in cur_longest_path]
									if not longest_path_overlap == [] :
										temp = list(runs)
										temp.remove(run)
										runs = tuple(temp)
										for x in longest_path_overlap :
											run.remove(x)
										Dict_append_unique(name_sequence_spur_dict,name,run)
										for x in run :
											del next_fid_linked_list[x]
										if debug_flag: print("added the spur "+str(run)+" to aux dict")       

							possible_connexions = {}
							for s_run in runs :
								for e_run in runs :
									if s_run != e_run :
										Dict_append_unique(possible_connexions,e_run[-1],s_run[0])
							if debug_flag: print("possible_connexions: "+str(possible_connexions))
							#cumbersome magic to organize and sort the distances of each gap for which we want to (maybe)
							#make a connexion based on the dicts created prior:
							dist_fid_list = []
							for k in possible_connexions.keys() :
								coord_diff_start_list = []
								coord_diff_end_list = []
								for v in possible_connexions[k] :
									coord_diff_start_list.append(list(filter(lambda x: x[1]==v, coord_diff_start[k])))
									coord_diff_end_list.append(list(filter(lambda x: x[1]==v, coord_diff_end[k])))
								shortest_gap = min(sorted(coord_diff_start_list)[0],sorted(coord_diff_end_list)[0])
								if isinstance(shortest_gap,list) and len(shortest_gap) > 0:
									if debug_flag:print("shortest_gap is a list (yes, this is still happening)")
									shortest_gap = shortest_gap[0]
								elif debug_flag:print("shortest_gap is NOT a list (not happening all the time)")

								shortest_gap += (k,)
								dist_fid_list.append(shortest_gap)
							
							#deal with cycles in inexact next gaps (this only applies to two-fid cycles)
							### have to find when there is a cycle in dist_fid_list 
							### when we have a cycle, we should remove the cyclic connexion that interferes with another connexion
							
							def deal_with_dist_fid_cycles() :
								dist_fid_cycles = []
								#identify cyclic gaps in dist_fid_list
								for i in range(0,len(dist_fid_list)-1) :
									for j in range(i+1,len(dist_fid_list)) :
										if dist_fid_list[i][1]==dist_fid_list[j][2] and dist_fid_list[i][2]==dist_fid_list[j][1] :
											dist_fid_cycles.append(dist_fid_list[i])
											dist_fid_cycles.append(dist_fid_list[j])
											break
								#isolate cyclic gaps from the rest of dist_fid_list
								for i in dist_fid_cycles :
									dist_fid_list.remove(i)
								if debug_flag: print("dist_fid_cycles: "+str(dist_fid_cycles))
								for i in dist_fid_list :
									#iterate over a copy of dist_fid_cycles so we can modify the original
									for j in list(dist_fid_cycles) :
										if i[1] == j[1] and i[2] != j[2] :
											#set distance to impossibly high value for the bad gap in the cycle
											dist_fid_cycles.remove(j)
											dist_fid_cycles.append((99999,)+j[1:])
											if debug_flag: print(str(j)+" was a bad egg cuz of "+str(i))
								for j in dist_fid_cycles :
									#add values back to list
									dist_fid_list.append(j)
									
							deal_with_dist_fid_cycles()

							dist_fid_list = sorted(dist_fid_list)
												
							if debug_flag: print("now, dist_fid_list is: "+str(dist_fid_list))
							while len(dist_fid_list) > 1 :
								connexion = dist_fid_list.pop(0)
								if debug_flag:print("checking connexion "+str(connexion))
								check_for_cycles_linked_list = dict(next_fid_linked_list)
								check_for_cycles_linked_list[connexion[2]] = connexion[1]
								if test_fid_loop(check_for_cycles_linked_list,connexion[2]) :
									#only create the connection if it does not create a cyclical loop
									next_fid_linked_list[connexion[2]] = connexion[1]
							if debug_flag:
								if len(dist_fid_list) :     
									print(name +": the last connexion (which was not made) was "+str(dist_fid_list[0]))
								else :
									print(name+" had no inexact connexions")
								
							#reconstruct order of segments and store in name_sequence_dict
							start_fid = [x for x in next_fid_linked_list.keys() if not x in next_fid_linked_list.values()]
							if debug_flag:
								wtf = [x for x in next_fid_linked_list.values() if not x in next_fid_linked_list.keys()]
								print(name+": "+str(start_fid)+ " -> "+str(wtf))
								print("fid_fullname_dict: "+str(fid_fullname_dict))
							runs = find_fid_runs(next_fid_linked_list)
							if debug_flag:print("runs: "+str(runs))
							run_namefreq_dict={}
							for run in runs :
								run_namefreq_dict[tuple(run)] = {}
								for fid in run :
									fullname = fid_fullname_dict[fid]
									if not fullname in run_namefreq_dict[tuple(run)].keys() :
										run_namefreq_dict[tuple(run)][fullname] = 1
									else :
										run_namefreq_dict[tuple(run)][fullname] += 1

							for run in run_namefreq_dict.keys() :
								if debug_flag:print(str(run)+": "+str(run_namefreq_dict[run]))
								most_common_name = max(run_namefreq_dict[run],key=run_namefreq_dict[run].get)

								Dict_append_flexible(name_sequence_dict, most_common_name, list(run))
		print("Finished.")
		return name_sequence_dict,exact_next_dict

	### Unresolved Issues ###

	# Broadway :
	# --<--|--<--|--<--|-->--|-->--|-->--
	#   6     5     4     1     2     3

	name_sequence_dict, exact_next_dict = get_consecutive(grid_shp)

	return name_sequence_dict, exact_next_dict

#
# FixDirAndBlockNumsUsingMap.py
#

def fix_micro_dir_using_ed_map(city_name, state_abbr, micro_street_var, grid_street_var, paths, decade, df_micro):

	r_path, script_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Files
	grid = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	ed = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	grid_ed_intersect = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_ED_intersect.shp"

	# Load files
	df_grid = dbf2DF(grid.replace('.shp','.dbf'))
	df_micro[micro_street_var+'_old'] = df_micro[micro_street_var]

	def get_dir(st):
		_, DIR, _, _ = standardize_street(st)
		return DIR

	df_grid['DIR'] = df_grid.apply(lambda x: get_dir(x[grid_street_var]), axis=1)
	grid_path = "/".join(grid.split("/")[:-1]) + "/"
	grid_filename = grid.split("/")[-1]
	save_dbf(df_grid, grid_filename, grid_path)

	arcpy.Intersect_analysis (in_features=[grid, ed], 
		out_feature_class=grid_ed_intersect, 
		join_attributes="ALL")

	# Get the spatial join dbf and extract some info
	df_intersect = dbf2DF(grid_ed_intersect.replace('.shp','.dbf'))
	df_dir_ed = df_intersect[['DIR','ed']].drop_duplicates()
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

def fix_micro_blocks_using_ed_map(city_name, state_abbr, paths, decade, df_micro):

	# Paths

	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/" 

	# File names

	rand_post = str(random.randint(1,100001))
	ed_shp_file = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	temp = geo_path + "temp"+rand_post+".shp"
	add_locator_contemp = geo_path + city_name + "_addloc"
	resid_add_dbf = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.dbf"
	resid_add_csv = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.csv"
	address_fields_contemp="Street address; City city; State state"
	points = geo_path + city_name + "_" + str(decade) + "_Points.shp"
	points_resid = geo_path + city_name + "_" + str(decade) + "_ResidPoints.shp"
	intersect_resid_ed = geo_path + city_name + "_" + str(decade) + "_intersect_resid_ed.shp"
	inrighted = geo_path + city_name + "_" + str(decade) + "_ResidPoints_inRightED.shp"
	intersect_correct_ed = geo_path + city_name + "_" + str(decade) + "_intersect_correct_ed.shp"
	block_shp_file = geo_path + city_name + "_" + str(decade) + "_block_ED_checked.shp"

	# Obtain residuals
	arcpy.MakeFeatureLayer_management(points, "geocodelyr")
	arcpy.SelectLayerByAttribute_management("geocodelyr", "NEW_SELECTION", """ "Status" <> 'M' """)
	arcpy.CopyFeatures_management("geocodelyr",temp)
	df = dbf2DF(temp.replace('.shp','.dbf'))
	# ERROR: LOST INDEX SOMEWHERE ALONG THE WAY
	resid_vars = ['index','ed','fullname','state','city','address']
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
	arcpy.GeocodeAddresses_geocoding(resid_add_dbf, add_locator_contemp, address_fields_contemp, points_resid)

	# Intersect geocoded points with ED map
	arcpy.Intersect_analysis([ed_shp_file, points_resid], intersect_resid_ed)

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
# FixStGridNames.py
#

def fix_st_grid_names(city_spaces, state_abbr, micro_street_var, grid_street_var, paths, decade, df_micro=None, v=7):

	city_name = city_spaces.replace(' ','')

	# Paths
	r_path, script_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	# Files
	grid_uns2 =  geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	grid_uns2_backup = grid_uns2.replace('.shp','prefix.shp')
	if city_name == "StLouis":
		ed_shp = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	st_grid_ed_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_ED_intersect.shp'

	arcpy.CopyFeatures_management(grid_uns2, grid_uns2_backup)

	#
	# Step 1: Intersect street grid and ED map, return a Pandas dataframe of attribute data
	#

	#Load dataframe based on intersection of st_grid and ED map (attaches EDs to segments)

	def get_grid_ed_df(grid_shp, ed_shp, st_grid_ed_shp):

		arcpy.Intersect_analysis (in_features=[grid_shp, ed_shp], 
			out_feature_class=st_grid_ed_shp, 
			join_attributes="ALL")

		df = dbf2DF(st_grid_ed_shp.replace('.shp','.dbf'))

		return df

	df_grid_ed = get_grid_ed_df(grid_uns2, ed_shp, st_grid_ed_shp)
	df_grid_ed[grid_street_var] = df_grid_ed[grid_street_var].astype(str)

	#
	# Step 2: Load microdata
	#

	# Load microdata
	if type(df_micro) == 'NoneType':
		try:
			microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAuto.dta"
			df_micro = load_large_dta(microdata_file)
		except:
			microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_AutoCleanedV" + str(v) + ".csv"
			df_micro = pd.read_csv(microdata_file)

	# Convert to string
	df_micro[micro_street_var] = df_micro[micro_street_var].astype(str)

	# Get list of all streets
	micro_all_streets = df_micro[micro_street_var].drop_duplicates().tolist()

	# Create ED-street dictionary for fuzzy matching
	micro_ed_st_dict = {str(ed):group[micro_street_var].drop_duplicates().tolist() for ed, group in df_micro.groupby(['ed'])}

	#
	# Step 3: Load Steve Morse data 
	#

	# Function to load Steve Morse dictionary (same as STclean.py)
	def load_steve_morse(city, state, decade):

		#NOTE: This dictionary must be built independently of this script
		sm_st_ed_dict_file = pickle.load(open('/'.join(dir_path.split('/')[:-1])+'/sm_st_ed_dict%s.pickle' % (str(decade)), 'rb'))
		sm_st_ed_dict_nested = sm_st_ed_dict_file[(city, '%s' % (state.lower()))]

		#Flatten dictionary
		temp = {k:v for d in [v for k, v in sm_st_ed_dict_nested.items()] for k, v in d.items()}

		#Capture all Steve Morse streets in one list
		sm_all_streets = temp.keys()

		#
		# Build a Steve Morse (sm) ED-to-Street (ed_st) dictionary (dict)
		#

		sm_ed_st_dict = {}
		#Initialize a list of street names without an ED in Steve Morse
		sm_ed_st_dict[''] = []
		for st, eds in temp.items():
			#If street name has no associated EDs (i.e. street name not found in Steve Morse) 
			#then add to dictionary entry for no ED
			if eds is None:
				sm_ed_st_dict[''].append(st)
			else:
				#For every ED associated with a street name...
				for ed in eds:
					#Initalize an empty list if ED has no list of street names yet
					sm_ed_st_dict[ed] = sm_ed_st_dict.setdefault(ed, [])
					#Add street name to the list of streets
					sm_ed_st_dict[ed].append(st)

		return sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict

	sm_all_streets, _, sm_ed_st_dict = load_steve_morse(city_spaces, state_abbr, decade)

	#
	# Step 4: Perform exact matching
	#

	#Initialize the current match variable
	df_grid_ed['current_match'] = ''
	df_grid_ed['current_match_bool'] = False

	#Function to update current best match (starts with either exact_match or '')
	def update_current_match(current_match, current_match_bool, new_match, new_match_bool, fullname=None):
		if ~current_match_bool and new_match_bool:
			if fullname == None:
				return new_match, True
			# Check if it's just an issue of missing DIR in either case
			else:
				_, DIR_old, NAME_old, TYPE_old = standardize_street(fullname)
				_, DIR_new, NAME_new, TYPE_new = standardize_street(new_match)
				if NAME_old == NAME_new:
					# Same NAME, different TYPE, same DIR
					if (TYPE_old != TYPE_new) & (DIR_old == DIR_new):
						new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_new).strip()
					# Same NAME, same TYPE, different DIR
					if (TYPE_old == TYPE_new) & (DIR_old != DIR_new):
						if DIR_old == '':
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
						if DIR_new == '':
							new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_old).strip()
						else:
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
					# Same NAME, different TYPE, different DIR
					if (TYPE_old != TYPE_new) & (DIR_old != DIR_new):
						if DIR_old == '':
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_new).strip()
						if DIR_new == '':
							new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_new).strip()
						else:
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
				# No conditional for different NAME, assume new_match is correct
				return new_match, True
			return new_match, True
		else:
			return current_match, current_match_bool

	#Function to do exact matching against Steve Morse street-ED lists (altered from STclean.py)
	def find_exact_matches(df, street, all_streets, basic_info, source):

		num_records, num_streets = basic_info

		exact_match = 'exact_match_' + source
		exact_bool = 'exact_match_bool_' + source

		# Check for exact matches, return True if exact match
		df[exact_match] = ''
		df[exact_bool] = df[street].apply(lambda s: s in all_streets)
		df.loc[df[exact_bool], exact_match] = df[street]
		# Update current match variables
		df['current_match'], df['current_match_bool'] = zip(*df.apply(lambda x: update_current_match(x['current_match'], x['current_match_bool'], x[exact_match], x[exact_bool]),axis=1))

		num_exact_matches = np.sum(df['current_match_bool'])
		num_noexact_matches =  num_records - num_exact_matches
		prop_exact_matches = float(num_exact_matches)/float(num_records)
		print("Cases with exact matches ("+source+"): "+str(num_exact_matches)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches, 1))+"%)")

		# Keep track of unique streets that do and do not have exact matches 
		df_exact_matches = df[df['current_match_bool']]
		df_noexact_matches = df[~df['current_match_bool']]

		num_streets_exact = len(df_exact_matches.groupby([street]).count())
		num_streets_noexact = len(df_noexact_matches.groupby([street]).count())
		while num_streets_exact + num_streets_noexact != num_streets:
			print("Error in number of streets")
			break
		prop_exact_streets = float(num_streets_exact)/float(num_streets)
		print("Streets with exact matches ("+source+"): "+str(num_streets_exact)+" of "+str(num_streets)+" streets ("+str(round(100*prop_exact_streets, 1))+"%)\n")

		# Compile info for later use
		exact_info = [num_exact_matches, num_noexact_matches, num_streets_exact, num_streets_noexact]

		return df, exact_info

	num_records = len(df_grid_ed)
	num_streets = len(df_grid_ed.groupby([grid_street_var]))
	basic_info = [num_records, num_streets]

	df_grid_ed, exact_info_micro = find_exact_matches(df=df_grid_ed, 
		street=grid_street_var, 
		all_streets=micro_all_streets, 
		basic_info=basic_info, 
		source="micro")

	#
	# Step 5: Perform fuzzy matching
	#

	#Function to do fuzzy matching using multiple sources
	def find_fuzzy_matches(df, city, street, all_streets, ed_st_dict, source):

		#Fuzzy matching algorithm
		def fuzzy_match_function(street, ed, ed_st_dict, all_streets_fuzzyset, check_too_similar=False):

			nomatch = ['', '', False]
			ed = str(ed)

			#Return null if street is blank
			if street == '':
				return nomatch
			#Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
			try:
				ed_streets = ed_st_dict[ed]
				ed_streets_fuzzyset = fuzzyset.FuzzySet(ed_streets)
			except:
			#	print("Problem ED:" + str(ed))
				return nomatch

			#Step 1: Find best match among streets associated with microdata ED
			try:
				best_match_ed = ed_streets_fuzzyset[street][0]
			except:
				return nomatch

			#Step 2: Find best match among all streets
			try:
				best_match_all = all_streets_fuzzyset[street][0]
			except:
				return nomatch    
			#Step 3: If both best matches are the same, return as best match

			if (best_match_ed[1] == best_match_all[1]) & (best_match_ed[0] >= 0.5):
				#Check how many other streets in ED differ by one character
				if check_too_similar:
					too_similar = sum([diff_by_one_char(st, best_match_ed[1]) for st in sm_ed_streets])
					if too_similar == 0:
						return [best_match_ed[1], best_match_ed[0], True]
					else:
						return nomatch
				else: 
					return [best_match_ed[1], best_match_ed[0], True]
			#Step 4: If both are not the same, return one with the higher score (to help manual cleaning)
			else:
				if best_match_all[0] < best_match_ed[0]:
					return [best_match_ed[1], best_match_ed[0], False]
				else:
					return [best_match_all[1], best_match_all[0], False]

		#Helper function (necessary since dictionary built only for cases without validated exact matches)
		def get_fuzzy_match(exact_match, fuzzy_match_dict, street, ed):
			#Only look at cases without validated exact match
			if not (exact_match):
				#Need to make sure "Unnamed" street doesn't get fuzzy matched
				if 'Unnamed' in street:
					return ['', '', False]
				#Get fuzzy match    
				else:
					return fuzzy_match_dict[street, ed]
			#Return null if exact validated match
			else:
				return ['', '', False]

		#Set var names
		fuzzy_match = 'fuzzy_match_'+source 
		fuzzy_bool = 'fuzzy_match_bool_'+source
		fuzzy_score = 'fuzzy_match_score_'+source

		#Create all street fuzzyset only once
		all_streets_fuzzyset = fuzzyset.FuzzySet(all_streets)

		#Create dictionary based on Street-ED pairs for faster lookup using helper function
		df_no_exact_match = df[~df['current_match_bool']]
		df_grouped = df_no_exact_match.groupby([street, 'ed'])
		fuzzy_match_dict = {}
		for st_ed, _ in df_grouped:
			fuzzy_match_dict[st_ed] = fuzzy_match_function(st_ed[0], st_ed[1], ed_st_dict, all_streets_fuzzyset)

		#Compute current number of residuals
		num_records = len(df)
		num_current_residual_cases = num_records - len(df[df['current_match_bool']])
		#Get fuzzy matches 
		df[fuzzy_match], df[fuzzy_score], df[fuzzy_bool] = zip(*df.apply(lambda x: get_fuzzy_match(x['current_match_bool'], fuzzy_match_dict, x[street], x['ed']), axis=1))
		#Update current match 
		df['current_match'], df['current_match_bool'] = zip(*df.apply(lambda x: update_current_match(x['current_match'], x['current_match_bool'], x[fuzzy_match], x[fuzzy_bool], x[street]),axis=1))

		#Generate dashboard information
		num_fuzzy_matches = np.sum(df[fuzzy_bool])
		prop_fuzzy_matches = float(num_fuzzy_matches)/num_records
		fuzzy_info = [num_fuzzy_matches]

		print("Fuzzy matches (using "+source+"): "+str(num_fuzzy_matches)+" of "+str(num_current_residual_cases)+" unmatched cases ("+str(round(100*float(num_fuzzy_matches)/float(num_current_residual_cases), 1))+"%)")

		return df, fuzzy_info

	df_grid_ed, fuzzy_info_micro = find_fuzzy_matches(df=df_grid_ed, 
		city=city_name, 
		street=grid_street_var, 
		all_streets=micro_all_streets, 
		ed_st_dict=micro_ed_st_dict, 
		source="micro")

	df_grid_ed, fuzzy_info_sm = find_fuzzy_matches(df=df_grid_ed, 
		city=city_name, 
		street=grid_street_var, 
		all_streets=sm_all_streets, 
		ed_st_dict=sm_ed_st_dict, 
		source="sm")

	df_grid_ed.loc[:,('fuzzy_match_bool')] = df_grid_ed['fuzzy_match_bool_sm'] | df_grid_ed['fuzzy_match_bool_micro']
	total_fuzzy_matches = df_grid_ed['fuzzy_match_bool'].sum()
	print("Total fuzzy matched: " + str(total_fuzzy_matches) + " of " + str(len(df_grid_ed[~df_grid_ed['exact_match_bool_micro']])) + " (" + '{:.1%}'.format(float(total_fuzzy_matches)/len(df_grid_ed[~df_grid_ed['exact_match_bool_micro']])) + ") ED-segment combinations without an exact match\n")

	total_matches = df_grid_ed['current_match_bool'].sum()
	print("Total matched: " + str(total_matches) + " of " + str(num_records) + " (" + '{:.1%}'.format(float(total_matches)/len(df_grid_ed)) + ") ED-segment combinations")

	#
	# Step 6: Create dictionary for fixing street names
	#

	df_grouped = df_grid_ed.groupby([grid_street_var, 'ed'])
	fullname_ed_st_dict = {}
	more_than_one = 0
	for fullname_ed, group in df_grouped:
		if group['current_match_bool'].any():
			no_match = False
			st = group['current_match'].drop_duplicates().tolist()[0]
		else:
			no_match = True
			st = group[grid_street_var].drop_duplicates().tolist()[0]
		fullname_ed_st_dict[fullname_ed] = {st:zip(group['grid_id'].tolist(),[no_match]*len(group))}
	grid_id_st_dict = {grid_id:v.keys()[0] for k,v in fullname_ed_st_dict.items() for grid_id in v.values()[0]}
	grid_id_st_dict = {k[0]:[v,k[1]] for k,v in grid_id_st_dict.items()}

	#
	# Step 7: Fix street names and save
	#

	df_uns2 = dbf2DF(grid_uns2)
	df_uns2[grid_street_var+'_old'] = df_uns2[grid_street_var]

	# Need to do this because missing grid_id numbers in grid_id_st_dict (which is bad)
	def fix_fullname(grid_id, FULLNAME):
		try:
			new_FULLNAME, nomatch = grid_id_st_dict[grid_id]
			if FULLNAME == new_FULLNAME:
				return [new_FULLNAME, nomatch]
			else:
				return [new_FULLNAME, nomatch]	
		except:
			return [FULLNAME, True]

	df_uns2[grid_street_var], df_uns2['NoMatch'] = zip(*df_uns2.apply(lambda x: fix_fullname(x['grid_id'],x['FULLNAME']), axis=1))

	# Fill in with old name if no match and switch name change to reflect
	df_uns2.loc[df_uns2['NoMatch'], grid_street_var] = df_uns2[grid_street_var+'_old']
	# Count number of changes
	df_uns2.loc[:,('NameChng')] = df_uns2[grid_street_var+'_old'] != df_uns2[grid_street_var]

	print("Number of street names changed: "+str(df_uns2['NameChng'].sum())+" of "+str(len(df_uns2))+" ("+'{:.1%}'.format(float(df_uns2['NameChng'].sum())/len(df_uns2))+") of cases")

	# Function to save Pandas DF as DBF file 
	def save_dbf_st(df, shapefile_name, field_map = False):
		file_temp = shapefile_name.split('/')[-1]
		rand_post = str(random.randint(1,100001))
		csv_file = geo_path + "/temp_for_dbf"+rand_post+".csv"
		df.to_csv(csv_file,index=False)
		try:
			os.remove(geo_path + "/schema.ini")
		except:
			pass

		# Add a specific field mapping for a special case
		if field_map:
			file = csv_file
			field_map = """FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
			FULLNAME_old "FULLNAME_old" true true false 80 Text 0 0 ,First,#,%s,FULLNAME_old,-1,-1;
			CITY "CITY" true true false 30 Text 0 0 ,First,#,%s,CITY,-1,-1;
			STATE "STATE" true true false 30 Text 0 0 ,First,#,%s,STATE,-1,-1;
			MIN_LFROMA "MIN_LFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_LFROMA,-1,-1;
			MAX_LTOADD "MAX_LTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_LTOADD,-1,-1;
			MIN_RFROMA "MIN_RFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_RFROMA,-1,-1;
			MAX_RTOADD "MAX_RTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_RTOADD,-1,-1;
			grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1;
			NoMatch "NoMatch" true true false 5 Text 0 0 ,First,#,%s,NoMatch,-1,-1;
			NameChng "NameChng" true true false 5 Text 0 0 ,First,#,%s,NameChng,-1,-1""" % (file, file, file, file, file, file, file, file, file, file, file)
		else:
			field_map = None

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=geo_path, 
			out_name="temp_for_shp"+rand_post+".dbf",
			field_mapping=field_map)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		os.remove(csv_file)
		os.rename(geo_path+"/temp_for_shp"+rand_post+".dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(geo_path+"/temp_for_shp"+rand_post+".dbf.xml")
		os.remove(geo_path+"/temp_for_shp"+rand_post+".cpg")

	save_dbf_st(df_uns2, grid_uns2, field_map=True)

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