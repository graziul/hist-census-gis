# -*- coding: utf-8 -*-

#
# EDguess.py - combines multiple automated approaches to identifying EDs into one shapefile
#

from histcensusgis.points.geocode import check_matt_dependencies, initial_geocode
from histcensusgis.microdata.misc import create_addresses
from histcensusgis.s4utils.AmoryUtils import *
from histcensusgis.s4utils.IOutils import *
from histcensusgis.text.standardize import *
from histcensusgis.polygons.block import create_pblks
import histcensusgis
import arcpy
from arcpy import management
from fuzzywuzzy import fuzz
from codecs import open
import os
import copy
import subprocess
import multiprocessing
arcpy.env.overwriteOutput = True

# Clear locks involving .gdb's
def clearWSlocks(inputWS):
  '''Attempts to clear locks on a workspace, returns stupid message.'''
  if all([arcpy.Exists(inputWS), arcpy.Compact_management(inputWS), arcpy.Exists(inputWS)]):
    return 'Workspace (%s) clear to continue...' % inputWS
  else:
    return '!!!!!!!! ERROR WITH WORKSPACE %s !!!!!!!!' % inputWS

# Identifies EDs and can be run independently (Matt's R script)
def ed_geocode_algo(city_info, paths):

	city_name, _, decade = city_info
	city_name = city_name.replace(' ','')

	r_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Ensure files exist for Matt's ED algorithm
	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	pblk_points_shp = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"
	if not os.path.isfile(pblk_shp) or not os.path.isfile(pblk_points_shp):
		check_matt_dependencies(city_info, paths)

	print("Identifying " + str(decade) + " EDs through geocoding\n")
	package_path = os.path.dirname(histcensusgis.__file__)
	t = subprocess.call([r_path,'--vanilla',package_path+'/polygons/Identify 1930 EDs.R',dir_path,city_name,str(decade)])
	print(t)
	if t != 0:
		print("Error identifying "+str(decade)+" EDs for "+city_name+"\n")
	else:
		print("OK!\n")

# Draw ED maps (descriptions, intersections)
def draw_EDs(city_info, paths, new_var_name, is_desc, grid_street_var) :

	city_name, state_abbr, decade = city_info

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	stgrid_shp = geo_path + city_name.replace(' ','') + state_abbr + '_' + str(decade) + "_stgrid_edit_Uns2.shp"
	intermed_path = geo_path + "IntersectionsIntermediateFiles/"
	ed_desc_shp = geo_path+city_name.replace(' ','')+state_abbr+"_"+str(decade)+"_ed_desc.shp"

	# If using Amory's ED description method do this
	if is_desc:

		if decade == 1930:

			arcpy.CreateFeatureclass_management(geo_path, ed_desc_shp.split('/')[-1])
			blk_file = intermed_path+"fullname_dissolve_split.shp"
			arcpy.MakeFeatureLayer_management(blk_file,"blk_lyr")
			arcpy.AddField_management(ed_desc_shp, "ed_desc", "TEXT", "", "", 20)

			with arcpy.da.InsertCursor(ed_desc_shp, ("SHAPE@", "ed_desc")) as cursor:
				for ED, inter in ED_Intersect_ID_dict.items() :
					inter = inter.replace("(","").replace(")","").split(",") #convert intersect string to list 
					block_list = []
					for ind,i in enumerate(inter) :
						i2 = inter[(ind+1)%len(inter)]
						block_list.append(get_block_by_intersections(i,i2))
					block_str = str(block_list).replace("'","").replace("[","(").replace("]",")")
					arcpy.SelectLayerByAttribute_management ("blk_lyr", "NEW_SELECTION", '"FID" IN '+block_str)
					#arcpy.CopyFeatures_management("blk_lyr", "lyr", "", "0", "0", "0")
					arcpy.FeatureToPolygon_management("blk_lyr", intermed_path+"poly_lyr.shp", "", "ATTRIBUTES", "")
					with arcpy.da.UpdateCursor(intermed_path+"poly_lyr.shp",("SHAPE@", "Id")) as icursor:
						for irow in icursor:
							irow[1]=ED
							cursor.insertRow(irow)
					#ASSIGN ED # TO POLYGON
					arcpy.SelectLayerByAttribute_management("blk_lyr", "CLEAR_SELECTION")
					#feature_to_polygon on the selected segments
					# AMORY: DID I MISS SOMETHING HERE?
			arcpy.Delete_management(intermed_path+"poly_lyr.shp")

		# We use a very different method for 1940 
		elif decade == 1940:

			def find_blk_by_stnames(stname_list,use_fuzz=False) :
				try :
					return fullname_blk_dict[tuple(stname_list)]
				except KeyError :
					if not use_fuzz :
						return None
					else :
						#find fuzzy match block
						best_r_avg = 0
						best_blk = None
						for blk,blk_st_list in blk_fullname_dict.items() :
							r_sum = 0
							#keep track of which SM streets have been matched???
							#match_list = copy.deepcopy(stname_list)
							r_avg = blk_fuzz_ratio(blk_st_list,stname_list)
							if r_avg > best_r_avg :
								best_r_avg = r_avg
								best_blk = blk
						if best_r_avg >= 80 :
							return best_blk

			def blk_fuzz_ratio(blk_st_list,stname_list) :
				r_sum = 0
				for blk_st in blk_st_list :
				#find best match for each blk_st
					best = ''
					best_r = 0
					for stname in stname_list :
						r = fuzz.ratio(blk_st,stname)
						if r > best_r :
							best_r = r
							best = stname
					r_sum += best_r
				r_avg = r_sum / max(len(blk_st_list),len(stname_list))
				return r_avg

			print("Matching block descriptions to physical blocks based on street grid...")

			#spatial join target=pblk file, join=Uns2, share_a_LINE_SEGMENT, join the grid_ids of all street segments for each block
			#format the joined grid ID field so it is like: (1047,1048,1081,168,197,218,219)

			grid_id_var = "grid_id"
			grid_id_str_var = "grid_id_s"

			city_state = city_name + state_abbr

			# Have to convert .shp to .gdb here because of text field size limit for dBase files
			gdb_path = geo_path+"scratch%s.gdb" % (city_name)
			if arcpy.Exists(gdb_path):
				arcpy.Delete_management(gdb_path)
			arcpy.CreateFileGDB_management(geo_path, "scratch%s" % (city_name))
			arcpy.env.workspace = gdb_path
			arcpy.FeatureClassToGeodatabase_conversion([pblk_shp, stgrid_shp], arcpy.env.workspace)
			arcpy.MakeFeatureLayer_management(os.path.join(arcpy.env.workspace,city_state+"_"+str(decade)+"_stgrid_edit_Uns2"), "st_lyr")
			arcpy.MakeFeatureLayer_management(os.path.join(arcpy.env.workspace,city_state[:-2] + "_"+str(decade)+"_Pblk"), "pblk_lyr")

			arcpy.AddField_management ('st_lyr', 'grid_id_s', "TEXT", 750)
			arcpy.CalculateField_management ('st_lyr', 'grid_id_s', 'str(!'+grid_id_var+'!)+","', 
				expression_type="PYTHON_9.3")

			join_file = os.path.join(arcpy.env.workspace,city_state+"_"+str(decade)+"_ed_desc")

			arcpy.SpatialJoin_analysis(target_features="pblk_lyr", 
				join_features="st_lyr", 
				out_feature_class=join_file, 
				join_operation="JOIN_ONE_TO_ONE", 
				join_type="KEEP_ALL",
				field_mapping="""pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,pblk_lyr,pblk_id,-1,-1;
				grid_id_s "grid_id_s" true true false 750 Text 0 0 ,Join,#,st_lyr,grid_id_s,-1,-1""", 
				match_option="SHARE_A_LINE_SEGMENT_WITH")

			with open(geo_path + 'ed_blk_desc.txt','r') as blk_desc_file :
				blk_desc = blk_desc_file.readlines()

			for ind,line in enumerate(blk_desc) :
				blk_desc[ind] = line.strip()    

			blk_desc_dict = {} # lookup SM ed_blk identifier -> SM description of block
			blk_gridID_dict = {} # lookup pblk_id -> string of grid_ids of streets comprising boundary of block
			blk_fullname_dict = {} # lookup pblk_id -> list of fullnames of streets comprising boundary of block
			fullname_blk_dict = {} # lookup alphabetical, unique tuple of streets comprising boundary of block -> pblk_id of block
			pblk_ed_blk_dict = {} # lookup pblk_id -> SM ed_blk identifier

			for line in blk_desc :
				line = line.split(', ')
				try :
					blk = line[1].split('-')[1]
				except :
					if line[1] :
						blk = line[1]
					else :
						continue
				blk_desc_dict[blk] = list(np.unique(line[2:]))

			def foo_format(s) :
				return '('+s[:-1]+')'

			with arcpy.da.SearchCursor(join_file,['pblk_id',grid_id_str_var]) as b_cursor :
				for b_row in b_cursor :
					blk = b_row[0]
					seg_str = foo_format(b_row[1])
					blk_gridID_dict[blk] = seg_str
					arcpy.SelectLayerByAttribute_management("st_lyr", 'NEW_SELECTION', '"'+grid_id_var+'" IN '+seg_str)
					with arcpy.da.SearchCursor("st_lyr",[grid_id_var,grid_street_var]) as s_cursor :
						stname_list = []
						for s_row in s_cursor :
							if city_state == "OklahomaCityOK" :
								phrase = isolate_st_name(str(s_row[1]),whole_phrase = True)
								if phrase[0] and re.search("^[A-Z][A-Z]$",phrase[0]):
									try :
										stname_list.append(' '.join(phrase[1:]))
									except TypeError :
										stname_list.append(str(s_row[1]))
							else :
								stname_list.append(str(s_row[1]))

						else :
							stname_list.append(str(s_row[1]))
						stname_list = list(np.unique(stname_list))
						blk_fullname_dict[blk] = stname_list
						fullname_blk_dict[tuple(stname_list)] = blk

			#dicts to keep track of which blocks need to be fuzzy-matched
			fuzz_blk_fullname_dict = copy.deepcopy(blk_fullname_dict)
			fuzz_blk_desc_dict = copy.deepcopy(blk_desc_dict)
			#find exact block matches
			print("Finding exact block matches...")
			for ed_blk, stname_list in blk_desc_dict.items() :
				pblk = find_blk_by_stnames(stname_list)
				if pblk :
					pblk_ed_blk_dict[pblk] = ed_blk
					try :
						fuzz_blk_fullname_dict.pop(pblk)
					except KeyError :
						print("Key "+str(pblk)+" already removed before matching "+str(stname_list))
					fuzz_blk_desc_dict.pop(ed_blk)

			#find fuzzy block matches
			print("Finding fuzzy block matches...")
			for ed_blk, stname_list in fuzz_blk_desc_dict.items() :
				pblk = find_blk_by_stnames(stname_list,use_fuzz=True)
				if pblk :
					if pblk in pblk_ed_blk_dict :
						prev_r = blk_fuzz_ratio(blk_fullname_dict[pblk],blk_desc_dict[pblk_ed_blk_dict[pblk]])
						cur_r = blk_fuzz_ratio(blk_fullname_dict[pblk],stname_list)
						if cur_r > prev_r :
							print("pblk "+str(pblk)+str(blk_fullname_dict[pblk])+" already matched w/ "+str(pblk_ed_blk_dict[pblk])+"("+str(prev_r)+")"+str(blk_desc_dict[pblk_ed_blk_dict[pblk]])+", now "+str(ed_blk)+"("+str(cur_r)+")"+str(stname_list))
							pblk_ed_blk_dict[pblk] = ed_blk
					else :
						pblk_ed_blk_dict[pblk] = ed_blk

			#resolve duplicate block matches
			print("Removing duplicate block matches...")
			arcpy.AddField_management(join_file, "ed_desc", "TEXT", "", "", 20)
			arcpy.AddField_management(join_file, "cblk_id", "TEXT", "", "", 20)
			with arcpy.da.UpdateCursor(join_file,['pblk_id','ed_desc','cblk_id']) as b_cursor :
				for row in b_cursor :
					try :
						ed_blk = pblk_ed_blk_dict[row[0]]
						row[1] = ed_blk.split('_')[0]
						row[2] = ed_blk.split('_')[1]
						b_cursor.updateRow(row)
					except KeyError :
						continue
					except IndexError:
						continue

			arcpy.FeatureClassToShapefile_conversion(join_file, geo_path)        
			print(clearWSlocks(gdb_path))

	# If using Amory's intersection method do this...
	else:

		intermed_path = geo_path + "IntersectionsIntermediateFiles/"
		ed_inter_shp = geo_path + city_name + "_" + str(decade) + "_ed_inter.shp"
		if os.path.isfile(ed_inter_shp):
			arcpy.Delete_management(ed_inter_shp)

		targ = intermed_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2_spatial_join.shp"
		arcpy.CopyFeatures_management(pblk_shp, ed_inter_shp)

		inter = arcpy.Intersect_analysis(in_features=[targ,ed_inter_shp],
			out_feature_class=intermed_path + "intersectToGetEDs.shp",
			join_attributes="ALL", 
			cluster_tolerance="-1 Unknown", 
			output_type="INPUT")

		field_names = [x.name for x in arcpy.ListFields(inter)]
		cursor = arcpy.da.SearchCursor(inter, field_names)
		# AMORY: This dict is never used?
		#inter_polyblk_dict = {} 
		polyblk_inter_dict = {} #polygon block ID -> intersections in block
		
		for row in cursor :
			#Dict_append_unique(inter_polyblk_dict, row[field_names.index("Interse_ID")], row[field_names.index("pblk_id")])
			Dict_append_unique(polyblk_inter_dict, row[field_names.index("pblk_id")], row[field_names.index("Interse_ID")])

		blk_ed_dict = {}
		for blk in polyblk_inter_dict.keys() :
				#retrieve a slice of Intersect_Info_DICT for just the intersections associated with blk
				blk_dict = {key: Intersect_Info_DICT[key] for key in Intersect_Info_DICT.viewkeys() if int(key) in polyblk_inter_dict[blk]}
				result = aggregate_blk_inter_data(blk_dict)
				blk_ed_dict[blk] = result
		try :
			arcpy.AddField_management (ed_inter_shp, new_var_name, "TEXT")
		except :
			pass
		with arcpy.da.UpdateCursor(ed_inter_shp, ["pblk_id",new_var_name]) as up_cursor:
			for row in up_cursor :
				try:
					row[1] = blk_ed_dict[row[0]]
					if row[1] == None :
						row[1] = 0
					up_cursor.updateRow(row)
				except KeyError:
					print("Error in draw_EDs: pblk_id " + str(row[0]) + " not in blk_ed_dict")
					pass

