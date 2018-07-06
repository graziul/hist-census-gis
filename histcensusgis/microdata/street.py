#
#	Name: 		STclean.py
#	Authors: 	Chris Graziul
#
#	Input:		file_name - File name of city file, saved in Stata 13 (or below) format
#	Output:		<file_name>_autocleaned.csv - City file with addresses cleaned 
#
#	Purpose:	This is the master script for automatically cleaning addresses before
#				manually cleaning the file using Ancestry images. Large functions will
#				eventually become separate scripts that will be further refined and
#				called from this script.
#

#   To do list: 1. Identify/flag institutions
#               2. Fix blank street names (naive)

import codecs
import sys
import re
import time
import math
import urllib
import dbf
import time
import math
import pickle
import fuzzyset
import geopandas as gpd
import pandas as pd
import numpy as np
from histcensusgis.microdata.hn import *
from histcensusgis.text.standardize import *
from histcensusgis.text.stevemorse import *
from histcensusgis.s4utils.IOutils import *

#
# Step 1: Load city
#

def load_city(city_info, file_path):

	city, state, year = city_info
	city = city.replace(' ','')

	start = time.time()

	if city == "StatenIsland":
		c = "Richmond"
	else:
		c = city

	# Try to load file, return error if can't load or file has no cases
	try:
		file_name = c + state.upper()
		df = pd.read_stata(file_path + '/%s/%s.dta' % (str(year), file_name), convert_categoricals=False)
	except:
		print('Error loading %s raw data' % (city))

	if len(df) == 0:
		print('Error loading %s raw data' % (city))  

	end = time.time()
	load_time = round(float(end-start)/60, 1)

	num_records = len(df)
	print('Loading data for %s took %s' % (city, load_time))

	df = rename_variables(df, year)

	# Remove duplicates
	try:
		df = remove_duplicates(df)
	except:
		print("Remove duplicates failed")

	# Sort by image_id and line_num (important for HN) 
	try: 
		df = df.sort_values(['image_id', 'line_num'])
		df.index = range(0, len(df))
	except:
		print('Not sorted, manuscript info is missing')

	return df, load_time

def rename_variables(df, decade) :
	decade = int(decade)
	print("\nStandardizing variable names\n")
	# Load renaming information from .csv
	var_names_ref = csv.reader(open("/home/s4-data/LatestCities/VariableRecodes.csv","rb"))
	columns = var_names_ref.next()
	for row in var_names_ref :
		std_name = row[0]
		name_to_change = None
		# Some decades are missing variables, so skip if missing
		try:
			for ind, name in enumerate(row) :
				name = name.strip()
				if name == "NONE" or name == "" :
					continue
				# if the correct decade is found in csv column label, and the corresponding var name is in df...
				if re.search(str(decade),columns[ind]) and name in df.columns :
					#if more than one contradictory var in df, throw assertion error
					if name_to_change :
						print("Two versions of " + std_name + " found: " + name_to_change + " and " + name)
						continue
						#assert(name+" and "+name_to_change+" both found in microdata; resolve" == False)
					name_to_change = name
				#if columns[ind] == "NOTES":
				#	print(std_name + ": " + name)
		except:
			continue
		if name_to_change != None:		
			df[std_name] = df[name_to_change]
	# Clean up raw variables a bit
	df['street_raw'] = df['street_raw'].astype(str)
	def remove_dash(ed):
		if '-' in ed:
			return ed.split('-')[1]
		else:
			return ed
	if decade != 1940:
		df['ed'] = df['ed'].astype(str)
		df['ed'] = df['ed'].str.split('.').str[0]
		df['ed'] = df['ed'].str.lstrip('0')
	df['ed'] = df['ed'].apply(lambda x: remove_dash(x))
	df['hn'], df['hn_flag'] = zip(*df['hn_raw'].map(standardize_hn))
	df['hn'] = df['hn'].apply(make_int)
	return df

