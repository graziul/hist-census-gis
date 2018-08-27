#!/usr/bin/env python

from histcensusgis.microdata import *
from histcensusgis.Clean import clean_microdata

city_name = sys.argv[1]
state_abbr = sys.argv[2]
decade = sys.argv[3]
ed_map_flag = sys.argv[4]
batch = sys.argv[5]

city_info = [city_name, state_abbr, decade]
print(city_info, ed_map_flag)
if batch:
	batch_clean_microdata(int(decade))
else:
	if city_info[:2] == ["All","All"] :
		batch_clean_microdata(int(decade))
	else :
		clean_microdata(city_info=city_info, ed_map=ed_map_flag)

def batch_clean_microdata(decade, city_list_csv='CityExtractionList.csv', file_path='/home/s4-data/LatestCities'):

	# Get city list
	city_info_file = file_path + '/' + city_list_csv 
	# Parse it appropriately
	try:
		city_info_df = pd.read_csv(city_info_file)
		city_info_df = city_info_df[city_info_df['Status']>0]
		city_info_df.loc[:,'city_name'], city_info_df.loc[:,'state_abbr'] = zip(*city_info_df['City'].str.split(','))
		city_info_df.loc[:,'city_name'] = city_info_df['city_name'].str.replace('Saint','St').str.replace('.','')
		city_info_df.loc[:,'state_abbr'] = city_info_df['state_abbr'].str.replace(' ','')
		city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()
	except:
		city_info_df = pd.read_csv(city_info_file)
		city_info_df.loc[:,'city_name'] = city_info_df['city_name'].str.replace('.','')
		city_info_list = city_info_df[['city_name','state_abbr']].values.tolist()

	# 1940 issues: Only Brooklyn in 5 boroughs, no Norfolk for unknown reasons
	#exclude = ['Manhattan','Bronx','Queens','Staten Island','Norfolk']
	#city_info_list = [i for i in city_info_list if i[0] not in exclude]

	# Get decade and add it to city list information
	for i in city_info_list:
		i.append(decade)
	# Add arguments as desired
	city_info_list_w_args=[]
	for i in city_info_list:
		city_info_list_w_args.append([i])

	# Check if all raw files exist
	missing_raw = []
	for city_info in city_info_list:
		city_name, state_abbr, decade = city_info
		# Rename Staten Island, NY to Richmond, NY
		if city_name == "StatenIsland":
			c = "Richmond"
		else:
			c = city_name.replace(' ','')
		# Look for file
		file_name = c + state_abbr.upper()
		file = file_path + '/%s/%s.dta' % (str(decade), file_name)
		if os.path.exists(file):
			continue
		else:
			missing_raw.append([c, state_abbr])
	if len(missing_raw) > 0:
		for i in missing_raw:
			print("Missing %s%s.dta" % (i[0], i[1]))
		#raise ValueError
	#for i in city_info_list_w_args:
	#	clean_microdata(i[0], i[1])
	#stuff = itertools.izip(city_info_list)
	#func = partial(clean_microdata, city_info)
	pool = Pool(processes=16, maxtasksperchild=1)
	temp = pool.map(clean_microdata_w_args, city_info_list)
	pool.close()

def clean_microdata_w_args(city_info):
	clean_microdata(city_info=city_info)

	#for i in city_info_list_w_args:
	#	clean_microdata(i[0],i[1])
	# Farm out cleaning across multiple instances of Python
	#stuff = itertools.izip(city_info_list, itertools.repeat(street_source), itertools.repeat(ed_map),itertools.repeat(debug), itertools.repeat(file_path))
	#to_do_list = list(stuff)

