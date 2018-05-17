#
# FixStGridNames.py
#
# Requires:	(1) A street grid
# 			(2) An ED map
#			(3) Street-EDs from cleaned Microdata
#			(4) Steve Morse
#
# NOTE: The fuzzy matching functions are based on functions in STclean.py but they are different
#
# Process: 	(1) Intersect street grid and ED map
#			(2) Load Steve Morse data
#			(3) Perform exact matching 
#			(4) Perform fuzzy matching on street-ED pairs 
#			(5) Assign correct names 

import arcpy
import os
import pickle
import fuzzyset
import pandas as pd
import pysal as ps
import numpy as np

# overwrite output
arcpy.env.overwriteOutput=True

# Function to read in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=False): 
	db = ps.open(dbfile) #Pysal to open DBF
	d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
	#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
	pandasDF = pd.DataFrame(d) #Convert to Pandas DF
	if upper == True: #Make columns uppercase if wanted 
		pandasDF.columns = map(str.upper, db.header) 
	db.close() 
	return pandasDF

# Function to save Pandas DF as DBF file 
def save_dbf(df, shapefile_name):
	csv_file = dir_path + "\\temp_for_dbf.csv"
	df.to_csv(csv_file,index=False)
	try:
		os.remove(dir_path + "\\schema.ini")
	except:
		pass
	arcpy.TableToTable_conversion(csv_file,dir_path,"temp_for_shp.dbf")
	os.remove(shapefile_name.replace('.shp','.dbf'))
	os.remove(csv_file)
	os.rename(dir_path+"\\temp_for_shp.dbf",shapefile_name.replace('.shp','.dbf'))
	os.remove(dir_path+"\\temp_for_shp.dbf.xml")
	os.remove(dir_path+"\\temp_for_shp.cpg")

c = "St Louis"
city = c.replace(' ','')
state = "MO"
year = 1930
street = 'FULLNAME'

# Paths
file_path = "S:\\Projects\\1940Census\\"
dir_path = file_path + city + "\\GIS_edited\\"

# Files
grid_uns2 =  dir_path + city + state + "_1930_stgrid_edit_Uns2.shp"
if city == "StLouis":
	ed_shp = dir_path + city + "_1930_ED.shp"
st_grid_ed_sj = dir_path + city + state + '_1930_stgrid_ED_intersect.shp'

#
# Step 1: Intersect street grid and ED map, return a Pandas dataframe of attribute data
#

#Load dataframe based on intersection of st_grid and ED map (attaches EDs to segments)
def get_grid_ed_df(grid_shp, ed_shp, st_grid_ed_sj_shp, street):

	arcpy.Intersect_analysis (in_features=[grid_shp, ed_shp], 
		out_feature_class=st_grid_ed_sj_shp, 
		join_attributes="ALL")

	df = dbf2DF(st_grid_ed_sj_shp.replace('.shp','.dbf'))

	return df

df = get_grid_ed_df(grid_uns2, ed_shp, st_grid_ed_sj, street)
df['FULLNAME'] = df['FULLNAME'].astype(str)

#
# Step 2: Load Steve Morse data
#

# Function to load Steve Morse dictionary (same as STclean.py)
def load_steve_morse(city, state, year):

	#NOTE: This dictionary must be built independently of this script
	sm_st_ed_dict_file = pickle.load(open(file_path + 'sm_st_ed_dict%s.pickle' % (str(year)), 'rb'))
	sm_st_ed_dict_nested = sm_st_ed_dict_file[(city, '%s' % (state.lower()))]

	#Flatten dictionary
	temp = {k:v for d in [v for k, v in sm_st_ed_dict_nested.items()] for k, v in d.items()}

	#Capture all Steve Morse streets in one list
	sm_all_streets = temp.keys()

	#
	# Build a Steve Morse (sm) ED-to-Street (ed_st) dictionary (dict)
	#

	sm_ed_st_dict = {}
	#Initialize a list of street names without an ED in Steve Morse
	sm_ed_st_dict[''] = []
	for st, eds in temp.items():
		#If street name has no associated EDs (i.e. street name not found in Steve Morse) 
		#then add to dictionary entry for no ED
		if eds is None:
			sm_ed_st_dict[''].append(st)
		else:
			#For every ED associated with a street name...
			for ed in eds:
				#Initalize an empty list if ED has no list of street names yet
				sm_ed_st_dict[ed] = sm_ed_st_dict.setdefault(ed, [])
				#Add street name to the list of streets
				sm_ed_st_dict[ed].append(st)

	return sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict

sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(c, state, year)
#Flatten for use elsewhere
sm_st_ed_dict = {k:v for d in [v for k, v in sm_st_ed_dict_nested.items()] for k, v in d.items()}
#For bookkeeping when validating matches using ED 
grid_all_streets = df[street].unique()
for st in grid_all_streets:
	if st not in sm_all_streets:
		sm_st_ed_dict[st] = None

#
# Step 3: Perform exact matching against Steve Morse data
#

#Function to do exact matching against Steve Morse street-ED lists (altered from STclean.py)
def find_exact_matches_sm(df, street, sm_all_streets, sm_st_ed_dict, basic_info):

	num_records, num_streets = basic_info

	# Check for exact matches between Steve Morse ST and microdata ST
	df['exact_match_bool'] = df[street].apply(lambda s: s in sm_all_streets)
	num_exact_matches_sm = np.sum(df['exact_match_bool'])
	num_noexact_matches_sm =  num_records - num_exact_matches_sm
	prop_exact_matches_sm = float(num_exact_matches_sm)/float(num_records)
	print("Cases with exact matches (Steve Morse): "+str(num_exact_matches_sm)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches_sm, 1))+"%)")

	# Keep track of unique streets that do and do not have exact matches 
	df_exact_matches_sm = df[df['exact_match_bool']]
	df_noexact_matches_sm = df[~df['exact_match_bool']]

	num_streets_exact_sm = len(df_exact_matches_sm.groupby([street]).count())
	num_streets_noexact_sm = len(df_noexact_matches_sm.groupby([street]).count())
	while num_streets_exact_sm + num_streets_noexact_sm != num_streets:
		print("Error in number of streets")
		break
	prop_exact_streets_sm = float(num_streets_exact_sm)/float(num_streets)
	print("Streets with exact matches (Steve Morse): "+str(num_streets_exact_sm)+" of "+str(num_streets)+" streets ("+str(round(100*prop_exact_streets_sm, 1))+"%)\n")

	# Compile info for later use
	exact_info_sm = [num_exact_matches_sm, num_noexact_matches_sm, 
	num_streets_exact_sm, num_streets_noexact_sm]

	return df, exact_info_sm

num_records = len(df)
num_streets = len(df.groupby([street]))
basic_info = [num_records, num_streets]

df, exact_info_sm = find_exact_matches_sm(df, street, sm_all_streets, sm_st_ed_dict, basic_info)

#
# Step 4: Perform fuzzy matchin using Steve Morse data
#

