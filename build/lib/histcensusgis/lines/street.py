#
# Name: street.py 
#
# Contents: Functions primarily associated with the street grid 
#

from histcensusgis.s4utils.AmoryUtils import *
from histcensusgis.s4utils.IOutils import *
from histcensusgis.text.standardize import *
from histcensusgis.text.stevemorse import *
from histcensusgis.microdata.misc import *
from histcensusgis.lines.hn import *
import os
import fuzzyset
import arcpy
arcpy.env.overwriteOutput=True

# Workhorse function for converting raw street grids into standardized street grids
def process_raw_grid(city_info, geo_path, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	"""
	Code to "fix up" street grid geometry (and duplicate ranges)

	Steps involved: 
		a) Dissolves multi-part street segments
		b) Splits on intersections
		c) Calls fix_dup_address_ranges

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
	[CITY][ST]_[DECADE]_stgrid_edit_Uns2.shp : ESRI shapefile
		Fixed street grid
	problem_segments : list
		List of street segments with multiple names of same length (arises from multi-part segments)

	"""

	#Create filenames to be used throughout process

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	#NOTE: By defualt we are starting with 1940 cleaned grids then saving them as 19X0 grids!	
	grid = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit.shp"
	grid_orig = "S:/Projects/1940Census/DirAdd/" + city_name + state_abbr + "_1940_stgrid_diradd.shp"
	dissolve_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Dissolve.shp"
	split_grid = geo_path + city_name + "_" + str(decade) + "_stgrid_Split.shp"
	grid_uns = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns.shp"
	grid_uns2 = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"

	#Create copy of "diradd" file to use as grid
	if not os.path.isfile(grid):
		if not os.path.isfile(grid_orig):
			print("%s%s_1940_stgrid_diradd.shp not found" % (city_name, state_abbr))
		else:
			arcpy.CopyFeatures_management(grid_orig, grid)

	#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MIN replace with big number
	codeblock_min = """def replace(x):
		if x == ' ':
			return 999999
		else:
			return x"""
	fieldName = "LFROMADD"
	expression = "replace(!LFROMADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

	fieldName = "RFROMADD"
	expression = "replace(!RFROMADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

	#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MAX replace with small number
	codeblock_max = """def replace(x):
		if x == ' ':
			return -1
		else:
			return x"""
	fieldName = "LTOADD"
	expression = "replace(!LTOADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

	fieldName = "RTOADD"
	expression = "replace(!RTOADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

	#First Dissolve to create split_grid (no multi-part segments, split at intersections)
	arcpy.Dissolve_management(grid, split_grid, 
		multi_part="SINGLE_PART", 
		unsplit_lines="DISSOLVE_LINES")

	#Add a unique, static identifier (so ranges can be changed later)
	expression="!FID! + 1"
	arcpy.AddField_management(split_grid, "grid_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(split_grid, "grid_id", expression, "PYTHON_9.3")

	#Intersect with grid
	temp = geo_path + "temp_step.shp"
	arcpy.CopyFeatures_management(grid, temp)
	arcpy.Intersect_analysis([temp, split_grid], grid)
	arcpy.DeleteFeatures_management(temp)

	#Second Dissolve St_Grid lines
	arcpy.Dissolve_management(in_features=grid, 
		out_feature_class=grid_uns, 
		dissolve_field="grid_id", 
		statistics_fields="LFROMADD MIN;LTOADD MAX;RFROMADD MIN;RTOADD MAX", 
		unsplit_lines="UNSPLIT_LINES")

	#Get the longest street name from multi-part segments
	df_grid = load_shp(grid, hn_ranges)
	longest_name_dict = {}
	problem_segments = {}
	for grid_id, group in df_grid.groupby(['grid_id']):
		max_chars = group['FULLNAME'].str.len().max()
		longest_name = group.loc[group['FULLNAME'].str.len()==max_chars,'FULLNAME'].drop_duplicates().tolist()
		if len(longest_name) > 1:
			problem_segments[grid_id] = longest_name
		# Always returns first entry in longest name (a list of names equal in length to max_chars)
		longest_name_dict[grid_id] = longest_name[0]

	#Assign longest street name by grid_id (also add city and state for geolocator)
	df_grid_uns = load_shp(grid_uns, hn_ranges)
	df_grid_uns.loc[:,'CITY'] = city_name
	df_grid_uns.loc[:,'STATE'] = state_abbr
	df_grid_uns.loc[:,'FULLNAME'] = df_grid_uns.apply(lambda x: longest_name_dict[x['grid_id']], axis=1)

	#Blank out the big/small numbers now that aggregation is done

	# Function to blank out big/small numbers
	def replace_nums(x):
		if x == "999999" or x == "-1":
			return ' '
		else:
			return x

	for field in hn_ranges:
		df_grid_uns[field] = df_grid_uns[field].astype(str)
		df_grid_uns[field] = df_grid_uns.apply(lambda x: replace_nums(x[field]), axis=1)

	save_shp(df_grid_uns, grid_uns)

	#Add a unique, static identifier (so ranges can be changed later)
	arcpy.DeleteField_management(grid_uns, "grid_id")
	expression="!FID! + 1"
	arcpy.AddField_management(grid_uns, "grid_id", "LONG", 10, "", "","", "", "")
	arcpy.CalculateField_management(grid_uns, "grid_id", expression, "PYTHON_9.3")

	#Fix duplicate address ranges
	t = fix_dup_address_ranges(grid_uns,hn_ranges)
	print(t)

	return problem_segments

# Check for streets not in grid 
def check_for_streets_not_grid(city_info, geo_path, df, grid_shp, df_street_var='st_best_guess', df_ed_var='ed', grid_street_var='FULLNAME'):

	"""
	Get street names in microdata but not in street grid

	Compares microdata street names to grid street names, returns names in former but not latter.

	Parameters
	----------
	city_info : list
		List containing city name (e.g. "Hartford"), state abbreviation (e.g. "CT"), and decade (e.g. 1930)
	geo_path : str
		Path to GIS files
	df : Pandas dataframe
		Dataframe that includes street names
	grid_shp : str
		Filename (including path) to street grid shapefile
	df_street_var : str (Optional)
		Variable in Pandas dataframe containing street names 
	df_ed_var : str (Optional)
		Variable in Pandas dataframe containing ED numbers
	grid_street_var : str (Optional)
		Variable in street grid shapefile containing street names

	Returns
	-------
	Excel file with list of streets for students to search for and (if possible) add to street grid

	"""

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Load grid dataframe
	df_grid = load_shp(grid_shp)
	# Get street list from grid
	grid_streets_list = df_grid[grid_street_var].drop_duplicates().tolist()

	# Get street-ED combinations from df 
	df_st_ed = df.loc[df[df_street_var]!='.',[df_street_var,df_ed_var]]
	df_microdata_st_ed = df_ungeocoded_st_ed.groupby([df_street_var,df_ed_var]).size().reset_index(name='count')
	# Select ungeocoded streets not in grid
	df_st_ed_tocheck = df_st_ed[~df_st_ed[df_street_var].isin(grid_streets_list)].sort_values([df_ed_var])
	# Remove streets with <50 people on them
	thresh = 50
	temp = df_st_ed_tocheck.groupby(df_street_var)['count'].aggregate(sum) >= thresh
	temp = temp.reset_index(name='select_street')
	st_list = temp.loc[temp['select_street'],df_street_var].tolist()
	df_st_ed_tocheck_final = df_st_ed_tocheck[df_st_ed_tocheck[df_street_var].isin(st_list)]

	# Create a Pandas Excel writer using XlsxWriter as the engine.
	file_name = geo_path + '/' + city_name + state_abbr + '_' + str(decade) + '_st_not_in_grid'+post+'.xlsx'
	writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
	# Convert the dataframe to an XlsxWriter Excel object.
	df_st_ed_tocheck_final.to_excel(writer, sheet_name='Missing from grid', index=False)
	# Close the Pandas Excel writer and output the Excel file.
	writer.save()

# Process street grid and return list of streets in microdata but not grid
def get_missing_streets(city_info, paths):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')

	_, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'
	
	# Load microdata 	
	df = load_cleaned_microdata(city_info, dir_path)

	# Return streets missing from grid
	grid_uns2 = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	check_for_streets_not_grid(city_info=city_info, geo_path=geo_path, df=df, grid_shp=grid_uns2)

# Find consecutive segments
def find_consecutive_segments(grid_shp, grid_street_var, debug_flag=False):

	"""
	Find consecutive street segments

	Employs a number of methods to identify consecutive line segments composing the same street

	Parameters
	----------
	grid_shp : ESRI shapefile
		Filename for street grid
	grid_street_var : str
		City name, no spaces
	debug_flag : bool (Optional)
		Flag for debugging 

	Returns
	-------
	name_sequence_dict : dictionary
		??
	exact_next_dict : dictionary
		??

	"""

	fields = arcpy.ListFields(grid_shp)

	for f in fields :
		if f.type == "OID" :
			fid_var = f.name

	#This should be the new standard for segment IDs:
	fid_var = "grid_id"

	field_names = [x.name for x in fields]


	#Return all unique values of field found in table
	def unique_values(table, field):
		with arcpy.da.SearchCursor(table, [field]) as search_cursor:
			return sorted({row[0] for row in search_cursor})

	#Returns just the NAME and TYPE components of the street phrase, if any#
	def remove_st_dir(st) :
		if (st == None or st == '' or st == ' ' or st == -1) or not (isinstance(st, str) or isinstance(st, unicode)) :
			return "" #.shp files do not support NULL !!!
		else :
			DIR = re.search("^[NSEW]+ ",st)
			if(DIR) :
				DIR = DIR.group(0)
				st = re.sub("^"+DIR, "",st)
				DIR = DIR.strip()
			st = st.strip()
			return st

	#function to make sure fids aren't accidentally looping through nexts
	#returns True if there is no loop. fnd = fid_next_dict
	def test_fid_loop(fnd,fid) :
		n = fid
		for i in range(0,len(fnd.keys())+1) :
			
			try :
				n = fnd[n]
			except KeyError :
				return True
			except TypeError :
				pass #BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD
			if n == fid :
				return False
		if debug_flag: print("ran out of fids?")
		return False

	#returns a tuple of lists comprising all discrete runs of consequent FIDs. fnd = fid_next_dict
	def find_fid_runs(fnd) :
		run_starts = [x for x in fnd.keys() if not x in fnd.values()]
		runs = ()
		if len(run_starts) == 0 :
			if debug_flag: print("FIDS ARE A LOOP AND WE CAN TELL FROM TRYING TO FIND RUNS!")
		for f in run_starts :
			runs += (fid_run_recurse(fnd, f),)
		return runs
	#recursion function called by find_fid_runs
	def fid_run_recurse(fnd, fid) :
		#if fid == None :
		#    return []
		try :
			next_fid = fnd[fid]
		except KeyError :
			return [fid]
		except TypeError :
			return [fid]
		else :
			return [fid]+fid_run_recurse(fnd,next_fid)

	#given a graph in the form of a dict: node -> [child_nodes]
	#return a list containing the nodes of the longest possible path
	#from a start node to an end 
	def longest_path(G) :
		keys = G.keys()
		values = []
		for v in G.values() :
			if isinstance(v,list) :
				values += v
			else :
				values.append(v)
		starts = set([x for x in keys if not x in values])
		ends = set([x for x in values if not x in keys])
		Gd = dict(G)
		#create new dict structure with entries for child vertices (v) and whether
		#current node is "discovered" (d)
		for k in Gd.keys() :
			if not isinstance(Gd[k],list) :
				Gd[k] = [Gd[k]]
			Gd[k] = {'v':Gd[k],'d':False}
		for e in ends :
			Gd[e] = {'v':[],'d':False}
		paths = []
		for s in starts :
			paths.append(depth_first_search(dict(Gd),s))
		return max(paths,key=len)
	#recursive search function called by longest_path
	def depth_first_search(G,v) :
		Gd = copy.deepcopy(G)
		#create an entirely new data structure in memory so that nodes' "discovered" 
		#values do not propagate backward to parent nodes!
		Gd[v]['d'] = True
		longest_subpath = []
		subpaths = []
		for n in Gd[v]['v'] :
			if not Gd[n]['d'] :
				subpaths.append(depth_first_search(Gd,n))
		if not subpaths == [] :
			longest_subpath = max(subpaths,key=len)
		return [v]+longest_subpath

	def fill_addr_gaps(grid_shp) :
		pass
		#Chris is working on this...

	# converts a stname -> [fid_sequence] dict into a fid -> [prev_fid, next_fid] dict
	def flatten_seq_dict(name_sequence_dict) :
		fid_prevnext_dict = {}
		for name, seq in name_sequence_dict.items() :
			for ind, fid in enumerate(seq) :
				if ind == 0 :
					prev_fid = None
				else :
					prev_fid = seq[ind-1]
				if ind == len(seq) - 1 :
					next_fid = None
				else :
					next_fid = seq[ind+1]
				fid_prevnext_dict[fid] = [prev_fid,next_fid]
		return fid_prevnext_dict

	#assumes that name_sequence_dict was created with ignore_dir = True
	def consec_to_arc(grid_shp,name_sequence_dict,exact_next_dict) :
		fid_prevnext_dict = flatten_seq_dict(name_sequence_dict)
		#try : arcpy.AddField_management (grid_shp, "flipLine", "SHORT"); except : pass
		with arcpy.da.UpdateCursor(grid_shp, [fid_var,"consecPrev","consecNext","exact_Prev",
										  "exact_Next"]) as up_cursor:
			for row in up_cursor :
				fid = row[0]
				try :
					prev_next = fid_prevnext_dict[fid]
				except KeyError :
					continue
				if debug_flag: print("row: "+str(row))
				row[1] = prev_next[0]
				row[2] = prev_next[1]
				try :
					if debug_flag: print("prev_next: "+str(prev_next))
					row[3] = exact_next_dict[prev_next[0]] == fid
				except KeyError :
					row[3] = False
				try :
					row[4] = exact_next_dict[fid] == prev_next[1]
				except KeyError :
					row[4] = False
				up_cursor.updateRow(row)

	#have to pass in a .shp
	#include_non_exact: True or False
	#logic: organize streets one stname at a time
	#       first find exactly consequent segments
	#       then, separately, decide about inexact consequent segments

	#ignore_dir determines whether streets with only differing directions are considered
	#the same street for purposes of determining consecutive-ness:
	def get_consecutive(grid_shp,include_non_exact = True,ignore_dir = True) :

		debug = True
		
		arcpy.AddGeometryAttributes_management(grid_shp, "LINE_START_MID_END")
		try :
			arcpy.AddField_management (grid_shp, "consecPrev", "TEXT")
			arcpy.AddField_management (grid_shp, "consecNext", "TEXT")
			arcpy.AddField_management (grid_shp, "exact_Prev", "SHORT")
			arcpy.AddField_management (grid_shp, "exact_Next", "SHORT")
		except :
			pass #just for debugging, as any .shp having this done will not have these fields
		fields = arcpy.ListFields(grid_shp)
		field_names = [x.name for x in fields]
		name_sequence_dict = {} #dict: st_name -> sequential list of FIDs for all segments with st_name
		name_sequence_spur_dict = {} #same format as name_sequence_dict, but comprising spurs and other segments that connect to main sequence
		#how do we account for two different groups of segs with same name when include_non_exact is False?
		exact_next_dict = {}
		if debug_flag: print("field_names"+str(field_names))
		if ignore_dir :
			arcpy.AddField_management (grid_shp, "name_type", "TEXT")
			with arcpy.da.UpdateCursor(grid_shp, [grid_street_var,"name_type"]) as up_cursor:
				for row in up_cursor :
					row[1] = remove_st_dir(row[0])
					up_cursor.updateRow(row)
			unique_names = unique_values(grid_shp,"name_type")
			name_var = "name_type"
		else :
			unique_names = unique_values(grid_shp,grid_street_var)
			name_var = grid_street_var
		
		for name in unique_names :
			fid_coord_dict = {}
			if name != " " and name != "City Limits" :
				name_grid_shp = name+"_lyr"
				name = name.replace("'","''") #replace apostrophe in name with two apostrophes (SQL-specific syntax)
				arcpy.MakeFeatureLayer_management(grid_shp,name_grid_shp,name_var+" = '"+name+"'")
				num_name_segments = int(arcpy.GetCount_management(name_grid_shp).getOutput(0))
				if debug_flag: 
					print("examining "+str(num_name_segments)+" segments named "+name)
				if num_name_segments > 1 : #if more than 1 st segment with name
					next_fid_list = []#fids that should be considered for next of another segment
					all_fid_list = []
					with arcpy.da.SearchCursor(name_grid_shp, [fid_var,'START_X', 'START_Y', 'END_X', 'END_Y']) as s_cursor :
						for row in s_cursor :
							#populate dict of fid -> coordinates_dict
							all_fid_list.append(row[0])
							next_fid_list.append(row[0])
							fid_coord_dict[row[0]] = {}
							fid_coord_dict[row[0]]['START_X'] = row[1]
							fid_coord_dict[row[0]]['START_Y'] = row[2]
							fid_coord_dict[row[0]]['END_X'] = row[3]
							fid_coord_dict[row[0]]['END_Y'] = row[4]
					with arcpy.da.UpdateCursor(name_grid_shp, [fid_var,"consecPrev","consecNext",
														   "exact_Prev","exact_Next",grid_street_var]) as up_cursor:
						next_fid_linked_list = {} #dict: fid -> fid of next segment(s)
						prev_fid_linked_list = {} #dict: fid -> fid of prev segment
						coord_diff_start = {} #keeps track of the segment that is spatially closest to cur_seg
						coord_diff_end = {}#for purposes of tracking down inexact next and prev segments
						singleton_segments = ()
						found_cyclic_loop = False
						fork_segs = [] #not used
						merge_segs = []#not used
						fid_fullname_dict = {}
						for row in up_cursor :
							cur_fid = row[0]
							cur_seg = fid_coord_dict[cur_fid]
							startx = round(cur_seg['START_X'],6) # Assuming units=decimal degrees,
							starty = round(cur_seg['START_Y'],6) #this rounds to roughly the
							endx = round(cur_seg['END_X'],6) # nearest inch.
							endy = round(cur_seg['END_Y'],6) # i.e. negligible (but necessary. Because Arc.)
							coord_diff_start[cur_fid] = []
							coord_diff_end[cur_fid] = []
							fid_fullname_dict[cur_fid] = row[5]
							found_exact_prev = False
							found_exact_next = False
							next_fid_candidates = []
							prev_fid_candidates = []
							for fid, seg in fid_coord_dict.items() :
								if not cur_fid == fid :#no segment can be the next or prev of itself...
									if round(seg['END_X'],6) == startx and round(seg['END_Y'],6) == starty : #found exact prev
										found_exact_prev = True
										prev_fid_candidates.append(fid)
									#print("cur_fid - endx: "+str(endx)+" endy:   "+str(endy)+" ("+str(fid)+")")
									#print("fid -  START_X: "+str(seg['START_X'])+" START_Y: "+str(seg['START_Y']))
									if round(seg['START_X'],6) == endx and round(seg['START_Y'],6) == endy : #found exact next
										if found_exact_next :
											### cur_fid is the last segment before a fork:
											###            \ /
											###             |  <- cur_fid
											###             ^
											if debug_flag:print(str(cur_fid)+" has multiple exact nexts!")
											fork_segs.append(cur_fid)#not used
										found_exact_next = True
										try :
											next_fid_list.remove(fid)
										except ValueError :
											### cur_fid is the last segment before a merge:
											###             ^
											###             |
											###            / \  <- cur_fid
											if debug_flag:print("an exact next is already the exact next of something else")
											merge_segs.append(fid)#not used
											
										next_fid_candidates.append(fid)
									#record distance of start and end coordinates relative to start and end of cur_seg:
									end_end_diff = math.sqrt((seg['END_X'] - endx)**2 + (seg['END_Y'] - endy)**2)
									end_start_diff = math.sqrt((seg['START_X'] - endx)**2 + (seg['START_Y'] - endy)**2)
									coord_diff_end[cur_fid].append((min(end_end_diff,end_start_diff), fid))
									start_end_diff = math.sqrt((seg['END_X'] - startx)**2 + (seg['END_Y'] - starty)**2)
									start_start_diff = math.sqrt((seg['START_X'] - startx)**2 + (seg['START_Y'] - starty)**2)
									coord_diff_start[cur_fid].append((min(start_end_diff,start_start_diff), fid))
							if not found_exact_prev and not found_exact_next :
								singleton_segments += ([cur_fid],)
							else :
								if len(prev_fid_candidates) == 1 :
									prev_fid_linked_list[cur_fid] = prev_fid_candidates[0]
								if len(prev_fid_candidates) > 1 :
									prev_fid_linked_list[cur_fid] = prev_fid_candidates
								if len(next_fid_candidates) == 1 :
									next_fid_linked_list[cur_fid] = next_fid_candidates[0]
								if len(next_fid_candidates) > 1 :
									next_fid_linked_list[cur_fid] = next_fid_candidates
							
							
						if test_fid_loop(next_fid_linked_list,fid) :
							pass
						else :
							if debug_flag: 
								print("Cyclic Loop detected.")
								print("Name of segments: "+name)
								print("FIDs of segments: "+str(all_fid_list))
							found_cyclic_loop = True
							#TODO: store this info somewhere?

						cur_longest_path = []
						
						if not found_cyclic_loop :
							if not next_fid_linked_list == {} :
								#PROBLEM:#PROBLEM:#PROBLEM: 
								#PROBLEM:#PROBLEM:#PROBLEM: test_fid_loop does not support lists in next_fid_linked_list
								#PROBLEM:#PROBLEM:#PROBLEM:
								#PROBLEM:#PROBLEM:#PROBLEM: CURRENTLY THIS IS BEING SILENCED WITH AN except TypeError!!!!
								#PROBLEM:#PROBLEM:#PROBLEM: instead, should change longest_path to detect cycles
								#PROBLEM:#PROBLEM:#PROBLEM:
								cur_longest_path = longest_path(next_fid_linked_list)
								if debug_flag:
									print("next_fid_linked_list is: "+str(next_fid_linked_list))
									print("longest path is: "+str(cur_longest_path))
									print("FIDs not in longest path: "+str([x for x in all_fid_list if not x in cur_longest_path]))

								#modify next_fid_linked_list to conform to longest_path
								for k,v in dict(next_fid_linked_list).items() :
									if k in cur_longest_path :
										if isinstance(v,list) :
											next_fid_linked_list[k] = cur_longest_path[cur_longest_path.index(k)+1]

							else :
								if debug_flag: print("no exact consecutive segments exist for "+name)

							street_is_too_messed_up = False
							for k, v in next_fid_linked_list.items() :
								if isinstance(v, list) :
									if debug_flag:
										print("There is a fork on a non-central path for the street "+name)
										print("This is not currently supported. Goodbye.")
									street_is_too_messed_up = True
									break
							if street_is_too_messed_up :
								continue

							exact_next_dict = dict(copy.deepcopy(next_fid_linked_list), **exact_next_dict)
							
							#determine if segments that do not have an exact next/prev should have an inexact next/prev:
							#start segment is somewhere in next_fid_list
							#first, break down entire sequence of street segments into contiguous runs:
							#then create a dict of possible connections (which will include end segment->start segment. we do not want this.)

							runs = find_fid_runs(next_fid_linked_list)
							runs += singleton_segments

							if debug_flag: print("runs: "+str(runs))

							#set aside runs that are spurs/forks of cur_longest_path
							#they will not be considered as candidates for inexact next/prev
							for run in tuple(runs) :
								if not run == cur_longest_path :
									longest_path_overlap = [x for x in run if x in cur_longest_path]
									if not longest_path_overlap == [] :
										temp = list(runs)
										temp.remove(run)
										runs = tuple(temp)
										for x in longest_path_overlap :
											run.remove(x)
										Dict_append_unique(name_sequence_spur_dict,name,run)
										for x in run :
											del next_fid_linked_list[x]
										if debug_flag: print("added the spur "+str(run)+" to aux dict")       

							possible_connexions = {}
							for s_run in runs :
								for e_run in runs :
									if s_run != e_run :
										Dict_append_unique(possible_connexions,e_run[-1],s_run[0])
							if debug_flag: print("possible_connexions: "+str(possible_connexions))
							#cumbersome magic to organize and sort the distances of each gap for which we want to (maybe)
							#make a connexion based on the dicts created prior:
							dist_fid_list = []
							for k in possible_connexions.keys() :
								coord_diff_start_list = []
								coord_diff_end_list = []
								for v in possible_connexions[k] :
									coord_diff_start_list.append(list(filter(lambda x: x[1]==v, coord_diff_start[k])))
									coord_diff_end_list.append(list(filter(lambda x: x[1]==v, coord_diff_end[k])))
								shortest_gap = min(sorted(coord_diff_start_list)[0],sorted(coord_diff_end_list)[0])
								if isinstance(shortest_gap,list) and len(shortest_gap) > 0:
									if debug_flag:print("shortest_gap is a list (yes, this is still happening)")
									shortest_gap = shortest_gap[0]
								elif debug_flag:print("shortest_gap is NOT a list (not happening all the time)")

								shortest_gap += (k,)
								dist_fid_list.append(shortest_gap)
							
							#deal with cycles in inexact next gaps (this only applies to two-fid cycles)
							### have to find when there is a cycle in dist_fid_list 
							### when we have a cycle, we should remove the cyclic connexion that interferes with another connexion
							
							def deal_with_dist_fid_cycles() :
								dist_fid_cycles = []
								#identify cyclic gaps in dist_fid_list
								for i in range(0,len(dist_fid_list)-1) :
									for j in range(i+1,len(dist_fid_list)) :
										if dist_fid_list[i][1]==dist_fid_list[j][2] and dist_fid_list[i][2]==dist_fid_list[j][1] :
											dist_fid_cycles.append(dist_fid_list[i])
											dist_fid_cycles.append(dist_fid_list[j])
											break
								#isolate cyclic gaps from the rest of dist_fid_list
								for i in dist_fid_cycles :
									dist_fid_list.remove(i)
								if debug_flag: print("dist_fid_cycles: "+str(dist_fid_cycles))
								for i in dist_fid_list :
									#iterate over a copy of dist_fid_cycles so we can modify the original
									for j in list(dist_fid_cycles) :
										if i[1] == j[1] and i[2] != j[2] :
											#set distance to impossibly high value for the bad gap in the cycle
											dist_fid_cycles.remove(j)
											dist_fid_cycles.append((99999,)+j[1:])
											if debug_flag: print(str(j)+" was a bad egg cuz of "+str(i))
								for j in dist_fid_cycles :
									#add values back to list
									dist_fid_list.append(j)
									
							deal_with_dist_fid_cycles()

							dist_fid_list = sorted(dist_fid_list)
												
							if debug_flag: print("now, dist_fid_list is: "+str(dist_fid_list))
							while len(dist_fid_list) > 1 :
								connexion = dist_fid_list.pop(0)
								if debug_flag:print("checking connexion "+str(connexion))
								check_for_cycles_linked_list = dict(next_fid_linked_list)
								check_for_cycles_linked_list[connexion[2]] = connexion[1]
								if test_fid_loop(check_for_cycles_linked_list,connexion[2]) :
									#only create the connection if it does not create a cyclical loop
									next_fid_linked_list[connexion[2]] = connexion[1]
							if debug_flag:
								if len(dist_fid_list) :     
									print(name +": the last connexion (which was not made) was "+str(dist_fid_list[0]))
								else :
									print(name+" had no inexact connexions")
								
							#reconstruct order of segments and store in name_sequence_dict
							start_fid = [x for x in next_fid_linked_list.keys() if not x in next_fid_linked_list.values()]
							if debug_flag:
								wtf = [x for x in next_fid_linked_list.values() if not x in next_fid_linked_list.keys()]
								print(name+": "+str(start_fid)+ " -> "+str(wtf))
								print("fid_fullname_dict: "+str(fid_fullname_dict))
							runs = find_fid_runs(next_fid_linked_list)
							if debug_flag:print("runs: "+str(runs))
							run_namefreq_dict={}
							for run in runs :
								run_namefreq_dict[tuple(run)] = {}
								for fid in run :
									fullname = fid_fullname_dict[fid]
									if not fullname in run_namefreq_dict[tuple(run)].keys() :
										run_namefreq_dict[tuple(run)][fullname] = 1
									else :
										run_namefreq_dict[tuple(run)][fullname] += 1

							for run in run_namefreq_dict.keys() :
								if debug_flag:print(str(run)+": "+str(run_namefreq_dict[run]))
								most_common_name = max(run_namefreq_dict[run],key=run_namefreq_dict[run].get)

								Dict_append_flexible(name_sequence_dict, most_common_name, list(run))
		print("Finished.")
		return name_sequence_dict,exact_next_dict

	### Unresolved Issues ###

	# Broadway :
	# --<--|--<--|--<--|-->--|-->--|-->--
	#   6     5     4     1     2     3

	name_sequence_dict, exact_next_dict = get_consecutive(grid_shp)

	return name_sequence_dict, exact_next_dict

# Fix street grid names using microdata
def grid_names_fix(city_info, paths, micro_street_var, grid_street_var, df_micro=None, v=7, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	"""
	Fix street grid names 

	Uses Microdata and Steve Morse to 'fix' street grid names. In reality, it harmonizes for consistency.

	Parameters
	----------
	city_info : list
		List containing city name (e.g. "Hartford"), state abbreviation (e.g. "CT"), and decade (e.g. 1930)
	paths : list
		List of paths to script and file locations
	micro_street_var : str
		Name of street variable from microdata (e.g. 'overall_match')
	grid_street_var : str
		Name of street variable in grid (e.g. 'FULLNAME')
	df_micro : Pandas dataframe (Optional)
		Microdata to use, if you want to specify. Searches for studauto or latest autoclean, otherwise.
	v : int (Optional)
		Version of autoclean to use, set to 7 by default.
	hn_ranges : list (Optional)
		List of string variables naming min/max from/to for house number ranges in street grid

	Returns
	-------
	Uns2 is returned, with old street names saved in a new variable and 'fixed' street names included
	
	"""

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	# Paths
	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	# Files
	grid_uns2 =  geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	grid_uns2_backup = grid_uns2.replace('.shp','prefix.shp')
	if city_name == "StLouis":
		ed_shp = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	st_grid_ed_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_ED_intersect.shp'

	arcpy.CopyFeatures_management(grid_uns2, grid_uns2_backup)

	#
	# Step 1: Intersect street grid and ED map, return a Pandas dataframe of attribute data
	#

	#Load dataframe based on intersection of st_grid and ED map (attaches EDs to segments)

	def get_grid_ed_df(grid_shp, ed_shp, st_grid_ed_shp, hn_ranges):

		arcpy.Intersect_analysis (in_features=[grid_shp, ed_shp], 
			out_feature_class=st_grid_ed_shp, 
			join_attributes="ALL")

		df = load_shp(st_grid_ed_shp, hn_ranges)

		return df

	df_grid_ed = get_grid_ed_df(grid_uns2, ed_shp, st_grid_ed_shp, hn_ranges)
	df_grid_ed[grid_street_var] = df_grid_ed[grid_street_var].astype(str)

	#
	# Step 2: Load microdata
	#

	# Load microdata
	df_micro = load_cleaned_microdata(city_info, dir_path)

	# Convert to string
	df_micro[micro_street_var] = df_micro[micro_street_var].astype(str)

	# Get list of all streets
	micro_all_streets = df_micro[micro_street_var].drop_duplicates().tolist()

	# Create ED-street dictionary for fuzzy matching
	micro_ed_st_dict = {str(ed):group[micro_street_var].drop_duplicates().tolist() for ed, group in df_micro.groupby(['ed'])}

	#
	# Step 3: Load Steve Morse data 
	#

	sm_all_streets, _, sm_ed_st_dict = load_steve_morse(city_spaces, state_abbr, decade, dir_path)

	#
	# Step 4: Perform exact matching
	#

	#Initialize the current match variable
	df_grid_ed['current_match'] = ''
	df_grid_ed['current_match_bool'] = False

	#Function to update current best match (starts with either exact_match or '')
	def update_current_match(current_match, current_match_bool, new_match, new_match_bool, fullname=None):
		if ~current_match_bool and new_match_bool:
			if fullname == None:
				return new_match, True
			# Check if it's just an issue of missing DIR in either case
			else:
				_, DIR_old, NAME_old, TYPE_old = standardize_street(fullname)
				_, DIR_new, NAME_new, TYPE_new = standardize_street(new_match)
				if NAME_old == NAME_new:
					# Same NAME, different TYPE, same DIR
					if (TYPE_old != TYPE_new) & (DIR_old == DIR_new):
						new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_new).strip()
					# Same NAME, same TYPE, different DIR
					if (TYPE_old == TYPE_new) & (DIR_old != DIR_new):
						if DIR_old == '':
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
						if DIR_new == '':
							new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_old).strip()
						else:
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
					# Same NAME, different TYPE, different DIR
					if (TYPE_old != TYPE_new) & (DIR_old != DIR_new):
						if DIR_old == '':
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_new).strip()
						if DIR_new == '':
							new_match = (DIR_old + ' ' + NAME_old + ' ' + TYPE_new).strip()
						else:
							new_match = (DIR_new + ' ' + NAME_old + ' ' + TYPE_old).strip()
				# No conditional for different NAME, assume new_match is correct
				return new_match, True
			return new_match, True
		else:
			return current_match, current_match_bool

	#Function to do exact matching against Steve Morse street-ED lists (altered from STclean.py)
	def find_exact_matches(df, street, all_streets, basic_info, source):

		num_records, num_streets = basic_info

		exact_match = 'exact_match_' + source
		exact_bool = 'exact_match_bool_' + source

		# Check for exact matches, return True if exact match
		df[exact_match] = ''
		df[exact_bool] = df[street].apply(lambda s: s in all_streets)
		df.loc[df[exact_bool], exact_match] = df[street]
		# Update current match variables
		df['current_match'], df['current_match_bool'] = zip(*df.apply(lambda x: update_current_match(x['current_match'], x['current_match_bool'], x[exact_match], x[exact_bool]),axis=1))

		num_exact_matches = np.sum(df['current_match_bool'])
		num_noexact_matches =  num_records - num_exact_matches
		prop_exact_matches = float(num_exact_matches)/float(num_records)
		print("Cases with exact matches ("+source+"): "+str(num_exact_matches)+" of "+str(num_records)+" cases ("+str(round(100*prop_exact_matches, 1))+"%)")

		# Keep track of unique streets that do and do not have exact matches 
		df_exact_matches = df[df['current_match_bool']]
		df_noexact_matches = df[~df['current_match_bool']]

		num_streets_exact = len(df_exact_matches.groupby([street]).count())
		num_streets_noexact = len(df_noexact_matches.groupby([street]).count())
		while num_streets_exact + num_streets_noexact != num_streets:
			print("Error in number of streets")
			break
		prop_exact_streets = float(num_streets_exact)/float(num_streets)
		print("Streets with exact matches ("+source+"): "+str(num_streets_exact)+" of "+str(num_streets)+" streets ("+str(round(100*prop_exact_streets, 1))+"%)\n")

		# Compile info for later use
		exact_info = [num_exact_matches, num_noexact_matches, num_streets_exact, num_streets_noexact]

		return df, exact_info

	num_records = len(df_grid_ed)
	num_streets = len(df_grid_ed.groupby([grid_street_var]))
	basic_info = [num_records, num_streets]

	df_grid_ed, exact_info_micro = find_exact_matches(df=df_grid_ed, 
		street=grid_street_var, 
		all_streets=micro_all_streets, 
		basic_info=basic_info, 
		source="micro")

	#
	# Step 5: Perform fuzzy matching
	#

	#Function to do fuzzy matching using multiple sources
	def find_fuzzy_matches(df, city, street, all_streets, ed_st_dict, source):

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
			#	print("Problem ED:" + str(ed))
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

		#Set var names
		fuzzy_match = 'fuzzy_match_'+source 
		fuzzy_bool = 'fuzzy_match_bool_'+source
		fuzzy_score = 'fuzzy_match_score_'+source

		#Create all street fuzzyset only once
		all_streets_fuzzyset = fuzzyset.FuzzySet(all_streets)

		#Create dictionary based on Street-ED pairs for faster lookup using helper function
		df_no_exact_match = df[~df['current_match_bool']]
		df_grouped = df_no_exact_match.groupby([street, 'ed'])
		fuzzy_match_dict = {}
		for st_ed, _ in df_grouped:
			fuzzy_match_dict[st_ed] = fuzzy_match_function(st_ed[0], st_ed[1], ed_st_dict, all_streets_fuzzyset)

		#Compute current number of residuals
		num_records = len(df)
		num_current_residual_cases = num_records - len(df[df['current_match_bool']])
		#Get fuzzy matches 
		df[fuzzy_match], df[fuzzy_score], df[fuzzy_bool] = zip(*df.apply(lambda x: get_fuzzy_match(x['current_match_bool'], fuzzy_match_dict, x[street], x['ed']), axis=1))
		#Update current match 
		df['current_match'], df['current_match_bool'] = zip(*df.apply(lambda x: update_current_match(x['current_match'], x['current_match_bool'], x[fuzzy_match], x[fuzzy_bool], x[street]),axis=1))

		#Generate dashboard information
		num_fuzzy_matches = np.sum(df[fuzzy_bool])
		prop_fuzzy_matches = float(num_fuzzy_matches)/num_records
		fuzzy_info = [num_fuzzy_matches]

		print("Fuzzy matches (using "+source+"): "+str(num_fuzzy_matches)+" of "+str(num_current_residual_cases)+" unmatched cases ("+str(round(100*float(num_fuzzy_matches)/float(num_current_residual_cases), 1))+"%)")

		return df, fuzzy_info

	df_grid_ed, fuzzy_info_micro = find_fuzzy_matches(df=df_grid_ed, 
		city=city_name, 
		street=grid_street_var, 
		all_streets=micro_all_streets, 
		ed_st_dict=micro_ed_st_dict, 
		source="micro")

	df_grid_ed, fuzzy_info_sm = find_fuzzy_matches(df=df_grid_ed, 
		city=city_name, 
		street=grid_street_var, 
		all_streets=sm_all_streets, 
		ed_st_dict=sm_ed_st_dict, 
		source="sm")

	df_grid_ed.loc[:,('fuzzy_match_bool')] = df_grid_ed['fuzzy_match_bool_sm'] | df_grid_ed['fuzzy_match_bool_micro']
	total_fuzzy_matches = df_grid_ed['fuzzy_match_bool'].sum()
	print("Total fuzzy matched: " + str(total_fuzzy_matches) + " of " + str(len(df_grid_ed[~df_grid_ed['exact_match_bool_micro']])) + " (" + '{:.1%}'.format(float(total_fuzzy_matches)/len(df_grid_ed[~df_grid_ed['exact_match_bool_micro']])) + ") ED-segment combinations without an exact match\n")

	total_matches = df_grid_ed['current_match_bool'].sum()
	print("Total matched: " + str(total_matches) + " of " + str(num_records) + " (" + '{:.1%}'.format(float(total_matches)/len(df_grid_ed)) + ") ED-segment combinations")

	#
	# Step 6: Create dictionary for fixing street names
	#

	df_grouped = df_grid_ed.groupby([grid_street_var, 'ed'])
	fullname_ed_st_dict = {}
	more_than_one = 0
	for fullname_ed, group in df_grouped:
		if group['current_match_bool'].any():
			no_match = False
			st = group['current_match'].drop_duplicates().tolist()[0]
		else:
			no_match = True
			st = group[grid_street_var].drop_duplicates().tolist()[0]
		fullname_ed_st_dict[fullname_ed] = {st:zip(group['grid_id'].tolist(),[no_match]*len(group))}
	grid_id_st_dict = {grid_id:v.keys()[0] for k,v in fullname_ed_st_dict.items() for grid_id in v.values()[0]}
	grid_id_st_dict = {k[0]:[v,k[1]] for k,v in grid_id_st_dict.items()}

	#
	# Step 7: Fix street names and save
	#

	df_uns2 = load_shp(grid_uns2, hn_ranges)
	df_uns2[grid_street_var+'_old'] = df_uns2[grid_street_var]

	# Need to do this because missing grid_id numbers in grid_id_st_dict (which is bad)
	def fix_fullname(grid_id, FULLNAME):
		try:
			new_FULLNAME, nomatch = grid_id_st_dict[grid_id]
			if FULLNAME == new_FULLNAME:
				return [new_FULLNAME, nomatch]
			else:
				return [new_FULLNAME, nomatch]	
		except:
			return [FULLNAME, True]

	df_uns2[grid_street_var], df_uns2['NoMatch'] = zip(*df_uns2.apply(lambda x: fix_fullname(x['grid_id'],x['FULLNAME']), axis=1))

	# Fill in with old name if no match and switch name change to reflect
	df_uns2.loc[df_uns2['NoMatch'], grid_street_var] = df_uns2[grid_street_var+'_old']
	# Count number of changes
	df_uns2.loc[:,('NameChng')] = df_uns2[grid_street_var+'_old'] != df_uns2[grid_street_var]

	print("Number of street names changed: "+str(df_uns2['NameChng'].sum())+" of "+str(len(df_uns2))+" ("+'{:.1%}'.format(float(df_uns2['NameChng'].sum())/len(df_uns2))+") of cases")

	save_shp(df_uns2, grid_uns2)

	'''
	# Function to save Pandas DF as DBF file 
	def save_dbf_st(df, shapefile_name, field_map = False):
		file_temp = shapefile_name.split('/')[-1]
		rand_post = str(random.randint(1,100001))
		csv_file = geo_path + "/temp_for_dbf"+rand_post+".csv"
		df.to_csv(csv_file,index=False)
		try:
			os.remove(geo_path + "/schema.ini")
		except:
			pass

		# Add a specific field mapping for a special case
		if field_map:
			file = csv_file
			field_map = """FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
			FULLNAME_old "FULLNAME_old" true true false 80 Text 0 0 ,First,#,%s,FULLNAME_old,-1,-1;
			CITY "CITY" true true false 30 Text 0 0 ,First,#,%s,CITY,-1,-1;
			STATE "STATE" true true false 30 Text 0 0 ,First,#,%s,STATE,-1,-1;
			MIN_LFROMA "MIN_LFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_LFROMA,-1,-1;
			MAX_LTOADD "MAX_LTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_LTOADD,-1,-1;
			MIN_RFROMA "MIN_RFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_RFROMA,-1,-1;
			MAX_RTOADD "MAX_RTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_RTOADD,-1,-1;
			grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1;
			NoMatch "NoMatch" true true false 5 Text 0 0 ,First,#,%s,NoMatch,-1,-1;
			NameChng "NameChng" true true false 5 Text 0 0 ,First,#,%s,NameChng,-1,-1""" % (file, file, file, file, file, file, file, file, file, file, file)
		else:
			field_map = None

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=geo_path, 
			out_name="temp_for_shp"+rand_post+".dbf",
			field_mapping=field_map)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		os.remove(csv_file)
		os.rename(geo_path+"/temp_for_shp"+rand_post+".dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(geo_path+"/temp_for_shp"+rand_post+".dbf.xml")
		os.remove(geo_path+"/temp_for_shp"+rand_post+".cpg")

	save_dbf_st(df_uns2, grid_uns2, field_map=True)
	'''

