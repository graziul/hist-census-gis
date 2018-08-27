#
#	Name: 		misc.py
#	Authors: 	Chris Graziul
#
#	Input:		df - Data frame (autocleaning completed)
#	Output:		df - Data frame (with cleaning priority) 
#				priority - dictionary {priority:num_cases}
#				num_priority - dictionary {priority:num_sequences}
#				priority_time - processing time
#
#	Purpose:	This script assigns a manual cleaning priority for students to follow

import codecs
import sys
import re
import time
import math
import urllib
import dbf
import time
import math
import pickle
import fuzzyset
import pandas as pd
import numpy as np
from histcensusgis.microdata.street import create_cleaning_street_dict

def set_priority(df):

	start_priority = time.time()

	#Set flags for cases to be manually checked
	df['check_hn'] = df['hn_outlier2']
	df['check_st'] = ~df['overall_match_bool']
	df['check_bool'] = np.where(df['check_hn'] | df['check_st'],True,False)

	#Convert street name into numeric value (so np.diff works)
	names = np.unique(df['street_raw'])
	name_int_dict = {}
	for i in range(len(names)):
		name_int_dict[names[i]] = i
	df['enum_street'] = df['street_raw'].apply(lambda x: name_int_dict[x])

	prev = 0
	splits = np.append(np.where((np.diff(df['enum_street'].astype(np.float32)) != 0) | (np.diff(df['check_bool'].astype(np.float32)) != 0))[0],len(df['enum_street'])-1)
	splits = np.insert(splits+1,0,0)
	
	#Generator crucial for reducing memory usage (Boston at 150gb+ without it)
	enum_check_list = (np.arange(0,df['enum_street'].size+1,1)[splits[i]:splits[i+1]] for i in range(0,len(splits)-1))
	df['enum_seq'] = 0
	for i in range(len(splits)-1):
		df.iloc[list(enum_check_list.next()),'enum_seq'] = i

	#Multiple sequences of same street in single ED 
	def gen_list(x):
		t = list(np.unique(x))
		return t

	same_st_ed_dict = df.groupby(['street_raw','ed','check_bool'])['enum_seq'].apply(gen_list).to_dict()
	df['enum_seq1'] = df.apply(lambda x: min(same_st_ed_dict[x['street_raw'],x['ed'],x['check_bool']]) if (x['street_raw'] is not '') else x['enum_seq'],axis=1)
	#PROBLEM: It's tagging ALL cases in sequence, not just ones with check_bool == True??
	#CG 3/27/17: Can't find problem noted above, all cases with priority are check_st | check_hn

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
		cprint('Priority ' + str(i) + ' cases to check: ' + str(priority_counts[i]) + ' (' + str(round(100*float(priority_counts[i])/num_records,1)) + '% of all cases)')
	print('\nTotal cases to check: ' + str(sum(priority_counts.values())) + ' (' + str(round(100*float(sum(priority_counts.values()))/num_records,1)) + '%)')

	end_priority = time.time()
	priority_time = round(float(end_priority-start_priority)/60,1)
	print('Setting priority took %s \n' % (priority_time))
	priority_info = priority_counts, num_priority, priority_time

	return df, priority_info

def create_overall_match_variables(df):

	#Tabulate the fuzzy matches
	df['fuzzy_match_bool'] = np.where(df['current_match_bool'] & ~df['exact_match_bool'],True,False)

	#Make sure to include blank fixes (and changes due to house number sequences)
	try:
		df['fuzzy_match_blank_fix'] = (df['street_post_fuzzy'] == '') & (df['street_post_fuzzyHN'] != df['street_post_fuzzy'])
		df['fuzzy_match_boolHN'] = np.where(df['fuzzy_match_bool'] | df['fuzzy_match_blank_fix'],True,False)
		#Incorporate street names from blank fixing into current_match
		df.loc[df['fuzzy_match_blank_fix'],'current_match'] = df['street_post_fuzzyHN']
		df.loc[df['fuzzy_match_blank_fix'],'current_match_bool'] = True
	except:
		df['fuzzy_match_blank_fix'] = False
		df['fuzzy_match_boolHN'] = False

	#Create overall_match
	df['overall_match'] = df['current_match']
	df['overall_match_bool'] = df['current_match_bool']

	df.loc[df['overall_match_bool'],'overall_match'] = df['current_match']
	df.loc[df['fuzzy_match_boolHN'],'overall_match_type'] = 'Fuzzy'
	df.loc[df['exact_match_bool'],'overall_match_type'] = 'Exact'

	del df['current_match']
	del df['current_match_bool']

	df['st_best_guess'] = df['overall_match']
	# If no overall match, use best fuzzy match
	try:
		df.loc[df['overall_match_bool']==False,'st_best_guess'] = df['street_post_fuzzyHN']
	except:
		df.loc[df['overall_match_bool']==False,'st_best_guess'] = df['street_post_fuzzy']
	# Re-add DIR if lost somewhere along the way
	cleaned_dict = create_cleaning_street_dict(df, 'st_best_guess')
	_, df['DIR_post'], _, _ = zip(*df['st_best_guess'].apply(lambda s: cleaned_dict[s]))
	df.loc[(df['DIR'] != df['DIR_post']) & (df['DIR_post'] == ''),'st_best_guess'] = df['DIR'] + ' ' + df['st_best_guess']

	return df

