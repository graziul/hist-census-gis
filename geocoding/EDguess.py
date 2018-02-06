#
# EDguess.py - combines multiple automated approaches to identifying EDs into one shapefile
#

from __future__ import print_function
import os
import re
import math
import csv
import xlrd
import sys
import pickle
import pandas as pd
import numpy as np
import arcpy
from collections import defaultdict
from fuzzywuzzy import fuzz
from blocknum.blocknum import *
arcpy.env.overwriteOutput = True

##
## Function definitions
##

#
# Shared functions
#

# Dict: add v(alue) to k(ey), create k if it doesn't exist
def Dict_append(Dict, k, v) :
	if not k in Dict :
		Dict[k] = [v]
	else :
		Dict[k].append(v)

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
	if not k in Dict :
		Dict[k] = [v]
	else :
		if not v in Dict[k] :
			Dict[k].append(v)

# Standardize numbered street name
def Num_Standardize(NAME) :

	NAME = re.sub("^[Tt]enth","10th",NAME)
	NAME = re.sub("^[Ee]leven(th)?","11th",NAME)
	NAME = re.sub("^[Tt]wel[fv]?e?th","12th",NAME)
	NAME = re.sub("^[Tt]hirteen(th)?","13th",NAME)
	NAME = re.sub("^[Ff]ourt[h]?een(th)?","14th",NAME)
	NAME = re.sub("^[Ff]ift[h]?een(th)?","15th",NAME)
	NAME = re.sub("^[Ss]ixt[h]?een(th)?","16th",NAME)
	NAME = re.sub("^[Ss]event[h]?een(th)?","17th",NAME)
	NAME = re.sub("^[eE]ighteen(th)?","18th",NAME)
	NAME = re.sub("^[Nn]inet[h]?e+n(th)?","19th",NAME)
	NAME = re.sub("^[Tt]went[iy]eth","20th",NAME)
	NAME = re.sub("^[Tt]hirt[iy]eth","30th",NAME)
	NAME = re.sub("^[Ff]o[u]?rt[iy]eth","40th",NAME)
	NAME = re.sub("^[Ff]ift[iy]eth", "50th",NAME)
	NAME = re.sub("^[Ss]ixt[iy]eth", "60th",NAME)
	NAME = re.sub("^[Ss]event[iy]eth", "70th",NAME)
	NAME = re.sub("^[Ee]ight[iy]eth", "80th",NAME)
	NAME = re.sub("^[Nn]inet[iy]eth", "90th",NAME)

	NAME = re.sub("[Tt]wenty[ \-]*","2",NAME)
	NAME = re.sub("[Tt]hirty[ \-]*","3",NAME)
	NAME = re.sub("[Ff]orty[ \-]*","4",NAME)
	NAME = re.sub("[Ff]ifty[ \-]*","5",NAME)
	NAME = re.sub("[Ss]ixty[ \-]*","6",NAME)
	NAME = re.sub("[Ss]eventy[ \-]*","7",NAME)
	NAME = re.sub("[Ee]ighty[ \-]*","8",NAME)
	NAME = re.sub("[Nn]inety[ \-]*","9",NAME)
	
	if re.search("(^|[0-9]+.*)([Ff]irst|[Oo]ne)",NAME) : NAME = re.sub("([Ff]irst|[Oo]ne)","1st",NAME)
	if re.search("(^|[0-9]+.*)([Ss]econd|[Tt]wo)",NAME) : NAME = re.sub("([Ss]econd|[Tt]wo)","2nd",NAME)
	if re.search("(^|[0-9]+.*)([Tt]hird|[Tt]hree)",NAME) : NAME = re.sub("([Tt]hird|[Tt]hree)","3rd",NAME)
	if re.search("(^|[0-9]+.*)[Ff]our(th)?",NAME) : NAME = re.sub("[Ff]our(th)?","4th",NAME)
	if re.search("(^|[0-9]+.*)([Ff]ifth|[Ff]ive)",NAME) : NAME = re.sub("([Ff]ifth|[Ff]ive)","5th",NAME)
	if re.search("(^|[0-9]+.*)[Ss]ix(th)?",NAME) : NAME = re.sub("[Ss]ix(th)?","6th",NAME)
	if re.search("(^|[0-9]+.*)[Ss]even(th)?",NAME) : NAME = re.sub("[Ss]even(th)?","7th",NAME)
	if re.search("(^|[0-9]+.*)[Ee]igh?th?",NAME) : NAME = re.sub("[Ee]igh?th?","8th",NAME)
	if re.search("(^|[0-9]+.*)[Nn]in(th|e)+",NAME) : NAME = re.sub("[Nn]in(th|e)+","9th",NAME)
	
	return NAME

