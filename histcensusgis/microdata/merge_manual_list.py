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

	print 'Merging autocleaned data with manual fixes for ' + city_name + ', ' + state_abbr

	# load autocleaned data and edited manual list
	auto = pd.read_csv(file_path + '/' + str(decade) + '/autocleaned/V8/' + auto_file, low_memory = False)
	manual = pd.read_csv(file_path + '/' + str(decade) + '/autocleaned/V8/manual_lists_edited/' + manual_file)

	# change the annoying 'HN' tag that is sometimes on precleaned variable
	if 'street_precleanedHN' in list(auto.columns):
		auto = auto.rename(index=str, columns={'street_precleanedHN': 'street_precleaned'})

	# rename columns in manual list for merging
	manual = manual.rename(index=str, columns={'micro_st':'street_precleaned', 'micro_ed':'ed', 'new_st':'manual_st', 'new_hn':'manual_hn', 'new_institution':'manual_institution'})

	# merge manual list to auto
	df = auto.merge(manual, how='left', on=['street_precleaned', 'ed'])

	### Finalize microdata

	# overwrite hn, block, and institution with manual info if cell is empty
	# Actually, this is more difficult than I thought, so I'm calling just having the manual info available enough

	# create clean_final variable 
	df['clean_final'] = ''
	# add all overall matches (both exact and fuzzy)
	df.loc[df['overall_match_bool']==True, 'clean_final'] = df['overall_match']
	# add all manual fixes
	df.loc[df['manual_st'].isnull()==False, 'clean_final'] = df['manual_st']

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





