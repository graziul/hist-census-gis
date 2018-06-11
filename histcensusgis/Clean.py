from histcensusgis.microdata import *
from histcensusgis.s4utils import *
import os
import pandas as pd

# Version number 
version = 7

# Changelog
#
# V7
#   - Using grid street names for exact name matching and first fuzzy name matching (SM used for second)
#	- Removed assignment of manual cleaning priority from the process
#	- Implemented funky ordering/source for street name matching
#	- Implemented functionality for 1940 (Note: No house number sequence blank fixing)
#
# V6
#	- Added fuzzy matching against 1940 grid, 1930 Chicago group grid, and contemporary grid (using ED maps)
#	- Updated Steve Morse dictionaries (harmonized TYPE across decades)
#
# V5
#	- Integrated street names from edited 1940 street grid in matching process*
#	- Removed code for validating exact matches by ED (still do fuzzy matching using ED)
#
# V4
#	- New Steve Morse dictionary ("La" -> "Ln")
#	- Include best fuzzy match even if doesn't meet threshold (for student use)
#
# V3
#	- Integrated new raw data (obsolete)
#	- Implemented sequential street/hn checking for both old and new raw data (obsolete)
#	- Implemented code to select best street given old and new raw data (obsolete)
#	- Flagged street where old raw street and new raw street do not match (obsolete)
#	- Flagged hn where old raw hn and new raw hn do no match (obsolete)
#	- Implemented code to find DIR given ED if no DIR in microdata*
#
# V2 
#	- Removed cases where line_num, street_raw, name_last, and name_first are all blank*
#	- Removed duplicate pages, keeping page with most information (used age/gender sequences > 2)*
#	- Fixed multiple hn/st cleaning issues found through manual cleaning (e.g. street direction issues)*
#	- Removed checking for ED matches
#	- Note: "Hangover" code did NOT make it into this version
#
# V1 - Original run

datestr = time.strftime("%Y_%m_%d")

def clean_microdata(city_info, street_source='sm', ed_map=False, debug=False, file_path='/home/s4-data/LatestCities', sis_project=False):

	# Let's be sure SIS project never tries to use spatial files
	if sis_project:
		street_source = 'sm'
		ed_map = False

	city_name, state_abbr, decade = city_info

	#
	# Step 0: Initialize a bunch of variables for use throughout
	#

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
 	#init()
 	#sys.stdout = open(file_path + "/%s/logs/%s_Cleaning%s.log" % (str(decade), city.replace(' ','')+state, datestr),'wb')

	print('%s Automated Cleaning\n' % (city_name))

	#
	# Step 1: Load city and standardize variable names
	#

	df, load_time = load_city(city_info, file_path, sis_project)

	# Side step: If processing NYC all at once, run a separate process
	# Process is identical to below, but must be applied to all boroughs separately

	if city_name == 'new york':
		clean_nyc(df, city_info, file_path, sis_project)
		return 

	#
	# Step 2: Format raw street names and fill in blank street names
	#

	# Step 2a: Properly format street names and get Steve Morse street-ed information
	df, preclean_info = preclean_street(df, city_info, file_path, sis_project)  
	sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, _, same_year  = preclean_info  

	# Step 2b: Use formatted street names to get house number sequences
	street_var = 'street_precleaned'
	df, HN_SEQ, ED_ST_HN_dict = handle_outlier_hns(df, street_var, 'hn_outlier1', decade, HN_SEQ, ED_ST_HN_dict)

	# Step 2c: Use house number sequences to fill in blank street names
	df, fix_blanks_info1 = fix_blank_st(df, city_name, HN_SEQ, 'street_precleaned', sm_st_ed_dict)

	#
	# Step 3: Identify exact matches
	#

	preclean_var = 'street_precleanedHN'

	# Identify exact matches based on 1930 Steve Morse and/or 1940 street grid
	df, exact_info = find_exact_matches(df, city_name, preclean_var, sm_all_streets, street_source)

	#
	# Step 4: Search for fuzzy matches and use result to fill in more blank street names
	#

	# Step 4a: Search for fuzzy matches
	df, fuzzy_info = find_fuzzy_matches(df, city_info, preclean_var, sm_all_streets, sm_ed_st_dict, file_path, ed_map, same_year = same_year)
	street_var = 'street_post_fuzzy'
	df[street_var] = df[preclean_var]
	df.loc[df['current_match_bool'],street_var] = df['current_match']

	# Step 4b: Use fuzzy matches to get house number sequences
	df, HN_SEQ, ED_ST_HN_dict = handle_outlier_hns(df, street_var, 'hn_outlier2', decade, HN_SEQ, ED_ST_HN_dict)

	# Step 4c: Use house number sequences to fill in blank street names
	df, fix_blanks_info2 = fix_blank_st(df, city_name, HN_SEQ, 'street_post_fuzzy', sm_st_ed_dict)

	#	
	# Step 5: Create overall match and all check variables
	#

	df = create_overall_match_variables(df)

	print("\nOverall matches: "+str(df['overall_match_bool'].sum())+" of "+str(len(df))+" total cases ("+str(round(100*float(df['overall_match_bool'].sum())/len(df),1))+"%)\n")

	#
	# Step 6: Set priority level for residual cases
	#

	#df, priority_info = set_priority(df)

	#
	# Step 7: Save full dataset and generate dashboard information 
	#

	if sis_project:
		file_name = city_name.upper() + '_' + state_abbr.upper() + '_' + str(decade) + '_clean'
		outfile = file_path + '/CleanData/%s/%s.csv' % (str(decade), file_name)
		df.to_csv(outfile)
	else:
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

