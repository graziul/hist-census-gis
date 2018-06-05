# -*- coding: utf-8 -*-

#
# All the functions for performing block numbering (includes many things)
#

from histcensusgis.lines.street import *
from histcensusgis.points.geocode import *
from histcensusgis.s4utils.IOutils import *
import arcpy
arcpy.env.overwriteOutput = True

# Create physical blocks and block points
def create_blocks_and_block_points(city_info, paths, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD'], geocode_file=None):
	
	"""
	Creates physical blocks, geocodes addresses, then intersects geocoded points with physical blocks

	Parameters
	----------
	city_info : list
		List containing city name (e.g. "Hartford"), state abbreviation (e.g. "CT"), and decade (e.g. 1930)
	paths : list 
		List of file paths for R code, Python scripts, and data files
	hn_ranges : list (Optional)
		List of string variables naming min/max from/to for house number ranges in street grid

	Returns
	-------
	Excel file with list of streets for students to search for and (if possible) add to street grid

	"""

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# overwrite output
	arcpy.env.overwriteOutput=True

	print("The script has started to work and is running the 'street' function")

	problem_segments = grid_geo_fix(city_info, geo_path, hn_ranges)
	print("The script has finished executing the 'street' function and has now started executing 'physical_blocks' function")

	physical_blocks(city_info, geo_path)
	print("The script has finished executing the 'physical_blocks' function and has now started executing 'geocode' function")

	initial_geocode(city_info, geo_path, hn_ranges)
	print("The script has finished executing the 'geocode' function and has now started excuting 'attach_pblk_id'")

	if geocode_file != None:
		points = geocode_file
		print("Different geocode")
	else:
		points_shp = geo_path + city_name + "_" + str(decade) + "_Points.shp"

	attach_pblk_id(city_info, geo_path, points_shp)
	print("The script has finished executing the 'attach_pblk_id' function and the entire script is complete")

# Creates physical blocks shapefile 
def physical_blocks(city_info, geo_path):

	city_name, _, decade = city_info
	city_name = city_name.replace(' ','')

	pblocks = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	split_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Split.shp"

	#if int(start_from) = 1930:
	#arcpy.AddField_management(grid, 'FULLNAME', 'TEXT')
	#arcpy.CalculateField_management(grid, "FULLNAME","!Strt_Fx!", "PYTHON_9.3")

	#Create Physical Blocks# #####
	arcpy.FeatureToPolygon_management(split_grid, pblocks)
	#Add a Physical Block ID
	expression="!FID! + 1"
	arcpy.AddField_management(pblocks, "pblk_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(pblocks, "pblk_id", expression, "PYTHON_9.3")

# Attach physical block IDs to geocoded points 
def attach_pblk_id(city_info, geo_path, points_shp):

	city_name, _, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Files
	pblk_points_shp = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"
	pblocks_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"

	#Attach Pblk ids to points
	arcpy.SpatialJoin_analysis(points_shp, 
		pblocks_shp, 
		pblk_points_shp, 
		"JOIN_ONE_TO_MANY", 
		"KEEP_ALL", 
		"#", 
		"INTERSECT")
	print("The script has finished executing the 'SpatialJoin' tool")

#
# Block numbering functions
# 

# Identifies block numbers and can be run independently (R script)
# NOTE: Assigns block numbers using microdata blocks. Examines proportion of cases that geocode 
# onto the same physical block and decides  
def identify_blocks_geocode(city_info, paths, script_path):

	city_name, _, decade = city_info
	city_name = city_name.replace(' ','')

	r_path, dir_path = paths

	print("Identifying " + str(decade) + " blocks\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Identify 1930 Blocks.R',dir_path,city_name,str(decade)], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying " + str(decade) + " blocks for "+city_name+"\n")
	else:
		print("OK!\n")

# Uses block descriptions from microdata to fill in block numbers 
def identify_blocks_microdata(city_info, paths, micro_street_var='st_best_guess', v=7):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	block_file = geo_path + city_name + "_" + str(decade) + "_Block_Choice_Map.shp"
	pblk_file = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	stgrid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	pblk_grid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_Pblk_Grid_SJ.shp"
	out_file = geo_path + city_name + "_" + str(decade) + "_Block_Choice_Map2.shp"
	pblk_grid_dict_file = geo_path + city_name + "_pblk_grid_dict.pkl"
	pblk_st_dict_file = geo_path + city_name + "_pblk_st_dict.pkl"
	microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAuto.dta"
	microdata_file2 = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_AutoCleanedV" + str(v) + ".csv"

	print("Getting block description guesses\n")

	#
	# Step 1: Create "block descriptions" using microdata
	#

	#Load data
	start = time.time()
	
	try:
		df_pre = load_large_dta(microdata_file)
	except:
		df_pre = pd.read_csv(microdata_file2)
	df_pre = df_pre[['ed','block',micro_street_var]]

	end = time.time()
	run_time = round(float(end-start)/60, 1)
	print("Finished loading microdata (took " + str(run_time) + " minutes)", 'cyan')

	#TO DO: Clean up block numbers
	df_pre = df_pre[df_pre['block'].notnull() & df_pre['ed'].notnull()]
	df_pre['ed_int'] = df_pre['ed'].astype(int)
	df_pre['ed_block'] = df_pre['ed_int'].astype(str) + '-' + df_pre['block'].astype(str)
	#del df_pre['ed']
	#del df_pre['block']

	#Get number of physical blocks
	num_physical_blocks = int(arcpy.GetCount_management(block_file).getOutput(0))
	#Get number of microdata blocks
	num_micro_blocks = len(df_pre['block'].unique())

	#Create {Census block:streets} dict from microdata 
	df = df_pre.groupby(['ed_block',micro_street_var]).size().to_frame('st_addresses').reset_index()
	block_num_addresses_dict = df.groupby('ed_block').sum().to_dict().values()[0]
	df['block_addresses'] = df.apply(lambda x: block_num_addresses_dict[x['ed_block']],axis=1)
	df['prop_block'] = df['st_addresses']/df['block_addresses']
	micro_blocks_dict = {group:streets[micro_street_var].values.tolist() for group, streets in df.groupby('ed_block')}
		#TO DO: Remove blocks defined by a single street (too indeterminate)???
	print("Finished building microdata block-street dictionary")

	#
	# Step 1.5: Spatial join stgrid to pblk to get {pblk_id:[FULLNAME]} and {pblk_id:[grid_id]}
	#

	start = time.time()

	field_mapSJ = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
	FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
	grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (pblk_file, stgrid_file, stgrid_file)
	arcpy.SpatialJoin_analysis(target_features=pblk_file, join_features=stgrid_file, out_feature_class=pblk_grid_file, 
		join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
		match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
	df_pblk_grid = dbf2DF(pblk_grid_file.replace(".shp",".dbf"))

	# Group by pblk_id to create some dictionaries
	df_grouped = df_pblk_grid.groupby('pblk_id')
	# This dictionary is used here as empiric census block descriptions
	pblk_st_dict = {pblk:list(set(grid_list['FULLNAME'].tolist())) for pblk, grid_list in df_grouped}
		#Exclude certain street names "City Limits"
	exclude_list = ['City Limits']
	pblk_st_dict = {k:[i for i in v if i not in exclude_list] for k,v in pblk_st_dict.items()}
	# This dictionary is used in RenumberGrid.py to match empiric house number ranges to grid segments based on block number
	pblk_grid_dict = {pblk:list(set(grid_list['grid_id'].tolist())) for pblk, grid_list in df_grouped}
	pickle.dump(pblk_grid_dict,open(pblk_grid_dict_file,'wb'))

	end = time.time()
	run_time = round(float(end-start)/60, 1)
	print("Finished overlaying physical blocks and street grid (took " + str(run_time) + " minutes)"+"\n")

	#
	# Step 2: Now use empiric block descriptions to try to label physical blocks 
	#

	#Get block numbers already labeled in Step 1 (strict criteria)
	def extract_step1_labels(fields):
		labels_step1 = []
		pblks_labeled1 = []
		for field in fields:
			with arcpy.da.SearchCursor(block_file,['pblk_id',field]) as cursor:
				for row in cursor:
					if row[1] != ' ':
						labels_step1.append(row[1])
						pblks_labeled1.append(row[0])
		num_labels_step1 = len(labels_step1)
		per_micro_blocks = round(100*float(num_labels_step1)/num_micro_blocks, 1)
		print("Physical blocks labeled in Step 1: "+str(num_labels_step1)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")
		return labels_step1, pblks_labeled1, num_labels_step1

	#This step determines which ED-blocks to consider labeled based on prior numbering efforts
	fields = ['MBID','MBID2']
	labels_step1, pblks_labeled_step1, num_labeled_step1 = extract_step1_labels(fields)

	#Look for block description matches

	def check_block(temp):
		map_block, map_streets = temp
		matches = []
		for micro_block, microdata_streets in unknown_micro_blocks_dict.items():
			u = [i.decode('utf-8') for i in microdata_streets]
			num_matching_streets = len(set(map_streets).intersection(set(u)))
			prop_matching_map = float(num_matching_streets)/len(map_streets)
			if prop_matching_map >= thresh:
				matches.append(micro_block)	
		temp_match_dict = {}
		temp_match_dict[map_block] = matches
		return temp_match_dict

	def match_using_block_desc(pblks_labeled):
		start = time.time()
		#Ensure that physical block (1) has not been labeled already and (2) intersects streets with names
		temp_pblk_st_dict = {k:v for k,v in pblk_st_dict.items() if (int(k) not in pblks_labeled) and (len(v) > 0)}
		#Use multiprocessing to compare street lists for matching blocks
		pool = Pool(4)
		pool_results = pool.map(check_block,temp_pblk_st_dict.items())
		pool.close()
		#Convert list of dictionaries into one dictionary, as long as there is only one microdata block guess
		temp_match_dict = {k:v[0] for d in pool_results for k,v in d.items() if len(v)==1}
		temp_pblks_labeled, temp_labels = zip(*temp_match_dict.items())
		num_matches = len(temp_match_dict)
		per_micro_blocks = round(100*float(num_matches)/num_micro_blocks, 1)
		end = time.time()
		run_time = round(float(end-start)/60, 1)
		print("Matches based on block description: "+str(num_matches)+" ("+str(per_micro_blocks)+r"% of microdata blocks)")
		print("Matching took "+str(run_time)+" minutes to complete\n")
		return temp_match_dict, list(temp_pblks_labeled), list(temp_labels), num_matches

	thresh = 1
	unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1}
	exact_match_dict, pblks_labeled_exact, labels_exact, num_exact_matches = match_using_block_desc(pblks_labeled_step1)

	thresh = 0.75
	unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1+labels_exact}
	good_match_dict, pblks_labeled_good, labels_good, num_good_matches = match_using_block_desc(pblks_labeled_step1+pblks_labeled_exact)

	num_labeled_step2 = num_exact_matches+num_good_matches
	per_micro_blocks = round(100*float(num_labeled_step2)/num_micro_blocks, 1)
	print("\n"+"Physical blocks labeled by Step 2: "+str(num_labeled_step2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")

	num_labeled_steps1and2 = num_labeled_step1+num_labeled_step2
	per_micro_blocks = round(100*float(num_labeled_steps1and2)/num_micro_blocks, 1)
	print("Physical blocks labeled by Step 1 and Step 2: "+str(num_labeled_steps1and2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n")

	#Add labels 

	pblks = pblk_st_dict.keys()
	for block in pblks:
		if block not in exact_match_dict.keys():
			exact_match_dict[block] = ''
		if block not in good_match_dict.keys():
			good_match_dict[block] = ''		

	arcpy.CopyFeatures_management(block_file,out_file)
	arcpy.AddField_management(out_file,'blockdesc','TEXT')
	arcpy.AddField_management(out_file,'blockdesc2','TEXT')

	cursor = arcpy.UpdateCursor(out_file)
	for row in cursor:
		pblk_id = row.getValue('pblk_id')
		row.setValue('blockdesc',exact_match_dict[int(pblk_id)])
		row.setValue('blockdesc2',good_match_dict[int(pblk_id)])
		cursor.updateRow(row)
	del(cursor)

#
# OCR related functions (not currently used) 
#

# Uses OCR and ED map images to fill in block numbers 
def run_ocr(city_info, paths, script_path):
	city_name, _, _ = city_info
	r_path, file_path = paths
	print("Runing Matlab script\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
	if t != 0:
		print("Error running Matlab OCR script for "+city_name+"\n")
	else:
		print("OK!\n")

# Incorporates OCR block data
def integrate_ocr(city_info, paths, script_path, file_name):
	city_name, _, _ = city_info
	r_path, file_path = paths
	print("Integrating OCR block numbering results\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/MapOCRintegration.py",file_path,city_name,file_name])
	if t != 0:
		print("Error integrating OCR block numbering results for "+city_name+"\n")
	else:
		print("OK!\n")

#
# FixDirAndBlockNumsUsingMap.py
#

def fix_micro_dir_using_ed_map(city_info, paths, micro_street_var, grid_street_var, df_micro, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Files
	grid = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	ed = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	grid_ed_intersect = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_ED_intersect.shp"

	# Load files
	df_grid = load_shp(grid, hn_ranges)
	df_micro[micro_street_var+'_old'] = df_micro[micro_street_var]

	def get_dir(st):
		_, DIR, _, _ = standardize_street(st)
		return DIR

	df_grid['DIR'] = df_grid.apply(lambda x: get_dir(x[grid_street_var]), axis=1)
	save_shp(df_grid, grid)

	arcpy.Intersect_analysis (in_features=[grid, ed], 
		out_feature_class=grid_ed_intersect, 
		join_attributes="ALL")

	# Get the spatial join dbf and extract some info
	df_intersect = dbf2DF(grid_ed_intersect.replace('.shp','.dbf'))
	df_dir_ed = df_intersect[['DIR','ed']].drop_duplicates()
	df_dir_ed = df_dir_ed[df_dir_ed['DIR']!='']
	df_dir_ed = df_dir_ed[df_dir_ed['ed']!=0]
	eds = df_dir_ed['ed'].drop_duplicates().tolist()

	# Create dictionary of {ED:list(DIRs)}
	ed_dir_dict = {}
	ed_grouped = df_dir_ed.groupby(['ed'])
	for ed, group in ed_grouped:
		ed_dir_dict[ed] = group['DIR'].tolist()

	## I feel like this could be simplified significantly

	# Create dictionary of {street_var:list(DIRs)} and delete any that have combination of N/S and E/W
	df_name_dir = df_micro[[micro_street_var,'dir']]
	df_name_dir.loc[:,('st')], df_name_dir.loc[:,('dir')], df_name_dir.loc[:,('name')], df_name_dir.loc[:,('type')] = zip(*df_name_dir.apply(lambda x: standardize_street(x[micro_street_var]), axis=1))
	df_name_dir.loc[:,('st')] = (df_name_dir['name'] + ' ' + df_name_dir['type']).str.strip()
	df_name_dir = df_name_dir.drop_duplicates(['dir','st'])
	df_name_dir = df_name_dir.loc[df_name_dir['dir']!='']

	# Create dictionary of microdata streets and DIRs
	micro_st_dir_dict = {}
	st_grouped = df_name_dir.groupby(['st'])
	for st, group in st_grouped:
		micro_st_dir_dict[st] = group['dir'].tolist()
	def check_st_dirs(dirs):
		if type(dirs) is not list:
			return True
		if ('N' in dirs or 'S' in dirs) and 'W' not in dirs and 'E' not in dirs:
			return True
		if ('E' in dirs or 'W' in dirs) and 'N' not in dirs and 'S' not in dirs:
			return True
		else:
			return False
	micro_st_dir_dict = {k:v for k,v in micro_st_dir_dict.items() if check_st_dirs(v)}

	# Pre-pend DIR to select streets
	def prepend_dir(ED, street_var):
		_, DIR, NAME, TYPE = standardize_street(street_var)
		#If DIR exists, return current values
		if DIR != '':
			return DIR, street_var
		else:
			try:
				st = (NAME + ' ' + TYPE).strip()
				micro_st_dirs = micro_st_dir_dict[st]
				ed_dirs = ed_dir_dict[ED]
			#	print([st, micro_st_dirs, ed_dirs])
				#If ED has single DIR, see if street has same DIR
				if len(ed_dirs) == 1 and ed_dirs == micro_st_dirs:
					new_DIR = ed_dirs[0]
					new_street = (new_DIR + ' ' + NAME + ' ' + TYPE).strip()
			#		print(new_street)
					return new_DIR, new_street
				#If street has single DIR, see if it's in the ED
				if len(micro_st_dirs) == 1 and micro_st_dirs in ed_dirs:
					new_DIR = micro_st_dirs[0]
					new_street = (new_DIR + ' ' + NAME + ' ' + TYPE).strip()
			#		print(new_street)
					return new_DIR, new_street
				#If ED has multiple DIRs, see if 
		#		if len(ed_dirs) > 1 and micro_st_dirs:
		#		if len(micro_st_dirs) > 1 and set(micro):
				else:
					return DIR, street_var
			except:
				return DIR, street_var

	df_micro.loc[:,('dir')], df_micro.loc[:,(micro_street_var)] = zip(*df_micro.apply(lambda x: prepend_dir(x['ed'], x[micro_street_var+'_old']), axis=1))	

	# Check how many streets had DIRs pre-pended
	df_micro['changed_Dir'] = df_micro[micro_street_var] != df_micro[micro_street_var+'_old']
	print("Number of cases with DIR prepended: "+str(df_micro['changed_Dir'].sum())+" of "+str(len(df_micro))+" ("+'{:.1%}'.format(float(df_micro['changed_Dir'].sum())/len(df_micro))+") of cases")

	return df_micro

def fix_micro_blocks_using_ed_map(city_info, paths, df_micro, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Paths

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/" 

	# File names

	rand_post = str(random.randint(1,100001))
	ed_shp_file = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	temp = geo_path + "temp"+rand_post+".shp"
	add_locator_contemp = geo_path + city_name + "_addloc"
	resid_add_dbf = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.dbf"
	resid_add_csv = geo_path + city_name + "_" + str(decade) + "_Addresses_residual.csv"
	address_fields_contemp="Street address; City city; State state"
	points = geo_path + city_name + "_" + str(decade) + "_Points.shp"
	points_resid = geo_path + city_name + "_" + str(decade) + "_ResidPoints.shp"
	intersect_resid_ed = geo_path + city_name + "_" + str(decade) + "_intersect_resid_ed.shp"
	inrighted = geo_path + city_name + "_" + str(decade) + "_ResidPoints_inRightED.shp"
	intersect_correct_ed = geo_path + city_name + "_" + str(decade) + "_intersect_correct_ed.shp"
	block_shp_file = geo_path + city_name + "_" + str(decade) + "_block_ED_checked.shp"

	# Obtain residuals
	#arcpy.MakeFeatureLayer_management(points, "geocodelyr")
	#arcpy.SelectLayerByAttribute_management("geocodelyr", "NEW_SELECTION", """ "Status" <> 'M' """)
	#arcpy.CopyFeatures_management("geocodelyr",temp)
	df_points = load_shp(points, hn_ranges)
	df = df_points[df_points['Status']!='M']
	# ERROR: LOST INDEX SOMEWHERE ALONG THE WAY
	resid_vars = ['index','ed','fullname','state','city','address']
	df_resid = df[resid_vars]
	if os.path.isfile(resid_add_csv):
		os.remove(resid_add_csv)
	df_resid.to_csv(resid_add_csv)
	if os.path.isfile(resid_add_csv.replace('.csv','.dbf')):
		os.remove(resid_add_csv.replace('.csv','.dbf'))
	arcpy.TableToTable_conversion(resid_add_csv, '/'.join(resid_add_dbf.split('/')[:-1]), resid_add_dbf.split('/')[-1])
	temp_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith("temp"+rand_post)]
	for f in temp_files:
		if os.path.isfile(f):
			os.remove(f)

	# Geocode residuals using street grid with contemporary HN ranges
	arcpy.GeocodeAddresses_geocoding(resid_add_dbf, add_locator_contemp, address_fields_contemp, points_resid)

	# Intersect geocoded points with ED map
	arcpy.Intersect_analysis([ed_shp_file, points_resid], intersect_resid_ed)

	# Identify points in the correct ED
	arcpy.MakeFeatureLayer_management(intersect_resid_ed, "geocodelyr1")
	arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", """ "ed" = "ed_1" """)
	arcpy.CopyFeatures_management("geocodelyr1",inrighted)

	# Intersect points in the correct ED with block map
	arcpy.Intersect_analysis([block_shp_file, inrighted], intersect_correct_ed)

	# Get correct block number based on block map and geocoded in correct ED
	df_correct_ed = load_shp(intersect_correct_ed, hn_ranges)
	df_correct_ed['block'] = df_correct_ed['am_bn'].str.split('-').str[1:].str.join('-')
	fix_block_dict = df_correct_ed[['index','block']].set_index('index')['block'].to_dict()

	# Replace microdata block number with block map block number
	df_micro['block_old'] = df_micro['block']

	def fix_block(index, block):
		try:
			fix_block = fix_block_dict[index]
			return fix_block
		except:
			return block

	df_micro['block'] = df_micro[['index','block_old']].apply(lambda x: fix_block(x['index'], x['block_old']), axis=1)
	df_micro['changed_Block'] = df_micro['block'] != df_micro['block_old']

	print("Number of blocks changed: "+str(df_micro['changed_Block'].sum())+" of "+str(len(df_micro))+" ("+'{:.1%}'.format(float(df_micro['changed_Block'].sum())/len(df_micro))+") of cases")

	return df_micro


# Sets confidence in block number based on multpiel sources
def set_blocknum_confidence(city_info, paths):
	city_name, _, _ = city_info
	r_path, file_path = paths
	print("Setting confidence\n")
	t = subprocess.call(["python",script_path+"/blocknum/Python/SetConfidence.py",file_path,city_name])
	if t != 0:
		print("Error setting confidence for for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Functions for intersecting ED map with street grids and uploading to Rhea/CS1 Unix server
#

'''
def intersect_ed_stgrid(ed_year, map_type):

def upload_to_unix(file_path, file_name, target_path, user, pw):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.load_system_host_keys
	#ssh.load_host_keys('C:/Users/cgraziul')
	ssh.connect('rhea.pstc.brown.edu',username=user,password=pw)
	sftp = ssh.open_sftp()
	map_files = [x for x in os.listdir(file_path) if x.split('.')[0]==file_name]
	#Try to find directory, create it if it doesn't exist
	try:
		sftp.listdir(target_path)
	except IOError:
		sftp.mkdir(target_path)
	for item in map_files:
		file_name = '%s/%s' % (target_path, item)
		if os.path.isfile(os.path.join(file_path, item)):
			#Try to remove old file if it exist
			try: 
				sftp.remove(file_name)
			except IOError:
				pass
			sftp.put(os.path.join(file_path, item), file_name)
	sftp.close()
	ssh.close()

def upload_ed_stgrid(ed_year, map_type, user, pw):
	file_path = 
	file_name = 
	upload_to_unix(file_path, file_name, targeT_path, user, pw)

	for map_type in ['1940','Contemp']:
		ed_year = 1940
		upload_ed_stgrid(ed_year, map_type, XX, YY)
'''