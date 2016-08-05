import unicodecsv as csv
import pandas as pd
import os
from multiprocessing import Pool

year = 1930

file_path = '/home/s4-data/LatestCities/1930' % (year)

city_info_file = file_path + '/CityInfo%s.csv' (year)
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df.values.tolist()
city_info_list.remove(['Philadelphia','Pennsylvania','Philadelphia','PA','phpa'])
city_info_list.remove(['Richmond', 'NewYork', 'Staten Island', 'NY', 'riny'])

def convert_raw_to_dta(city_info):

	city_no_spaces = city_info[0].lower()
	state_raw = city_info[1]
	city_name = city_info[2]
	state_abbr = city_info[3]

	raw_file_name = file_path + '/raw/Census1930_%s.txt' % (state_raw)
	stata_file_name = file_path + '/%s%s.dta' % (city_no_spaces,state_abbr)

	if not os.path.isfile(stata_file_name):
		with open(raw_file_name) as source:
			reader = csv.reader(source, delimiter='|')
			header = next(reader)
			data = [row for row in reader if row[7]==city_name]
	df = pd.DataFrame(data,columns=header)
	df.to_stata(stata_file_name,encoding='utf-8')

pool = Pool(4)
pool.map(convert_raw_to_dta, city_info_list)
pool.close()