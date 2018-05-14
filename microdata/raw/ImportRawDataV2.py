#
#	Filename: 	ImportRawDataV2.py
#	Author(s):	Chris Graziul
#	
#	Purpose: 	- Import and save a list of cities (provided by CityInfo.csv) for later cleaning
#				- This script uses PID to merge new/old versions of 1930 data
#
#	Inputs:		year - Census decade to import (must be 1930 currently)
#				
#				CityInfo.csv - List of cities with necessary information for import 
#					Variables:
#					state_raw 	Raw state name (e.g. "Pennyslvania") for looking up raw file
#					state_abbr  State abbreviation 
#					cityname	City name
#
#				CityPop.csv - List of cities with their official (1940 Census) population for
#							  years 1880, 1900, 1910, 1920, and 1940
#					Variables:
#					state_abbr 	State abbreviation
#					cityname 	City name
#					pop1XXX		City population in year 1XXX

import unicodecsv as csv
import pandas as pd
import numpy as np
import os, sys
from multiprocessing import Pool

csv.field_size_limit(sys.maxsize)

file_path = '/home/s4-data/LatestCities' 

city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df.values.tolist()

city_pop_file = file_path + '/CityPop.csv' 
city_pop_df = pd.read_csv(city_pop_file)
city_pop_df['city_state'] = city_pop_df['City'] + city_pop_df['State']
city_pop_dict = city_pop_df.set_index('city_state').to_dict()

states = city_info_df['state_raw'].unique().tolist() 
state_abbr_dict = city_info_df.set_index('state_raw').to_dict()['state_abbr']

# Merge raw 1930 old file with crosswalk for 1930 old file

def get_old_raw(s):

	state_raw = s[0]
	state_abbr = s[1]
	city_name_list = s[2]
	year = s[3]

	# Skip if state is done
	cities_done = 0
	for c in city_name_list:
		stata_file_name = file_path + '/%s/%s%s.dta' % (str(year),c.replace(' ',''),state_abbr.upper())
		if os.path.isfile(stata_file_name):
			cities_done += 1
	if cities_done == len(city_name_list):
		return None

	if year == 1930 and state_raw == "DistrictOfColumbia":
		state_raw = "DistrictofColumbia"
		state_raw_for_crosswalk = "DistrictofColumbia"
	else:
		state_raw_for_crosswalk = state_raw

	raw_file_name = file_path + '/%s/raw/old_raw/Census%s_%s.txt' % (str(year),str(year),state_raw)

	with open(raw_file_name) as source:
		reader = csv.reader(source, delimiter='|')
		header = next(reader)
		# Pull in data, but only if it has right number of variables
		data = [row for row in reader if (len(row) == len(header))]
	df_raw = pd.DataFrame(data,columns=header)
#	df_raw.rename(columns={'histid':'mpcid'},inplace=True)

	crosswalk_file_name = file_path + '/%s/raw/1930_pid_merge/%s.csv' % (str(year),state_raw_for_crosswalk)
	with open(crosswalk_file_name) as source:
		reader = csv.reader(source, delimiter='|')
		header = next(reader)
		data = [row for row in reader]
	df_crosswalk = pd.DataFrame(data,columns=header)
	df_crosswalk['mpcid'] = df_crosswalk['mpcid'].str.upper()

	df = df_raw.merge(df_crosswalk,on='pid',how='left',indicator=True)
	print("Merging crosswalk into old raw data for %s:" % (state_raw))
	print(df[['pid','_merge']].groupby('_merge').count())
	del df['_merge']

	city_data_list = []
	for c in city_name_list:
		if year == 1930:
			if c == "Staten Island":
				city_data_list.append(df[df['self_residence_place_county']=="Richmond"])
			else:
				city_data_list.append(df[df['self_residence_place_city']==c])

	return pd.concat(city_data_list)

# Merge raw 1930 old file w/ crosswalk variables with raw 1930 new file