'''
def rename_variables(df, year):

	year = int(year)

	# Street
	def pick_best_raw_street(st1, st2, st_match):
		if st_match: 
			return st1  
		else:
			if st1 == '' or st1 == None:
				return st2
			if st2 == '' or st2 == None:
				return st1
			else:
				return ''

	if year == 1940:
		# New 1940 data (Summer 2016)
		df['street_raw'] = df['street']		
		# Old 1940 data
		#df['street_raw'] = df['indexed_street']
	if year == 1930:
		df['street_raw'] = df['self_residence_place_streetaddre'].str.lower()
	if year == 1920:
		df['street_raw'] = df['indexed_street']
	if year == 1910:
		df['street_raw'] = df['Street']
	df['street_raw'] = df['street_raw'].astype(str)

	# ED
	if year == 1940:
		# New 1940 data (Summer 2016)
		try:
			df['ed'] = df['derived_enumdist']
		except:
			df['ed'] = df['us1940b_0083']
		# Old 1940 data
		#df['ed'] = df['indexed_enumeration_district']
	if year == 1930:
		df['ed'] = df['indexed_enumeration_district']
	if year == 1920:
		df['ed'] = df['general_enumeration_district']
	if year == 1910:
		df['ed'] = df['EnumerationDistrict']

		#Strip leading zeroes from EDs
	if year != 1940:
		df['ed'] = df['ed'].astype(str)
		df['ed'] = df['ed'].str.split('.').str[0]
		df['ed'] = df['ed'].str.lstrip('0')

	# Some years/cities have ED as a combination of [city code]-[ED number]
	def remove_dash(ed):
		if '-' in ed:
			return ed.split('-')[1]
		else:
			return ed
	df['ed'] = df['ed'].apply(lambda x: remove_dash(x))

	# House number
	def pick_best_raw_hn(hn1, hn2, hn_match):
		if hn_match: 
			return hn1  
		else:
			if hn1 == '' or hn1 == None:
				return hn2
			if hn2 == '' or hn2 == None:
				return hn1
			else:
				return ''

	if year == 1940:
		# New 1940 data (Summer 2016)
		try:
			df['hn_raw'] = df['housenum']
		except:
			df['hn_raw'] = df['us1940b_0078']
		# Old 1940 data
		#df['hn_raw'] = df['general_house_number']
	if year == 1930:
		df['hn_raw'] = df['general_house_number_in_cities_o']
	if year == 1920:
		df['hn_raw'] = df['general_housenumber']
	if year == 1910:
		df['hn_raw'] = df['HouseNumber']    

	df['hn'], df['hn_flag'] = zip(*df['hn_raw'].map(standardize_hn))
	df['hn'] = df['hn'].apply(make_int)  
   
	# Image ID
	if year==1940:
		# New 1940 data (Summer 2016)
		df['image_id'] = None
		# Old 1940 data
		#df['image_id'] = df['stableurl']
	if year==1930:
		df['image_id'] = df['imageid']

	# Line number
	if year==1940:
		df['line_num'] = df['linep']
	if year==1930:
		df['line_num'] = df['general_line_number'].apply(make_int)

	# Dwelling number
	if year==1940:
		df['dn'] = None    
	if year==1930:
		df['dn'] = df['general_dwelling_number']

	# Family ID
	if year==1940:
		df['fam_id'] = None
	if year==1930:
		df['fam_id'] = df['general_family_number']

	# Block ID
	if year==1930:
		df['block'] = df['general_block']

	# Institution (name)
	if year==1940:
		# New 1940 data (Summer 2016)
		df['institution'] = None
		# Old 1940 data
		#df['institution'] = df['general_institution']
	if year==1930:
		df['institution'] = df['general_institution']

	# Rel ID
	if year==1940:
		df['rel_id'] = None
	if year==1930:
		df['rel_id'] = df['general_RelID']

	# Household ID
	if year==1940:
		# New 1940 data (Summer 2016)
		df['hhid'] = df['serial']		
		# Old 1940 data
		#df['hhid_raw'] = df['hhid']
		#df['hhid'] = df['hhid_numeric']
	if year==1930:
		df['hhid'] = df['general_HOUSEHOLD_ID']

	# PID
	if year==1940:
		df['pid'] = df['histid']
	if year==1930:
		df['pid'] = df['pid']

	# Name
	if year==1940:
		# New 1940 data (Summer 2016)
		df['name_last'] = df['namelast']
		df['name_first'] = df['namefrst']
	if year==1930:
		df['name_last'] = df['self_empty_name_surname']
		df['name_first'] = df['self_empty_name_given']

	return df
'''

def remove_duplicates(df):

	try: 
		t = df['name_last']
	except:
		return df

	def removekey(d, key):
		r = dict(d)
		del r[key]
		return r

	def unique_sequences(seq): 
	   # order preserving
	   noDupes = []
	   [noDupes.append(i) for i in seq if not noDupes.count(i)]
	   return noDupes

	def num_blank(x):
		return sum(x == '')

	start = time.time()

	# Remove cases if line_num, street_raw, name_last, and name_first are all blank
	len1 = len(df)
	df = df[~(df['line_num'].isnull() & (df['street_raw'] == '') & (df['name_last'] == '') & (df['name_first'] == ''))]
	len2 = len(df)
	print('%s line number blanks removed' % (str(len1-len2)))

	# Remove if pages are duplicates (using sequences of age/gender)
	if ~df['image_id'].isnull().all():
		image_id = df[['image_id', 'self_residence_info_age', 'self_empty_info_gender']]
		image_id_chunks = image_id.groupby('image_id')
		image_id_chunks_dict = {name:np.array(group[['self_residence_info_age', 'self_empty_info_gender']].values).tolist() for name, group in image_id_chunks}
		repeat = {k:v for k, v in image_id_chunks_dict.items() if v in removekey(image_id_chunks_dict, k).values() and len(v) > 2}

		# Identify and remove image_id where all age/gender values are blank ('')
		blank = []
		for k, v in repeat.items():
			if set([i for s in v for i in s]) == {''}:
				blank.append(k)
				repeat = removekey(repeat, k)

		# Identify unique sequences of age/gender that are repeated
		sequence_list = unique_sequences(repeat.values())

		# Create list of image_id sharing the same age/gender sequence 
		repeat_list = []
		df_list = []
		for i in range(len(sequence_list)):
			repeat_list.append([k for k, v in repeat.items() if v == sequence_list[i]])
			df_list.append(df[df['image_id'].isin(repeat_list[i])])

		# Pick the page with the fewest blanks in the data
		drop_imageids = []
		for df_temp in df_list:
			image_ids = np.unique(df_temp['image_id'])
			blanks_dict = {}
			for image in image_ids:
				blanks_dict[image] = df_temp[df_temp['image_id']==image].apply(num_blank).sum()
			min_blanks = min(blanks_dict.values())
			max_blanks = max(blanks_dict.values())
			if min_blanks == max_blanks:
				drop_imageids.append(blanks_dict.keys()[1:])
			else:
				#Have to make sure only one image_id is saved since multiple may have max_blanks
				temp = [k for k, v in blanks_dict.items() if v != max_blanks]
				if temp is list:
					temp = temp[0]
				drop_imageids.append(temp)
		drop_imageids = [i for s in drop_imageids for i in s]

		len1 = len(df)
		df = df[~df['image_id'].isin(drop_imageids)]
		len2 = len(df)
		print('%s cases removed due to duplicate pages\n' % (str(len1-len2)))

	end = time.time()
	search_time = round(float(end-start)/60, 1)
	print('Searching for duplicates took %s minutes\n' % (search_time))

	return df