def gen_dashboard_info(df, city_info, exact_info, fuzzy_info, preclean_info, times, fix_blanks_info1=None, fix_blanks_info2=None):

	city_name, state_abbr, decade = city_info
	
	#Parse exact matching info
	num_exact_matches_sm, num_noexact_matches_sm, \
	num_streets_exact_sm, num_streets_noexact_sm, \
	num_records, num_streets, \
	num_exact_matches_stgrid, num_noexact_matches_stgrid, \
	num_streets_exact_stgrid, num_streets_noexact_stgrid, \
	exact_matching_time = exact_info 
	#Calculate exact matching variables
	try:
		prop_exact_matches_sm = float(num_exact_matches_sm)/num_records
	except:
		prop_exact_matches_sm = 0
	try:
		prop_exact_matches_stgrid = float(num_exact_matches_stgrid)/num_records
	except:
		prop_exact_matches_stgrid = 0
	prop_exact_matches = prop_exact_matches_sm + prop_exact_matches_stgrid
	num_exact_matches = num_exact_matches_sm + num_exact_matches_stgrid

	#Parse fuzzy matching info
	num_fuzzy_matches, fuzzy_matching_time = fuzzy_info
	#Calculate fuzzy matching variables
	prop_fuzzy_matches = float(num_fuzzy_matches)/num_records

	if decade != 1940:
		num_street_changes1, num_blank_street_names1, \
		num_blank_street_singletons1, per_singletons1, \
		num_blank_street_fixed1, per_blank_street_fixed1, \
		blank_fix_time1 = fix_blanks_info1

		num_street_changes2, num_blank_street_names2, \
		num_blank_street_singletons2, per_singletons2, \
		num_blank_street_fixed2, per_blank_street_fixed2, \
		blank_fix_time2 = fix_blanks_info2

		blank_fix_time = blank_fix_time1 + blank_fix_time2

		num_hn_outliers1 = 	df['hn_outlier1'].sum()  
		num_hn_outliers2 = 	df['hn_outlier2'].sum() 

		num_street_changes_total = num_street_changes1 + num_street_changes2
		prop_street_changes_total = float(num_street_changes_total)/num_records

		#Have to back this out of num/prop_exact_match 
		prop_blank_street_fixed1 =	float(num_blank_street_fixed1)/num_records
		prop_blank_street_fixed2 =	float(num_blank_street_fixed2)/num_records

		num_blank_street_fixed_total = num_blank_street_fixed1 + num_blank_street_fixed2
		prop_blank_street_fixed_total = float(num_blank_street_fixed_total)/num_records


	_, _, _, preclean_time = preclean_info

	load_time,total_time = times

	'''
	problem_EDs = list(set(problem_EDs))
	print("\nProblem EDs: %s" % (problem_EDs))

	problem_EDs_present = False
	if len(problem_EDs) > 0:
		problem_EDs_present = True
	'''

	num_overall_matches = df['overall_match_bool'].sum()

	'''
	num_resid_check_st = len(df[df['check_st'] & ~df['check_hn']])
	prop_resid_check_st = float(num_resid_check_st)/num_records

	num_resid_check_hn = len(df[~df['check_st'] & df['check_hn']])
	prop_resid_check_hn = float(num_resid_check_hn)/num_records

	num_resid_check_st_hn = len(df[df['check_st'] & df['check_hn']])
	prop_resid_check_st_hn = float(num_resid_check_st_hn)/num_records
	'''

	'''
	num_resid_st = len(df[df['check_st']]) 
	prop_resid_st = float(num_resid_st)/num_records
	
	num_resid_hn_total = num_resid_check_hn + num_resid_check_st_hn
	prop_resid_hn_total = prop_resid_check_hn + prop_resid_check_st_hn

	num_resid_total = num_resid_check_st + num_resid_check_st_hn + num_resid_check_hn
	prop_resid_total = prop_resid_check_st + prop_resid_check_st_hn + prop_resid_check_hn
	'''

	header = [decade, city_name, state_abbr, num_records]
	sp = ['']

	#Old solution: Back out first blank fixing since it occurs before exact matching
	#New solution: Ignore first blank fixing since it occurs before exact matching
	if decade != 1940:
		STprop = [prop_exact_matches_stgrid, prop_fuzzy_matches, prop_blank_street_fixed2]
		STnum = [city_name, state_abbr, num_exact_matches_stgrid, num_fuzzy_matches, num_blank_street_fixed2]
		ED = [city_name, state_abbr, problem_EDs_present]
		FixBlank = [city_name, state_abbr, num_hn_outliers1, num_blank_street_names1, num_blank_street_singletons1, per_singletons1,   
			num_hn_outliers2, num_blank_street_names2, num_blank_street_singletons2, per_singletons2]
		Time = [city_name, state_abbr, load_time, preclean_time, exact_matching_time, fuzzy_matching_time, 
			blank_fix_time, priority_time, total_time]

		info = header + STprop + sp + STnum + sp + ED + sp + FixBlank + sp + Time

	else:
		num_resid = num_records - num_exact_matches - num_fuzzy_matches
		prop_resid = float(num_resid)/num_records
		STprop = [prop_exact_matches, prop_fuzzy_matches, prop_resid]
		STnum = [city_name, state_abbr, num_exact_matches, num_fuzzy_matches, num_resid]
		Time = [city_name, state_abbr, load_time, preclean_time, exact_matching_time, fuzzy_matching_time, total_time]

		info = header + STprop + sp + STnum + sp + Time

	return info