def merge_new_raw(s,city_data):

	state_raw = s[0]
	state_abbr = s[1]
	city_name_list = s[2]
	year = s[3]

	# Skip if state is done
	cities_done = 0
	for c in city_name_list:
		if year == 1930 and c == "Staten Island":
			c = "Richmond"
		stata_file_name = file_path + '/%s/%s%s.dta' % (str(year),c.replace(' ',''),state_abbr.upper())
		if os.path.isfile(stata_file_name):
			cities_done += 1
	if cities_done == len(city_name_list):
		return None

	for c in city_name_list:
		city = c
		if year == 1930 and c == "Staten Island":
			c = "Richmond"
		stata_file_name = file_path + '/%s/%s%s.dta' % (str(year),c.replace(' ',''),state_abbr.upper())
		if not os.path.isfile(stata_file_name):
			if year == 1930:
				if city == "Staten Island":	
					df_old = city_data[city_data['self_residence_place_county']=="Richmond"]	
				else:
					df_old = city_data[city_data['self_residence_place_city']==city]
			stata_new_raw_file_name = file_path + '/%s/raw/%s%s.dta' % (str(year),c.replace(' ',''),state_abbr.upper())
			df_new = pd.read_stata(stata_new_raw_file_name, convert_categoricals=False)
			df_new.rename(columns={'histid':'mpcid'},inplace=True)

			df = df_new.merge(df_old,on='mpcid',how='left',indicator=True)
			print("Merging new raw data for %s:" % (c))
			print(df[['mpcid','_merge']].groupby('_merge').count())
			del df['_merge']

			df = drop_repeat_vars(df,c)
			df.to_stata(stata_file_name,encoding='utf-8')

# Drop repeated variables

def drop_repeat_vars(df,c):
	variables = df.columns.values.tolist()
	variables.sort(reverse=True)
	us_vars = [i for i in variables if 'us1930d' in i]
	non_us_vars = [i for i in variables if i not in us_vars]
	non_us_vars.remove('general_block')
	# Delete "us1930d_XXXX" if idencical to another "us1930d_XXXX" variable
	print('Total "us1930d_XXXX" vars in %s: %s' % (c,str(len(us_vars))))
	for i in range(len(us_vars)):
		var1 = us_vars.pop()
		for var2 in us_vars:
			try:
				if np.array_equal(df[var1],df[var2]):
					del df[var2]
#					print("Deleted %s since it was identical to %s" % (var2,var1))
			except:
				continue
	# Delete non-"us1930d_XXXX" if idencical to another non-"us1930d_XXXX" variable
	print('Total non-"us1930d_XXXX" vars in %s: %s' % (c,str(len(non_us_vars))))
	for i in range(len(non_us_vars)):
		var1 = non_us_vars.pop()
		for var2 in non_us_vars:
			try:
				if np.array_equal(df[var1],df[var2]):
					del df[var2]
#					print("Deleted %s since it was identical to %s" % (var2,var1))
			except:
				continue	
	# Tally unique vars			
	variables = df.columns.values.tolist()
	variables.sort(reverse=True)
	us_vars = [i for i in variables if 'us1930d' in i]
	print('Unique "us1930d_XXXX" vars in %s: %s' % (c,str(len(us_vars))))
	non_us_vars = [i for i in variables if i not in us_vars]
	print('Unique non-"us1930d_XXXX" vars in %s: %s' % (c,str(len(non_us_vars))))
	# Delete "us1930d_XXXX" if identical to non-"us1930d_XXXX" variable
	for var1 in non_us_vars:
		for var2 in us_vars:
			try:
				if np.array_equal(df[var1],df[var2]):
					del df[var2]
#					print("Deleted %s since it was identical to %s" % (var2,var1))
			except:
				continue
	return df

def get_raw_data(s):
	city_data = get_old_raw(s)
	merge_new_raw(s,city_data)

year = 1930
state_info_list = [[s,state_abbr_dict[s],[i[0] for i in city_info_list if i[2] == s],year] for s in states]
il = state_info_list[8]
get_raw_data(il)
'''
state_info_list.remove(['NewYork', 'NY', ['Albany', 'Buffalo', 'Rochester', 'Syracuse', 'Yonkers', 'Brooklyn', 'Manhattan', 'Bronx', 'Queens', 'Staten Island'], year])

pool = Pool(processes=2,maxtasksperchild=1)

pool.map(get_raw_data, state_info_list)

ny = ['NewYork', 'NY', ['Albany', 'Buffalo', 'Rochester', 'Syracuse', 'Yonkers', 'Brooklyn', 'Manhattan', 'Bronx', 'Queens', 'Staten Island'], year]
get_raw_data(ny)
'''