#
# Step 2a: Properly format street names and get Steve Morse street-ed information
#

# Three functions are used withing the preclean_street() function

def create_cleaning_street_dict(df, var):
	temp = df[var].drop_duplicates().apply(standardize_street)
	temp.index = df[var].drop_duplicates()
	cleaning_dict = temp.to_dict()
	return cleaning_dict

def replace_singleton_names_w_st(st, NAME, TYPE):
	try:
		if num_NAME_versions[NAME] == 1 & TYPE == '':
			TYPE = "St"
			st = st + " St"
		return st, TYPE    
	except:
		return st, TYPE

def try_to_find_dir(st, DIR, ed):
	#If st has DIR then do nothing 
	if len(DIR) > 0:
		return st, False, False
	#Get streets in same ED
	try:
		streets = sm_ed_st_dict[ed]
	except:
		return st, True, False
	#See if exact street name is in that ED
	exact = st in streets
	#See if street name contained in any other streets
	contains = [i for i in streets if st in i]
	#If exact street name is not in ED and only one street in 
	if not exact and len(contains) == 1:
		has_DIR = re.search(r'^([Nn]|[Ss]|[Ee]|[Ww])[\s]?([Nn]|[Ss]|[Ee]|[Ww])?[\s]', contains[0])
		if has_DIR:
			return contains[0], False, True
		else:
			return st, False, False
	else:
		#POSSIBLE: Add something to catch when only some cases are missing DIR (based on street-ED)?
		return st, True, False

# This is the higher level precleaning function (with SIS flag)

def preclean_street(df, city_info, file_path):

	city_name, state_abbr, decade = city_info 
	city_info = [city_name.replace(' ',''), state_abbr, decade]

	start = time.time()

	#Create dictionary for (and run precleaning on) unique street names
	cleaning_dict = create_cleaning_street_dict(df, 'street_raw')
	
	#Use dictionary create st (cleaned street), DIR (direction), NAME (street name), and TYPE (street type)
	df['street_precleaned'], df['DIR'], df['NAME'] ,df['TYPE'] = zip(*df['street_raw'].apply(lambda s: cleaning_dict[s]))

	#Loading Steve Morse dicitonary
	sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(city_info)

	# If we found Steve Morse data for that decade, proceed as usual
	if len(sm_all_streets) != 0:
		print('SM file does exists for '+city_name+', '+state_abbr+' in '+str(decade))
		#Create dictionary {NAME:num_NAME_versions}
		num_NAME_versions = {k:len(v) for k, v in sm_st_ed_dict_nested.items()}
		#Flatten for use elsewhere
		sm_st_ed_dict = {k:v for d in [v for k, v in sm_st_ed_dict_nested.items()] for k, v in d.items()}
		#For bookkeeping when validating matches using ED 
		microdata_all_streets = df['street_precleaned'].unique()
		for st in microdata_all_streets:
			if st not in sm_all_streets:
				sm_st_ed_dict[st] = None
		# set same_year = True for later functions, this is always true for Geocoding project
		same_year = True
	# If we cannot find Steve Morse data for that decade, try other decades
	else:
		same_year = False
		# Try other decades until we find data
		year_try = decade
		while len(sm_all_streets) == 0:
			try:
				year_try = year_try + 10
				sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse([city_name, state_abbr, year_try])
			except KeyError:
				sm_all_streets = []
		# delete the ED dictionaries, they are wrong
		del sm_st_ed_dict_nested
		sm_ed_st_dict = None
		sm_st_ed_dict = None
		# If we found Steve Morse data for the city, use it 
		if len(sm_all_streets) != 0:
			#print SM status
			print('SM file does not exist for '+city_name+', '+state_abbr+' in '+str(decade))
		# If we did not find Steve Morse data, return a bunch of Nones
		else:
			print('SM file could not be found for '+city_name+', '+state_abbr)
			# delete the ED dictionaries, they are wrong
			sm_all_streets = None

	#If no TYPE, check if NAME is unique (and so we can assume TYPE = "St")
	df['street_precleaned'], df['TYPE'] = zip(*df.apply(lambda x: replace_singleton_names_w_st(x['street_precleaned'], x['NAME'], x['TYPE']), axis=1))

	if same_year:
		#If no DIR, check Steve Mose ED for street to see if it should have a DIR
		df['street_precleaned'], df['check_DIR'], df['DIR_added'] = zip(*df.apply(lambda x: try_to_find_dir(x['street_precleaned'], x['DIR'], x['ed']), axis=1))
	else:
		df['check_DIR'] = False
		df['DIR_added'] = False

	end = time.time()
	preclean_time = round(float(end-start)/60, 1)

	print('Precleaning street names for %s took %s\n' % (city_name, str(preclean_time)))
	
	preclean_info = sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, preclean_time, same_year

	return df, preclean_info


#
# Step 3a: Import street names from street grids  
#

specstd = {ord(u'’'): u"'", }
def specials(error):
	return specstd.get(ord(error.object[error.start]), u''), error.end

codecs.register_error('specials', specials)