def load_cleaned_microdata(city_info, dir_path, v=7):
	city_name, state_abbr, decade = city_info
	try:
		microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAuto.dta"
		df = load_large_dta(microdata_file)
	except:
		for version in range(1,v+1)[::-1]:
			try:
				microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_AutoCleanedV" + str(version) + ".csv"
				df = pd.read_csv(microdata_file, low_memory=False)
				return df
			except:
				print("Error loading microdata for %s %s, %s" % (decade, city_name, state_abbr))
				raise

# This function replaces Matt's R script but produces exactly the same file
def create_addresses(city_info, paths, df=None):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	_, dir_path = paths
	# Load microdata file if not passed to function
	if type(df) == 'NoneType' or df == None:
		df = load_cleaned_microdata(city_info, dir_path)
	df.columns = map(str.lower, df.columns)
	# Set index variable
	df['index'] = df.index
	if decade == 1930:
		# Change name of 'block' to 'Mblk' (useful for later somehow? Matt did it)
		df.loc[:,('mblk')] = df['block']
	elif decade == 1940:
		df['mblk'] = ''
	# Choose the best available street name variable (st_best_guess includes student cleaning)
	# NOTE: When student cleaning is unavailable we should probably fill in overall_match_bool==FALSE
	#	    with street_precleanedHN, but this has not been done yet to my knowledge.
	if 'st_best_guess' in df.columns.values:
		street_var = 'st_best_guess'
	elif 'overall_match' in df.columns.values:
		street_var = 'overall_match'
	# Change '.' to blank string
	df.loc[:,'fullname'] = df[street_var]
	df.loc[df['fullname']=='.','fullname'] = ''
	# Make sure we found a street name variable
	if 'fullname' not in df.columns.values:
		print("No street name variable selected")
		raise

	# Select variables for file
	# Create ED-block
	if decade == 1930:
		vars_of_interest = ['index','fullname', 'ed','type','Mblk','hn','ed_block']
		df.loc[:,('ed_int')] = df['ed'].astype(int)
		df.loc[:,('ed_block')] = df['ed_int'].astype(str) + '-' + df['mblk'].astype(str)
		del df['ed_int']
	elif decade == 1940:
		vars_of_interest = ['index','fullname', 'ed','type','hn']

	df_add = df.loc[:,vars_of_interest]

	# Change missing and 0 to blank string
	df_add.loc[(np.isnan(df_add['hn']))|(df_add['hn']==0),'hn'] = '-1'
	df_add.loc[:,'hn'] = df_add['hn'].astype(int)
	df_add.loc[:,'hn'] = df_add['hn'].astype(str).str.replace('-1','')
	df_add.loc[:,'city'] = city_name
	df_add.loc[:,'state'] = state_abbr
	df_add.loc[:,'address'] = (df_add['hn'] + " " + df_add['fullname']).str.strip()
	# Save address file	
	addresses = dir_path + "/GIS_edited/" + city_name + "_" + str(decade) + "_Addresses.csv"
	df_add.to_csv(addresses, index=False)