#
# Functions for using intersections to derive EDs
#

# (New) Program Logic #
# 1) Find all streets that intersect and share an ED #
# 2) Decide which intersections are ED boundaries vs. internal #
#     Resolve ambiguities* using microdata  #
# 3) To get ED boundaries, "connect" boundary intersections using #
#     existing street segments #
#
# *) 3-way intersections are always ambiguous - could be internal or boundary #
#    (even & odd = internal)


# Ideas to (Consider) Implement
# - Supplement Steve Morse ED data with microdata - which STs in which ED (SM incomplete!!) - DONE
# - Do address ambiguity resolution for 4-way intersections
#   - John's idea: analyze based on multiple EDs instead of only when there is one ED 
# - tweak even_or_odd(): either adjust threshold to .85, eliminate outliers from address list, or both - DONE
#   ->>> outlier detection was implemented. this changed the numbers although it's unclear if for the better!?
# - Do Fuzzymatching to match map names with morse&micro. DONE - improve results using TYPEs?
#   - only need to do this when name is not found, e.g. Potter's Ave from map does not match with Potters Ave from morse&micro
# - investigate using logic:
#   Intersection    A----B----C
#   ED              1    ?    2
#   Conclusion      B must be a boundary between 1 and 2
# - look at Matt's code and the results from it - how can approaches be combined (also '40 block descriptions,
#   '30 EDs that are coterminous with '40 EDs

# Problems:
# Directional Streets - fuzzy matching will match E Howard Ave w/ W Howard Ave instead of Howard Ave
# Numbered Streets - fuzzy matching will match S 27th St with S 17th St instead of 27th St
# ->->-> GO THRU CHRIS's fuzzy match, copy the code over

# Prepare map intersections
def prepare_map_intersections(city_info, grid_street_var, paths) :
	print("Preparing Map Intersections File")

	city_name, state_abbr, decade = city_info
	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"
	
	stgrid_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2.shp'

	if not os.path.exists(geo_path + "IntersectionsIntermediateFiles"):
		os.makedirs(geo_path + "IntersectionsIntermediateFiles")
	intermed_path = geo_path + "IntersectionsIntermediateFiles/"

	latest_stage = intermed_path + "fullname_dissolve.shp"
	#dissolve all street segments based on FULLNAME
	arcpy.Dissolve_management(in_features=stgrid_shp, 
		out_feature_class=latest_stage,
		dissolve_field=grid_street_var, 
		statistics_fields="", 
		multi_part="SINGLE_PART", 
		unsplit_lines="DISSOLVE_LINES")

	previous_stage = latest_stage
	latest_stage =  intermed_path + "fullname_dissolve_split.shp"
	#split street segments at their intersections
	arcpy.FeatureToLine_management(in_features=previous_stage, 
		out_feature_class=latest_stage,
		cluster_tolerance="", 
		attributes="ATTRIBUTES")

	previous_stage = latest_stage
	latest_stage = intermed_path + "split_endpoints.shp"
	#create points at both ends of every split segment
	arcpy.FeatureVerticesToPoints_management(in_features=previous_stage, 
		out_feature_class=latest_stage,
		point_location="BOTH_ENDS")

	#calculate x and y coordinates of points
	arcpy.AddGeometryAttributes_management(latest_stage, 
		"POINT_X_Y_Z_M")

	previous_stage = latest_stage
	latest_stage = intermed_path+"xy_dissolve.shp"
	#dissolve points based on x and y
	arcpy.Dissolve_management(in_features=previous_stage, 
		out_feature_class=latest_stage,
		dissolve_field="POINT_X;POINT_Y", 
		statistics_fields="", 
		multi_part="MULTI_PART", 
		unsplit_lines="DISSOLVE_LINES")

	arcpy.AddField_management(in_table=latest_stage, 
		field_name="Interse_ID", 
		field_type="LONG", 
		field_precision="", 
		field_scale="", 
		field_length="", 
		field_alias="",
		field_is_nullable="NULLABLE",
		field_is_required="NON_REQUIRED", 
		field_domain="")
	#preserve intersection ID field
	arcpy.CalculateField_management(in_table=latest_stage, 
		field="Interse_ID", 
		expression="!FID!", 
		expression_type="PYTHON_9.3", 
		code_block="")

	previous_stage = latest_stage
	latest_stage = intermed_path + city_name + "_spatial_join.shp"
	target_feature_file = intermed_path + "split_endpoints.shp"
	#join intersection ID back to points file with the rest of the data

	field_mapping_ls = """FID_fullna "FID_fullna" true true false 10 Long 0 10 ,First,#,%s,FID_fullna,-1,-1;
	%s "%s" true true false 100 Text 0 0 ,First,#,%s,%s,-1,-1;
	ORIG_FID "ORIG_FID" true true false 10 Long 0 10 ,First,#,%s,ORIG_FID,-1,-1;
	POINT_X "POINT_X" true true false 19 Double 0 0 ,First,#,%s,POINT_X,-1,-1;
	POINT_Y "POINT_Y" true true false 19 Double 0 0 ,First,#,%s,POINT_Y,-1,-1;
	POINT_X_1 "POINT_X_1" true true false 19 Double 0 0 ,First,#,%s,POINT_X,-1,-1;
	POINT_Y_1 "POINT_Y_1" true true false 19 Double 0 0 ,First,#,%s,POINT_Y,-1,-1;
	Interse_ID "Interse_ID" true true false 10 Long 0 10 ,First,#,%s,Interse_ID,-1,-1""" % \
	(target_feature_file, 
		grid_street_var, 
		grid_street_var, 
		target_feature_file, 
		grid_street_var, 
		target_feature_file, 
		target_feature_file, 
		target_feature_file, 
		previous_stage, 
		previous_stage, 
		previous_stage)

	arcpy.SpatialJoin_analysis(target_features=target_feature_file, 
		join_features=previous_stage,
		out_feature_class=latest_stage, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL",
		field_mapping=field_mapping_ls,
		match_option="INTERSECT", 
		search_radius="", 
		distance_field_name="")

	# EXPORT ATTRIBUTE TABLE
	arcpy.ExportXYv_stats(Input_Feature_Class=latest_stage, 
		Value_Field="FID;Join_Count;TARGET_FID;FID_fullna;"+grid_street_var+";ORIG_FID;POINT_X;POINT_Y;POINT_X_1;POINT_Y_1;Interse_ID", 
		Delimiter="COMMA",
		Output_ASCII_File = intermed_path + city_name + "_Intersections.txt", 
		Add_Field_Names_to_Output="ADD_FIELD_NAMES")