#Function to load 1940 street grid data (no or incomplete ED information)
def get_streets_from_street_grid(city_info, paths, use_1940=True): 

	city_name, state_abbr, decade = city_info 
	_, dir_path = paths

	if use_1940:
		decade = 1940

	special_cities = {'Birmingham':'standardiz',
					'Bridgeport':'standardiz',
					'Dallas':'standardiz',
					'Springfield':'standardiz'}

	if city_name == 'StatenIsland':
		c = 'Richmond'
	else:
		c = city_name.replace(' ','')

	# Try to load file, return error if can't load or file has no cases
	try:
		file_name_st_grid = c + state_abbr + '_' + str(decade) + '_stgrid_diradd.dbf'
		st_grid_path = dir_path + '/' + str(decade) + '/shp/' + c + state_abbr + '/'
	#TODO: AltSt has street name if FULLNAME/standardized == "City limits" (actually "City limit")
		if city_name in special_cities.keys():
			var = special_cities[city_name]
		if city_name == "Kansas City" and state_abbr == "MO":
			var = 'stndrdname'
		else:
			var = 'fullname'
		table = dbf.Table(st_grid_path + file_name_st_grid)
		table.open()
		s = [i[var].encode('utf-8').strip() for i in table]
		table.close()
		s_no_utf = [i.replace('\xc2\xbd',' 1/2') for i in list(set(s))]
		streets = list(set(s_no_utf))
	except:
		print('Error getting %s street grid data' % (city_name))

	return streets

#Function to load 1940, Contemporary, and Chicago group 1930 street grid data (joined with Chicago group 1930 EDs)
def get_stgrid_with_EDs(city_info, map_type, file_path, use_1940=True): 

	city_name, state_abbr, decade = city_info

	if use_1940:
		decade = 1940

	special_cities = {'Birmingham':'standardiz',
					'Bridgeport':'standardiz',
					'Dallas':'standardiz',
					'Springfield':'standardiz'}

	if city_name == 'StatenIsland':
		c = 'Richmond'
	else:
		c = city_name.replace(' ','')

	st_grid_path = file_path + '/' + str(decade) + '/shp/' + c + state_abbr + '/'

	#Map from 1940 street grid (student edited to 1940 black/white map - in future may be 1930)
	if map_type == "1940":
		stgrid_ED_sj_shp = st_grid_path + c + state_abbr + '_1940_stgrid_ED_sj.shp' 
		street = 'FULLNAME'

	#Map from Tiger/Line 2012 (clipped to approximate city boundary)
	if map_type == "Contemp":
		stgrid_ED_sj_shp = st_grid_path + c + state_abbr + '_Contemp_stgrid_ED_sj.shp'
		street = 'FULL2012'

	#Map from Chicago group (only very certain cities)
	if map_type == "Chicago":
		stgrid_ED_sj_shp = st_grid_path + c + state_abbr + '_1930_stgrid_ED_sj.shp'
		street = 'FULLNAME'

	df = load_shp(stgrid_ED_sj_shp) 

	all_streets = df[street].drop_duplicates().tolist()

	df1 = df[(df['ED']!='') & (df[street]!='')]
	ed_st_dict = {}
	df_grouped = df1.groupby(['ED'])
	for group, data in df_grouped:
		ed_st_dict[group] = data[street].drop_duplicates().tolist()

	return all_streets, ed_st_dict

#
# Step 3b: Identify exact matches based on Steve Morse and 1940 street grid
#

#Function to do exact matching against Steve Morse street-ED lists
def find_exact_matches_sm(df, street, sm_all_streets, basic_info):

	post, num_records, num_streets = basic_info

	# Check for exact matches between Steve Morse ST and microdata ST
	df['exact_match_sm_bool'+post] = df[street].apply(lambda s: s in sm_all_streets)
	num_exact_matches_sm = np.sum(df['exact_match_sm_bool'+post])
	num_noexact_matches_sm =  num_records - num_exact_matches_sm
	prop_exact_matches_sm = float(num_exact_matches_sm)/float(num_records)
	print("Cases with exact matches (Steve Morse): "+str(num_exact_matches_sm)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches_sm, 1))+"%)")

	# Keep track of unique streets that do and do not have exact matches 
	df_exact_matches_sm = df[df['exact_match_sm_bool'+post]]
	df_noexact_matches_sm = df[~df['exact_match_sm_bool'+post]]

	num_streets_exact_sm = len(df_exact_matches_sm.groupby([street]).count())
	num_streets_noexact_sm = len(df_noexact_matches_sm.groupby([street]).count())
	while num_streets_exact_sm + num_streets_noexact_sm != num_streets:
		print("Error in number of streets")
		break
	prop_exact_streets_sm = float(num_streets_exact_sm)/float(num_streets)
	print("Streets with exact matches (Steve Morse): "+str(num_streets_exact_sm)+" of "+str(num_streets)+" streets ("+str(round(100*prop_exact_streets_sm, 1))+"%)")

	# Compile info for later use
	exact_info_sm = [num_exact_matches_sm, num_noexact_matches_sm, 
	num_streets_exact_sm, num_streets_noexact_sm]

	return df, exact_info_sm

