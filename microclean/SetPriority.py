#
#	Name: 		SetPriority.py
#	Authors: 	Chris Graziul
#
#	Input:		df - Data frame (autocleaning completed)
#	Output:		df - Data frame (with cleaning priority) 
#				priority - dictionary {priority:num_cases}
#				num_priority - dictionary {priority:num_sequences}
#				priority_time - processing time
#
#	Purpose:	This script assigns a manual cleaning priority for students to follow

import time, sys
import pandas as pd
import numpy as np
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

def set_priority(df):

	start_priority = time.time()

	df['check_hn'] = df['hn_outlier2']
	df['check_st'] = ~df['overall_match_bool']
#	df['check_ed'] = np.where(df['sm_exact_match_bool'] & ~df['sm_ed_match_bool'],True,False)
#	df['check_bool'] = np.where(df['check_hn'] | df['check_st'] | df['check_ed'],True,False)
	df['check_bool'] = np.where(df['check_hn'] | df['check_st'],True,False)
	df['enum_seq'] = 0

	#Convert street name into numeric value (so np.diff works)
	names = np.unique(df['street_raw'])
	name_int_dict = {}
	for i in range(len(names)):
		name_int_dict[names[i]] = i
	df['enum_street'] = df['street_raw'].apply(lambda x: name_int_dict[x])

	prev = 0
	splits = np.append(np.where((np.diff(df['enum_street']) != 0) | (np.diff(df['check_bool']) != 0))[0],len(df['enum_street'])-1)
	splits = np.insert(splits+1,0,0)
	
	#Generator crucial for reducing memory usage (Boston at 150gb+ without it)
	enum_check_list = (np.arange(0,df['enum_street'].size+1,1)[splits[i]:splits[i+1]] for i in range(0,len(splits)-1))

	for i in range(len(splits)-1):
		df.ix[list(enum_check_list.next()),'enum_seq'] = i

	#Multiple sequences of same street in single ED 
	def gen_list(x):
		t = list(np.unique(x))
		return t

	same_st_ed_dict = df.groupby(['street_raw','ed','check_bool'])['enum_seq'].apply(gen_list).to_dict()
	df['enum_seq1'] = df.apply(lambda x: min(same_st_ed_dict[x['street_raw'],x['ed'],x['check_bool']]) if (x['street_raw'] is not '') else x['enum_seq'],axis=1)
	#PROBLEM: It's tagging ALL cases in sequence, not just ones with check_bool == True??

	resid_case_counts = df[['check_bool','enum_seq1']].groupby(['enum_seq1'])
	enum_seq_counts_dict = resid_case_counts.size().to_dict()
	enum_seq_check_dict = resid_case_counts['check_bool'].mean().to_dict()


	#	Clean_priority: 
	#
	#	1 = >100 cases in sequence (either HN or ST)
	#	2 = >50 cases in sequence (either HN or ST)
	#	3 = >20 cases in sequence (either HN or ST)
	#	4 = >10 cases in sequence (either HN or ST)
	#	5 = >5 cases in sequence (either HN or ST)
	# 	6 = >1 case in sequence (either HN or ST)
	#	7 = 1 case in sequence (either HN or ST)

	def assign_priority(enum):
		count = enum_seq_counts_dict[enum]
		check = enum_seq_check_dict[enum]
		if check:
			if count == 1:
				priority = 7	
			if count > 1:
				priority = 6	
			if count >= 5:
				priority = 5
			if count >= 10:
				priority = 4
			if count >= 20:
				priority = 3	
			if count >= 50:
				priority = 2																				
			if count >= 100:
				priority = 1
		else:
			priority = None		
		return priority	

	priority = {}
	for enum,_ in resid_case_counts:
		priority[enum] = assign_priority(enum)
 
	num_priority = {}
	for i in range(1,8):
		num_priority[i] = len([k for k,v in priority.items() if v == i])

	df['clean_priority'] = df['enum_seq1'].apply(assign_priority)

	priority_counts = df.groupby(['clean_priority']).size().to_dict()
	for i in range(1,8):
		try:
			priority_counts[i]
		except KeyError:
			priority_counts[i] = 0

	num_records = len(df)
	for i in range(1,8):
		cprint('Priority ' + str(i) + ' cases to check: ' + str(priority_counts[i]) + ' (' + str(round(100*float(priority_counts[i])/num_records,1)) + '% of all cases)',file=AnsiToWin32(sys.stdout))
	cprint('\nTotal cases to check: ' + str(sum(priority_counts.values())) + ' (' + str(round(100*float(sum(priority_counts.values()))/num_records,1)) + '%)','red',file=AnsiToWin32(sys.stdout))

	end_priority = time.time()
	priority_time = round(float(end_priority-start_priority)/60,1)
	cprint('Setting priority took %s \n' % (priority_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))
	priority_info = priority_counts, num_priority, priority_time

	return df, priority_info