# Prepare map intersections
def prepare_map_intersections(stgrid_file, fullname_var, paths) :
	print("Preparing Map Intersections File")

	city_name, _ =  os.path.splitext(stgrid_file)
	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"
	
	if not os.path.exists(geo_path + "IntersectionsIntermediateFiles"):
		os.makedirs(geo_path + "IntersectionsIntermediateFiles")
	intermed_path = geo_path + "IntersectionsIntermediateFiles/"

	latest_stage = intermed_path + "fullname_dissolve.shp"
	#dissolve all street segments based on FULLNAME
	arcpy.Dissolve_management(in_features = geo_path + stgrid_file, 
		out_feature_class = latest_stage,
		dissolve_field=fullname_var, 
		statistics_fields="", 
		multi_part="SINGLE_PART", 
		unsplit_lines="DISSOLVE_LINES")

	previous_stage = latest_stage
	latest_stage =  intermed_path + "fullname_dissolve_split.shp"
	#split street segments at their intersections
	arcpy.FeatureToLine_management(in_features = previous_stage, 
		out_feature_class = latest_stage,
		cluster_tolerance="", 
		attributes="ATTRIBUTES")

	previous_stage = latest_stage
	latest_stage = intermed_path + "split_endpoints.shp"
	#create points at both ends of every split segment
	arcpy.FeatureVerticesToPoints_management(in_features = previous_stage, 
		out_feature_class = latest_stage,
		point_location="BOTH_ENDS")

	#calculate x and y coordinates of points
	arcpy.AddGeometryAttributes_management(latest_stage, 
		"POINT_X_Y_Z_M")

	previous_stage = latest_stage
	latest_stage = intermed_path+"xy_dissolve.shp"
	#dissolve points based on x and y
	arcpy.Dissolve_management(in_features = previous_stage, 
		out_feature_class = latest_stage,
		dissolve_field="POINT_X;POINT_Y", 
		statistics_fields="", 
		multi_part="MULTI_PART", 
		unsplit_lines="DISSOLVE_LINES")

	arcpy.AddField_management(in_table = latest_stage, 
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
	arcpy.CalculateField_management(in_table = latest_stage, 
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
		fullname_var, 
		fullname_var, 
		target_feature_file, 
		fullname_var, 
		target_feature_file, 
		target_feature_file, 
		target_feature_file, 
		previous_stage, 
		previous_stage, 
		previous_stage)

	arcpy.SpatialJoin_analysis(target_features = target_feature_file, 
		join_features = previous_stage,
		out_feature_class = latest_stage, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL",
		field_mapping=field_mapping_ls,
		match_option="INTERSECT", 
		search_radius="", 
		distance_field_name="")

	# EXPORT ATTRIBUTE TABLE
	arcpy.ExportXYv_stats(Input_Feature_Class = latest_stage, 
		Value_Field="FID;Join_Count;TARGET_FID;FID_fullna;"+fullname_var+";ORIG_FID;POINT_X;POINT_Y;POINT_X_1;POINT_Y_1;Interse_ID", 
		Delimiter="COMMA",
		Output_ASCII_File = intermed_path + city_name + "_Intersections.txt", 
		Add_Field_Names_to_Output="ADD_FIELD_NAMES")

# Draw ED maps (descriptions, intersections)
def draw_EDs(city, state, paths, new_var_name, is_desc) :

	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"
	intermed_path = geo_path + "/IntersectionsIntermediateFiles/"

	targ = intermed_path + city + state + "_1930_stgrid_edit_Uns2_spatial_join.shp"
	targ1 = geo_path + city + "_1930_Pblk.shp"

	inter = arcpy.Intersect_analysis(in_features=[targ,targ1],
		out_feature_class=intermed_path + "intersectToGetEDs.shp",
		join_attributes="ALL", 
		cluster_tolerance="-1 Unknown", 
		output_type="INPUT")

	field_names = [x.name for x in arcpy.ListFields(inter)]
	cursor = arcpy.da.SearchCursor(inter, field_names)
	inter_polyblk_dict = {}
	polyblk_inter_dict = {} #polygon block ID -> intersections in block
	
	for row in cursor :
		Dict_append_unique(inter_polyblk_dict, row[field_names.index("Interse_ID")], row[field_names.index("pblk_id")])
		Dict_append_unique(polyblk_inter_dict, row[field_names.index("pblk_id")], row[field_names.index("Interse_ID")])

	# If using Amory's ED description method do this
	if is_desc:
		output_shp = geo_path+city+"_ED_desc.shp"
		arcpy.CreateFeatureclass_management(geo_path,city+"_ED_desc.shp")
		blk_file = intermed_path+"fullname_dissolve_split.shp"
		arcpy.MakeFeatureLayer_management(blk_file,"blk_lyr")
		arcpy.AddField_management(output_shp, "ed_desc", "TEXT", "", "", 20)
		with arcpy.da.InsertCursor(output_shp, ("SHAPE@", "ed_desc")) as cursor:
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
		arcpy.Delete_management(intermed_path+"poly_lyr.shp")
	# If using Amory's intersection method do this...
	elif ~is_desc:
		blk_ed_dict = {}
		for blk in polyblk_inter_dict.keys() :
				#retrieve a slice of Intersect_Info_DICT for just the intersections associated with blk
				blk_dict = {key: Intersect_Info_DICT[key] for key in Intersect_Info_DICT.viewkeys() if int(key) in polyblk_inter_dict[blk]}
				result = aggregate_blk_inter_data(blk_dict)
				blk_ed_dict[blk] = result
		try :
			arcpy.AddField_management (targ1, new_var_name, "TEXT")
		except :
			pass
		with arcpy.da.UpdateCursor(targ1, ["pblk_id",new_var_name]) as up_cursor:
			for row in up_cursor :
				row[1] = blk_ed_dict[row[0]]
				if row[1] == None :
					row[1] = 0
				up_cursor.updateRow(row)
		return polyblk_inter_dict

#
# Amory's ED descriptions script
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

#Returns just the NAME component of the street phrase, if any#
#If second argument is True, return a list of all components 
def isolate_st_name(st,whole_phrase = False) :
	if (st == None or st == '' or st == -1) or (not isinstance(st, str)) :
		return ''
	else :
		TYPE = re.search(" (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$",st)
		if(TYPE) :
			TYPE = TYPE.group(0)
			st = re.sub(TYPE+"$", "",st)
			TYPE = TYPE.strip()
		DIR = re.search("^[NSEW]+ ",st)
		if(DIR) :
			DIR = DIR.group(0)
			st = re.sub("^"+DIR, "",st)
			DIR = DIR.strip()
		st = st.strip()
		
	if whole_phrase :
		return [DIR,st,TYPE]
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

# looks for duplicate adjacent elements and deletes one
# iterate backwards to avoid problems with iterating and modifying list simultaneously...!
def f7(seq):
	ind = len(seq) - 2
	while ind >= 0 :
		if seq[ind] == seq[ind+1] :
			del seq[ind+1]
		ind -= 1
	return seq

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
		if len(l) > 200:
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

def RunAnalysisDesc(city, state, paths, InterLines, Descriptions, shp_targ) :

	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	output = open(geo_path + city+"_EDs.txt","w+")
	problem_EDs = open(geo_path + city+"_problem_EDs.txt","w+")

	debug = False

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
	Intersect_ST_dict = defaultdict(list) # lookup intersection -> which STs (phrases)
	Intersect_BLOCK_dict = {} # lookup intersection -> which BLOCKs
	Intersect_NAME_dict = defaultdict(list) # lookup intersection -> which STs (NAMEs)
	ST_Intersect_dict = {} # lookup ST -> which intersections
	BLOCK_Intersect_dict = {} # lookup BLOCK ID -> which intersections
	BLOCK_NAME_dict = {} # lookup BLOCK ID -> NAME of segment

	print("Preparing Input for "+city+ " (descriptions)")

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
		ED_description_dict[line_list[0]] = [x.strip('"\' \n') for x in line_list[1:]]
		ED_NAME_description_dict[line_list[0]] = [isolate_st_name(x.strip('"\' \n')) for x in line_list[1:]]

	# Isolate St NAMEs
	arcpy.AddField_management (shp_targ, "NAME", "TEXT")
	with arcpy.da.UpdateCursor(shp_targ, [fullname_var,"NAME"]) as up_cursor:
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
		descript = f7(descript)
		
		intersect = []
		start_ind = 0
		#find an exactly matching starting intersection
		while start_ind <= len(descript) - 1:
			start_streets = [descript[start_ind], descript[(start_ind+1)%len(descript)]]
			if debug:print("start_streets: "+str(start_streets))
			intersect = get_intersect_by_stnames(start_streets)
			if intersect == [] or start_streets[0] == start_streets[1] :
				start_ind += 1
			else :
				break
		if intersect == [] or start_streets[0] == start_streets[1] :
			if debug:print("Could not find any exactly matching intersections out of "+str(descript))
		else :
			#breadth-first search through block/intersection dicts to find
			#path to intersection with next street in the description

			#change descript to be just the NAMEs of the streets
			descript = ED_NAME_description_dict[ED]
			#keep only unique street names, but preserve order in description
			descript = f7(descript)
			if debug:print(str(ED)+": "+str(descript))

			success, string = find_descript_segments(descript,intersect,start_ind,start_streets,debug=debug)
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
		descript = f7(descript)
		
		#find an exactly matching starting intersection
		while start_ind <= len(descript) - 1:
			start_streets = [descript[start_ind], descript[(start_ind+1)%len(descript)]]
			if debug:print("start_streets: "+str(start_streets))
			intersect = get_intersect_by_stnames(start_streets)
			if intersect == [] :
				start_ind += 1
			else :
				break
		if intersect == [] :
			if debug:print("Could not find any exactly matching intersections out of "+str(descript))
		else :
			#breadth-first search through block/intersection dicts to find
			#path to intersection with next street in the description

			#change descript to be just the NAMEs of the streets
			descript = ED_NAME_description_dict[ED]
			#keep only unique street names, but preserve order in description
			descript = f7(descript)
			if debug:print(str(ED)+": "+str(descript))

			success, string = find_descript_segments(descript,intersect,start_ind,start_streets,fuzzy = True,debug=debug)
			if success :
				if debug:print("FUZZY WORKED FOR "+str(ED)+"!!!!!!!!!!!!!!!!!!!!!")
				output.write(str(ED)+": "+string+"\n")
				ED_Intersect_ID_dict[ED] = string
			else :
				problem_EDs.write(str(ED)+": "+string+"\n")

	if debug:print("discovered_problem: "+str(discovered_problem))

def ed_desc_algo(city, state, fullname_var, paths):

	city = city.replace(' ','')
	r_path, script_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	global discovered_problem
	discovered_problem = 0

	shp_targ = geo_path + city + state + "_1930_stgrid_edit_Uns2.shp"
	# LOAD SM DESCRIPTIONS....
	if os.path.isfile(shp_targ) :
		#pass
		prepare_map_intersections(city + state +'_1930_stgrid_edit_Uns2.shp', fullname_var, paths)
	else :
		print(city+": Error finding stgrid")
		return

	Descriptions_path = 'S:/Projects/1940Census/SMdescriptions/'+city+'_EDdraw_test.txt'
	Intersect_TXT = open(geo_path+"/IntersectionsIntermediateFiles/"+city+state+'_1930_stgrid_edit_Uns2_Intersections.txt')
	InterLines = Intersect_TXT.readlines()[1:]
	Descriptions = open(Descriptions_path).readlines()

	# Derived Dict #
	global ED_Intersect_ID_dict
	ED_Intersect_ID_dict = {} # lookup ED -> string of Intersection IDs

	st_grid_exists = os.path.isfile(shp_targ)
	descriptions_exist = os.stat(Descriptions_path).st_size != 0
	if st_grid_exists and descriptions_exist:
		RunAnalysisDesc(city, state, paths, InterLines, Descriptions, shp_targ)
	else :
		print(city+": Error finding stgrid ("+str(st_grid_exists)+") and/or descriptions ("+str(descriptions_exist)+")")
	
	print("Creating ED Map for %s (Descriptions algorithm)" % (city))
	draw_EDs(city, state, paths, "ED_desc", True)

#
# Amory's intersection script
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

def csv_from_excel(excel_file, csv_name):
	workbook = xlrd.open_workbook(excel_file)
	all_worksheets = workbook.sheet_names()
	for i,worksheet_name in enumerate(all_worksheets[:-1]) : #exclude last worksheet (1940 stnames)
		worksheet = workbook.sheet_by_name(worksheet_name)
		if i==0 :
			namename = csv_name
		elif i == 1 :
			namename = csv_name+"_ED"
		else :
			assert(True == False)
		with open('{}.csv'.format(namename), 'w+') as your_csv_file:
			for rownum in range(worksheet.nrows):
				rowstr = ""
				for v in worksheet.row_values(rownum) :
					if v=="" :
						break
					rowstr = rowstr+v+","
				rowstr = rowstr[:-1] #remove trailing comma
				your_csv_file.write(rowstr+"\n")

def morse_standardize(st) :
	if re.search('[Cc]ity [Ll]imits',st) :
		return 'City Limits'
	st = re.sub(" [Rr]iv($| St$)"," River",st)
	st = re.sub("^Mt ","Mount ",st)
	return st

def load_steve_morse(city, state, year, file_path):

	#NOTE: This dictionary must be built independently of this script
	sm_st_ed_dict_file = pickle.load(open(file_path + '/%s/sm_st_ed_dict%s.pickle' % (str(year), str(year)), 'rb'))
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

def get_cray_z_scores(arr) :
	debug = False
	if not None in arr :
		inc_arr = np.unique(arr) #returns sorted array of unique values
		if(len(inc_arr)>2) :
			if debug : print("uniques: "+str(inc_arr))
			median = np.median(inc_arr,axis=0)
			diff = np.abs(inc_arr - median)
			med_abs_deviation = np.median(diff)
			mean_abs_deviation = np.mean(diff)
			meanified_z_score = diff / (1.253314 * mean_abs_deviation)

			if med_abs_deviation == 0 :
					modified_z_score = diff / (1.253314 * mean_abs_deviation)
			else :
					modified_z_score = diff / (1.4826 * med_abs_deviation)
			if debug : print ("MedAD Zs: "+str(modified_z_score))
			if debug : print("MeanAD Zs: "+str(meanified_z_score))
			if debug : print ("Results: "+str(meanified_z_score * modified_z_score > 16))

			return dict(zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score)))
	return None

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

