from histcensusgis.microdata import *
from histcensusgis.s4utils import *
import pandas as pd
import os

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

	# set up objects for exact and fuzzy matching
	sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(city_info)
	if len(sm_all_streets) == 0:
		same_year = False
	else:
		same_year = True
	list_dict = None

	# load autocleaned data and edited manual list
	auto = pd.read_csv(file_path + '/' + str(decade) + '/autocleaned/V8/' + auto_file)
	manual = pd.read_csv(file_path + '/' + str(decade) + '/autocleaned/V8/manual_lists_edited/' + manual_file).replace(np.nan, '', regex=True)

	# change the annoying 'HN' tag that is sometimes on precleaned variable
	if 'street_precleanedHN' in list(auto.columns):
		auto = auto.rename(index=str, columns={'street_precleanedHN': 'street_precleaned'})

	# rename columns in manual list for merging
	manual = manual.rename(index=str, columns={'micro_st':'street_precleaned', 'micro_ed':'ed', 'new_st':'manual_st', 'new_hn':'manual_hn', 'new_institution':'manual_institution'})
	manual['ed'] = manual['ed'].apply(str)

	# run exact and fuzzy matching on manual streets
	manual, exact_info = find_exact_matches(manual, city_info, street_var, sm_all_streets, sm_ed_st_dict, ed_map = False, same_year=same_year, file_path=file_path, list_dict=list_dict, use_lists = False)
	manual, fuzzy_info = find_fuzzy_matches(manual, city_info, street_var, sm_all_streets, sm_ed_st_dict, ed_map = False, same_year=same_year, file_path=file_path, list_dict=list_dict, use_lists = False)

	# overwrite manual_st with matched versions from SM
	manual.loc[manual['exact_match']!='', 'manual_st'] = manual['exact_match']
	manual.loc[manual['fuzzy_match_sm']!='', 'manual_st'] = manual['fuzzy_match_sm']

	# drop all added columns
	manual = manual[[0,1,2,3,4,5,6,7]]

	# merge manual list to auto
	manual['ed'] = manual['ed'].apply(int)
	df = auto.merge(manual, how='left', on=['street_precleaned', 'ed'])

	### Finalize microdata

	# overwrite hn, block, and institution with manual info if cell is empty
	# Actually, this is more difficult than I thought, so I'm calling just having the manual info available enough

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
	df.to_csv(out_file)

	# print completion message
	print city_name + ', ' + state_abbr + ' in ' + str(decade) + ' is fully cleaned!'





