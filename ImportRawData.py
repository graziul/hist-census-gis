import unicodecsv as csv
import pandas as pd
import os, sys
from multiprocessing import Pool

csv.field_size_limit(sys.maxsize)

year = int(sys.argv[1])

file_path = '/home/s4-data/LatestCities/%s' % (str(year))

city_info_file = file_path + '/CityInfo%s.csv' % (str(year))
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df.values.tolist()

states = list(set([i[1] for i in city_info_list]))
t = dict([(i[3],i[1]) for i in city_info_list])
abbr_dict = {v:k for k,v in t.items()}

state_info_list = [[s,abbr_dict[s],[i[2] for i in city_info_list if i[1] == s],year] for s in states]

def convert_raw_to_dta(s):

	state_raw = s[0]
	state_abbr = s[1]
	city_name_list = s[2]
	year = s[3]

	raw_file_name = file_path + '/raw/Census%s_%s.txt' % (str(year),state_raw)

	with open(raw_file_name) as source:
		reader = csv.reader(source, delimiter='|')
		# Count number of cases
		for count,line in enumerate(reader,1):
		    pass
		orig_len = count-1
		# Go back to the beginning
		source.seek(0)
		# Get variable names
		header = next(reader)
		# Pull in data, but only if it has right number of variables
		if year == 1930:
			data = [row for row in reader if (row[7] in city_name_list) & (len(row) == len(header))]
		if year == 1920:
			data = [row for row in reader if (len(row) == len(header))]
		if year == 1910:	
			data = [row for row in reader if (len(row) == len(header))]
		final_len = len(data)
		if orig_len != final_len:
			print("For %s in %s there were %s cases with wrong number of variables" % (state_abbr,year,str(orig_len-final_len)))
	df = pd.DataFrame(data,columns=header)

	for c in city_name_list:
		stata_file_name = file_path + '/%s%s.dta' % (c.replace(' ',''),state_abbr)
		if year == 1930:
			df[df['self_residence_place_city']==c].to_stata(stata_file_name,encoding='utf-8')
		if year == 1920:
			df.ix[df['self_residence_place_city'].str.findall(c).nonzero()].to_stata(stata_file_name,encoding='utf-8')
		if year == 1910:
			if state_abbr == 'DC':
				df.to_stata(stata_file_name,encoding='utf-8')
			else:
				df.ix[df['ResidenceCity'].str.findall(c).nonzero()].to_stata(stata_file_name,encoding='utf-8')

pool = Pool(4)
pool.map(convert_raw_to_dta, state_info_list)
pool.close()