#Returns just the NAME component of the street phrase, if any#
#If second argument is True, return a list of all components 
def isolate_st_name(st,whole_phrase = False) :
	if (st == None or st == '' or st == -1) or (not isinstance(st, str)) :
		# print("it is "+str(whole_phrase))
		# print(str(st)+" is not a silly string")
		return None
	else :
		TYPE = re.search(" (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$",st)
		if(TYPE) :
			TYPE = TYPE.group(0)
			st = re.sub(TYPE+"$", "",st)
			TYPE = TYPE.strip()
		DIR = re.search("^[NSEW]+ ",st)
		if(DIR) :
			DIR = DIR.group(0)
			st = re.sub("^"+DIR, "",st)
			DIR = DIR.strip()
		st = st.strip()
		
	if whole_phrase :
		return [DIR,st,TYPE]
	else :
		return st

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

def find_mode(l) :
	mode_dict = {}
	for i in l :
		if not i in mode_dict.keys() :
			mode_dict[i] = 1
		else :
		   mode_dict[i] += 1
	try :
		max_freq = sorted(mode_dict.values())[-1]
	except :
		#print("max_freq prob")
		#print(l)
		return -999
	return [x[0] for x in mode_dict.items() if x[1]==max_freq]

# given a intersect->info dict for a particular block, return what ED the block should be in
def aggregate_blk_inter_data(inter_dict) :
	possible_eds = []
	for k,v in inter_dict.items() :
		if isinstance(v[1],int) :
			possible_eds += [v[1]]
		if isinstance(v[1],list) :
			try :
				possible_eds += [int(x) for x in v[1]]
			except :
				continue
	mode = find_mode(possible_eds)
	if mode == -999 :
		#print(inter_dict)
		return 0
	if len(mode) == 1 :
		return mode[0]
	else :
		return '|'.join([str(x) for x in mode])  