# Example: clean_microdata(['Flint','MI',1930],ed_map=False)

'''

# Get city list
file_path = '/home/s4-data/LatestCities' 
city_info_file = file_path + '/CityInfo.csv' 
#city_info_file = file_path + '/CityInfo_with_map.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_df['city_name'] = city_info_df['city_name'].str.replace('.','')
city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()
# 1940 issues: Only Brooklyn in 5 boroughs, no Norfolk for unknown reasons
exclude = ['Manhattan','Bronx','Queens','Staten Island','Norfolk']
city_info_list = [i for i in city_info_list if i[0] not in exclude]

# Get decade and add it to city list information
#decade = int(sys.argv[1])
decade = 1940
for i in city_info_list:
	i.append(decade)

# Check if all raw files exist
missing_raw = []
for i in city_info_list:
	city, state, decade = i

	if city == "StatenIsland":
		c = "Richmond"
	else:
		c = city.replace(' ','')

	file_name = c + state.upper()
	file = file_path + '/%s/%s.dta' % (str(decade), file_name)
	if os.path.exists(file):
		continue
	else:
		missing_raw.append([city,state])
if len(missing_raw) > 0:
	for i in missing_raw:
		print("Missing %s, %s" % (i[0], i[1]))
	raise ValueError

# Farm out cleaning across multiple instances of Python
pool = Pool(processes=8, maxtasksperchild=1)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

# Build dashboard for decade and save

city_state = ['City','State']
header_names = ['decade'] + city_state + ['NumCases']

if decade != 1940:
	STprop_names = ['propExactMatchesStGrid','propFuzzyMatches','propBlankSTfixed']
	STnum_names = city_state + ['numExactMatchesStGrid','numFuzzyMatches','numBlankSTfixed']
	ED_names = city_state + ['ProblemEDs']
	FixBlank_names = city_state + ['HnOutliers1','StreetNameBlanks1','BlankSingletons1','PerSingletons1',
		'HnOutliers2','StreetNameBlanks2','BlankSingletons2','PerSingletons2']
	Time_names = city_state + ['LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime',
		'BlankFixTime','PriorityTime','TotalTime']

	sp = ['']
	names = header_names + STprop_names + sp + STnum_names + sp + ED_names + sp + FixBlank_names + sp + Time_names

	df = pd.DataFrame(temp,columns=names)

	dfSTprop = df.iloc[:,1:8].sort_values(by='prop_exact_matches_stgrid').reset_index()
	dfSTnum = df.iloc[:,8:14].sort_values(by='ResidSt').reset_index()
	dfED = df.iloc[:,14:18].sort_values(by=city_state,ascending=False).reset_index()
	dfFixBlank = df.iloc[:,18:29].reset_index()
	dfTime = df.iloc[:,29:40].sort_values(by='TotalTime').reset_index()

	dashboard = pd.concat([dfSTprop, dfSTnum, dfHNprop, dfHNnum, dfRprop, dfRnum, dfperPriority, dfPriority, dfseqPriority, dfperseqPriority, dfED, dfFixBlank, dfTime],axis=1)
else:
	STprop_names = ['propExactMatches','propFuzzyMatches','propResid']
	STnum_names = city_state + ['numExactMatches','numFuzzyMatches','numResid']
	Time_names = city_state + ['LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','TotalTime']

	sp = ['']
	names = header_names + STprop_names + sp + STnum_names + sp + Time_names

	df = pd.DataFrame(temp,columns=names)

	dfSTprop = df.iloc[:,1:8].sort_values(by='propExactMatches').reset_index()
	dfSTnum = df.iloc[:,8:14].sort_values(by='numResid').reset_index()
	dfTime = df.iloc[:,15:25].sort_values(by='TotalTime').reset_index()

	dashboard = pd.concat([dfSTprop, dfSTnum, dfTime],axis=1)

dashboard['version'] = version
csv_file = file_path + '/%s/CleaningSummary%s_%s.csv' % (str(decade),str(decade),datestr)
dashboard.to_csv(csv_file,index=False)
'''