# returns list of all EDs shared by all streets in st_ed_dict_chk
def ED_in_common(st_ed_dict_chk) :
	EDs = list(st_ed_dict_chk.values())
	in_common = set(EDs[0])
	for i in EDs[1:] :
		in_common = in_common & set(i)
	return list(in_common)

# Function that takes a list of streets and returns the street name that appears only once, if it exists
def find_unique_st(st_list) :
	unique_sts = []
	redundant_sts = []
	for st in st_list :
		if st not in unique_sts :
			if st not in redundant_sts :
				unique_sts.append(st)
		else :
			unique_sts.remove(st)
			redundant_sts.append(st)
	if not len(unique_sts) == 1 :
		raise ValueError("Failed to find a single unique street")
	else :
		return unique_sts,redundant_sts

#helper function for is_ED_boundary
#if >= 90% of addresses are even or odd, return 'even' or 'odd', respectively. Otherwise, return 'both'
def even_or_odd(Address_List) :
	even_cnt = 0
	odd_cnt = 0
	if len(Address_List) < 2 :
		return 'na'
	for a_str in Address_List :
		try :
			a = int(a_str)
			if a%2 == 0 :
				even_cnt = even_cnt+1
			else :
				odd_cnt = odd_cnt+1
		except ValueError :
			# print("not an address #: "+str(a_str))
			continue
	if even_cnt / len(Address_List) >= .9 :
		return 'even'
	elif odd_cnt / len(Address_List) >= .9 :
		return 'odd'
	else :
		return 'both'
		
# function for resolving ambiguous 3-way intersections
def is_ED_boundary(st,ED) :
	#print("called ED boundary")
	try :
		temp_addresses_unfiltered = ST_ED_Address_DICT[st+ED]
	except KeyError : #st_ed from map+morse not found in micro
		return 'nfm'
	temp_addresses = list(filter(lambda x: not (x==None or x=='' or x==' ' or x=='nan'),temp_addresses_unfiltered))
	for a in list(temp_addresses) :
		try :
			float(a)
		except :
			temp_addresses.remove(a)
	ED_addr_outliers = get_cray_z_scores([int(x) for x in temp_addresses if not math.isnan(float(x))])
	if ED_addr_outliers == None : #this happens if there's only 1 or 2 addresses in temp_addresses
		ED_Addresses = temp_addresses
	else :
		ED_Addresses = list(filter(lambda x: ED_addr_outliers[int(x)]<4, temp_addresses))
		#print(temp_addresses)
		#print(ED_Addresses)

	City_Addresses = list(filter(lambda x: not (x==None or x=='' or x==' ' or x=='nan'),ST_Address_DICT[st]))
	city_even_odd = even_or_odd(City_Addresses)
	ED_even_odd = even_or_odd(ED_Addresses)
	if city_even_odd == 'na' or ED_even_odd == 'na' :
		return 'na'
	if city_even_odd == 'both' and not ED_even_odd == 'both' :
		return 'yes'
	else :
		return 'no'

# returns a list of all street phrases in st_dict that have the NAME name
# expects a dict with st_phrase -> st_name keys and values
def get_st_by_name(name, st_dict) :
	name_list = []
	for k,v in st_dict.items() :
		if v == name :
			name_list.append(k)
	return name_list

# return all EDs associated with st according to st_ed_dict_chk
# st can be a string or an iterable of strings
def get_eds_by_st(st,st_ed_dict_chk) :
	if st == None :
		return None
	if isinstance(st,str) :
		return st_ed_dict_chk[st]
	ed_list = []
	for s in st :
		ed_list = ed_list + st_ed_dict_chk[s]
	return list(np.unique(ed_list))
		
# match based on entire street phrase, but favor matches with an exact match for NAME
##    principles:
##        don't return any match below 85 unless exact NAME match
##        don't return any match where TYPEs conflict (it's NOT OK if TYPE is missing from match)
##        if DIR does not match, favor matches with no DIR
##        always return highest scoring exact NAME match, unless it violates the above principles

##  --> the only time we eschew an exact NAME match for a non-exact NAME match is when the TYPE does not match
##  --> we may eschew an exact NAME match for a lower-scoring exact NAME match if the TYPEs or DIRs conflict in the higher-scoring match
def fuzzy_match(phrase,st_list) :
	if (not isinstance(phrase, str)) or (phrase == None or phrase == '' or phrase == -1):
		print(str(phrase)+" is not a gosh darn string")
		return None
	debug = False
	
	possible_match = []
	exact_name_match = []
	phrase_list = isolate_st_name(phrase,True)
	DIR = phrase_list[0]
	NAME = phrase_list[1]
	TYPE = phrase_list[2]
	for st in st_list: 
		if(not st=="") :
			score = fuzz.ratio(phrase,st)
			match_NAME = isolate_st_name(st)
			NAME_score = fuzz.ratio(NAME,match_NAME)
			
			if score >= 75 or NAME_score == 100 and score > 50 :
				if NAME_score == 100 :
					exact_name_match.append((score,st))
				else :
					possible_match.append((score,st))
	if debug :print("exact name matches: "+str(exact_name_match))
	if debug :print("other matches: "+str(possible_match))
	name_type_match = {}
	dir_name_match = []
	exact_name_dict = {}
	for score, st in exact_name_match :
		Dict_append_unique(exact_name_dict,score, st)
	for score in reversed(sorted(exact_name_dict)) :#iterate from highest to lowest score
		matches = exact_name_dict[score]
		matches_to_return = []
		for m in matches :
			m_list = isolate_st_name(m,True)
			m_DIR = m_list[0]
			m_TYPE = m_list[2]
			if m_DIR == None and m_TYPE == TYPE :
				matches_to_return.append(m)
			if m_TYPE == TYPE :
				Dict_append_unique(name_type_match,score,m)
			if m_DIR == DIR :
				dir_name_match.append((score,m))
		if matches_to_return :
			return set(matches_to_return)

	for score in reversed(sorted(name_type_match)) :
		return set(name_type_match[score]) # return highest score with name and type matching, if it exists
	
	possible_match.sort()
	for _,m in reversed(possible_match) :
		m_list = isolate_st_name(m,True)
		m_TYPE = m_list[2]
		if(m_TYPE == TYPE) :
			return m

# given a intersect->info dict for a particular block, return what ED the block should be in
def aggregate_blk_inter_data(inter_dict) :
	possible_eds = []
	for k,v in inter_dict.items() :
		if not isinstance(v[1],list):
			possible_eds += [v[1]]
		if isinstance(v[1],list) :
			try :
				possible_eds += int(v[1])
			except :
				continue
	mode = find_mode(possible_eds)
	if mode == -999 :
		#print(inter_dict)
		return '0'
	if len(mode) == 1 :
		return mode[0]
	else :
		return '|'.join([str(x) for x in mode])  