# Main Program Loop - also outputs statistics and results to .txt files
def RunAnalysisInt(city_name) :
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
					Intersect_Info_DICT[i] = ['b',[int(x) for x in EDs]]
				elif EDs == None or EDs == [] : #Steve Morse contradicts map
					Intersect_Info_DICT[i] = ['mc',STList]
					#print("no ED data: "+str(STList))
				else : #all streets in intersection share at least 1 ED
					
					BLOCKs = Intersect_BLOCK_DICT[i]
					
					if(len(EDs)==1 and len(BLOCKs)>3) :
						Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal
					else :
						if(len(EDs)==1 and len(BLOCKs)==3) : # 3-way intersections #
							# resolve ambiguity using addresses
							try :
								_,ambig_st = find_unique_st(discrete_st_list) #ambig_st is the non-unique st in the intersection
								ED_bound_test = is_ED_boundary(ambig_st[0],EDs[0])
								if ED_bound_test == "nfm" : #st_ed from map+morse not found in micro
									Intersect_Info_DICT[i] = ['nfm',int(EDs[0])]
								elif ED_bound_test == "na" :
									Intersect_Info_DICT[i] = ['na',int(EDs[0])]
								elif ED_bound_test == "yes" :
									Intersect_Info_DICT[i] = ['b',int(EDs[0])] #boundary
								else :
									Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal
							except ValueError :
								if debug : print("couldn't find a unique st out of "+str(discrete_st_list))
								Intersect_Info_DICT[i] = ['a', 0] #ambiguous
						elif len(EDs)>1 :
							Intersect_Info_DICT[i] = ['e',[int(x) for x in EDs]] #external (could include boundary intersections) - associated with more than one ED
						elif len(EDs)==1 :
							Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal, 2-way
						else :
							print("something is up with intersection "+str(i))
							assert (False == True)

	# What are these initializations?
	internal_cnt = 0
	external_cnt = 0
	nf_cnt = 0
	boundary_cnt = 0
	contradiction_cnt = 0
	nf_micro_cnt = 0
	na_cnt = 0

	ED_Intersect_DICT = {}

	# What's this doing?
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

	# What's this doing?
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