#Function to do exact matching against 1940 street grid
def find_exact_matches_grid(df, street, st_grid_st_list, basic_info):

	post, num_records, num_streets = basic_info

	# Determine if cases without Steve Morse exact match have street grid exact match
	df.loc[df['exact_match_sm_bool'+post]==False,'exact_match_stgrid_bool'+post] = df.loc[df['exact_match_sm_bool'+post]==False,street].apply(lambda s: s in st_grid_st_list)
	num_exact_matches_stgrid = np.sum(df['exact_match_stgrid_bool'+post])
	num_noexact_matches_stgrid = num_records - num_exact_matches_stgrid
	prop_exact_matches_stgrid = float(num_exact_matches_stgrid)/float(num_records)
	print("Cases with exact matches (street grid): "+str(num_exact_matches_stgrid)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches_stgrid, 1))+"%)")

	# Keep track of unique streets that do and do not have exact matches in street grid
	df['temp'] = df['exact_match_stgrid_bool'+post].fillna('')
	df_exact_matches_stgrid = df[df['temp']==True]
	df_noexact_matches_stgrid = df[df['temp']==False]
	del df['temp']

	num_streets_exact_stgrid = len(df_exact_matches_stgrid.groupby([street]).count())
	num_streets_noexact_stgrid = len(df_noexact_matches_stgrid.groupby([street]).count())
	prop_exact_streets_stgrid = float(num_streets_exact_stgrid)/float(num_streets)
	print("Streets with exact matches (street grid): "+str(num_streets_exact_stgrid)+" of "+str(num_streets)+" streets ("+str(round(100*prop_exact_streets_stgrid, 1))+"%)\n")

	# Compile info for later use
	exact_info_stgrid = [num_exact_matches_stgrid, num_noexact_matches_stgrid, 
	num_streets_exact_stgrid, num_streets_noexact_stgrid]

	return df, exact_info_stgrid

# Function to run all exact matching and return results to Clean.py
# We are considering adding a step for exact matching within ED before checking the city
# Will need a flag to check if same_year = True (if not, both ED-street dictionaries are 'None' values and can't be used)
def find_exact_matches(df, city, street, sm_all_streets, source):

	print("\nExact matching algorithm for %s \n" % (street))

	# Timer start
	start = time.time()

	# Bookkeeping
	try:
		post = '_' + street.split('_')[2].split('HN')[0]
	except:
		post = ''
	num_records = len(df)
	num_streets = len(df.groupby([street]).count())
	basic_info = [post,num_records,num_streets]

	if source == 'sm':
		# Check for exact matches between microdata and Steve Morse
		df, exact_info_sm = find_exact_matches_sm(df, street, sm_all_streets, basic_info)
		df['exact_match_stgrid_bool'+post] = False
		exact_info_stgrid = [0, 0, 0, 0]
	elif source == 'stgrid':
		st_grid_st_list = get_streets_from_street_grid(city,state,file_path)
		# Check for exact matches between microdata and 1940 street grid 
		df, exact_info_stgrid = find_exact_matches_grid(df, street, st_grid_st_list, basic_info)
		df['exact_match_sm_bool'+post] = False
		exact_info_sm = [0, 0, 0, 0]
	elif source == 'both':
		# Check for exact matches between microdata and Steve Morse
		df, exact_info_sm = find_exact_matches_sm(df, street, sm_all_streets, basic_info)
		# Try to check for exact matches between microdata and 1940 street grid 
		try:
			st_grid_st_list = get_streets_from_street_grid(city,state,file_path)
			df, exact_info_stgrid = find_exact_matches_grid(df, street, st_grid_st_list, basic_info)
		except:
			exact_info_stgrid = [0, 0, 0, 0]
			df['exact_match_stgrid_bool'+post] = False
			
	# Create final exact match variable
	df['exact_match_bool'+post] = np.where(df['exact_match_sm_bool'+post] | df['exact_match_stgrid_bool'+post]==True,True,False)
	df['exact_match_type'] = np.where(df['exact_match_stgrid_bool'+post] & ~df['exact_match_sm_bool'+post],'StGrid','')
	df.loc[df['exact_match_sm_bool'+post],'exact_match_type'] = 'SM'

	# Generate some information
	num_exact_matches = df['exact_match_bool'+post].sum()
	prop_exact_matches = float(num_exact_matches)/float(num_records)
	print("Total cases with exact matches: "+str(num_exact_matches)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches, 1))+"%)")

	df_exact_matches = df[df['exact_match_bool'+post]]
	num_streets_exact = len(df_exact_matches.groupby([street]).count())
	prop_exact_streets = float(num_streets_exact)/float(num_streets)
	print("Total streets with exact matches: "+str(num_streets_exact)+" of "+str(num_streets)+" total streets pairs ("+str(round(100*prop_exact_streets, 1))+"%)")

	# Timer stop
	end = time.time()
	exact_matching_time = round(float(end-start)/60, 1)
	print("Exact matching took %s minutes\n" % (str(exact_matching_time)))

	# Generate dashboard info
	exact_info = exact_info_sm + [num_records, num_streets] + exact_info_stgrid + [exact_matching_time]

	return df, exact_info

#
# Step 4a: Search for fuzzy matches
#

#Function to check if street names differ by one character
def diff_by_one_char(st1, st2):
	if len(st1) == len(st2):
		st1chars = list(st1)
		st2chars = list(st2)
		#Check how many characters differ, return True if only 1 character difference
		if sum([st1chars[i]!=st2chars[i] for i in range(len(st1chars))]) == 1:
			return True
		else:
			return False
	else:
		return False

#Fuzzy matching algorithm
def fuzzy_match_function(street, ed, ed_streets_dict, all_streets_fuzzyset, check_too_similar=False):

	nomatch = ['', '', False]

	#Return null if street is blank
	if street == '':
		return nomatch
	#Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
	try:
		ed_streets = ed_streets_dict[ed]
		ed_streets_fuzzyset = fuzzyset.FuzzySet(ed_streets)
	except:
 #		print("Problem ED:" + str(ed))
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