# Main Program Loop - also outputs statistics and results to .txt files
def run_inter_analysis(city_name) :
	#Put this  on  hold until it can be standardized or discarded, as necessary (based on the decade comparison of SM 10/30/40)
	#SM_st_corrections = pickle.load( open("SM_decade_compare_st_corrections.p","rb"))
	print("Preparing Input for "+city_name+ " (intersections)")

	# Create Map DICTs
	for ind, iline in enumerate(InterLines) :
		IList = iline.rstrip().split(",")
		NAME = Num_Standardize(IList[6])
		Dict_append(Intersect_ST_DICT,IList[-1],NAME)
		Dict_append_unique(ST_Intersect_DICT,NAME,IList[-1])
		Dict_append_unique(Intersect_BLOCK_DICT,IList[-1],IList[7])
		Dict_append_unique(BLOCK_Intersect_DICT,IList[7],IList[-1])

	# Create Morse DICTs
	for ind, sline in enumerate(SMLines) : #
		st = morse_standardize(sline[0])
		EDList = list(filter(None,sline[1:]))
 ##        try :
 ##            temp = SM_st_corrections[("Hartford","ct")][st]
 ##            if not st == temp :
 ##                print("%s changed to %s" % (st,temp))
 ##                st = temp
 ##        except KeyError :
 ##            pass
		
		if not st=="" :
			ST_ED_DICT[st] = EDList
		for ed in EDList :
			Dict_append_unique(ED_ST_DICT,ed,st)

	# Create Micro DICTs
	for ind, mline in enumerate(MicroLines) :
		MList = mline.rstrip().split(",")
		NAME = standardize_street(MList[2])[0]
		ED = MList[3]
		ADDR = MList[6]
		Dict_append_unique(ST_ED_Address_DICT,NAME+ED,ADDR) # used to be Dict_append_unique!!!
		Dict_append_unique(ST_Address_DICT,NAME,ADDR) # used to be Dict_append_unique!!!
		
		Dict_append_unique(ST_ED_DICT_mi,NAME,ED)
		Dict_append_unique(ED_ST_DICT_mi,ED,NAME)

	SM_streets = ST_ED_DICT.keys()#all streets found in Steve Morse
	micro_streets = ST_ED_DICT_mi.keys() #all streets found in Micro

	print("Finished preparing files. Starting Intersections analysis.")
	# Intersections Analysis loop
	for i,slist in Intersect_ST_DICT.items() :
		debug = False
		# i is the current intersection ID
		#get list of STs in i, filter out blank STs
		STList = list(filter(lambda x: not x==' ' and not x=='',np.unique(slist))) #unique street names
		discrete_st_list = list(filter(lambda x: not x==' ' and not x=='',slist)) #all street names
		if len(STList) > 1 :
			proceed = True
			match_ed_dict = {}
			for st in STList :
				# for each street in intersection, find fuzzy matches with morse and micro and collect ED data for that street from both sources
				match_ed_dict[st] = []
				morse_match = fuzzy_match(st,SM_streets)
				if not morse_match == None :
					match_ed_dict[st] = match_ed_dict[st] + get_eds_by_st(morse_match,ST_ED_DICT)
				micro_match = fuzzy_match(st,micro_streets)
				if not micro_match == None :
					match_ed_dict[st] = match_ed_dict[st] + get_eds_by_st(micro_match,ST_ED_DICT_mi)
				match_ed_dict[st] = list(np.unique(match_ed_dict[st]))
			
			EDs = ED_in_common(match_ed_dict)

			if proceed :
				if "City Limits" in STList :
					Intersect_Info_DICT[i] = ['b',EDs]
				elif EDs == None or EDs == [] : #Steve Morse contradicts map
					Intersect_Info_DICT[i] = ['mc',STList]
					#print("no ED data: "+str(STList))
				else : #all streets in intersection share at least 1 ED
					
					BLOCKs = Intersect_BLOCK_DICT[i]
					
					if(len(EDs)==1 and len(BLOCKs)>3) :
						Intersect_Info_DICT[i] = ['i',EDs[0]] #internal
					else :
						if(len(EDs)==1 and len(BLOCKs)==3) : # 3-way intersections #
							# resolve ambiguity using addresses
							try :
								_,ambig_st = find_unique_st(discrete_st_list) #ambig_st is the non-unique st in the intersection
								ED_bound_test = is_ED_boundary(ambig_st[0],EDs[0])
								if ED_bound_test == "nfm" : #st_ed from map+morse not found in micro
									Intersect_Info_DICT[i] = ['nfm',EDs[0]]
								elif ED_bound_test == "na" :
									Intersect_Info_DICT[i] = ['na',EDs[0]]
								elif ED_bound_test == "yes" :
									Intersect_Info_DICT[i] = ['b',EDs[0]] #boundary
								else :
									Intersect_Info_DICT[i] = ['i',EDs[0]] #internal
							except ValueError :
								if debug : print("couldn't find a unique st out of "+str(discrete_st_list))
								Intersect_Info_DICT[i] = ['a', 0] #ambiguous
						elif len(EDs)>1 :
							Intersect_Info_DICT[i] = ['e',EDs] #external (could include boundary intersections) - associated with more than one ED
						elif len(EDs)==1 :
							Intersect_Info_DICT[i] = ['i',EDs[0]] #internal, 2-way
						else :
							print("something is up with intersection "+str(i))
							assert (False == True)

	# initialize counters for the various categories of intersections
	internal_cnt = 0
	external_cnt = 0
	nf_cnt = 0
	boundary_cnt = 0
	contradiction_cnt = 0
	nf_micro_cnt = 0
	na_cnt = 0

	ED_Intersect_DICT = {}

	# take stock of the intersections based on their various flags
	# record all "internal" ('i') intersections in ED_Intersect_DICT
	for i,info in Intersect_Info_DICT.items() :
		if(info[0] == 'e') :
		   external_cnt = external_cnt+1
		if(info[0] == 'i') :
			internal_cnt=internal_cnt+1
			Dict_append(ED_Intersect_DICT,info[1],i)
		if(info[0] == 'nf') :
			nf_cnt = nf_cnt+1
			#print(str(i)+": 1 not found in Morse: "+str(Intersect_ST_DICT[i]))
		if(info[0] == 'b') :
			boundary_cnt = boundary_cnt+1
		if(info[0] == 'mc') :
			contradiction_cnt = contradiction_cnt+1
		if(info[0] == 'nfm') :
			nf_micro_cnt = nf_micro_cnt+1
		if(info[0] == 'na') :
			na_cnt = na_cnt+1
	print(city_name+" analysis finished.")
	print("internal: "+str(internal_cnt))
	print("external: "+str(external_cnt))
	print("boundary: "+str(boundary_cnt))
	print("not found in Morse or micro: "+str(nf_cnt))
	print("Morse contradicts map: "+str(contradiction_cnt))
	print("st_ed from map+morse not found in micro: "+str(nf_micro_cnt))
	print("not enough address data to resolve ambiguity: "+str(na_cnt))

	# Check streets from those intersections that are not found in morse or micro
	# If streets are not found in ST_ED_DICT, add them to nf_list (not found)
	nf_list = []
	for i,info in Intersect_Info_DICT.items() :
		if(info[0]=='nf') :
			STlist = Intersect_ST_DICT[i]
			for st in STlist :
				try :
					ST_ED_DICT[st]
				except KeyError :
					nf_list.append(st)

	Output_TXT = open(city_name+'IntersectionsStatistics.txt','w+')
	Output_TXT.write("internal: "+str(internal_cnt)+"\n")
	Output_TXT.write("external: "+str(external_cnt)+"\n")
	Output_TXT.write("boundary: "+str(boundary_cnt)+"\n")
	Output_TXT.write("not found in Morse: "+str(nf_cnt)+"\n")
	Output_TXT.write("Morse contradicts map: "+str(contradiction_cnt)+"\n")
	Output_TXT.write("st_ed from map+morse not found in micro: "+str(nf_micro_cnt)+"\n")
	Output_TXT.write("not enough address data to resolve ambiguity: "+str(na_cnt))

	Output_TXT = open(city_name+'IntersectionsResults.csv','w+')
	for i,info in Intersect_Info_DICT.items() :
		if len(info)==2 :
			Output_TXT.write(i+","+info[0]+",\""+re.sub("[\[\]]",'',str(info[1]).replace(',','|'))+"\"\n")
		else :
			Output_TXT.write(i+","+info[0]+"\n")