def ed_inter_algo(city, state, fullname_var, paths, decade=1930):

	city = city.replace(' ','')
	r_path, script_path, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

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
	Intersect_ST_DICT = defaultdict(list) # lookup intersection -> which STs (names)
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

	Micro_TXT = open(geo_path + city + '_1930_Addresses.csv')

	sm_path = r"S:\Projects\1940Census\SMlists"
	os.chdir(sm_path+"\\"+str(decade))
	csv_name = city+state+"_SM"
	csv_from_excel(csv_name+".xlsx",csv_name)

	SM_ED_TXT = open(csv_name+".csv",'r')
	SM_ED_TXT1 = open(csv_name+"_ED.csv",'r')

	if ~os.path.isfile(geo_path + '/IntersectionsIntermediateFiles/' + city + state + '_1930_stgrid_edit_Uns2_Intersections.shp'):
		prepare_map_intersections(city + state + '_1930_stgrid_edit_Uns2.shp', fullname_var, paths)

	Intersect_TXT = open(geo_path + '/IntersectionsIntermediateFiles/' + city + state + '_1930_stgrid_edit_Uns2_Intersections.txt')
	SMLines = csv.reader(SM_ED_TXT)
	next(SMLines, None)  # skip header
	SMLines1 = csv.reader(SM_ED_TXT1)
	InterLines = Intersect_TXT.readlines()[1:]
	MicroLines = Micro_TXT.readlines()[1:]

	RunAnalysisInt(city)

	print("Creating ED Map for %s (Intersections algorithm)" % (city))
	draw_EDs(city, state, paths, "ED_inter", False)
		
