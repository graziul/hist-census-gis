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
	df['check_ed'] = np.where(df['sm_exact_match_bool'] & ~df['sm_ed_match_bool'],True,False)
	df['check_bool'] = np.where(df['check_hn'] | df['check_st'] | df['check_ed'],True,False)

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

	resid_case_counts = df[['check_bool','enum_seq']].groupby(['enum_seq'])
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

	df['clean_priority'] = df['enum_seq'].apply(assign_priority)
	priority_counts = df.groupby(['clean_priority']).size().to_dict()

	end_priority = time.time()
	priority_time = round(float(end_priority-start_priority)/60,1)
	cprint('Setting priority took %s \n' % (priority_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

	return df, priority_counts, num_priority, priority_time
