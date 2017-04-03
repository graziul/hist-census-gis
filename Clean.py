from multiprocessing import Pool
import pandas as pd
import sys, os, subprocess
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STclean import *
from microclean.HNclean import *
from microclean.SetPriority import *

# Version number
version = 5

# Changelog
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

def clean_microdata(city_info):

	#
	# Step 0: Initialize a bunch of variables for use throughout
	#

	city = city_info[0]
	state = city_info[1]
	year = city_info[2]
	start_total = time.time()

	city_file_name = city.replace(' ','') + state
	file_name_all = file_path + '/%s/autocleaned/%s_AutoCleaned%s.csv' % (str(year), city_file_name, 'V'+str(version))
	file_name_stata = file_path + '/%s/forstudents/%s_ForStudents%s.dta' % (str(year), city_file_name, 'V'+str(version))

 	if os.path.isfile(file_name_all) & os.path.isfile(file_name_stata):
 		print("%s is done" % (city))
 		return None

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
	init()
 	sys.stdout = open(file_path + "/%s/logs/%s_Cleaning%s.log" % (str(year), city.replace(' ','')+state, datestr),'wb')

	cprint('%s Automated Cleaning\n' % (city), attrs=['bold'], file=AnsiToWin32(sys.stdout))

	#
	# Step 1: Load city and standardize variable names
	#

	df, load_time = load_city(city.replace(' ',''), state, year)

	#
	# Step 2: Format raw street names and fill in blank street names
	#

	# Step 2a: Properly format street names and get Steve Morse street-ed information
	df, preclean_info = preclean_street(df, city, state, year)  
	sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, _ = preclean_info  

	# Step 2b: Use formatted street names to get house number sequences
	street_var = 'street_precleaned'
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df, year, street_var, debug=True)
	df['hn_outlier1'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'], s[street_var], s['hn'], ED_ST_HN_dict[street_var]),axis=1)

	# Step 2c: Use house number sequences to fill in blank street names
	df, fix_blanks_info1 = fix_blank_st(df, city, HN_SEQ, 'street_precleaned', sm_st_ed_dict)

	#
	# Step 3: Identify exact matches
	#

	# Step 3a: Import street names from 1940 street grid  
	st_grid_st_list = get_streets_from_1940_street_grid(city,state)

	# Step 3b: Identify exact matches based on Steve Morse and 1940 street grid
	df, exact_info = find_exact_matches(df, city, 'street_precleanedHN', sm_all_streets, sm_st_ed_dict, st_grid_st_list)

	#
	# Step 4: Search for fuzzy matches and use result to fill in more blank street names
	#

	# Step 4a: Search for fuzzy matches
	df, fuzzy_info = find_fuzzy_matches(df, city, 'street_precleanedHN', sm_all_streets, sm_ed_st_dict)

	# Step 4b: Use fuzzy matches to get house number sequences
	street_var = 'street_post_fuzzy'
	df[street_var] = df['street_precleanedHN']
	df.loc[df['fuzzy_match_sm_bool'],street_var] = df['fuzzy_match_sm']
	HN_SEQ_new = {}
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df, year, street_var, debug=True)
	df['hn_outlier2'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'], s[street_var], s['hn'], ED_ST_HN_dict[street_var]),axis=1)

	# Step 4c: Use house number sequences to fill in blank street names
	df, fix_blanks_info2 = fix_blank_st(df, city, HN_SEQ, 'street_post_fuzzy', sm_st_ed_dict)

	#	
	# Step 5: Create overall match and all check variables
	#

	df = create_overall_match_variables(df)
	cprint("Overall matches: "+str(df['overall_match_bool'].sum())+" of "+str(len(df))+" total cases ("+str(round(100*float(df['overall_match_bool'].sum())/len(df),1))+"%)\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	#
	# Step 6: Set priority level for residual cases
	#

	df, priority_info = set_priority(df)

	#
	# Step 7: Save full dataset and generate dashboard information 
	#

	city_file_name = city.replace(' ','') + state
	file_name_all = file_path + '/%s/autocleaned/%s_AutoCleaned%s.csv' % (str(year), city_file_name, 'V'+str(version))
	df.to_csv(file_name_all)

	end_total = time.time()
	total_time = round(float(end_total-start_total)/60,1)
	cprint("Total processing time for %s: %s\n" % (city, total_time),'cyan',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	#Generate dashbaord info
	times = [load_time, total_time]
	info = gen_dashboard_info(df, city, state, year, exact_info, fuzzy_info, preclean_info, fix_blanks_info1, fix_blanks_info2, priority_info, times)

	# Save only a subset of variables for students to use when cleaning
	df = df.replace({'check_ed' : { True : 'yes', False: ''}})

	if year==1940:
		student_vars = ['hhid','hhorder','institution','rel_id','dn','image_id','line_num','ed','hn_raw','hn','hn_flag','street_raw','street_precleanedHN','check_ed','clean_priority']
	if year==1930:
		df['street_fuzzy_match'] = ''
		df.loc[~df['overall_match_bool'],'street_fuzzy_match'] = df['fuzzy_match_sm']		
		student_vars = ['index','pid','hhid','dn','institution','block','rel_id','image_id','line_num','ed','hn_raw','hn','hn_flag','street_raw','street_precleanedHN','street_fuzzy_match','overall_match','clean_priority']

	df = df[student_vars]
	file_name_students = file_path + '/%s/forstudents/%s_ForStudents%s.csv' % (str(year), city_file_name, 'V'+str(version))
	df.to_csv(file_name_students)

	# Set do-file information
	dofile = file_path + "/ConvertCsvToDta.do"
	file_name_stata = file_path + '/%s/forstudents/%s_ForStudents%s.dta' % (str(year), city_file_name, 'V'+str(version))
	cmd = ["stata","-b","do", dofile, file_name_students, file_name_stata,"&"]
	# Run do-file
	subprocess.call(cmd) 

	# Remove .csv's
	os.remove(file_name_students)

	return info 

# Get city list
file_path = '/home/s4-data/LatestCities' 
#city_info_file = file_path + '/CityInfo.csv' 
city_info_file = file_path + '/CityInfo_with_map.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_df['city_name'] = city_info_df['city_name'].str.replace('.','')
city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()

# Get year and add it to city list information
year = int(sys.argv[1])
for i in city_info_list:                
	i.append(year)

# Farm out cleaning across multiple instances of Python
pool = Pool(processes=4, maxtasksperchild=1)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

# Build dashboard for decade and save
city_state = ['City','State']
header_names = ['Year'] + city_state + ['NumCases']
STprop_names = ['propExactMatchesSM','propExactMatchesStGrid','propFuzzyMatches','propBlankSTfixed','propResidSt']
STnum_names = city_state + ['ExactMatchesSM','propExactMatchesStGrid','FuzzyMatches','BlankSTfixed','ResidSt']
HNprop_names = city_state + ['propCheckHn','propCheckStHn','propCheckHnTotal']
HNnum_names = city_state + ['CheckHn','CheckStHn','CheckHnTotal']
Rprop_names = city_state + ['propCheckHn','propCheckStHn','propCheckSt','propCheckTotal']
Rnum_names = city_state + ['CheckHn','CheckStHn','CheckSt','CheckTotal']
Priority_names = city_state + ['100+ Cases','50-99 Cases','20-49 Cases','10-19 Cases','5-9 Cases','2-4 Cases','1 Case','TotalPriority']
perPriority_names = city_state + ['100+ Cases (%)','50-99 Cases (%)','20-49 Cases (%)','10-19 Cases (%)','5-9 Cases (%)','2-4 Cases (%)','1 Case (%)','perTotalPriority']
seqPriority_names = city_state + ['Seq 100+','Seq 50-99','Seq 20-49','Seq 10-19','Seq 5-9','Seq 2-4','Seq 1','seqTotal']
perseqPriority_names = city_state + ['Seq 100+ (%)','Seq 50-99 (%)','Seq 20-49 (%)','Seq 10-19 (%)','Seq 5-9 (%)','Seq 2-4 (%)','Seq 1 (%)','perseqTotal']
ED_names = city_state + ['ProblemEDs']
FixBlank_names = city_state + ['HnOutliers1','StreetNameBlanks1','BlankSingletons1','PerSingletons1',
	'HnOutliers2','StreetNameBlanks2','BlankSingletons2','PerSingletons2']
Time_names = city_state + ['LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime',
	'BlankFixTime','PriorityTime','TotalTime']

sp = ['']
names = header_names + STprop_names + sp + STnum_names + sp + HNprop_names + sp + HNnum_names + sp + Rprop_names + sp + Rnum_names + sp + Priority_names + sp + perPriority_names + sp + seqPriority_names + sp + perseqPriority_names + sp + ED_names + sp + FixBlank_names + sp + Time_names

df = pd.DataFrame(temp,columns=names)

dfSTprop = df.ix[:,1:10].sort_values(by='propResidSt').reset_index()
dfSTnum = df.ix[:,10:18].sort_values(by='ResidSt').reset_index()
dfHNprop = df.ix[:,18:24].sort_values(by='propCheckHnTotal').reset_index()
dfHNnum = df.ix[:,24:30].sort_values(by='CheckHnTotal').reset_index()
dfRprop =df.ix[:,30:37].sort_values(by='propCheckTotal').reset_index()
dfRnum = df.ix[:,37:44].sort_values(by='CheckTotal').reset_index()
dfPriority = df.ix[:,44:55].sort_values(by='TotalPriority').reset_index()
dfperPriority = df.ix[:,55:66].sort_values(by='perTotalPriority').reset_index()
dfseqPriority = df.ix[:,66:77].sort_values(by='seqTotal').reset_index()
dfperseqPriority = df.ix[:,77:88].sort_values(by='perseqTotal').reset_index()
dfED = df.ix[:,88:92].sort_values(by=city_state,ascending=False).reset_index()
dfFixBlank = df.ix[:,92:103].reset_index()
dfTime = df.ix[:,103:114].sort_values(by='TotalTime').reset_index()

dashboard = pd.concat([dfSTprop, dfSTnum, dfHNprop, dfHNnum, dfRprop, dfRnum, dfperPriority, dfPriority, dfseqPriority, dfperseqPriority, dfED, dfFixBlank, dfTime],axis=1)
del dashboard['index']

csv_file = file_path + '/%s/CleaningSummary%s_%s.csv' % (str(year),str(year),datestr)
dashboard.to_csv(csv_file)