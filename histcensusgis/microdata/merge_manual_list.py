from histcensusgis.microdata import *
from histcensusgis.s4utils import *
import pandas as pd
import numpy as np
import geopandas as gpd
import os
import re
import fuzzyset
import copy
from functools import partial

#city_name = 'Flint'
#state_abbr = 'MI'
#file_path='/home/s4-data/LatestCities'

# This function appends the manually cleaned leftover streets to the autocleaned microdata
# Written by Ben Bellman

# This is written assuming V8 is going to be the last version of autocleaning that is developed

# Final street variable is 'clean_final'
# Empty where no automatic or manual fix was made

def merge_manual_list(city_info, file_path='/home/s4-data/LatestCities'):

	# initialize process
	city_name, state_abbr, decade = city_info
	state_abbr = state_abbr.upper()
	manual_file = city_name + state_abbr + '_' + str(decade) + '_manual_list_edited.csv'
	auto_file = city_name + state_abbr + '_AutoCleanedV8.csv'
	street_var = 'manual_st'
	print 'Merging autocleaned data with manual fixes for ' + city_name + ', ' + state_abbr

	# Loading Steve Morse dicitonaries
	# Test to see if full-city dictionary including all possible streets is available
	sm_all_streets = pickle.load(open(package_path + '/text/full_city_street_dict.pickle', 'rb'))[(city_name, state_abbr.lower())]

	# if exists, don't load "all_streets" SM list for that year
	if sm_all_streets:
		_, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(city_info)
	# if doesn't exist (sm_all_streets == None), load all three SM objects
	else:
		sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(city_info)

	# set up flags for exact and fuzzy matching
	if len(sm_st_ed_dict_nested) == 0:
		same_year = False
	else:
		same_year = True
	list_dict = None

	# load autocleaned data and edited manual list
	auto = pd.read_csv(file_path + '/' + str(decade) + '/autocleaned/V8/' + auto_file)
	auto = auto.loc[:, ~auto.columns.str.contains('^Unnamed')]
	manual = pd.read_csv(file_path + '/manual_edits_19/manual_lists_edited/' + manual_file).replace(np.nan, '', regex=True)

	# drop n_people column from manual list
	manual = manual.drop(['n_people'], axis=1) 

	# change the annoying 'HN' tag that is sometimes on precleaned variable
	if 'street_precleanedHN' in list(auto.columns):
		auto = auto.rename(index=str, columns={'street_precleanedHN': 'street_precleaned'})

	# rename columns in manual list for merging
	manual = manual.rename(index=str, columns={'micro_st':'street_precleaned', 'micro_ed':'ed', 'new_st':'manual_st', 'new_hn':'manual_hn', 'new_institution':'manual_institution'})
	#manual['ed'] = manual['ed'].apply(str)

	# run exact and fuzzy matching on manual streets
	manual, exact_info = find_exact_matches(manual, city_info, street_var, sm_all_streets, sm_ed_st_dict, ed_map = False, same_year=same_year, file_path=file_path, list_dict=list_dict, use_lists = False)
	manual, fuzzy_info = find_fuzzy_matches(manual, city_info, street_var, sm_all_streets, sm_ed_st_dict, ed_map = False, same_year=same_year, file_path=file_path, list_dict=list_dict, use_lists = False)

	# overwrite manual_st with matched versions from SM
	manual.loc[manual['exact_match']!='', 'manual_st'] = manual['exact_match']
	manual.loc[manual['fuzzy_match_sm']!='', 'manual_st'] = manual['fuzzy_match_sm']

	# drop all added columns
	manual = manual.drop(['exact_match', 'exact_match_bool', 'fuzzy_match_bool', 'current_match_bool', 'current_match', 'fuzzy_match_sm', 'fuzzy_match_sm_score', 'fuzzy_match_sm_bool'], axis = 1)

	# merge manual list to auto
	#manual['ed'] = manual['ed'].apply(int)
	manual['ed'] = manual['ed'].apply(str)
	auto['ed'] = auto['ed'].apply(str)
	df = auto.merge(manual, how='left', on=['street_precleaned', 'ed'])
	# overwrite NaN introduced in manual columns by merge
	df[manual.columns] = df[manual.columns].fillna('')

	### Finalize microdata

	# only organizing fixed street names
	# other information is still available in "manual" columns for later use

	# create clean_final variable 
	df['clean_final'] = ''
	# add all overall matches (both exact and fuzzy)
	df.loc[df['overall_match_bool']==True, 'clean_final'] = df['overall_match']
	# add all manual fixes
	df.loc[df['manual_st']!='', 'clean_final'] = df['manual_st']

	# output "fully cleaned" csv file
	out_path = file_path + '/' + str(decade) + '/fully_cleaned'
	out_file = out_path + '/' + city_name + state_abbr + '_' + str(decade) + '_FullyCleaned.csv'
	# make sure directory exists
	if not os.path.exists(out_path):
		os.makedirs(out_path)
	# write file
	df.to_csv(out_file, index=False)

	# print completion message
	print city_name + ', ' + state_abbr + ' in ' + str(decade) + ' is fully cleaned!'