#Fuzzy matching algorithm when SM file is from a later year (same_year = False)
def fuzzy_match_function_no_ed(street, all_streets_fuzzyset):
	
	nomatch = ['', '', False]
	
	#Return null if street is blank
	if street == '':
		return nomatch
	
	#Find best match among all streets
	try:
		best_match_all = all_streets_fuzzyset[street][0]
	except:
		return nomatch
	return [best_match_all[1], best_match_all[0], True]

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

#Function to update current best match (starts with either exact_match or '')
def update_current_match(current_match, current_match_bool, new_match, new_match_bool):
	if ~current_match_bool and new_match_bool:
		return new_match, new_match_bool
	else:
		return current_match, current_match_bool

#Function to do fuzzy matching using multiple sources
def find_fuzzy_matches_module(df, street_var, all_streets, ed_st_dict, map_type, same_year, resid=0):

	start = time.time()

	try:
		post = '_' + street.split('_')[2].split('HN')[0]
	except:
		post = ''

	#Set var names
	fuzzy_match = 'fuzzy_match_' + map_type + post
	fuzzy_bool = 'fuzzy_match_' + map_type + '_bool'+post
	fuzzy_score = 'fuzzy_match_' + map_type + '_score'+post

	#Create all street fuzzyset only once
	all_streets_fuzzyset = fuzzyset.FuzzySet(all_streets)

	#Create dictionary based on Street-ED pairs for faster lookup using helper function
	df_no_exact_match = df[~(df['current_match_bool'+post])]
	df_grouped = df_no_exact_match.groupby([street_var, 'ed'])
	fuzzy_match_dict = {}
	# Check that we found Steve Morse data
	if len(all_streets) != 0:
		for st_ed, _ in df_grouped:
			# If Steve Morse data come from same year as microdata, use ED for fuzzy matching
			if same_year:
				fuzzy_match_dict[st_ed] = fuzzy_match_function(st_ed[0], st_ed[1], ed_st_dict, all_streets_fuzzyset)
			# If Steve Morse data DO NOT come from same year as microdata, do not use ED for fuzzy matching
			else:
				fuzzy_match_dict[st_ed] = fuzzy_match_function_no_ed(st_ed[0], all_streets_fuzzyset)
	else:
		# For when there is no Steve Morse dictionary or Street Grid
		return df, [0, 0], len(df)-len(df_no_exact_match)

	#Compute current number of residuals
	num_records = len(df)
	if resid == 0:
		resid = num_records - len(df[df['current_match_bool'+post]])
	#Get fuzzy matches 
	df[fuzzy_match], df[fuzzy_score], df[fuzzy_bool] = zip(*df.apply(lambda x: get_fuzzy_match(x['current_match_bool'+post], fuzzy_match_dict, x[street_var], x['ed']), axis=1))
	#Update current match 
	df['current_match'+post], df['current_match_bool'+post] = zip(*df.apply(lambda x: update_current_match(x['current_match'+post], x['current_match_bool'+post], x[fuzzy_match], x[fuzzy_bool]),axis=1))

	#Generate dashboard information
	num_fuzzy_matches = np.sum(df[fuzzy_bool])
	prop_fuzzy_matches = float(num_fuzzy_matches)/num_records
	print("Fuzzy matches (using " + map_type + "): "+str(num_fuzzy_matches)+" of "+str(resid)+" unmatched cases ("+str(round(100*float(num_fuzzy_matches)/float(resid), 1))+"%)")
	end = time.time()
	fuzzy_matching_time = round(float(end-start)/60, 1)
	print("Fuzzy matching took %s minutes\n" % (str(fuzzy_matching_time)))
	fuzzy_info = [num_fuzzy_matches, fuzzy_matching_time]

	return df, fuzzy_info, resid

