from multiprocessing import Pool
import pandas as pd
import sys
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STclean import *
from microclean.HNclean import *

file_path = '/home/s4-data/LatestCities' 
city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_df['city'] = city_info_df['city_name'].str.replace(" ","")
city_info_list = city_info_df[['city','state_abbr']].values.tolist()

year = 1930
city = "Albany"
state = "NY"

def STclean_city(city,state,year):

	start_total = time.time()

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
	#	init()
	#	sys.stdout = open(file_path + "/%s/logs/%s_Cleaning.log" % (str(year),city),'wb')

	cprint('%s Automated Cleaning\n' % (city), attrs=['bold'], file=AnsiToWin32(sys.stdout))

	# Load city
	df, load_time = load_city(city,state,year)

	# Pre-clean street names
	df, preclean_time = preclean_street(df,city)    

	# Use pre-cleaned street names to get house number sequences
	HN_SEQ['street_precleaned'], ED_ST_HN_dict['street_precleaned'] = get_HN_SEQ(df,year,'street_precleaned',debug=True)

	# Load Steve Morse Street-ED data
	sm_all_streets, sm_st_ed_dict, sm_ed_st_dict = load_steve_morse(df,city,state,year,flatten=True)

	# Use house number sequences to fill in blank street names
	df, fix_blanks_info1 = fix_blank_st(df,city,HN_SEQ,'street_precleaned',sm_st_ed_dict)
	num_blank_street_names1, num_blank_street_singletons1, per_singletons1, num_blank_street_fixed1, per_blank_street_fixed1, blank_fix_time1 = fix_blanks_info1

	# Get exact matches
	df, exact_info = find_exact_matches(df,city,'street_precleanedHN',sm_all_streets,sm_st_ed_dict)
	num_records, num_passed_validation, prop_passed_validation, num_failed_validation, prop_failed_validation, num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation, exact_matching_time = exact_info 

	# Get fuzzy matches
	df, fuzzy_info, problem_EDs = find_fuzzy_matches(df,city,'street_precleanedHN',sm_all_streets,sm_ed_st_dict)
	num_fuzzy_matches, prop_fuzzy_matches, fuzzy_matching_time = fuzzy_info

	# Use fuzzy matches to get house number sequences
	df['street_post_fuzzy'] = df['street_precleanedHN']
	df.loc[df['sm_fuzzy_match_bool'],'street_post_fuzzy'] = df['sm_fuzzy_match']
	df = df.sort_values(['ed','street_post_fuzzy','hn'])
	df.index = range(0,len(df))
	HN_SEQ['street_post_fuzzy'], ED_ST_HN_dict['street_post_fuzzy'] = get_HN_SEQ(df,year,'street_post_fuzzy')

	# Use house number sequences to fill in blank street names
	df, fix_blanks_info2 = fix_blank_st(df,city,HN_SEQ,'street_post_fuzzy',sm_st_ed_dict)
	num_blank_street_names2, num_blank_street_singletons2, per_singletons2, num_blank_street_fixed2, per_blank_street_fixed2, blank_fix_time2 = fix_blanks_info2

	cprint("Overall matches of any kind\n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

	# Initialize cases as having no match
	df['overall_match'] = ''
	df['overall_match_type'] = 'NoMatch'
	df['overall_match_bool'] = False

	df.loc[df['sm_fuzzy_match_bool'],'overall_match'] = df['street_post_fuzzy']
	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match'] = df['street_precleanedHN']

	df.loc[df['sm_fuzzy_match_bool'],'overall_match_type'] = 'FuzzySM'
	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match_type'] = 'ExactSM'

	df.loc[(df['overall_match_type'] == 'ExactSM') | (df['overall_match_type'] == 'FuzzySM'),'overall_match_bool'] = True 

	df['street_autocleaned'] = df['overall_match']

	num_overall_matches = np.sum(df['overall_match_bool'])
	cprint("Overall matches: "+str(num_overall_matches)+" of "+str(num_records)+" total cases ("+str(round(100*float(num_overall_matches)/float(num_records),1))+"%)\n",file=AnsiToWin32(sys.stdout))

	end_total = time.time()
	total_time = round(float(end_total-start_total)/60,1)
	cprint("Total processing time for %s: %s\n" % (city,total_time),'cyan',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	problem_EDs = list(set(problem_EDs))
	print("Problem EDs: %s" % (problem_EDs))

	#	sys.stdout.close()

	problem_EDs_present = False
	if len(problem_EDs) > 0:
		problem_EDs_present = True

	num_residual_cases = num_records - num_overall_matches
	prop_residual_cases = float(num_residual_cases)/float(num_records)
	prop_overall_matches = float(num_overall_matches)/float(num_records)

	temp = [year, city, state, num_records, 
		num_passed_validation, prop_passed_validation,
		num_fuzzy_matches, prop_fuzzy_matches,
		num_overall_matches, prop_overall_matches,
		num_residual_cases, prop_residual_cases,
		num_failed_validation, prop_failed_validation,
		num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation,
		problem_EDs_present,
		num_blank_street_names1, num_blank_street_singletons1, per_singletons1, num_blank_street_fixed1, per_blank_street_fixed1, 
		num_blank_street_names2, num_blank_street_singletons2, per_singletons2, num_blank_street_fixed2, per_blank_street_fixed2,
		load_time, preclean_time, exact_matching_time, fuzzy_matching_time, blank_fix_time1, blank_fix_time2, total_time] 

	file_name = city.replace(' ','') + state

	return df, temp 

df, temp = STclean_city("Albany","NY",1930)

names = ['Year', 'City', 'State', 'NumCases',
	'ExactMatchesValidated','propExactMatchesValidated',
	'FuzzyMatches','propFuzzyMatches',
	'OverallMatches','propOverallMatches',
	'ResidualCases','propResidualCases',
	'ExactMatchesFailed','propExactMatchesFailed',
	'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
	'ProblemEDs',
	'StreetNameBlanks1','BlankSingletons1','PerSingletons1','BlanksFixed1','PerBlanksFixed1',
	'StreetNameBlanks2','BlankSingletons2','PerSingletons2','BlanksFixed2','PerBlanksFixed2',
	'LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','TotalTime']


dashboard = pd.DataFrame(columns=names)


'''	
	df.to_csv(file_path + '/%s/autocleaned/%s_AutoCleaned.csv' % (str(year),file_name))

	# Save only a subset of variables for students to use when cleaning
	student_vars = ['ed','street_raw','hn','dn','fam_id','image_id','line_num','street_precleanedHN','overall_match_bool']
	df_forstudents = df[student_vars]
	df_forstudents.to_csv(file_path + '/%s/forstudents/%s_forstudents.csv' % (str(year),file_name))

#	dashboard = pd.DataFrame(columns=names)
#	dashboard.loc[0] = temp
'''


'''

names = ['Year', 'City', 'State', 'NumCases',
	'ExactMatchesValidated','propExactMatchesValidated',
	'FuzzyMatches','propFuzzyMatches',
	'OverallMatches','propOverallMatches',
	'ResidualCases','propResidualCases',
	'ExactMatchesFailed','propExactMatchesFailed',
	'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
	'ProblemEDs',
	'StreetNameBlanks1','BlankSingletons1','PerSingletons1','BlanksFixed1','PerBlanksFixed1',
	'StreetNameBlanks2','BlankSingletons2','PerSingletons2','BlanksFixed2','PerBlanksFixed2',
	'LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','TotalTime']


year = int(sys.argv[1])

city_info_list = [i.append(year) for i in city_info_list]

pool = Pool(8)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

names = ['Year', 'City', 'State', 'NumCases',
    'ExactMatchesValidated','propExactMatchesValidated',
    'FuzzyMatches','propFuzzyMatches',
    'OverallMatches','propOverallMatches',
    'ResidualCases','propResidualCases',
    'ExactMatchesFailed','propExactMatchesFailed',
    'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
    'LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','TotalTime']

dashboard = pd.DataFrame(temp,columns=names)
csv_file = file_path + '/%s/CleaningSummary%s.csv' % (str(year),str(year))
dashboard.to_csv(csv_file)
'''