### Function to generate lists of streets to check and add to the street grid
def streets_to_add_in_grid(city_name, state_abbr, file_path='/home/s4-data/LatestCities'):

	print 'Getting streets to check in grid for ' + city_name + ', ' + state_abbr

	# load both the 1930 and 1940 fully cleaned microdata files, keep only needed columns and dropping blank streets
	fc30 = pd.read_csv(file_path + '/1930/fully_cleaned/'+ city_name + state_abbr + '_1930_FullyCleaned.csv')[['ed', 'street_precleaned', 'clean_final']]
	fc30 = fc30.loc[fc30.street_precleaned.isna() == False]
	fc40 = pd.read_csv(file_path + '/1940/fully_cleaned/'+ city_name + state_abbr + '_1940_FullyCleaned.csv')[['ed', 'street_precleaned', 'clean_final']]
	fc40 = fc40.loc[fc40.street_precleaned.isna() == False]

	# short function to return valid street ending match
	def st_type(st):
		return re.search(' (St|Ave?|Blvd|Pl|Dr|Drive|Rd|Road|Ct|Railway|Circuit|Hwy|Fwy|Pkwy|Cir|Ter|La|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|Line|Plaza|Esplanade|Viaduct|Trafficway|Trfy|Turnpike|Pike)$', st)

	# short function to return valid street ending match
	def drop_type(st):
		test = st_type(st)
		if test:
			return st.replace(test.group(), '')
		else:
			return(st)

	# short function to drop direciton from a street name
	def drop_dir(st):
		return re.sub('^[NSEW][EW]? ', '', st)

	# short function to detect question mark in string (True if no question mark)
	def no_qm(st):
		return np.where(re.search('\?', st) is None, True, False)

	# short function to get unqiue values of a column
	def col_unique(x):
		return x.unique().tolist()

	# short function to get unqiue values of a column
	def col_n_unique(x):
		return len(x.unique().tolist())

	# combine street_precleaned and clean_final into one column
	fc30['original'] = fc30['clean_final']
	fc30.loc[fc30['original'].isna(), ['original']] = fc30['street_precleaned']
	fc40['original'] = fc40['clean_final']
	fc40.loc[fc40['original'].isna(), ['original']] = fc40['street_precleaned']
	# create column for which street names to keep for search
	# keep if not blank, and valid ending is found, and there is no question mark in text
	fc30['keep'] = np.where((fc30.original.apply(st_type).apply(lambda x: x is not None)) & (fc30.original.apply(no_qm)), 1, 0)
	fc30 = fc30.loc[fc30.keep == 1]
	fc40['keep'] = np.where((fc40.original.apply(st_type).apply(lambda x: x is not None)) & (fc40.original.apply(no_qm)), 1, 0)
	fc40 = fc40.loc[fc40.keep == 1]
	# limit to only original street name and ed, summarize people and eds of street name
	fc30 = fc30[['original', 'ed']].groupby('original').agg([col_unique, col_n_unique, 'count'])
	fc40 = fc40[['original', 'ed']].groupby('original').agg([col_unique, col_n_unique, 'count'])
	# restructure into new df
	st30 = pd.DataFrame({'original': fc30.index.tolist(), 'ed_list': fc30['ed'].col_unique.tolist(), 'n_ed': fc30['ed'].col_n_unique.tolist(), 'n_people': fc30['ed']['count'].tolist()})
	st40 = pd.DataFrame({'original': fc40.index.tolist(), 'ed_list': fc40['ed'].col_unique.tolist(), 'n_ed': fc40['ed'].col_n_unique.tolist(), 'n_people': fc40['ed']['count'].tolist()})

	# merge street name dfs together to create list of overlap
	stboth = st30.merge(st40, on = 'original', how = 'inner', suffixes = ('_30', '_40'))
	# drop these street names from the year-specific lists
	st30 = st30.loc[st30.original.isin(stboth.original) == False]
	st40 = st40.loc[st40.original.isin(stboth.original) == False]

	# re-order the columns
	stboth = stboth[['original', 'n_people_30', 'n_ed_30', 'ed_list_30', 'n_people_40', 'n_ed_40', 'ed_list_40']]
	st30 = st30[['original', 'n_people', 'n_ed', 'ed_list']]
	st40 = st40[['original', 'n_people', 'n_ed', 'ed_list']]

	## Setting up GIS data

	# load polygon files
	ed_poly_30 = gpd.read_file(file_path + '/manual_edits_19/add_grid_streets/ed_polygons/1930/' + city_name + state_abbr + '_1930_ed_guess.shp')
	ed_poly_40 = gpd.read_file(file_path + '/manual_edits_19/add_grid_streets/ed_polygons/1940/' + city_name + state_abbr + '_1940_EDmap.shp')

	# drop empty geometries
	ed_poly_30 = ed_poly_30.loc[ed_poly_30.geometry.isnull() == False]
	ed_poly_40 =ed_poly_40.loc[ed_poly_40.geometry.isnull() == False]

	# dissolve blocks to get a single polygon row for each ED
	ed_poly_30 = ed_poly_30[['ED_edit', 'geometry']].dissolve(by='ED_edit').reset_index()	
	ed_poly_40 = ed_poly_40[['ED_num', 'geometry']].dissolve(by='ED_num').reset_index()

	# load grid line file
	grid_geo = gpd.read_file(file_path + '/manual_edits_19/grids/pre_manual_historical_grids/' + city_name + state_abbr.upper() + '_streets_corrected_corners_restored.shp')
	grid_geo = grid_geo.loc[grid_geo.geometry.isnull() == False]
	grid_geo = grid_geo[['geometry', 'st30', 'st40']]
	grid_geo = grid_geo.fillna('')
	# add any other troublesome unicode errors in grid street names here
	grid_geo.st30 = grid_geo.st30.apply(lambda x: re.sub(u'\xbd', '', x))
	grid_geo.st40 = grid_geo.st40.apply(lambda x: re.sub(u'\xbd', '', x))

	## Compare each valid street name in each list to grid
	# only writing code for 1930 right now
	# as I run for other years in future, raw starting files will get regenerated, but remain unchanged

	# for stboth, only use 1930 EDs for comparing with grid

	# input is a tuple of street name and list of EDs it appears in form microdata
	def compare_st_to_grid(info, year):
		stname, ed_list = info

		# convert ed_list to all strings, make lower to match letters in polygon files
		ed_list = [str(a).lower() for a in ed_list]
		# spatial join the grid with EDs the microdata street appears in
		if year == 1930:
			joined = gpd.sjoin(ed_poly_30.loc[ed_poly_30.ED_edit.isin(ed_list)], grid_geo)
		if year == 1940:
			joined = gpd.sjoin(ed_poly_40.loc[ed_poly_40.ED_num.isin(ed_list)], grid_geo)
		# create new df out of unique street names in grid
		df = pd.DataFrame({'grid': joined.st30.dropna().unique().tolist() + joined.st40.dropna().unique().tolist()})
		df = df.loc[df.grid != '']
		# drop direction from all grid names
		df['nodir'] = df.grid.apply(drop_dir).apply(lambda x: x.decode('utf-8', 'ignore'))
		# separate type from all grid names
		df['notype'] = df.nodir.apply(drop_type).apply(lambda x: x.decode('utf-8', 'ignore'))
		#df = df.loc[df.nodir != df.notype]
		df['type'] = df.nodir.apply(st_type)
		df = df.loc[df.type.apply(lambda x: x is not None)]
		df['type'] = df['type'].apply(lambda x: x.group().replace(' ', '')).apply(lambda x: x.decode('utf-8', 'ignore'))

		# create a list of no-direction street names from the entire grid
		all_streets = grid_geo.st30.dropna().unique().tolist() + grid_geo.st40.dropna().unique().tolist()
		all_streets = map(drop_dir, all_streets)
		all_streets = list(set(all_streets))

		# CHECK 1: if microdata street appears exactly IN ENTIRE GRID, drop from list to check later
		stname_nodir = drop_dir(stname).decode('utf-8', 'ignore')
		if stname_nodir in all_streets:
			return pd.DataFrame({'original':[stname], 'exact':[1], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[0], 'correct_st':['']})

		# CHECK 2: if microdata name of street appears, and both types are one of St, Ave, Road, accept the grid version as correct
		stname_nodir_notype = drop_type(stname_nodir)
		try:
			stname_type = st_type(stname_nodir).group().replace(' ', '')
		# if code to get street type fails, it should be looked for in grid
		except:
			return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})
		# check condition
		if stname_nodir_notype in df['notype'].tolist():
			check = df.loc[(df.notype == stname_nodir_notype) & (df.type.isin(['St', 'Ave', 'Road']))].reset_index()
			# check that there is only one option to choose from
			if len(check) == 1:
				return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[1], 'fuzzy':[0], 'check_grid':[0], 'correct_st':[check.iloc[0]['nodir']]})
			else:
				return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})

		# CHECK 3: if microdata street has very close name fuzzy match and exact type match, accept the grid version as correct
		notype_fs = fuzzyset.FuzzySet(df.notype.unique())
		match = notype_fs.get(stname_nodir_notype)
		# if match fails, case must be checked in grid
		if match is None:
			return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})
		# first, see if best match is high enough score
		if match[0][0] > 0.8:
			# next, see if corresponding grid name has exact same type
			check = df.loc[df.notype == match[0][1]].reset_index()
			# confirm only one matching street
			if len(check) == 1:
				# confirm same type
				if stname_type == check.iloc[0]['type']:
					return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[1], 'check_grid':[0], 'correct_st':[check.iloc[0]['nodir']]})
				else:
					return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})
			else:
				return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})

		# if all checks fail, return a row marking that street to be checked, no correct street yet
		else:
			return pd.DataFrame({'original':[stname], 'exact':[0], 'type_fix':[0], 'fuzzy':[0], 'check_grid':[1], 'correct_st':['']})

	# create partial versions of functions
	compare_st_to_grid_30 = partial(compare_st_to_grid, year = 1930)
	compare_st_to_grid_40 = partial(compare_st_to_grid, year = 1940)

	### Check streets in both years
	# using 1930 EDs only for spatial join
	stboth_checks = pd.concat(map(compare_st_to_grid_30, zip(*[stboth.original.tolist(), stboth.ed_list_30.tolist()]))).reset_index(drop = True)
	stboth_full = stboth.merge(stboth_checks, how = 'left')
	# export full table of check info to folder
	stboth_full.to_csv(file_path + '/manual_edits_19/add_grid_streets/micro_grid_check_info/' + city_name + state_abbr.upper() + '_check_info_both.csv', index = False)
	# keep only cases that need checking, format table for students
	stboth_slim = stboth_full.loc[stboth_full.check_grid == 1]
	stboth_slim = stboth_slim[['original', 'n_people_30', 'n_ed_30', 'ed_list_30', 'n_people_40', 'n_ed_40', 'ed_list_40', 'correct_st']]
	stboth_slim['change_made'] = ''
	stboth_slim['notes'] = ''
	# export list of streets for students to check/add in grid
	stboth_slim.to_csv(file_path + '/manual_edits_19/add_grid_streets/lists_to_check/both/' + city_name + state_abbr.upper() + '_add_streets_both.csv', index = False)


	### Check streets in 1930
	st30_checks = pd.concat(map(compare_st_to_grid_30, zip(*[st30.original.tolist(), st30.ed_list.tolist()]))).reset_index(drop = True)
	st30_full = st30.merge(st30_checks, how = 'left')
	# export full table of check info to folder
	st30_full.to_csv(file_path + '/manual_edits_19/add_grid_streets/micro_grid_check_info/' + city_name + state_abbr.upper() + '_check_info_1930.csv', index = False)
	# keep only cases that need checking, format table for students
	st30_slim = st30_full.loc[st30_full.check_grid == 1]
	st30_slim = st30_slim[['original', 'n_people', 'n_ed', 'ed_list', 'correct_st']]
	st30_slim['added_to_grid'] = 0
	st30_slim['notes'] = ''
	# export list of streets for students to check/add in grid
	st30_slim.to_csv(file_path + '/manual_edits_19/add_grid_streets/lists_to_check/1930/' + city_name + state_abbr.upper() + '_add_streets_1930.csv', index = False)


	### Check streets in 1940
	st40_checks = pd.concat(map(compare_st_to_grid_40, zip(*[st40.original.tolist(), st40.ed_list.tolist()]))).reset_index(drop = True)
	st40_full = st40.merge(st40_checks, how = 'left')
	# export full table of check info to folder
	st40_full.to_csv(file_path + '/manual_edits_19/add_grid_streets/micro_grid_check_info/' + city_name + state_abbr.upper() + '_check_info_1940.csv', index = False)
	# keep only cases that need checking, format table for students
	st40_slim = st40_full.loc[st40_full.check_grid == 1]
	st40_slim = st40_slim[['original', 'n_people', 'n_ed', 'ed_list', 'correct_st']]
	st40_slim['added_to_grid'] = 0
	st40_slim['notes'] = ''
	# export list of streets for students to check/add in grid
	st40_slim.to_csv(file_path + '/manual_edits_19/add_grid_streets/lists_to_check/1940/' + city_name + state_abbr.upper() + '_add_streets_1940.csv', index = False)

	print city_name + ', ' + state_abbr + ' is done'

