from multiprocessing import Pool
import pandas as pd
import rpy2.robjects as robjects
import sys
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STclean import *
from microclean.HNclean import *
from microclean.SetPriority import *

datestr = time.strftime("%Y_%m_%d")

def create_overall_match_variables(df):

	df['overall_match'] = ''
	df['overall_match_type'] = 'NoMatch'
	df['overall_match_bool'] = False

	df.loc[df['sm_fuzzy_match_bool'],'overall_match'] = df['street_post_fuzzy']
	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match'] = df['street_precleanedHN']

	df.loc[df['sm_fuzzy_match_bool'],'overall_match_type'] = 'FuzzySM'
	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match_type'] = 'ExactSM'

	df.loc[(df['overall_match_type'] == 'ExactSM') | (df['overall_match_type'] == 'FuzzySM'),'overall_match_bool'] = True 

	num_overall_matches = np.sum(df['overall_match_bool'])

	return df, num_overall_matches

def clean_microdata(city_info):

	city = city_info[0]
	state = city_info[1]
	year = city_info[2]
	start_total = time.time()

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
#	init()
#	sys.stdout = open(file_path + "/%s/logs/%s_Cleaning%s.log" % (str(year),city.replace(' ','')+state,datestr),'wb')

	cprint('%s Automated Cleaning\n' % (city), attrs=['bold'], file=AnsiToWin32(sys.stdout))

	# Load city
	df, load_time = load_city(city.replace(' ',''),state,year)

	# Pre-clean street names
	df, sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, preclean_time = preclean_street(df,city,state,year)    

	# Use pre-cleaned street names to get house number sequences
	street_var = 'street_precleaned'
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var,debug=True)
	df['hn_outlier1'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

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

	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var,debug=True)
	df['hn_outlier2'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

	# Use house number sequences to fill in blank street names
	df, fix_blanks_info2 = fix_blank_st(df,city,HN_SEQ,'street_post_fuzzy',sm_st_ed_dict)
	num_blank_street_names2, num_blank_street_singletons2, per_singletons2, num_blank_street_fixed2, per_blank_street_fixed2, blank_fix_time2 = fix_blanks_info2

	cprint("Overall matches of any kind\n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

	# Create overall match variables
	df, num_overall_matches = create_overall_match_variables(df)
	cprint("Overall matches: "+str(num_overall_matches)+" of "+str(num_records)+" total cases ("+str(round(100*float(num_overall_matches)/float(num_records),1))+"%)\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	# Set priority level for residual cases
	df, priority_counts, num_priority, priority_time = set_priority(df)
	for i in range(1,8):
		cprint('Priority ' + str(i) + ' cases to check: ' + str(priority_counts[i]) + ' (' + str(round(100*float(priority_counts[i])/num_records,1)) + '% of all cases)',file=AnsiToWin32(sys.stdout))
	cprint('\nTotal cases to check: ' + str(sum(priority_counts.values())) + ' (' + str(round(100*float(sum(priority_counts.values()))/num_records,1)) + '%)','red',file=AnsiToWin32(sys.stdout))
	# Save full dataset 
	city_file_name = city.replace(' ','') + state
	file_name_all = file_path + '/%s/autocleaned/%s_AutoCleaned%s.csv' % (str(year),city_file_name,'V1')
	df.to_csv(file_name_all)

	# Generate remaining dashboard variables

	problem_EDs = list(set(problem_EDs))
	print("\nProblem EDs: %s" % (problem_EDs))

	problem_EDs_present = False
	if len(problem_EDs) > 0:
		problem_EDs_present = True

	num_hn_outliers1 = 	df['hn_outlier1'].sum()  
	num_hn_outliers2 = 	df['hn_outlier2'].sum() 
	num_resid_check_st = len(df[df['check_st'] & ~df['check_hn']])
	prop_resid_check_st = float(num_resid_check_st)/num_records
	num_resid_check_hn = len(df[~df['check_st'] & df['check_hn']])
	prop_resid_check_hn = float(num_resid_check_hn)/num_records
	num_resid_check_st_hn = len(df[df['check_st'] & df['check_hn']])
	prop_resid_check_st_hn = float(num_resid_check_st_hn)/num_records

	num_blank_street_fixed = num_blank_street_fixed1 + num_blank_street_fixed2
	prop_blank_street_fixed = float(num_blank_street_fixed)/num_records

	num_resid_st = len(df[df['check_st']]) - num_blank_street_fixed 
	prop_resid_st = float(num_resid_st)/num_records
#	num_resid_hn = len(df[df['check_hn']])
#	prop_resid_hn = float(num_resid_hn)/num_records
#	num_resid_st_hn = len(df[df['check_st'] | df['check_hn']]) 
#	prop_resid_st_hn = float(num_resid_st_hn)/float(num_records)

	num_resid_hn_total = num_resid_check_hn + num_resid_check_st_hn
	prop_resid_hn_total = prop_resid_check_hn + prop_resid_check_st_hn
	num_resid_total = num_resid_check_st + num_resid_check_st_hn + num_resid_check_hn
	prop_resid_total = prop_resid_check_st + prop_resid_check_st_hn + prop_resid_check_hn

	blank_fix_time = blank_fix_time1 + blank_fix_time2

	end_total = time.time()
	total_time = round(float(end_total-start_total)/60,1)
	cprint("\nTotal processing time for %s: %s\n" % (city,total_time),'cyan',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	info = [year, city, state, num_records, 
		prop_passed_validation, prop_fuzzy_matches, prop_blank_street_fixed, prop_resid_st,
		'', 
		city, state, num_passed_validation, num_fuzzy_matches, num_blank_street_fixed, num_resid_st,
		'', 
		city, state, prop_resid_check_hn, prop_resid_check_st_hn, prop_resid_hn_total,
		'',
		city, state, num_resid_check_hn, num_resid_check_st_hn, num_resid_hn_total,
		'',		
		city, state, prop_resid_check_hn, prop_resid_check_st_hn, prop_resid_check_st, prop_resid_total,
		'',
		city, state, num_resid_check_hn, num_resid_check_st_hn, num_resid_check_st, num_resid_total,
		'',
		city, state, priority_counts[1],priority_counts[2],priority_counts[3],priority_counts[4],priority_counts[5],priority_counts[6],priority_counts[7],sum(priority_counts.values()),
		'',
		city, state, float(priority_counts[1])/num_records,
		float(priority_counts[2])/num_records,
		float(priority_counts[3])/num_records,
		float(priority_counts[4])/num_records,
		float(priority_counts[5])/num_records,
		float(priority_counts[6])/num_records,
		float(priority_counts[7])/num_records,sum(priority_counts.values()),
		'',
		city, state, num_priority[1],num_priority[2],num_priority[3],num_priority[4],num_priority[5],num_priority[6],num_priority[7],sum(num_priority.values()),
		'',
		city, state, problem_EDs_present, num_failed_validation, prop_failed_validation, 
		num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation, 
		'',		
		city, state, num_hn_outliers1, num_blank_street_names1, num_blank_street_singletons1, per_singletons1,   
		num_hn_outliers2, num_blank_street_names2, num_blank_street_singletons2, per_singletons2, 
		'',
		city, state, load_time, preclean_time, exact_matching_time, fuzzy_matching_time, 
		blank_fix_time, priority_time, total_time] 

	# Save only a subset of variables for students to use when cleaning
	df = df.replace({'check_hn' : { True : 'yes', False: ''}, 
		'check_st' : { True : 'yes', False: ''},
		'check_ed' : { True : 'yes', False: ''}})

	if year==1940:
		student_vars = ['image_id','line_num','institution','ed','hhid','hhorder','rel_id','pid','dn','hn','street_raw','street_precleanedHN','check_ed','clean_priority']
	if year==1930:
		student_vars = ['index','image_id','line_num','institution','ed','block','hhid','rel_id','pid','dn','hn','street_raw','street_precleanedHN','check_hn','check_st','check_ed','clean_priority']
	
	df = df[student_vars]
	file_name_students = file_path + '/%s/forstudents/%s_ForStudents%s.csv' % (str(year),city_file_name,'V1')
	df.to_csv(file_name_students)

	return info 

file_path = '/home/s4-data/LatestCities' 
city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()

year = int(sys.argv[1])
#year = 1930

for i in city_info_list:                
	i.append(year)

'''
temp =[]
for i in city_info_list:
	temp.append(clean_microdata(i))
'''	

pool = Pool(processes=4,maxtasksperchild=1)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

names = ['Year', 'City', 'State', 'NumCases',
	'propExactMatchesValidated','propFuzzyMatches','propBlankSTfixed','propResidSt',
	'',
	'City', 'State','ExactMatchesValidated','FuzzyMatches','BlankSTfixed','ResidSt',
	'',
	'City', 'State','propCheckHn','propCheckStHn','propCheckHnTotal',
	'',
	'City', 'State','CheckHn','CheckStHn','CheckHnTotal',
	'',
	'City', 'State','propCheckHn','propCheckStHn','propCheckSt','propCheckTotal',
	'',
	'City', 'State','CheckHn','CheckStHn','CheckSt','CheckTotal',
	'',
	'City', 'State','100+ Cases','50-99 Cases','20-49 Cases','10-19 Cases','5-9 Cases','2-4 Cases','1 Case','TotalPriority',
	'',
	'City', 'State','100+ Cases (%)','50-99 Cases (%)','20-49 Cases (%)','10-19 Cases (%)','5-9 Cases (%)','2-4 Cases (%)','1 Case (%)','TotalPriority',
	'',
	'City', 'State','st 100+','st 50-99','st 20-49','st 10-19','st 5-9','st 2-4','st 1','StTotalPriority',
	'',
	'City', 'State','ProblemEDs', 'ExactMatchesFailed','propExactMatchesFailed',
	'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
	'',
	'City', 'State','HnOutliers1','StreetNameBlanks1','BlankSingletons1','PerSingletons1',
	'HnOutliers2','StreetNameBlanks2','BlankSingletons2','PerSingletons2',
	'',
	'City', 'State','LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime',
	'BlankFixTime','PriorityTime','TotalTime']

df = pd.DataFrame(temp,columns=names)

dfSTprop = df.ix[:,1:9].sort_values(by='propResidSt').reset_index()
dfSTnum = df.ix[:,9:16].sort_values(by='ResidSt',ascending=False).reset_index()
dfHNprop = df.ix[:,16:22].sort_values(by='propCheckHnTotal').reset_index()
dfHNnum = df.ix[:,22:28].sort_values(by='CheckHnTotal',ascending=False).reset_index()
dfRprop =df.ix[:,28:35].sort_values(by='propCheckTotal').reset_index()
dfRnumber = df.ix[:,35:42].sort_values(by='CheckTotal',ascending=False).reset_index()
dfPriority = df.ix[:,42:53].sort_values(by='TotalPriority',ascending=False).reset_index()
dfperPriority = df.ix[:,53:64].sort_values(by='TotalPriority',ascending=False).reset_index()
dfstPriority = df.ix[:,64:75].sort_values(by='StTotalPriority',ascending=False).reset_index()
dfED = df.ix[:,75:84].reset_index()
dfFixBlank = df.ix[:,84:95].reset_index()
dfTime = df.ix[:,95:104].sort_values(by='TotalTime',ascending=False).reset_index()

dashboard = pd.concat([dfSTprop,dfSTnum,dfHNprop,dfHNnum,dfRprop,dfRnumber,dfPriority,dfperPriority,dfstPriority,dfED,dfFixBlank,dfTime],axis=1)
del dashboard['index']

csv_file = file_path + '/%s/CleaningSummary%s_%s.csv' % (str(year),str(year),datestr)
dashboard.to_csv(csv_file)

#convert_dta_cmd = "stata -b do ConvertToStataForStudents%s.do" % (str(year))
#os.system(convert_dta_cmd)