#
# Matt's initial geocoding script (written in R)
#

# See "/blocknum/R/Identify 1930 EDs.R" for details
def identify_1930_eds(city_name, paths):
	r_path, script_path, file_path = paths
	print("Identifying 1930 EDs\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Identify 1930 EDs.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying 1930 EDs for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Function to select best ED guess based on three methods
#

def select_best_ed_guess(x):
	
	_, ed_desc, ed_inter, ed_geocode = x
	
	# Split if multiple EDs
	if '|' in str(ed_desc):
		ed_desc = ed_desc.split('|')
		ed_desc = [int(i) for i in ed_desc]
	else:
		ed_desc = [int(ed_desc)]
	if '|' in str(ed_inter):
		ed_inter = ed_inter.split('|')
		ed_inter = [int(i) for i in ed_inter]
	else:
		ed_inter = [int(ed_inter)]
	if '|' in str(ed_inter):
		ed_geocode = ed_geocode.split('|')
		ed_geocode = [int(i) for i in ed_geocode]
	else:
		ed_geocode = [int(ed_geocode)]

	# List of EDs guessed
	ed_list = list(set(ed_desc + ed_inter + ed_geocode))
	ed_list = [i for i in ed_list if i != 0]

	# List of ED guesses by confidence
	ed_guess_list = []
	
	# Initialize guess to be missing, confidence -1 
	ed_guess_conf = [-1, 0]
	
	# If no guesses, return missing
	if len(ed_list) == 0:
		return ed_guess_conf
	# Otherwise, try to find a unique guess
	else:
		for ed in ed_list:
			# If all three agree, highest confidence
			if ed in ed_desc and ed in ed_inter and ed in ed_geocode:
				ed_guess_list.append([ed, 1])
			# If any two agree, second highest confidence
			elif (ed in ed_desc and ed in ed_inter) or (ed in ed_desc and ed in ed_geocode) or (ed in ed_inter and ed in ed_geocode):
				ed_guess_list.append([ed, 2])
			# If ed_desc not missing, third highest confidence
			elif ed in ed_desc:
				ed_guess_list.append([ed, 3])
			# If ed_inter not missing, fourth highest confidence
			elif ed in ed_inter:
				ed_guess_list.append([ed, 4])
			# If ed_geocode not missing, fifth highest confidence
			elif ed in ed_geocode:
				ed_guess_list.append([ed, 5])

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

	return ed_guess_conf

##
## Execute functions
##

# Head script for running everything - produces ED guess map and statistics
def get_ed_guesses(city, state, fullname_var):

	city = city.replace(' ','')

	# Paths
	dir_path = "S:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr
	r_path = "C:/Program Files/R/R-3.4.2/bin/Rscript"
	script_path = "C:/Users/cgraziul/Documents/GitHub/hist-census-gis"
	paths = [r_path, script_path, dir_path]
	geo_path = dir_path + '/GIS_edited/'

	# Step 1: create address file, street grid, physical block, and initial geocode shapefiles 
	create_1930_addresses(city, state, paths)
	create_blocks_and_block_points(city, state, paths)

	# Step 2: Run Amory's ED descriptions script (unmodified from Amory's script)
	ed_desc_algo(city, state, fullname_var, paths)

	# Step 3: Run Amory's intersections script
	ed_inter_algo(city, state, fullname_var, paths)

	# Step 4: Run Matt's script (based on initial geocoding)
	identify_1930_eds(city, paths)

	# Step 5: Create new shapefile including all three then...
	#	a. Identify best guesses
	#	b. Assign confidence to guesses

	# Create a copy of file created by Matt's script (contains guesses from all three methods)
	last_step = geo_path + city + '_1930_ED_Choice_map.shp'
	ed_desc_map = geo_path + city + '_ED_desc.shp'
	ed_guess_file = geo_path + city + state + '_ED_guess_map.shp'

	# Spatially join ed_desc polygons to assign ed_desc guesses to pblk_id

	arcpy.SpatialJoin_analysis(target_features=last_step, 
		join_features=ed_desc_map, 
		out_feature_class=ed_guess_file, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL",
		match_option="HAVE_THEIR_CENTER_IN")

	# Select relevant variables and extract best ED guesses
	df = dbf2DF(ed_guess_file)
	def replace_blanks(ed):
		if ed == '':
			return '0'
		else:
			return ed
	df.loc[:,'ed_desc'] = df.apply(lambda x: replace_blanks(x['ed_desc']), axis=1).astype(int)
	def get_ed_geocode(eds):
		eds = [ed for ed in eds if ed != '0']
		if len(eds) == 0:
			return '0'
		elif len(eds) == 1:
			return eds[0]
		else:
			return '|'.join(eds)
	df.loc[:,'ed_geocode'] = df[['ED_ID','ED_ID2','ED_ID3']].astype(int).astype(str).apply(lambda x: get_ed_geocode(x), axis=1)
	relevant_vars = ['pblk_id','ed_desc','ed_inter','ed_geocode']
	df_ed_guess = df[relevant_vars]
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
	
	# Save dbf (have to use field mapping to preserve TEXT data format)
	def save_dbf_ed(df, geo_path, shapefile_name):
		file_temp = shapefile_name.split('/')[-1]
		rand_post = str(random.randint(1,100001))
		csv_file = geo_path + "/temp_for_dbf"+rand_post+".csv"
		df.to_csv(csv_file,index=False)
		try:
			os.remove(geo_path + "/schema.ini")
		except:
			pass

		# Add a specific field mapping for a special case
		file = csv_file
		field_map = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
		ed_desc "ed_desc" true true false 10 Text 0 0 ,First,#,%s,ed_desc,-1,-1;
		ed_inter "ed_inter" true true false 80 Text 0 0 ,First,#,%s,ed_inter,-1,-1;
		ed_geocode "ed_geocode" true true false 10 Text 0 0 ,First,#,%s,ed_geocode,-1,-1;
		ed_conf "ed_conf" true true false 30 Text 0 0 ,First,#,%s,ed_conf,-1,-1;
		ed_guess "ed_guess" true true false 10 Text 0 0 ,First,#,%s,ed_guess,-1,-1""" % (file, file, file, file, file, file)

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=geo_path, 
			out_name="temp_for_shp"+rand_post+".dbf",
			field_mapping=field_map)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		os.rename(geo_path+"/temp_for_shp"+rand_post+".dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(geo_path+"/temp_for_shp"+rand_post+".dbf.xml")
		os.remove(geo_path+"/temp_for_shp"+rand_post+".cpg")
		os.remove(csv_file)

	save_dbf_ed(df_ed_guess, geo_path, ed_guess_file)

	df_ed_guess.index = df_ed_guess['pblk_id']
	df_ed_guess_dict = df_ed_guess.to_dict('index')
	with arcpy.da.UpdateCursor(ed_guess_file, ['pblk_id','ed_inter']) as up_cursor:
		for row in up_cursor :
			row[1] = df_ed_guess_dict[str(row[0])]['ed_inter']
			up_cursor.updateRow(row)


	# Create a tabular summary of number guessed by confidence in guess
	info = df_ed_guess.groupby(['ed_conf'], as_index=False).count()[['ed_conf','pblk_id']]
	info['city'] = city
	info['state'] = state

	return info


# City info
#city = "Dayton"
#state = "OH"

# Full street name variable
fullname_var = "FULLNAME"

#info = get_ed_guesses(city, state, fullname_var)

# To be included in the city_info_list, must have:
#	a. [CITY][STATE]_1940_stgrid_diradd.shp
#	b. [CITY][STATE]_StudAuto.dta

city_info_list = [
	['Albany','NY'],	
	['Dayton','OH'], 	
	['Houston','TX'],
	['Miami','FL'],
	['New Haven','CT'], 
	['Newark','NJ'], 	
	['Rochester','NY'], 
	['San Diego','CA'], 
	['Seattle','WA'],
	['St Paul','MN'],
	['Worcester','MA'], 
	['Yonkers','NY']  	
	]

info = []
num_finished = 0
for city_info in city_info_list:
	city, state = city_info
	try:
		info.append(get_ed_guesses(city, state, fullname_var))
		num_finished += 1
	except:
		continue
print("%s of %s cities processed" % (str(num_finished), str(len(city_info_list))))
df = pd.concat(info)
df_to_write = pd.pivot_table(df, values='pblk_id', index=['city','state'], columns=['ed_conf'])
df_to_write.to_csv('S:/Users/Chris/ed_guess_info.csv')
