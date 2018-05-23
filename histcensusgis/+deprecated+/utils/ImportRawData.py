#
#	Filename: 	ImportRawData.py
#	Author(s):	Chris Graziul
#	
#	Purpose: 	Import and save a list of cities (provided by CityInfo.csv) for later cleaning
#
#	Inputs:		year - Census decade to import (must be 1910, 1930, or 1940 currently)
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

def convert_raw_to_dta(s):

	state_raw = s[0]
	state_abbr = s[1]
	city_name_list = s[2]
	year = s[3]

	if year == 1930 and state_raw == "DistrictOfColumbia":
		state_raw = "DistrictofColumbia"

	raw_file_name = file_path + '/%s/raw/Census%s_%s.txt' % (str(year),str(year),state_raw)

	with open(raw_file_name) as source:
		reader = csv.reader(source, delimiter='|')
		# Count number of cases
#		for count,line in enumerate(reader,1):
#		    pass
#		orig_len = count-1
#		# Go back to the beginning
#		source.seek(0)
		# Get variable names
		header = next(reader)
		# Pull in data, but only if it has right number of variables
		data = [row for row in reader if (len(row) == len(header))]
		final_len = len(data)
	df = pd.DataFrame(data,columns=header)

	for c in city_name_list:
		stata_file_name = file_path + '/%s/%s%s.dta' % (str(year),c.replace(' ',''),state_abbr)
		if year == 1930:
			if c == "Staten Island":
				city_data = df[df['self_residence_place_county']=="Richmond"]
			else:
				city_data = df[df['self_residence_place_city']==c]
		# Use regex to find city names for 1910/1920 due to "Ward" and other appended to city name
		if year == 1920:
			city_data = df.ix[df['self_residence_place_city'].str.findall(c).nonzero()]
		if year == 1910:
			if state_abbr == 'DC':
				df.to_stata(stata_file_name,encoding='utf-8')
			else:
				city_data = df.ix[df['ResidenceCity'].str.findall(c).nonzero()]
		city_data.to_stata(stata_file_name,encoding='utf-8')
		# Check that population matches official Census records	
#		city_state = c + state_abbr
#		pop_year = 'pop%s' % (str(year))
#		city_pop = city_pop_dict[pop_year][city_state]
#		per_pop_diff = 100*abs((len(city_data) - city_pop)/city_pop)
#		print("Difference in population from official records for %s: %s%%" % (c,str(per_pop_diff)))
#		if per_pop_diff < 10:
#			city_data.to_stata(stata_file_name,encoding='utf-8')
#		if per_pop_diff >= 10:
#			print("Error: Difference greater than 10%")
#		return city_data
#		city_state = c + state_abbr
#		pop_year = 'pop%s' % (str(year))
#		city_pop = city_pop_dict[pop_year][city_state]
#		per_pop_diff = 100*abs((len(city_data) - city_pop)/city_pop)
#		print("Difference in population from official records for %s: %s%%" % (c,str(per_pop_diff)))
#		if per_pop_diff < 10:
#			city_data.to_stata(stata_file_name,encoding='utf-8')
#		if per_pop_diff >= 10:
#			print("Error: Difference greater than 10%")
#		return city_data

def import_year(year):
	state_info_list = [[s,state_abbr_dict[s],[i[0] for i in city_info_list if i[2] == s],year] for s in states]
	pool = Pool(4)
	pool.map(convert_raw_to_dta, state_info_list)
	pool.close()

year = int(sys.argv[1])

import_year(year)