#Function to run all fuzzy matching and return results to Clean.py
def find_fuzzy_matches(df, city_info, street_var, sm_all_streets, sm_ed_st_dict, file_path, ed_map, same_year):

	city_name, state_abbr, _ = city_info

	try:
		post = '_' + street.split('_')[2].split('HN')[0]
	except:
		post = ''

	print("Fuzzy matching algorithm for %s \n" % (street_var))

	#Initialize fuzzy_match_bool
	df['fuzzy_match_bool'] = False

	#Initialize current match to exact matches that were found
	df['current_match'+post] = ''
	df['current_match_bool'+post] = df['exact_match_bool']
	df.loc[df['current_match_bool'+post],'current_match'+post] = df[street_var]

	if ed_map==True:

		#Get 1940 grid fuzzy matches
		grid_1940_all_streets, grid_1940_ed_st_dict = get_stgrid_with_EDs(city_info=city_info, 
			map_type='1940', 
			file_path=file_path)
		df, fuzzy_info_1940_grid, resid = find_fuzzy_matches_module(df=df, 
			street_var=street_var, 
			all_streets=grid_1940_all_streets, 
			ed_st_dict=grid_1940_ed_st_dict, 
			map_type='1940', 
			same_year=same_year)

		#Get Contemporary grid fuzzy matches
		grid_Contemp_all_streets, grid_Contemp_ed_st_dict = get_stgrid_with_EDs(city_info=city_info, 
			map_type='Contemp', 
			file_path=file_path)
		df, fuzzy_info_Contemp_grid, resid = find_fuzzy_matches_module(df=df, 
			street_var=street_var, 
			all_streets=grid_Contemp_all_streets, 
			ed_st_dict=grid_Contemp_ed_st_dict, 
			map_type='Contemp', 
			resid=resid, 
			same_year=same_year)

		#Get Chicago group 1930 grid fuzzy matches
		if city_name in ['Boston', 'Cincinnatti','Philadelphia']:
			grid_1930_all_streets, grid_1930_ed_st_dict = get_stgrid_with_EDs(city_info=city_info, 
				map_type='Chicago', 
				file_path=file_path)
			df, fuzzy_info_1930_grid, resid = find_fuzzy_matches_module(df=df, 
				street_var=street_var, 
				all_streets=grid_1930_all_streets, 
				ed_st_dict=grid_1930_ed_st_dict, 
				map_type='Chicago', 
				resid=resid, 
				same_year=same_year)
			fuzzy_info = fuzzy_info_1940_grid + fuzzy_info_Contemp_grid + fuzzy_info_1930_grid
		else:
			fuzzy_info = fuzzy_info_1940_grid + fuzzy_info_Contemp_grid 

		# Get Steve Morse fuzzy matches
		df, fuzzy_info_sm, resid = find_fuzzy_matches_module(df=df, 
			street_var=street_var, 
			all_streets=sm_all_streets, 
			ed_st_dict=sm_ed_st_dict, 
			map_type='sm', 
			same_year=same_year, 
			resid=resid)

		fuzzy_info = fuzzy_info + fuzzy_info_sm 

	else:
		# If no street-ED map information, just get Steve Morse fuzzy matches
		df, fuzzy_info_sm, resid = find_fuzzy_matches_module(df=df, 
			street_var=street_var, 
			all_streets=sm_all_streets, 
			ed_st_dict=sm_ed_st_dict, 
			map_type='sm', 
			same_year=same_year)
		fuzzy_info = fuzzy_info_sm

	return df, fuzzy_info

#
# Step 2c/4c: Use house number sequences to fill in blank street names
#

def fix_blank_st(df, city, HN_seq, street, sm_st_ed_dict):

	print("\nFixing blank street names using house number sequences\n")

	start = time.time()
	
	# Identify cases with blank street names
	df_STblank = df[df[street]=='']
	num_blank_street_names = len(df_STblank)    
	# Get indices of cases with blank street names
	STblank_indices = df_STblank.index.values
	# Create dictionary {k = index of blank street name : v = house number sequence}
	def get_range(blank_index):
		for i in HN_seq[street]:
			if i[0] <= blank_index <= i[1]:
				return i
	STblank_HNseq_dict = {}
	for blank_index in STblank_indices:
		STblank_HNseq_dict[blank_index] = get_range(blank_index)
	# Create list of ranges that contain cases with blank street names
	HNseq_w_blanks = [list(x) for x in set(tuple(x) for x in STblank_HNseq_dict.values())]
	# Create list of HNseq ranges with blanks
	seq_ranges_w_blanks = [range(i[0], i[1]+1) for i in HNseq_w_blanks]
	# Create singleton list
	singleton_list = [i for i in STblank_indices if len(range(STblank_HNseq_dict[i][0], STblank_HNseq_dict[i][1])) == 0]    
	# Create dictionary to hold {keys = frozenset(seq_ranges) : values = <assigned street name> }
	df['%sHN' % (street)] = df[street]
	for i in seq_ranges_w_blanks:
		# Select part of df with the blank street name
		df_seq_streets = df.ix[i[0]:i[-1], ['ed', street, 'hn']]
		# Collect street names (this will include '')
		seq_street_names = df_seq_streets[street].unique().tolist()
		# Count how many cases of each street name, store in dictionary
		street_count_dict = df_seq_streets.groupby([street]).count().to_dict().values()[0]
		ed_list = df_seq_streets['ed'].unique().tolist()
		# If sequence has only blank street names, leave street as blank
		if len(seq_street_names) == 1:
			continue
		# If sequence has one street name, replace blanks with that street name: (BUT ONLY IF SM IS FROM SAME YEAR)
		if len(seq_street_names) == 2:
			seq_street_names.remove('')
			potential_street_name = seq_street_names[0]
			# Only change name if sequence does not span EDs and street-ED can be validated
			for ed in ed_list:
				if check_ed_match(ed, potential_street_name, sm_st_ed_dict) or ed == '':
					df.ix[i, '%sHN' % (street)] = potential_street_name
			continue        
		# If sequence has one blank and more than one street name:
		else:
			non_blank_entries = len(df_seq_streets[df_seq_streets[street]!=''])
			for name in seq_street_names:
				# Choose a street name only if it constitutes at least 50% of non-blank street name entries
				if float(street_count_dict[name])/float(non_blank_entries) > 0.5:
					potential_street_name = name
					for ed in ed_list:
						if check_ed_match(ed, potential_street_name, sm_st_ed_dict) or ed == '':
							df.ix[i, '%sHN' % (street)] = potential_street_name

	df_STblank_post = df[df['%sHN' % (street)]=='']
	num_blank_street_names_post = len(df_STblank_post)    
	#NOTE: This is just blanks changed. Function will also change street names based on HN seq!
	num_blank_street_fixed = num_blank_street_names - num_blank_street_names_post
	temp = df['%sHN' % (street)] != df[street]
	num_street_changes_total = temp.sum()

	end = time.time()

	print("Found %s cases with blank street names" % (str(num_blank_street_names)))
 
	num_blank_street_singletons = len(singleton_list)
	per_singletons = round(100*float(num_blank_street_singletons)/float(num_blank_street_names), 1)
	print("Of these cases, "+str(num_blank_street_singletons)+" ("+str(per_singletons)+r"% of blanks) were singletons")

	per_blank_street_fixed = round(100*float(num_blank_street_fixed)/len(df), 1)
	per_street_changes_total = round(100*float(num_street_changes_total)/len(df), 1)
	print("Of non-singleton cases, "+str(num_blank_street_fixed)+" ("+str(per_blank_street_fixed)+r"% of all cases) could be fixed using HN sequences")
	print("A total of "+str(num_street_changes_total)+" ("+str(per_street_changes_total)+r"% of all cases) were changed")

	blank_fix_time = round(float(end-start)/60, 1)
	print("Fixing blank streets took %s minutes" % (str(blank_fix_time)))

	fix_blanks_info = [num_street_changes_total, num_blank_street_names, num_blank_street_singletons, per_singletons, num_blank_street_fixed, per_blank_street_fixed, blank_fix_time]

	return df, fix_blanks_info

