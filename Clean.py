from multiprocessing import Pool
import pandas as pd
import rpy2.robjects as robjects
import sys
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STclean import *
from microclean.HNclean import *

def clean_microdata(city_info):

	city = city_info[0]
	state = city_info[1]
	year = city_info[2]
	start_total = time.time()

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
	init()
	sys.stdout = open(file_path + "/%s/logs/%s_Cleaning.log" % (str(year),city.replace(' ','')),'wb')

	cprint('%s Automated Cleaning\n' % (city), attrs=['bold'], file=AnsiToWin32(sys.stdout))

	# Load city
	df, load_time = load_city(city.replace(' ',''),state,year)

	# Pre-clean street names
	df, preclean_time = preclean_street(df,city)    

	# Use pre-cleaned street names to get house number sequences
	street_var = 'street_precleaned'
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var,debug=True)
	df['hn_outlier1'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

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
	street_var = 'street_post_fuzzy'
	df[street_var] = df['street_precleanedHN']
	df.loc[df['sm_fuzzy_match_bool'],street_var] = df['sm_fuzzy_match']

	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var)
	df['hn_outlier2'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

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

	city_file_name = city.replace(' ','') + state

	df['check_hn'] = df['hn_outlier2']
	df['check_st'] = ~df['overall_match_bool']

	# Save full dataset 
	file_name_all = file_path + '/%s/autocleaned/%s_AutoCleaned.csv' % (str(year),city_file_name)
	df.to_csv(file_name_all)

	# Save only a subset of variables for students to use when cleaning

	df.replace({'check_hn' : { True : 'Yes', False: 'No'}, 
		'check_st' : { True : 'Yes', False: 'No'}})

	student_vars = ['index','image_id','line_num','institution','ed','block','hhid','rel_id','pid','dn','hn','street_raw','street_precleanedHN','check_hn','check_st']
	df_forstudents = df[student_vars]
	file_name_students = file_path + '/%s/forstudents/%s_ForStudents.csv' % (str(year),city_file_name)
	df_forstudents.to_csv(file_name_students)

	num_hn_outliers1 = 	df['hn_outlier1'].sum()  
	num_hn_outliers2 = 	df['hn_outlier2'].sum() 
	num_resid_check_st = len(df[df['check_st'] & ~df['check_hn']])
	prop_resid_check_st = float(num_resid_check_st)/num_records
	num_resid_check_hn = len(df[~df['check_st'] & df['check_hn']])
	prop_resid_check_hn = float(num_resid_check_hn)/num_records
	num_resid_check_st_hn = len(df[df['check_st'] & df['check_hn']])
	prop_resid_check_st_hn = float(num_resid_check_st_hn)/num_records

	num_residual_cases = len(df[df['check_st'] | df['check_hn']]) 
	prop_residual_cases = float(num_residual_cases)/float(num_records)
	prop_overall_matches = float(num_overall_matches)/float(num_records)

	info = [year, city, state, num_records, 
		num_passed_validation, prop_passed_validation,
		num_fuzzy_matches, prop_fuzzy_matches,
		num_resid_check_st, prop_resid_check_st,
		num_resid_check_hn, prop_resid_check_hn,
		num_resid_check_st_hn, prop_resid_check_st_hn,
		num_residual_cases, prop_residual_cases,
		num_overall_matches, prop_overall_matches,
		problem_EDs_present,
		num_failed_validation, prop_failed_validation,
		num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation,
		num_hn_outliers1, num_blank_street_names1, num_blank_street_singletons1, per_singletons1, num_blank_street_fixed1, per_blank_street_fixed1, 
		num_hn_outliers2, num_blank_street_names2, num_blank_street_singletons2, per_singletons2, num_blank_street_fixed2, per_blank_street_fixed2,
		load_time, preclean_time, exact_matching_time, fuzzy_matching_time, blank_fix_time1, blank_fix_time2, total_time] 

	return info 

file_path = '/home/s4-data/LatestCities' 
city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()

year = int(sys.argv[1])
#year = 1930

for i in city_info_list:                
	i.append(year)


#temp =[]
#for i in city_info_list:
#	print(i)
#	temp.append(clean_microdata(i))

	
pool = Pool(8)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

names = ['Year', 'City', 'State', 'NumCases',
	'ExactMatchesValidated','propExactMatchesValidated',
	'FuzzyMatches','propFuzzyMatches',
	'ResidSt','propResidSt',
	'ResidHn','propResidHn',
	'ResidStHn','propResidStHn',
	'ResidualCases','propResidualCases',
	'OverallMatches','propOverallMatches',
	'ProblemEDs',
	'ExactMatchesFailed','propExactMatchesFailed',
	'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
	'HnOutliers1','StreetNameBlanks1','BlankSingletons1','PerSingletons1','BlanksFixed1','PerBlanksFixed1',
	'HnOutliers2','StreetNameBlanks2','BlankSingletons2','PerSingletons2','BlanksFixed2','PerBlanksFixed2',
	'LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','BlankFixTime1','BlankFixtime2','TotalTime']
dashboard = pd.DataFrame(temp,columns=names)

csv_file = file_path + '/%s/CleaningSummary%s.csv' % (str(year),str(year))
dashboard.to_csv(csv_file)

convert_dta_cmd = "stata -b ConvertToStataForStudents%s.do" % (str(year))
os.system(convert_dta_cmd)