# Run the entire intersections algorithm on the given city_info
def ed_inter_algo(city_info, paths, grid_street_var):

	city_name, state_abbr, decade = city_info
	city_spaces = city_name
	city_name = city_name.replace(' ','')

	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	# Ensure that address file exists
	address_file = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	if ~os.path.isfile(address_file):
		create_addresses(city_info, paths)

	# Ensure street grid file exists (for now use 1940)
	stgrid_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2.shp'
	if not os.path.isfile(stgrid_shp):
		print("Missing stgrid file")
		raise ValueError

	global SMLines
	global SMLines1
	global InterLines
	global MicroLines
	SMLines = None
	SMLines1 = None
	InterLines = None
	MicroLines = None

	# Morse Dicts: #
	global ST_ED_DICT
	global ED_ST_DICT
	ST_ED_DICT = {} # lookup ST -> which EDs
	ED_ST_DICT = {} # lookup ED -> which STs

	# Map Dicts: #
	global Intersect_ST_DICT
	global Intersect_BLOCK_DICT
	global ST_Intersect_DICT
	global BLOCK_Intersect_DICT
	Intersect_ST_DICT = {} # lookup intersection -> which STs (names)
	Intersect_BLOCK_DICT = {} # lookup intersection -> which BLOCKs
	ST_Intersect_DICT = {} # lookup ST -> which intersections
	BLOCK_Intersect_DICT = {} # lookup BLOCK ID -> which intersections

	# Micro Dicts: #
	global ST_ED_Address_DICT
	global ST_Address_DICT
	global ST_ED_DICT_mi
	global ED_ST_DICT_mi
	ST_ED_Address_DICT = {} # lookup ST_ED -> list all addresses in ED
	ST_Address_DICT = {} # lookup ST -> list all addresses in city
	ST_ED_DICT_mi = {} # lookup ST -> which EDs
	ED_ST_DICT_mi = {} # lookup ED -> which STs

	# Derived Dict: #
	global Intersect_Info_DICT
	Intersect_Info_DICT = {} # lookup intersection -> list of information

	Micro_TXT = open(geo_path + city_name + '_' + str(decade) + '_Addresses.csv')

	sm_path = r"S:\Projects\1940Census\SMlists"
	os.chdir(sm_path+"\\"+str(decade))
	try:
		csv_name = city_spaces+state_abbr+"_SM"
		csv_from_excel(csv_name+".xlsx",csv_name)
	except:
		csv_name = city_name + state_abbr + "_SM"
		csv_from_excel(csv_name+".xlsx",csv_name)
	SM_ED_TXT = open(csv_name+".csv",'r')
	SM_ED_TXT1 = open(csv_name+"_ED.csv",'r')

	# Ensure required files exist (i.e. dependent processes have been run)
	print("Checking for files necessary to process %s (Intersections algorithm)" % (city_name))
	intersections_file = geo_path + '/IntersectionsIntermediateFiles/' + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2_Intersections.shp'
	if ~os.path.isfile(intersections_file):
		prepare_map_intersections(city_info, grid_street_var, paths)

	Intersect_TXT = open(geo_path + '/IntersectionsIntermediateFiles/' + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2_Intersections.txt')
	SMLines = csv.reader(SM_ED_TXT)
	next(SMLines, None)  # skip header
	SMLines1 = csv.reader(SM_ED_TXT1)
	InterLines = Intersect_TXT.readlines()[1:]
	MicroLines = Micro_TXT.readlines()[1:]

	# Run intersections algorithm
	print("Processing %s (Intersections algorithm)" % (city_name))
	run_inter_analysis(city_name)

	print("Creating ED Map for %s (Intersections algorithm)" % (city_name))
	draw_EDs(city_info=city_info, 
		paths=paths, 
		new_var_name="ed_inter", 
		is_desc=False,
		grid_street_var=grid_street_var)

#
# Functions for ED descriptions
#

# Created: Amory Kisch, 1/8/2018
#
# Purpose: To convert Steve Morse ED text descriptions to ED polygons using historical street grid shapefiles.
#
# Method: For each ED description:
#           1) find an intersection in the street grid that exactly matches the full street phrases of two adjoining
#               streets in the description
#           2) for each of the remaining streets, select all segments that connect the preceding and following streets
#               in the description
#               - if exact matches do not exist, match using just street NAME, and then try fuzzy matching
#           3) create the ED polygon using feature_to_polygon on the selected segments
#               - if correct polygon cannot be created, flag ED for manual checking

def check_for_desc_files(city_info, paths, grid_street_var):

	city_name, state_abbr, decade = city_info
	city_spaces = city_name
	city_name = city_name.replace(' ','')

	_, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	# Ensure street grid file exists 
	stgrid_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2.shp'
	if not os.path.isfile(stgrid_shp):
		print("Missing stgrid file")
		raise ValueError

	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	if not os.path.isfile(pblk_shp):
		print("Creating Pblk file for %s" %decade)
		create_pblks(city_info, geo_path)


	if decade == 1940:

		global blk_lines
		global ed_lines
		global st_lines

		block_lines_file = dir_path+"/Textfile/"+city_name+"_Block_lines_edit.txt"
		ed_lines_file = dir_path+"/Textfile/"+city_name+"_ED_lines_edit.txt"
		attr_file = dir_path+"/Textfile/"+city_name+"_attr.txt"

		# Ensure that the block lines file exists
		block_lines_exists = os.stat(block_lines_file).st_size != 0
		if not block_lines_exists:
			print("No Block lines file found for " + city_spaces + state_abbr)
			raise ValueError

		# Ensure that the ed lines file exists
		ed_lines_exists = os.stat(ed_lines_file).st_size != 0
		if not ed_lines_exists:
			print("No ED lines file found for " + city_spaces + state_abbr)
			raise ValueError

		# Create the file needed to make st_lines
		arcpy.ExportXYv_stats(Input_Feature_Class=stgrid_shp, 
			Value_Field=grid_street_var, Delimiter="COMMA",
			Output_ASCII_File=attr_file, 
			Add_Field_Names_to_Output="NO_FIELD_NAMES")

		with open(block_lines_file,'r',encoding='utf-8-sig', errors='ignore') as blk_txt_file :
			blk_lines = blk_txt_file.readlines()
		with open(ed_lines_file,'r',encoding='utf-8-sig', errors='ignore') as ed_txt_file :
			ed_lines = ed_txt_file.readlines()
		with open(attr_file,'r') as st_list_file :
			st_lines = st_list_file.readlines()

		for i in range(0,len(st_lines)) :
			st_lines[i] = st_lines[i].split(',')[2].strip()
		st_lines = list(np.unique(st_lines))

	elif decade == 1930:

		global InterLines
		global Descriptions

		# Ensure intersections file exist
		intersections_file = geo_path + '/IntersectionsIntermediateFiles/' + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2_Intersections.shp'
		if not os.path.isfile(intersections_file):
			prepare_map_intersections(city_info, grid_street_var, paths)
		Intersect_TXT = open(intersections_file.replace('.shp','.txt'))
		InterLines = Intersect_TXT.readlines()[1:]

		# Ensure desriptions file exist
		descriptions_file = 'S:/Projects/1940Census/SMdescriptions/'+city_spaces+'_EDdraw_test.txt'
		if os.stat(descriptions_file).st_size == 0 or not os.path.isfile(descriptions_file):
			print("No ED description data found for " + city_spaces + state_abbr)
			raise ValueError
		Descriptions = open(descriptions_file).readlines()

# fuzzy matches a given fullname st string against the list of all streets from grid
def fuzzy_match_list(st) :
	best = ""
	best_r = 0
	for sm in st_lines :
		r = fuzz.ratio(sm,st)
		if r > best_r :
			best = sm
			best_r = r
	name = isolate_st_name(st)
	if (len(name)<=4 and best_r > 86) or (len(name)>4 and best_r >= 80) :
		return best
	else :
		return st

def get_intersect_by_stnames(stlist) :
	try :
		in_common = set(ST_Intersect_dict[stlist[0]])
	except KeyError :
		return []
	for st in stlist[1:] :
		try :
			in_common = in_common & set(ST_Intersect_dict[st])
		except KeyError :
			return []
	return list(in_common)

def get_block_by_intersections(i1,i2) :
	in_common = [x for x in Intersect_BLOCK_dict[i1] if x in Intersect_BLOCK_dict[i2]]
	if in_common :
		try :
			assert len(in_common) == 1
		except :
			print("Warning: More than one block "+str(in_common)+" associated with intersections "+str(i1)+" & "+str(i2))
		return in_common[0]
	else :
		print("NO BLOCK FOUND FOR INTERSECTIONS "+str(i1)+" and "+str(i2))

#compares st1 with st2, which can be a string or a list of strings
#if list, return True if st1 matches with ANY string in st2
def fuzzy_st_test(st1,st2) :
	threshold = 80
	if isinstance(st2,str) :
		st1 = st1.lower()
		st2 = st2.lower()
		return fuzz.ratio(st1,st2) >= threshold
	if isinstance(st2,list) :
		st1 = st1.lower()
		for s in st2 :
			s = s.lower()
			if fuzz.ratio(st1,s) >= threshold :
				return True
		return False

#don't have to worry about KeyError because first vertex always has None as its parent
def get_predecessors(pre_dict,v) :
	orig_v = v
	l = []
	while pre_dict[v] and pre_dict[v] != orig_v :
		if len(l) > 100:
			return l
		else:
			l.append(pre_dict[v])
			v = pre_dict[v]
	return l

def find_descript_segments(descript,intersect,start_ind,start_streets,fuzzy = False,debug = False) :

	finished = False
	
	start = intersect[0]
	predecessor_dict = {start:None} #record path traversed by search: lookup intersection -> ID of prev intersection
	visited, queue = set(), [start]
	cur_name = isolate_st_name(start_streets[1])
	start_ind = (start_ind + 1) % len(descript)
	assert(cur_name == descript[start_ind])
	next_name = descript[(start_ind+1)%len(descript)]
	if debug:print("cur_name: "+cur_name)
	if debug:print("next_name: "+next_name)
	descript_ind = 1
	while queue :
		found_next = False
		vertex = queue.pop(0)
		if debug:print("vertex: "+str(vertex))
		if debug:print("rest of queue: "+str(queue))
		if vertex not in visited : #update visited to at least be the so-far path of correct intersections
			if vertex == start and descript_ind > 1 and descript_ind < len(descript) :
				return False,str(filter(None,predecessor_dict.values())).replace("'","").replace("[","(").replace("]",")")+" "+next_name
			if descript_ind == len(descript)+1 and vertex == start :
				if debug:print("THIS SHOULD NOT HAPPEN BECAUSE THE START VERTEX SHOULD ALREADY BE IN VISITED")
				if debug:print(predecessor_dict)
				#assert(False)
				queue = []
				finished = True
				if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
				pre = predecessor_dict[vertex]
				string = "("+str(pre)+","
				pre_ind = 0
				while pre != start and pre_ind <= len(predecessor_dict.items()) + 10:
					pre = predecessor_dict[pre]
					string+=str(pre)+","
					pre_ind += 1
				string = string[:-1]+")"
				if pre == start :
					return finished,string
				else :
					return finished,"erroneous starting intersection: "+str(start)+string

			visited.add(vertex)
			new_vertices = []
			for block in Intersect_BLOCK_dict[vertex] :
				#if debug:print("block: "+str(block)+" ("+str(BLOCK_NAME_dict[block])+")")
				if BLOCK_NAME_dict[block] == cur_name or fuzzy and fuzzy_st_test(BLOCK_NAME_dict[block], cur_name) :
					new_vertices.extend(BLOCK_Intersect_dict[block])
					
			#if the correct next intersection is already in visited, don't filter it out!
			#check results if using descript_ind rather than x==start as the condition to satisfy this ^
			new_vertices = filter(lambda x : (not x == vertex or (next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x]))) and not x == predecessor_dict[vertex] and not x in queue and (not x in visited or (x==start and (next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x])))), new_vertices)
			#new_vertices = filter(lambda x : not x == vertex and not x == predecessor_dict[vertex] and not x in queue and (not x in visited or next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x])), new_vertices)
			if debug:print("new_vertices: "+str(new_vertices))
			for v in new_vertices :
				predecessor_dict[v] = vertex
			for v in new_vertices :
				if descript_ind == len(descript) and v == start :
					queue = []
					finished = True
					if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
					pre = predecessor_dict[v]
					string = "("+str(pre)+","
					while pre != start :
						pre = predecessor_dict[pre]
						string+=str(pre)+","
					string = string[:-1]+")"
					return finished,string
				if next_name in Intersect_NAME_dict[v] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[v]) :
					if found_next :
						queue.append(v)
					else :
						descript_ind += 1
						queue = [v]
					visited = set(get_predecessors(predecessor_dict,v))
					if debug:print("FOUND THE NEXT STREET! (v = "+str(v)+")")
					if debug:print("descript_ind: "+str(descript_ind))
					if debug:print("visited: "+str(visited))
					#check to see if any additional cur_name blocks intersect with next_name:
					for block in Intersect_BLOCK_dict[v] :
						if BLOCK_NAME_dict[block] == cur_name or fuzzy and fuzzy_st_test(BLOCK_NAME_dict[block], cur_name) :
							aux_vertex = filter(lambda x : not x == v and not x == vertex,BLOCK_Intersect_dict[block])
							if aux_vertex :
								assert len(aux_vertex) == 1
								aux_vertex = aux_vertex[0]
								if next_name in Intersect_NAME_dict[aux_vertex] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[aux_vertex]) :
									queue.append(aux_vertex)
									predecessor_dict[aux_vertex] = v
									if debug:print("FOUND ANOTHER CANDIDATE FOR THE NEXT STREET! (v = "+str(aux_vertex)+")")
					found_next = True
					#break ### GOOD IDEA???
			if found_next :
				cur_name = next_name
				next_name = descript[(start_ind+descript_ind)%len(descript)]
				if debug:print("cur_name: "+cur_name)
				if debug:print("next_name: "+next_name)
				continue
			else :
				queue.extend(new_vertices)
		elif next_name in Intersect_NAME_dict[vertex] :
			global discovered_problem
			discovered_problem += 1
			if debug:print("OH DEAR :( DISCOVERED PROBLEM :(")
		elif descript_ind == len(descript)+1 and vertex == start :
			queue = []
			finished = True
			if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
			pre = predecessor_dict[vertex]
			string = "("+str(pre)+","
			while pre != start :
				pre = predecessor_dict[pre]
				string+=str(pre)+","
			string = string[:-1]+")"
			return finished,string

	return finished,str(filter(None,predecessor_dict.values())).replace("'","").replace("[","(").replace("]",")")+" "+str(vertex)+" "+next_name