#streets_to_add_in_grid('Akron','OH')




### Function to split edited "both" street grids into separate files for further editing
# steps: 
# 1) pull into new folder on server
# 2) load grid into python
# 3) create two new versions after changing stname column names and pasting values in for 1940
# 4) export as two new shapefiles with descriptive names

def split_grid_to_edit(city_name, state_abbr, file_path='/home/s4-data/LatestCities'):
	print 'splitting grid for '+city_name+state_abbr
	# load edited "both" grid
	both_grid = gpd.read_file(file_path + '/manual_edits_19/grids/edited_both_grids/' + city_name + state_abbr.upper() + '_streets_corrected_corners_restored.shp')
	both_grid = both_grid.loc[both_grid.geometry.isnull() == False]
	# if no "stboth40", create a null column so code works for all cases
	if 'stboth40' not in both_grid.columns:
		both_grid['stboth40'] = ''
	# drop st30 and st40 since I want to use these names
	both_grid = both_grid.drop(columns = ['st30', 'st40'])
	# copy into 1930 and 1940 versions
	grid_30 = copy.copy(both_grid)
	grid_40 = copy.copy(both_grid)
	# in 1930, rename st_both as st30, drop extra colums
	grid_30['st30'] = grid_30['st_both']
	grid_30 = grid_30.drop(columns = ['st_both', 'stboth40'])
	# in 1940, create st40 by supplementing any values from stboth40, drop extra colums
	grid_40['st40'] = np.where(grid_40['stboth40'].notna(), grid_40['stboth40'], grid_40['st_both'])
	grid_40 = grid_40.drop(columns = ['st_both', 'stboth40'])
	# export shapefiles
	grid_30.to_file(file_path + '/manual_edits_19/grids/grids_to_edit_1930/' + city_name + state_abbr.upper() + '_add_missing_streets_1930.shp')
	grid_40.to_file(file_path + '/manual_edits_19/grids/grids_to_edit_1940/' + city_name + state_abbr.upper() + '_add_missing_streets_1940.shp')
	# done!
	print city_name+state_abbr+' grid is split!'




