def check_ed_match(microdata_ed,microdata_st,sm_st_ed_dict):
	if (microdata_st is None) or (sm_st_ed_dict is None) or (sm_st_ed_dict[microdata_st] is None):
		return False
	else:
		if microdata_ed in sm_st_ed_dict[microdata_st]:
			return True
		else:
			return False

# Side-step for NYC files
# Since SM dictionaries are for the 5 boroughs, the process must be done for each
# This function is identical to the clean_microdata() process for other cities, but includes this loop and append

def clean_nyc(df, city_info, file_path):

	boros = {50:'bronx', 470:'brooklyn', 610:'manhattan', 810:'queens', 850:'staten island'}
	codes = df['county'].unique()
	for code in codes:
		boro = boros[code]

		city_info[0] = boro
				
		print('Begin cleaning ' + boro)
				
		boro_df = df.loc[df['county'] == code]

		#
		# Step 2: Format raw street names and fill in blank street names
		#

		# Step 2a: Properly format street names and get Steve Morse street-ed information
		boro_df, preclean_info = preclean_street(boro_df, city_info, file_path)  
		sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, _, same_year  = preclean_info  

		# Step 2b: Use formatted street names to get house number sequences
		street_var = 'street_precleaned'
		boro_df, HN_SEQ, ED_ST_HN_dict = handle_outlier_hns(boro_df, street_var, 'hn_outlier1', decade, HN_SEQ, ED_ST_HN_dict)

		# Step 2c: Use house number sequences to fill in blank street names
		boro_df, fix_blanks_info1 = fix_blank_st(boro_df, boro, HN_SEQ, 'street_precleaned', sm_st_ed_dict)

		#
		# Step 3: Identify exact matches
		#

		preclean_var = 'street_precleanedHN'

		# Identify exact matches based on 1930 Steve Morse and/or 1940 street grid
		boro_df, exact_info = find_exact_matches(boro_df, city_name, preclean_var, sm_all_streets, street_source)

		#
		# Step 4: Search for fuzzy matches and use result to fill in more blank street names
		#

		# Step 4a: Search for fuzzy matches
		boro_df, fuzzy_info = find_fuzzy_matches(boro_df, city_info, preclean_var, sm_all_streets, sm_ed_st_dict, file_path, ed_map = False, same_year = same_year)
		street_var = 'street_post_fuzzy'
		boro_df[street_var] = boro_df[preclean_var]
		boro_df.loc[boro_df['current_match_bool'],street_var] = boro_df['current_match']

		# Step 4b: Use fuzzy matches to get house number sequences
		boro_df, HN_SEQ, ED_ST_HN_dict = handle_outlier_hns(boro_df, street_var, 'hn_outlier2', decade, HN_SEQ, ED_ST_HN_dict)

		# Step 4c: Use house number sequences to fill in blank street names
		boro_df, fix_blanks_info2 = fix_blank_st(boro_df, boro, HN_SEQ, 'street_post_fuzzy', sm_st_ed_dict)

		#	
		# Step 5: Create overall match and all check variables
		#

		post_var = 'street_post_fuzzyHN'
		boro_df = create_overall_match_variables(boro_df, decade)

		print("\nOverall matches: "+str(boro_df['overall_match_bool'].sum())+" of "+str(len(boro_df))+" total cases ("+str(round(100*float(boro_df['overall_match_bool'].sum())/len(boro_df),1))+"%)\n")

		# Append all the borough files together

		try:
			nyc
		except NameError:
			nyc = new_df
		else:            
			nyc = nyc.append(new_df)
				
		print(boro + ' is done!')


	#
	# Step 6: Set priority level for residual cases
	#

	#df, priority_info = set_priority(df)

	#
	# Step 7: Save full dataset and generate dashboard information 
	#

	city_state = city_name.replace(' ','') + state_abbr
	autoclean_path = file_path + '/%s/autocleaned/%s/' % (str(decade), 'V'+str(version))
	if ~os.path.exists(autoclean_path):
		os.makedirs(autoclean_path)
	file_name_all = autoclean_path + '%s_AutoCleaned%s.csv' % (city_state, 'V'+str(version))
	df.to_csv(file_name_all)

	'''
	#Generate dashbaord info
	times = [load_time, total_time]
	if decade != 1940:
		info = gen_dashboard_info(df, city_info, exact_info, fuzzy_info, preclean_info, times, fix_blanks_info1, fix_blanks_info2)
	else:
		info = gen_dashboard_info(df, city_info, exact_info, fuzzy_info, preclean_info, times)
	'''
	
	print("%s %s, %s complete" % (decade, city_name, state_abbr))