def run_desc_analysis(city_info, paths, grid_street_var) :

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')

	stgrid_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_stgrid_edit_Uns2.shp'

	if decade == 1930:

		output = open(geo_path + city_name+"_EDs.txt","w+")
		problem_EDs = open(geo_path + city_name+"_problem_EDs.txt","w+")

		debug = False

		# Derived Dict #
		global ED_Intersect_ID_dict
		ED_Intersect_ID_dict = {} # lookup ED -> string of Intersection IDs

		# Morse Dicts: #
		global ED_Intersect_dict
		global ED_NAME_description_dict
		ED_description_dict = {} # lookup ED -> list streets in order of description
		ED_NAME_description_dict = {} # lookup ED -> list street NAMEs in order of description

		# Map Dicts: #
		global Intersect_ST_dict
		global Intersect_BLOCK_dict
		global Intersect_NAME_dict
		global ST_Intersect_dict
		global BLOCK_Intersect_dict
		global BLOCK_NAME_dict
		Intersect_ST_dict = {} # lookup intersection -> which STs (phrases)
		Intersect_BLOCK_dict = {} # lookup intersection -> which BLOCKs
		Intersect_NAME_dict = {}  # lookup intersection -> which STs (NAMEs)
		ST_Intersect_dict = {} # lookup ST -> which intersections
		BLOCK_Intersect_dict = {} # lookup BLOCK ID -> which intersections
		BLOCK_NAME_dict = {} # lookup BLOCK ID -> NAME of segment

		print("Preparing Input for "+city_name+ " (descriptions)")

		# Create Map DICTs
		for ind, iline in enumerate(InterLines) :
			IList = iline.rstrip().split(",")
			NAME = Num_Standardize(IList[6])
			Dict_append(Intersect_ST_dict,IList[-1],NAME)
			Dict_append(Intersect_NAME_dict,IList[-1],isolate_st_name(NAME))
			Dict_append_unique(ST_Intersect_dict,NAME,IList[-1])
			Dict_append_unique(Intersect_BLOCK_dict,IList[-1],IList[7])
			Dict_append_unique(BLOCK_Intersect_dict,IList[7],IList[-1])
			BLOCK_NAME_dict[IList[7]] = isolate_st_name(NAME)

		# Create Morse DICTs
		for line in Descriptions :
			line_list = line.split(',')
			ED_description_dict[line_list[0]] = [x.strip('"\' \n\r') for x in line_list[1:]]
			ED_NAME_description_dict[line_list[0]] = [isolate_st_name(x.strip('"\' \n\r')) for x in line_list[1:]]

		# Isolate St NAMEs
		arcpy.AddField_management (stgrid_shp, "NAME", "TEXT")
		with arcpy.da.UpdateCursor(stgrid_shp, [grid_street_var,"NAME"]) as up_cursor:
			for row in up_cursor :
				row[1] = isolate_st_name(str(row[0]))
				up_cursor.updateRow(row)

		# Isolate St NAMEs

		print("Analyzing ED Descriptions")

		good_EDs = []
		try_fuzzy_EDs = []

		for ED, descript in ED_description_dict.items() :
			#if ED != "486" and ED!="225" and ED!='152':
			#    continue

			#keep only unique street names, but preserve order in description
			descript_stripped,rem_list = f7(copy.copy(descript))

			intersect = []
			start_ind = 0
			#find an exactly matching starting intersection
			while start_ind <= len(descript_stripped) - 1:
				start_streets = [descript_stripped[start_ind], descript_stripped[(start_ind+1)%len(descript_stripped)]]
				if debug:print("start_streets: "+str(start_streets))
				intersect = get_intersect_by_stnames(start_streets)
				if intersect == [] or start_streets[0] == start_streets[1] :
					start_ind += 1
				else :
					break

			if intersect == [] or start_streets[0] == start_streets[1] :
				if debug:print("Could not find any exactly matching intersections out of "+str(descript_stripped))
			else :
				#breadth-first search through block/intersection dicts to find
				#path to intersection with next street in the description
				#change descript to be just the NAMEs of the streets

				descript_orig = copy.copy(ED_NAME_description_dict[ED])
				#remove streets at the indices that were previously removed
				for i in rem_list :
					del descript_orig[i]

				success, string = find_descript_segments(descript_orig,intersect,start_ind,start_streets,debug=debug)
				if success :
					output.write(str(ED)+": "+string+"\n")
					ED_Intersect_ID_dict[ED] = string
				else :
					try_fuzzy_EDs.append(ED)
		
		for ED in try_fuzzy_EDs :
			descript = ED_description_dict[ED]
			intersect = []
			start_ind = 0

			#keep only unique street names, but preserve order in description
			descript_stripped,rem_list = f7(copy.copy(descript))
			#find an exactly matching starting intersection
			while start_ind <= len(descript_stripped) - 1:
				start_streets = [descript_stripped[start_ind], descript_stripped[(start_ind+1)%len(descript_stripped)]]
				if debug:print("start_streets: "+str(start_streets))
				intersect = get_intersect_by_stnames(start_streets)
				if intersect == [] or start_streets[0] == start_streets[1]:
					start_ind += 1
				else :
					break
			if intersect == [] :
				if debug:print("Could not find any exactly matching intersections out of "+str(descript_stripped))
			else :
				#breadth-first search through block/intersection dicts to find
				#path to intersection with next street in the description

				#change descript to be just the NAMEs of the streets
				descript_orig = copy.copy(ED_NAME_description_dict[ED])
				#remove streets at the indices that were previously removed
				for i in rem_list :
					del descript_orig[i]
				if debug:print(str(ED)+": "+str(descript_orig))

				success, string = find_descript_segments(descript_orig,intersect,start_ind,start_streets,fuzzy = True,debug=debug)
				if success :
					if debug:print("FUZZY WORKED FOR "+str(ED)+"!!!!!!!!!!!!!!!!!!!!!")
					output.write(str(ED)+": "+string+"\n")
					ED_Intersect_ID_dict[ED] = string
				else :
					problem_EDs.write(str(ED)+": "+string+"\n")

		if debug:print("discovered_problem: "+str(discovered_problem))

	elif decade == 1940:

		line_blk_dict = {} #lookup line number -> blk descript
		ed_line_dict = {} #lookup ed -> which line numbers
		ed_tract_dict = {} #lookup ed -> which tract/area/precinct

		print("Creating lookup dictionaries based on block/ED data from Steve Morse...")

		for line in blk_lines :
			line = line.strip()
			if line == "" or line == "\n" :
				continue
			
			line_num = re.search("\(\*([0-9]+)\*\):? ",line)
			try :
				descript = re.sub(re.escape(line_num.group(0)),"",line)
				line_blk_dict[int(line_num.group(1))] = descript.strip()
			except AttributeError:
				print(line)
				#assert False
				continue

		prev_line_num = ""
		prev_descript = ""
		for ind,line in enumerate(ed_lines) :
			line = line.strip()
			if line == "" or line == "\n" :
				continue

			line_num = re.search("\(\*([0-9]+)\*\): ",line)
			try :
				descript = re.sub(re.escape(line_num.group(0)),"",line)
			except :
				print(repr(line))
				#assert False
				continue

			if prev_line_num == "" :
				prev_line_num = int(line_num.group(1))
				prev_descript = descript
				continue
			try :
				ed = re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower()
			except :
				print(prev_descript)
				print(ind)
				#assert False
				continue
			line_num = int(line_num.group(1))

			Dict_append(ed_line_dict, ed, (prev_line_num+1,line_num-1))
			
			tract = re.search("\(((?:Area|Tract) \S+)",prev_descript)
			try :
				tract = tract.group(1)
				ed_tract_dict[ed] = tract
			except :
				print("No tract found: "+prev_descript)

			prev_line_num = line_num
			prev_descript = descript

		#finish adding last ED line to dicts
		try :
			Dict_append(ed_line_dict, re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower(), (prev_line_num+1,max(line_blk_dict.keys())))
			ed_tract_dict[re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower()] = re.search("\(((?:Area|Tract) \S+)",prev_descript).group(1)
		except :
			print("Problem with last line in ED lines")

		ed_blk_dict = {} #lookup ed -> which block numbers
		blk_desc_dict = {} #lookup ed+block identifier -> description for block

		print("Creating lookup dictionaries for block number and block description...")

		for ed, blk_list in ed_line_dict.items() :
			for blk in blk_list :
				for line in range(blk[0],blk[1]) :
					try :
						line_blk_dict[line]
					except KeyError :
						continue
					blk_line = line_blk_dict[line]
					if re.search("Block|Image",blk_line) :
						continue
					blk_num = re.search("^([0-9A-Za-z]+)[\-\— ]+",blk_line)
					if blk_num :
						desc = re.sub(re.escape(blk_num.group(0)),"",blk_line)
						desc = desc.replace('\n','')
						desc_list = desc.split(', ')
						has_dir = re.search("^.\.[\s]?.\.?$",desc_list[-1])
						if has_dir:
							dir_to_prepend = has_dir.group(0)
							desc = ', '.join([standardize_street_40_desc(dir_to_prepend+' '+i) for i in desc_list[:-1]]) #put direction in front of all streets
						blk_num = blk_num.group(1)
						Dict_append(ed_blk_dict,ed,blk_num)
						blk_desc_dict[ed+'_'+blk_num] = desc

		output = open(geo_path+"ed_blk_desc.txt","w+")

		for ind,(blk,desc) in enumerate(blk_desc_dict.items()) :
			st_list = ""
			for st in desc.split(", ") :
				diff = False
				foo = st
				if st.encode('ascii',errors='ignore') != st :
					diff = True
				st = preserve_chars(st)
				st_add = standardize_street_40_desc(st)
				#if use_fuzz :
				#    st_add = fuzzy_match_list(st_add)
				if diff:
					print(str(ind)+": before: "+foo+", after: "+st_add)
				st_list += st_add+", "
			st_list = st_list[:-2]
			try :
				output.write((str(ind)+", "+blk+", "+st_list+"\n").encode('utf8'))
			except UnicodeEncodeError:
				#print(str(ind)+", "+blk+", "+st_list)
				#assert False
				continue

		output.close()

		# HERE BEGINS CODE FOR MATCHING DESCRIPTION BLOCKS TO STGRID BLOCKS #

