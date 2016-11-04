from multiprocessing import Pool
import pandas as pd
import rpy2.robjects as robjects
import sys, os
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STclean import *
from microclean.HNclean import *
from microclean.SetPriority import *

version = 2

datestr = time.strftime("%Y_%m_%d")

def clean_microdata(city_info):

	city = city_info[0]
	state = city_info[1]
	year = city_info[2]
	start_total = time.time()

	HN_SEQ = {}
	ED_ST_HN_dict = {}

	#Save to logfile
	init()
	sys.stdout = open(file_path + "/%s/logs/%s_Cleaning%s.log" % (str(year),city.replace(' ','')+state,datestr),'wb')

	cprint('%s Automated Cleaning\n' % (city), attrs=['bold'], file=AnsiToWin32(sys.stdout))

	# Load city
	df, load_time = load_city(city.replace(' ',''),state,year)

	# Pre-clean street names
	df, preclean_info = preclean_street(df,city,state,year)  
	sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, _ = preclean_info  

	# Use pre-cleaned street names to get house number sequences
	street_var = 'street_precleaned'
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var,debug=True)
	df['hn_outlier1'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

	# Use house number sequences to fill in blank street names
	df, fix_blanks_info1 = fix_blank_st(df,city,HN_SEQ,'street_precleaned',sm_st_ed_dict)

	# Get exact matches
	df, exact_info = find_exact_matches(df,city,'street_precleanedHN',sm_all_streets,sm_st_ed_dict)

	# Get fuzzy matches
	df, fuzzy_info = find_fuzzy_matches(df,city,'street_precleanedHN',sm_all_streets,sm_ed_st_dict)

	# Use fuzzy matches to get house number sequences
	street_var = 'street_post_fuzzy'
	df[street_var] = df['street_precleanedHN']
	df.loc[df['sm_fuzzy_match_bool'],street_var] = df['sm_fuzzy_match']
	HN_SEQ[street_var], ED_ST_HN_dict[street_var] = get_HN_SEQ(df,year,street_var,debug=True)
	df['hn_outlier2'] = df.apply(lambda s: is_HN_OUTLIER(s['ed'],s[street_var],s['hn'],ED_ST_HN_dict[street_var]),axis=1)

	# Use house number sequences to fill in blank street names
	df, fix_blanks_info2 = fix_blank_st(df,city,HN_SEQ,'street_post_fuzzy',sm_st_ed_dict)
	cprint("Overall matches of any kind\n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

	# Create overall match and all check variables
	df = create_overall_match_variables(df)
	cprint("Overall matches: "+str(df['overall_match_bool'].sum())+" of "+str(len(df))+" total cases ("+str(round(100*float(df['overall_match_bool'].sum())/len(df),1))+"%)\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	# Set priority level for residual cases
	df, priority_info = set_priority(df)

	# Save full dataset 
	city_file_name = city.replace(' ','') + state
	file_name_all = file_path + '/%s/autocleaned/%s_AutoCleaned%s.csv' % (str(year),city_file_name,'V'+str(version))
	df.to_csv(file_name_all)

	end_total = time.time()
	total_time = round(float(end_total-start_total)/60,1)
	cprint("\nTotal processing time for %s: %s\n" % (city,total_time),'cyan',attrs=['bold'],file=AnsiToWin32(sys.stdout))

	#Generate dashbaord info
	times = [load_time,total_time]
	info = gen_dashboard_info(df, city, state, year, exact_info, fuzzy_info, preclean_info, fix_blanks_info1, fix_blanks_info2, priority_info,times)

	# Save only a subset of variables for students to use when cleaning
	df = df.replace({'check_ed' : { True : 'yes', False: ''}})

	if year==1940:
		student_vars = ['hhid','hhorder','institution','rel_id','dn','image_id','line_num','ed','hn_raw','hn','hn_flag','street_raw','street_precleanedHN','check_ed','clean_priority']
	if year==1930:
		student_vars = ['index','pid','hhid','dn','institution','block','rel_id','image_id','line_num','ed','hn_raw','hn','hn_flag','street_raw','street_precleanedHN','clean_priority']
	
	df = df[student_vars]
	file_name_students = file_path + '/%s/forstudents/%s_ForStudents%s.csv' % (str(year),city_file_name,'V'+str(version))
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

pool = Pool(processes=8,maxtasksperchild=1)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

city_state = ['City','State']
header_names = ['Year'] + city_state + ['NumCases']
STprop_names = ['propExactMatchesValidated','propFuzzyMatches','propBlankSTfixed','propResidSt']
STnum_names = city_state + ['ExactMatchesValidated','FuzzyMatches','BlankSTfixed','ResidSt']
HNprop_names = city_state + ['propCheckHn','propCheckStHn','propCheckHnTotal']
HNnum_names = city_state + ['CheckHn','CheckStHn','CheckHnTotal']
Rprop_names = city_state + ['propCheckHn','propCheckStHn','propCheckSt','propCheckTotal']
Rnum_names = city_state + ['CheckHn','CheckStHn','CheckSt','CheckTotal']
Priority_names = city_state + ['100+ Cases','50-99 Cases','20-49 Cases','10-19 Cases','5-9 Cases','2-4 Cases','1 Case','TotalPriority']
perPriority_names = city_state + ['100+ Cases (%)','50-99 Cases (%)','20-49 Cases (%)','10-19 Cases (%)','5-9 Cases (%)','2-4 Cases (%)','1 Case (%)','perTotalPriority']
seqPriority_names = city_state + ['Seq 100+','Seq 50-99','Seq 20-49','Seq 10-19','Seq 5-9','Seq 2-4','Seq 1','seqTotal']
perseqPriority_names = city_state + ['Seq 100+ (%)','Seq 50-99 (%)','Seq 20-49 (%)','Seq 10-19 (%)','Seq 5-9 (%)','Seq 2-4 (%)','Seq 1 (%)','perseqTotal']
ED_names = city_state + ['ProblemEDs', 'ExactMatchesFailed','propExactMatchesFailed',
	'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed']
FixBlank_names = city_state + ['HnOutliers1','StreetNameBlanks1','BlankSingletons1','PerSingletons1',
	'HnOutliers2','StreetNameBlanks2','BlankSingletons2','PerSingletons2']
Time_names = city_state + ['LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime',
	'BlankFixTime','PriorityTime','TotalTime']

sp = ['']
names = header_names + STprop_names + sp + STnum_names + sp + HNprop_names + sp + HNnum_names + sp + Rprop_names + sp + Rnum_names + sp + Priority_names + sp + perPriority_names + sp + seqPriority_names + sp + perseqPriority_names + sp + ED_names + sp + FixBlank_names + sp + Time_names

df = pd.DataFrame(temp,columns=names)

dfSTprop = df.ix[:,1:9].sort_values(by='propResidSt').reset_index()
dfSTnum = df.ix[:,9:16].sort_values(by='ResidSt').reset_index()
dfHNprop = df.ix[:,16:22].sort_values(by='propCheckHnTotal').reset_index()
dfHNnum = df.ix[:,22:28].sort_values(by='CheckHnTotal').reset_index()
dfRprop =df.ix[:,28:35].sort_values(by='propCheckTotal').reset_index()
dfRnum = df.ix[:,35:42].sort_values(by='CheckTotal').reset_index()
dfPriority = df.ix[:,42:53].sort_values(by='TotalPriority').reset_index()
dfperPriority = df.ix[:,53:64].sort_values(by='perTotalPriority').reset_index()
dfseqPriority = df.ix[:,64:75].sort_values(by='seqTotal').reset_index()
dfperseqPriority = df.ix[:,75:86].sort_values(by='perseqTotal').reset_index()
dfED = df.ix[:,86:95].sort_values(by='propExactMatchesFailed',ascending=False).reset_index()
dfFixBlank = df.ix[:,95:106].reset_index()
dfTime = df.ix[:,106:117].sort_values(by='TotalTime').reset_index()

dashboard = pd.concat([dfSTprop,dfSTnum,dfHNprop,dfHNnum,dfRprop,dfRnum,dfperPriority,dfPriority,dfseqPriority,dfperseqPriority,dfED,dfFixBlank,dfTime],axis=1)
del dashboard['index']

csv_file = file_path + '/%s/CleaningSummary%s_%s.csv' % (str(year),str(year),datestr)
dashboard.to_csv(csv_file)

#convert_dta_cmd = "stata -b do ConvertToStataForStudents%s.do" % (str(year))
#os.system(convert_dta_cmd)