#Function to do fuzzy matching using multiple sources
def find_fuzzy_matches_sm(df, city, street, sm_all_streets, sm_ed_st_dict):

	#Fuzzy matching algorithm
	def fuzzy_match_function(street, ed, ed_st_dict, all_streets_fuzzyset, check_too_similar=False):

		nomatch = ['', '', False]
		ed = str(ed)

		#Return null if street is blank
		if street == '':
			return nomatch
		#Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
		try:
			ed_streets = ed_st_dict[ed]
			ed_streets_fuzzyset = fuzzyset.FuzzySet(ed_streets)
		except:
	#		print("Problem ED:" + str(ed))
			return nomatch

		#Step 1: Find best match among streets associated with microdata ED
		try:
			best_match_ed = ed_streets_fuzzyset[street][0]
		except:
			return nomatch

		#Step 2: Find best match among all streets
		try:
			best_match_all = all_streets_fuzzyset[street][0]
		except:
			return nomatch    
		#Step 3: If both best matches are the same, return as best match

		if (best_match_ed[1] == best_match_all[1]) & (best_match_ed[0] >= 0.5):
			#Check how many other streets in ED differ by one character
			if check_too_similar:
				too_similar = sum([diff_by_one_char(st, best_match_ed[1]) for st in sm_ed_streets])
				if too_similar == 0:
					return [best_match_ed[1], best_match_ed[0], True]
				else:
					return nomatch
			else: 
				return [best_match_ed[1], best_match_ed[0], True]
		#Step 4: If both are not the same, return one with the higher score (to help manual cleaning)
		else:
			if best_match_all[0] < best_match_ed[0]:
				return [best_match_ed[1], best_match_ed[0], False]
			else:
				return [best_match_all[1], best_match_all[0], False]

	#Helper function (necessary since dictionary built only for cases without validated exact matches)
	def get_fuzzy_match(exact_match, fuzzy_match_dict, street, ed):
		#Only look at cases without validated exact match
		if not (exact_match):
			#Need to make sure "Unnamed" street doesn't get fuzzy matched
			if 'Unnamed' in street:
				return ['', '', False]
			#Get fuzzy match    
			else:
				return fuzzy_match_dict[street, ed]
		#Return null if exact validated match
		else:
			return ['', '', False]

	#Function to update current best match (starts with either exact_match or '')
	def update_current_match(current_match, current_match_bool, new_match, new_match_bool):
		if ~current_match_bool and new_match_bool:
			return new_match, new_match_bool
		else:
			return current_match, current_match_bool

	start = time.time()

	#Get Steve Morse fuzzy matches
	df['current_match'] = ''
	df['current_match_bool'] = df['exact_match_bool']
	df.loc[df['current_match_bool'],'current_match'] = df['FULLNAME']
	
	#Set var names
	fuzzy_match = 'fuzzy_match' 
	fuzzy_bool = 'fuzzy_match_bool'
	fuzzy_score = 'fuzzy_match_score'

	#Initialize fuzzy_match_bool
	df[fuzzy_bool] = False

	#Create all street fuzzyset only once
	sm_all_streets_fuzzyset = fuzzyset.FuzzySet(sm_all_streets)

	#Create dictionary based on Street-ED pairs for faster lookup using helper function
	df_no_exact_match = df[~(df['current_match_bool'])]
	df_grouped = df_no_exact_match.groupby([street, 'ed'])
	fuzzy_match_dict = {}
	for st_ed, _ in df_grouped:
		fuzzy_match_dict[st_ed] = fuzzy_match_function(st_ed[0], st_ed[1], sm_ed_st_dict, sm_all_streets_fuzzyset)

	#Compute current number of residuals
	num_records = len(df)
	num_current_residual_cases = num_records - len(df[df['current_match_bool']])
	#Get fuzzy matches 
	df[fuzzy_match], df[fuzzy_score], df[fuzzy_bool] = zip(*df.apply(lambda x: get_fuzzy_match(x['current_match_bool'], fuzzy_match_dict, x[street], x['ed']), axis=1))
	#Update current match 
	df['current_match'], df['current_match_bool'] = zip(*df.apply(lambda x: update_current_match(x['current_match'], x['current_match_bool'], x[fuzzy_match], x[fuzzy_bool]),axis=1))

	#Generate dashboard information
	num_fuzzy_matches = np.sum(df[fuzzy_bool])
	prop_fuzzy_matches = float(num_fuzzy_matches)/num_records
	end = time.time()
	fuzzy_matching_time = round(float(end-start)/60, 1)
	fuzzy_info_sm = [num_fuzzy_matches, fuzzy_matching_time]

	print("Fuzzy matches (using Steve Morse): "+str(num_fuzzy_matches)+" of "+str(num_current_residual_cases)+" unmatched cases ("+str(round(100*float(num_fuzzy_matches)/float(num_current_residual_cases), 1))+"%)\n")

	return df, fuzzy_info_sm

df, fuzzy_info_sm = find_fuzzy_matches_sm(df, city, street, sm_all_streets, sm_ed_st_dict)
print("Total matched: " + str(df['current_match_bool'].sum()) + " accounting for " + '{:.1%}'.format(float(df['current_match_bool'].sum())/len(df)) + " of ED-segment combinations")


#
# Step 5: For remaining cases, use original FULLNAME
#

df.loc[~df['current_match_bool'],'current_match'] = df[street]

#
# Step 6: Create dictionary for fixing street names
#

### Keep in mind that Amory's algorithm will handle missing DIR

# NEED TO USE GRID_ID SO CAN ASSIGN TO UNS2!
df_grouped = df.groupby([street, 'ed'])
fullname_ed_st_dict = {}
more_than_one = 0
for fullname_ed, group in df_grouped:
	list_of_streets = group['current_match'].drop_duplicates().tolist()
	if len(list_of_streets) > 1:
		more_than_one += 1
	else:
		fullname_ed_st_dict[fullname_ed] = list_of_streets[0]
if more_than_one > 0:
	print("Some entries have more than one street")



#
# Step 6: Reconcile streets that stradle ED borders
#

df_grouped_grid_id = df.groupby(['grid_id'])

grid_id 