# Run the entire descriptions algorithm on the given city_info
def ed_desc_algo(city_info, paths, grid_street_var='FULLNAME'):

	city_name, state_abbr, decade = city_info
	city_spaces = city_name
	city_name = city_name.replace(' ','')

	global discovered_problem
	discovered_problem = 0

	# Ensure required files exist (i.e. dependent processes have been run)
	print("Checking for files necessary to process %s (Descriptions algorithm)" % (city_name))
	check_for_desc_files(city_info, paths, grid_street_var)

	# Run descriptions algorithm
	print("Processing %s (Descriptions algorithm)" % (city_name))
	run_desc_analysis(city_info, paths, grid_street_var)

	# Draw the ED map based on descriptions algorithm
	print("Creating ED Map for %s (Descriptions algorithm)" % (city_name))
	draw_EDs(city_info=city_info, 
		paths=paths, 
		new_var_name="ED_desc", 
		is_desc=True, 
		grid_street_var=grid_street_var)

#
# Misc ED functions
#

# Get adjacent EDs (used for validation of geocoding)
def get_adjacent_eds(city_info, geo_path):
	
	city_name, state_abbr, decade = city_info

	# Files

	# "vm" is the verified map (e.g., ED or block map)
	vm = geo_path + city_name + "_" + str(decade) + "_ED.shp"
	# Feature Class to Feature Class file
	fc = city_name + state_abbr + "_" + str(decade) + "_ED_Feature.shp"
	# Spatial weights files:
	swm_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_spatweight.swm"
	swm_table = geo_path + city_name + state_abbr + "_" + str(decade) + "_swmTab.dbf"
	# Amory's formatted EDs dbf
	fe = geo_path + city_name + state_abbr + "_" + str(decade) + "_formattedEDs.dbf"
	fe_file = city_name + state_abbr + "_" + str(decade) + "_formattedEDs.dbf"

	print("creating the swm")
	# Process: Feature Class to Feature Class
	ftc_mapping = """OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,%s,OBJECTID,-1,-1;
		ed \"ed\" true true false 19 Double 0 0 ,First,#,%s,ed,-1,-1;
		Shape_Leng \"Shape_Leng\" true true false 19 Double 0 0 ,First,#,%s,Shape_Leng,-1,-1;
		Shape_Area \"Shape_Area\" true true false 19 Double 0 0 ,First,#,%s,Shape_Area,-1,-1;
		ED_int \"ED_int\" true true false 5 Long 0 5 ,First,#,%s,ED_int,-1,-1;
		Ed_str \"Ed_str\" true true false 5 Text 0 0 ,First,#,%s,Ed_str,-1,-1""" % (vm, vm, vm, vm, vm, vm)
	arcpy.FeatureClassToFeatureClass_conversion(in_features=vm, 
		out_path=geo_path, 
		out_name=fc, 
		field_mapping=ftc_mapping)

		#Calculate some fields

	arcpy.CalculateField_management(in_table=geo_path+fc, 
		field="Shape_Leng", 
		expression="!SHAPE.LENGTH!",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=geo_path+fc, 
		field="Shape_Area", 
		expression="!SHAPE.AREA!",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=geo_path+fc, 
		field="ED_int", 
		expression="int(!ed!)",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=geo_path+fc, 
		field="Ed_str", 
		expression="str(int(!ed!))",
		expression_type="PYTHON_9.3")

	# Process: Generate Spatial Weights Matrix
	arcpy.GenerateSpatialWeightsMatrix_stats(Input_Feature_Class=geo_path+fc, 
		Unique_ID_Field="ED_int", 
		Output_Spatial_Weights_Matrix_File=swm_file, 
		Conceptualization_of_Spatial_Relationships="CONTIGUITY_EDGES_CORNERS", 
		Distance_Method="EUCLIDEAN", 
		Exponent=1,  
		Number_of_Neighbors=0, 
		Row_Standardization="NO_STANDARDIZATION")

	# Process: Convert Spatial Weights Matrix to Table
	arcpy.ConvertSpatialWeightsMatrixtoTable_stats(Input_Spatial_Weights_Matrix_File=swm_file, 
		Output_Table=swm_table)

	# Do the thing to create the lists for adjacent EDs (inclusive of the ED)

	field_names = [x.name for x in arcpy.ListFields(swm_table)]
	cursor = arcpy.da.SearchCursor(swm_table, field_names)
	silly_dict = {}

	for row in cursor :
		Dict_append_unique(silly_dict,row[2],row[3])
		Dict_append_unique(silly_dict,row[2],row[2])

	#Remove ED = 0 (unknown EDs)
	silly_dict = {k:[i for i in v if v != 0] for k,v in silly_dict.items() if k != 0}

	#Formatted ED's from Amory's weights matrix formating script
	if os.path.isfile(fe):
		os.remove(fe)	

	arcpy.CreateTable_management(out_path=geo_path, 
		out_name=fe_file)

	arcpy.AddField_management(in_table=fe, 
		field_name="ed", 
		field_type="SHORT")
	arcpy.AddField_management(in_table=fe, 
		field_name="contig_ed", 
		field_type="TEXT")

	rows = arcpy.InsertCursor(fe)

	for k, v in silly_dict.items():
		row = rows.newRow()
		row.setValue("ed",k)
		v = [str(x) for x in v]
		row.setValue("contig_ed",";".join(v))
		rows.insertRow(row)

	del row
	del rows