def create_overall_match_variables(df,street_post_fuzzy=None):
	if street_post_fuzzy is None:
		street_post_fuzzy = 'street_post_fuzzy'
	try:
		post = '_' + street_post_fuzzy.split('_')[3].split('HN')[0]
	except:
		post = ''

	df['sm_fuzzy_match_blank_fix'+post] = (df[street_post_fuzzy] == '') & (df[street_post_fuzzy+'HN'] != df[street_post_fuzzy])
	df['sm_fuzzy_match_bool'+post+'HN'] = np.where(df['sm_fuzzy_match_bool'+post] | df['sm_fuzzy_match_blank_fix'+post],True,False)

	df['overall_match'+post] = ''
	df['overall_match_type'+post] = ''
	df['overall_match_bool'+post] = False

	df.loc[df['sm_fuzzy_match_bool'+post+'HN'],'overall_match'+post] = df['street_post_fuzzy'+post+'HN']
#	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match'] = df['street_precleanedHN']
	df.loc[df['sm_exact_match_bool'+post],'overall_match'+post] = df['street_precleaned'+post+'HN']

	df.loc[df['sm_fuzzy_match_bool'+post+'HN'],'overall_match_type'+post] = 'Fuzzy'
#	df.loc[df['sm_exact_match_bool'] & df['sm_ed_match_bool'],'overall_match_type'] = 'ExactSM'
	df.loc[df['sm_exact_match_bool'+post],'overall_match_type'+post] = 'Exact'

	df.loc[(df['overall_match_type'+post] == 'Exact') | (df['overall_match_type'+post] == 'Fuzzy'),'overall_match_bool'+post] = True 

	return df

def gen_dashboard_info(df, city, state, year, exact_info, fuzzy_info, preclean_info, fix_blanks_info1, fix_blanks_info2, priority_info, times):

	num_records, num_passed_validation, prop_passed_validation, num_failed_validation, prop_failed_validation, num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation, exact_matching_time = exact_info 
	num_fuzzy_matches, prop_fuzzy_matches, fuzzy_matching_time, problem_EDs = fuzzy_info
	num_street_changes1, num_blank_street_names1, num_blank_street_singletons1, per_singletons1, num_blank_street_fixed1, per_blank_street_fixed1, blank_fix_time1 = fix_blanks_info1
	num_street_changes2, num_blank_street_names2, num_blank_street_singletons2, per_singletons2, num_blank_street_fixed2, per_blank_street_fixed2, blank_fix_time2 = fix_blanks_info2
	sm_all_streets, sm_st_ed_dict, sm_ed_st_dict, preclean_time = preclean_info
	priority_counts, num_priority, priority_time = priority_info
	load_time,total_time = times

	blank_fix_time = blank_fix_time1 + blank_fix_time2

	problem_EDs = list(set(problem_EDs))
	print("\nProblem EDs: %s" % (problem_EDs))

	problem_EDs_present = False
	if len(problem_EDs) > 0:
		problem_EDs_present = True

	num_overall_matches = df['overall_match_bool'].sum()

	num_hn_outliers1 = 	df['hn_outlier1'].sum()  
	num_hn_outliers2 = 	df['hn_outlier2'].sum() 

	num_resid_check_st = len(df[df['check_st'] & ~df['check_hn']])
	prop_resid_check_st = float(num_resid_check_st)/num_records

	num_resid_check_hn = len(df[~df['check_st'] & df['check_hn']])
	prop_resid_check_hn = float(num_resid_check_hn)/num_records

	num_resid_check_st_hn = len(df[df['check_st'] & df['check_hn']])
	prop_resid_check_st_hn = float(num_resid_check_st_hn)/num_records

	num_street_changes_total = num_street_changes1 + num_street_changes2
	prop_street_changes_total = float(num_street_changes_total)/num_records

	#Have to back this out of num/prop_exact_match (e.g. prop_passed_validation + prop_failed_validation)
	prop_blank_street_fixed1 =	float(num_blank_street_fixed1)/num_records

	num_blank_street_fixed_total = num_blank_street_fixed1 + num_blank_street_fixed2
	prop_blank_street_fixed_total = float(num_blank_street_fixed_total)/num_records

	num_resid_st = len(df[df['check_st']]) 
	prop_resid_st = float(num_resid_st)/num_records

	num_resid_hn_total = num_resid_check_hn + num_resid_check_st_hn
	prop_resid_hn_total = prop_resid_check_hn + prop_resid_check_st_hn

	num_resid_total = num_resid_check_st + num_resid_check_st_hn + num_resid_check_hn
	prop_resid_total = prop_resid_check_st + prop_resid_check_st_hn + prop_resid_check_hn

	header = [year, city, state, num_records]
	#Back out first blank fixing since it occurs before exact matching
	STprop = [prop_passed_validation+prop_failed_validation-prop_blank_street_fixed1, 
		prop_fuzzy_matches, prop_blank_street_fixed_total, prop_resid_st]
	#Back out first blank fixing since it occurs before exact matching
	STnum = [city, state, num_passed_validation+num_failed_validation-num_blank_street_fixed1, 
		num_fuzzy_matches, num_blank_street_fixed_total, num_resid_st]
	HNprop = [city, state, prop_resid_check_hn, prop_resid_check_st_hn, prop_resid_hn_total]
	HNnum = [city, state, num_resid_check_hn, num_resid_check_st_hn, num_resid_hn_total]
	Rprop = [city, state, prop_resid_check_hn, prop_resid_check_st_hn, prop_resid_check_st, prop_resid_total]
	Rnum = [city, state, num_resid_check_hn, num_resid_check_st_hn, num_resid_check_st, num_resid_total]
	Priority = [city, state, priority_counts[1],priority_counts[2],priority_counts[3],priority_counts[4],priority_counts[5],priority_counts[6],priority_counts[7],sum(priority_counts.values())]
	perPriority = [city, state, float(priority_counts[1])/num_records,
		float(priority_counts[2])/num_records,
		float(priority_counts[3])/num_records,
		float(priority_counts[4])/num_records,
		float(priority_counts[5])/num_records,
		float(priority_counts[6])/num_records,
		float(priority_counts[7])/num_records,float(sum(priority_counts.values()))/num_records]
	seqPriority = [city, state, num_priority[1],num_priority[2],num_priority[3],num_priority[4],num_priority[5],num_priority[6],num_priority[7],sum(num_priority.values())]
	num_seqs = len(np.unique(df['enum_seq1']))
	perseqPriority = [city, state, float(priority_counts[1])/num_seqs,
		float(num_priority[2])/num_seqs,
		float(num_priority[3])/num_seqs,
		float(num_priority[4])/num_seqs,
		float(num_priority[5])/num_seqs,
		float(num_priority[6])/num_seqs,
		float(num_priority[7])/num_seqs,float(sum(num_priority.values()))/num_seqs]
	ED = [city, state, problem_EDs_present, num_failed_validation, prop_failed_validation, 
		num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation]
	FixBlank = [city, state, num_hn_outliers1, num_blank_street_names1, num_blank_street_singletons1, per_singletons1,   
		num_hn_outliers2, num_blank_street_names2, num_blank_street_singletons2, per_singletons2]
	Time = [city, state, load_time, preclean_time, exact_matching_time, fuzzy_matching_time, 
		blank_fix_time, priority_time, total_time]

	sp = ['']
	info = header + STprop + sp + STnum + sp + HNprop + sp + HNnum + sp + Rprop + sp + Rnum + sp + Priority + sp + perPriority + sp + seqPriority + sp + perseqPriority + sp + ED + sp + FixBlank + sp + Time

	return info