def combine_ed_maps(city_info, geo_path, hn_ranges):

	# Function to select best ED guess based on three methods
	def select_best_ed_guess(x):
		
		# 1940 also had cblk_id, but 1930 does not (may need if/else with decade in future)
		try:
			_, _, ed_desc, ed_inter, ed_geocode, _ = x
		except:
			_, _, ed_desc, ed_inter, ed_geocode = x
		# Split if multiple EDs
		if '|' in str(ed_desc):
			ed_desc = ed_desc.split('|')
			ed_desc = [i for i in ed_desc]
		else:
			ed_desc = [ed_desc]
		if '|' in str(ed_inter):
			ed_inter = ed_inter.split('|')
			ed_inter = [i for i in ed_inter]
		else:
			ed_inter = [ed_inter]
		if '|' in str(ed_inter):
			ed_geocode = ed_geocode.split('|')
			ed_geocode = [i for i in ed_geocode]
		else:
			ed_geocode = [ed_geocode]

		# List of EDs guessed
		ed_list = list(set(ed_desc + ed_inter + ed_geocode))
		ed_list = [i for i in ed_list if i != '']

		# List of ED guesses by confidence
		ed_guess_list = []
		# Initialize guess to be missing, confidence -1 
		ed_guess_conf = [-1, '']
		
		def check_ed_num(ed_n, ed_list):
			for ed in ed_list:
				if ed_n == ed.replace(r'[a-zA-Z]+',''):
					return True
			return False

		# If no guesses, return missing
		if len(ed_list) == 0:
			return ed_guess_conf
		# Otherwise, try to find a unique guess
		else:
			for ed in ed_list:
				ed_n = ed.replace(r'[a-zA-Z]+','')
				in_desc = check_ed_num(ed_n, ed_desc)
				in_inter = check_ed_num(ed_n, ed_inter)
				in_geocode = check_ed_num(ed_n, ed_geocode)
				# If all three agree, highest confidence
				if in_desc and in_inter and in_geocode:
					ed_guess_list.append([ed, 1])
				# If any two agree, second highest confidence
				elif (in_desc and in_inter) or (in_desc and in_geocode) or (in_inter and in_geocode):
					ed_guess_list.append([ed, 2])
				# If ed_desc not missing, third highest confidence
				elif in_desc:
					ed_guess_list.append([ed, 3])
				# If ed_inter not missing, fourth highest confidence
				elif in_inter:
					ed_guess_list.append([ed, 4])
				# If ed_geocode not missing, fifth highest confidence
				elif in_geocode:
					ed_guess_list.append([ed, 5])
		
		# If didn't find a guess, return guess to be missing, confidence -1
		if len(ed_guess_list) == 0:
			return ed_guess_conf

		df_ed_guess = pd.DataFrame(ed_guess_list, columns=['ed','conf'])
		num_guesses = df_ed_guess.groupby(['conf'], as_index=False).size().to_dict()
		df_ed_guess['count'] = df_ed_guess.apply(lambda x: num_guesses[x['conf']], axis=1)
		df_one_ed_guess = df_ed_guess[df_ed_guess['count']==1]
		if len(df_one_ed_guess) > 0:
			ed_conf = df_one_ed_guess['conf'].min()
			ed_guess = df_one_ed_guess.loc[df_one_ed_guess['conf']==ed_conf,'ed'].values[0]
			ed_guess_conf = [ed_conf, ed_guess]
		elif len(df_ed_guess[df_ed_guess['count']>1]) > 0:
			df_two_plus_ed_guess = df_ed_guess[df_ed_guess['count']>1]
			for ed in df_two_plus_ed_guess['ed'].tolist():
				if ed in ed_desc:
					if (ed in ed_inter) or (ed in ed_geocode):
						ed_guess_conf = [2, ed]
						return ed_guess_conf
					else:
						ed_guess_conf = [3, ed]
						return ed_guess_conf
				elif ed in ed_inter:
					if ed in ed_geocode:
						ed_guess_conf = [2, ed]
						return ed_guess_conf
					else:
						ed_guess_conf = [4, ed]
						return ed_guess_conf
				elif ed in ed_geocode:
					ed_guess_conf = [5, ed]
					return ed_guess_conf

		return ed_guess_conf

	def format_ed_desc(ed):
		if ed == '':
			return ed
		for c in ed:
			if c.islower():
				ed = ed.replace(c,c.upper())
		else:
			return ed

	def get_ed_geocode(eds):
		eds = [ed for ed in eds if ed != '']
		if len(eds) == 0:
			return ''
		elif len(eds) == 1:
			return eds[0]
		else:
			return '|'.join(eds)

	city_name, state_abbr, decade = city_info 
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	ed_inter_shp = geo_path + city_name + '_' + str(decade) + '_ed_inter.shp'
	df_ed_inter = load_shp(ed_inter_shp)
	df_ed_inter.loc[:,'ed_inter'] = df_ed_inter['ed_inter'].astype(str).replace('0','')
	df_ed_inter.loc[:,'pblk_id'] = df_ed_inter['pblk_id'].astype(int)

	ed_geo_shp = geo_path + city_name + '_' + str(decade) + '_ed_geo.shp'
	df_ed_geo = load_shp(ed_geo_shp)
	df_ed_geo.loc[:,'pblk_id'] = df_ed_geo['pblk_id'].astype(int)
	df_ed_geo.loc[:,['ED_ID','ED_ID2','ED_ID3']]= df_ed_geo[['ED_ID','ED_ID2','ED_ID3']].astype(object).replace(np.nan,0).astype(int).astype(str).replace('0','')

	ed_desc_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_desc.shp'

	# If 1940, can use non-spatial joins...
	if decade == 1940:
		df_ed_desc= load_shp(ed_desc_shp)
		df_ed_desc.loc[:,'ed_desc'] = df_ed_desc['ed_desc'].astype(str).replace('None','')
		df_ed_desc.loc[:,'cblk_id'] = df_ed_desc['cblk_id'].astype(str).replace('None','')
		df_ed_desc.loc[:,'pblk_id'] = df_ed_desc['pblk_id'].astype(int)
		df_ed_inter_geo = df_ed_inter.merge(df_ed_geo.drop(['geometry'], axis=1), on='pblk_id')
		df = df_ed_inter_geo.merge(df_ed_desc.drop(['geometry'], axis=1), on='pblk_id')
	# ...otherwise, spatially join ed_desc polygons to assign ed_desc guesses to pblk_id
	else:
		ed_inter_desc_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_inter_desc.shp'
		arcpy.SpatialJoin_analysis(target_features=ed_inter_shp, 
			join_features=ed_desc_shp, 
			out_feature_class=ed_inter_desc_shp, 
			join_operation="JOIN_ONE_TO_ONE", 
			join_type="KEEP_ALL",
			match_option="HAVE_THEIR_CENTER_IN")
		df_ed_inter_desc_shp = load_shp(ed_inter_desc_shp)
		df_ed_inter_desc_shp.loc[:,'ed_desc'] = df_ed_inter_desc_shp['ed_desc'].astype(str).replace('None','')
		df = df_ed_inter_desc_shp.merge(df_ed_geo.drop(['geometry'], axis=1), on='pblk_id')

	# Select relevant variables and extract best ED guesses
	df.loc[:,'ed_geocode'] = df[['ED_ID','ED_ID2','ED_ID3']].apply(lambda x: get_ed_geocode(x), axis=1)
	df.loc[:,'ed_desc'] = df.apply(lambda x: format_ed_desc(x['ed_desc']), axis=1)
	df.loc[:,'ed_inter'] = df['ed_inter'].astype(str)
	if decade == 1940:
		relevant_vars = ['geometry','pblk_id','ed_desc','ed_inter','ed_geocode','cblk_id']
	else:
		relevant_vars = ['geometry','pblk_id','ed_desc','ed_inter','ed_geocode']
	df_ed_guess = df.loc[:,relevant_vars]
	df_ed_guess.loc[:,'ed_conf'], df_ed_guess.loc[:,'ed_guess'] = zip(*df_ed_guess[relevant_vars].apply(lambda x: select_best_ed_guess(x), axis=1))

	# Relabel confidence variable descriptively 
	label_conf = {}

	label_conf[-1] = "-1. No guess"
	label_conf[1] = "1. Three agree"
	label_conf[2] = "2. Two agree"
	label_conf[3] = "3. Descriptions only"
	label_conf[4] = "4. Intersections only"
	label_conf[5] = "5. Geocoding only"

	df_ed_guess.loc[:,'ed_conf'] = df_ed_guess.apply(lambda x: label_conf[x['ed_conf']], axis=1)

	ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_guess.shp'
	save_shp(df_ed_guess, ed_guess_shp)

# Save information
def get_ed_guess_stats(city_info, paths, hn_ranges):
	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"
	# Load dbf data
	ed_guess_file = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_guess.shp'
	df_ed_guess = load_shp(ed_guess_file, hn_ranges)
	if decade == 1940:
		# Get number of blocks in block description file
		with open(geo_path + 'ed_blk_desc.txt','r') as blk_desc_file :
			blk_desc = blk_desc_file.readlines()
		for ind,line in enumerate(blk_desc) :
			blk_desc[ind] = line.strip()    

		blk_desc_dict = {} # lookup SM ed_blk identifier -> SM description of block
	
		for line in blk_desc :
			line = line.split(', ')
			try :
				blk = line[1].split('-')[1]
			except :
				if line[1] :
					blk = line[1]
				else :
					continue
			blk_desc_dict[blk] = list(np.unique(line[2:]))
		# Initialize block guess count
		df_ed_guess['b_guess'] = df_ed_guess['cblk_id'] != ''
		# Create a tabular summary of number guessed by confidence in guess
		info1 = df_ed_guess.groupby(['ed_conf'], as_index=False).count()[['ed_conf','pblk_id']]
		info2 = df_ed_guess.groupby(['b_guess'], as_index=False).count()[['b_guess','pblk_id']]
		info3 = pd.DataFrame(data={'ed_conf':'Num Census Blocks', 'pblk_id':[len(blk_desc_dict.keys())]})
		info = info1.append(info2)
		info = info.append(info3)
		info.loc[info['ed_conf'].isnull(),'ed_conf'] = info.loc[info['b_guess'].notnull(),'b_guess']
		info['ed_conf'].replace({False:'No Block Guess',True:'Block Guess'},inplace=True)
		del info['b_guess']
		info['city'] = city_name
		info['state'] = state_abbr
	else:
		# Create a tabular summary of number guessed by confidence in guess
		info = df_ed_guess.groupby(['ed_conf'], as_index=False).count()[['ed_conf','pblk_id']]
		info['city'] = city_name
		info['state'] = state_abbr		
	return info

def run_ed_guess(decade=1940, grid_street_var="FULLNAME"):
	
	city_info_list0 = [['Akron','OH'],
		['Albany','NY'],
		['Atlanta','GA'],
		['Baltimore','MD'],
		['Birmingham','AL'],
		['Boston','MA'],
		['Bridgeport','CT'],
		['Bronx','NY'],
		['Buffalo','NY'],
		['Chicago','IL']]

	city_info_list1 = [['Cincinnati','OH'],
		['Columbus','OH'],
		['Dallas','TX'],
		['Dayton','OH'],
		['Denver','CO'],
		['Des Moines','IA'],
		['Flint','MI'],
		['Fort Worth','TX'],
		['Grand Rapids','MI'],
		['Hartford','CT']]

	city_info_list2 = [['Houston','TX'],
		['Indianapolis','IN'],
		['Jacksonville','FL'],
		['Jersey City','NJ'],
		['Kansas City','KS'],
		['Kansas City','MO'],
		['Miami','FL'],
		['Milwaukee','WI'],
		['Minneapolis','MN'],
		['Nashville','TN']]

	city_info_list3 = [['New Haven','CT'],
		['New Orleans','LA'],
		['Newark','NJ'],
		['Oakland','CA'],
		['Oklahoma City','OK'],
		['Omaha','NE'],
		['Paterson','NJ'],
		['Pittsburgh','PA'],
		['Portland','OR'],
		['Providence','RI']]

	city_info_list4 = [['San Antonio','TX'],
		['San Diego','CA'],
		['San Francisco','CA'],
		['Scranton','PA'],
		['Seattle','WA'],
		['Spokane','WA'],
		['Springfield','MA'],
		['St Louis','MO'],
		['St Paul','MN'],
		['Syracuse','NY']]

	city_info_list5 = [['Toledo','OH'],
		['Trenton','NJ'],
		['Tulsa','OK'],
		['Washington','DC'],
		['Worcester','MA'],
		['Yonkers','NY']] 


	def do_city_list(city_info_list):
		city_list = []
		for city_info in city_info_list:
			city_name, state_abbr, decade = city_info
			city_list.append(city_info+[fullname_var])
		for city_info in city_list:
			try:
				get_ed_guesses(city_info)
			except:
				continue

	city_info_list = city_info_list0 + city_info_list1 + city_info_list2 + \
		city_info_list3 + city_info_list4 + city_info_list5

	info_list = []
	for city_info in city_info_list:
		try:
			info_list.append(get_ed_guess_stats(city_info,decade))
		except:
			continue
	df = pd.concat(info_list)
	df_to_write = pd.pivot_table(df, values='pblk_id', index=['city','state'], columns=['ed_conf'])
	datestr = time.strftime("%Y_%m_%d")
	df_to_write.to_csv('S:/Users/Chris/ed_guess_info'+str(decade)+'_'+datestr+'.csv')

	num_finished = len(df_to_write)

	print("%s of %s cities processed for %s" % (str(num_finished), str(len(city_info_list)), str(decade)))
