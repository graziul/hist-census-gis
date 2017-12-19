"""
Title: GeocodeFunctions.py
Objective: automate our current (circa Nov. 2017) geocoding process
Notes:  Specifically intersects a user-specified street grid with a verified map (e.g., ED or block) to
		determine which street segments fall in which regions of the verified map (e.g., ED or block),
		creates an address locator using that grid and other user-specified parameters (e.g., use ED as city)
		and then execute the geocode using that address locator on a user-specified table of addresses (i.e.,
		full list of addresses for a specific city or a list of residual addresses from a previous geocode)
Author: Joseph Danko
Created: 11/3/2017
Updated: Chris Graziul, 12/11/2017 (stripped down to functions only)
"""

# Import the ESRI library of tools into Python
import arcpy
import os
import pysal as ps
import pandas as pd
from blocknum.blocknum import *
import random

# All Python to overwrite any ESRI output files (e.g., shapefiles)
arcpy.env.overwriteOutput=True

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
	if not k in Dict :
		Dict[k] = [v]
	else :
		if not v in Dict[k] :
			Dict[k].append(v)

# Add and calculate check field, save the result
def is_touch(ED, neighbor):
	a =  str(int(ED))
	try:
		blist = neighbor.split(';')    
		if a in blist:        
			return 1    
		else:        
			return 0
	# Handles "nan" 
	except:
		blist = neighbor
		if a == blist:
			return 1
		else:
			return 0

# Get adjacent EDs
def get_adjacent_eds(geo_path, city_name, state_abbr):
	
	# Files

	# "vm" is the verified map (e.g., ED or block map)
	vm = geo_path + city_name + "_1930_ED.shp"
	# Feature Class to Feature Class file
	fc = city_name + state_abbr + "_1930_ED_Feature.shp"
	# Spatial weights files:
	swm_file = geo_path + city_name + state_abbr + "_1930_spatweight.swm"
	swm_table = geo_path + city_name + state_abbr + "_1930_swmTab.dbf"
	# Amory's formatted EDs dbf
	fe = geo_path + city_name + state_abbr + "_1930_formattedEDs.dbf"
	fe_file = city_name + state_abbr + "_1930_formattedEDs.dbf"

	print "creating the swm"
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

# Geocode function
def geocode(geo_path,city_name,add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr,no_side_offset=True):
	print("Step 1 of 3: The 'Geocode' function has started and the program has started to implement the intersect function")
	arcpy.Intersect_analysis (in_features=[sg, vm], 
		out_feature_class=sg_vm, 
		join_attributes="ALL")
	print("Step 2 of 3: The program has finished implementing the intersect function and has begun creating the address locator")
	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [geo_path+'\\'+x for x in os.listdir(geo_path) if x.startswith(al.split('/')[-1]+'.')]
	for f in add_loc_files:
		if os.path.isfile(f):
			os.remove(f)
	arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges",
										 in_reference_data=sg_vm,
										 in_field_map="'Feature ID' <None> VISIBLE NONE;\
													'*From Left' "+fl+" VISIBLE NONE;\
													'*To Left' "+tl+" VISIBLE NONE;\
													'*From Right' "+fr+" VISIBLE NONE;\
													'*To Right' "+tr+" VISIBLE NONE;\
													'Prefix Direction' <None> VISIBLE NONE;\
													'Prefix Type' <None> VISIBLE NONE;\
													'*Street Name' "+cal_street+" VISIBLE NONE;\
													'Suffix Type' <None> VISIBLE NONE;\
													'Suffix Direction' <None> VISIBLE NONE;\
													'Left City or Place' "+cal_city+" VISIBLE NONE;\
													'Right City or Place' "+cal_city+" VISIBLE NONE;\
													'Left ZIP Code' <None> VISIBLE NONE;\
													'Right ZIP Code' <None> VISIBLE NONE;\
													'Left State' "+cal_state+" VISIBLE NONE;\
													'Right State' "+cal_state+" VISIBLE NONE;\
													'Left Street ID' <None> VISIBLE NONE;\
													'Right Street ID' <None> VISIBLE NONE;\
													'Display X' <None> VISIBLE NONE;\
													'Display Y' <None> VISIBLE NONE;\
													'Min X value for extent' <None> VISIBLE NONE;\
													'Max X value for extent' <None> VISIBLE NONE;\
													'Min Y value for extent' <None> VISIBLE NONE;\
													'Max Y value for extent' <None> VISIBLE NONE;\
													'Left parity' <None> VISIBLE NONE;\
													'Right parity' <None> VISIBLE NONE;\
													'Left Additional Field' "+addfield+" VISIBLE NONE;\
													'Right Additional Field' "+addfield+" VISIBLE NONE;\
													'Altname JoinID' <None> VISIBLE NONE",
										out_address_locator=al)

	if no_side_offset:
		locator_fn = al+'.loc'
		locator_file = open(locator_fn,'a')  # open for appending
		locator_file.writelines('SideOffset = 0')
		locator_file.writelines('SideOffsetUnits = Feet')
		locator_file.close()

	print("Step 3 of 3: The program has finished creating the address locator and has started the geocoding process")

	arcpy.GeocodeAddresses_geocoding(in_table=add, 
		address_locator=al,
		in_address_fields="Street "+g_address+" VISIBLE NONE;\
			City "+g_city+" VISIBLE NONE;\
			State "+g_state+" VISIBLE NONE",
		out_feature_class=gr, 
		out_relationship_type="STATIC")

	print("The program has finished the geocoding process and 'Geocode' function is complete")

# Validate function (adjacent EDs)
def validate(geo_path, city_name, state_abbr, gr, vm, spatjoin, notcor, cor, residual_file, slow=False):

	fe = geo_path + city_name + state_abbr + "_1930_formattedEDs.dbf"

	# Process: Spatial Join
	arcpy.SpatialJoin_analysis(target_features=gr, 
		join_features=vm, 
		out_feature_class=spatjoin, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL")
	print "spatial join has finished"

	print "joining the swm"
	# Process: Join field using Pandas and not ArcPy (since it's super slow)

	df_fe = dbf2DF(fe)
	del df_fe['Field1']

	df_spatjoin = dbf2DF(spatjoin.replace('.shp','.dbf'))
	try:
		del df_spatjoin['contig_ed']
	except:
		pass

	df_merge = df_spatjoin.merge(df_fe, how='left', left_on='ed_1', right_on='ed')
	df_merge['ed'] = df_merge['ed_x']
	df_merge['is_touch'] = df_merge.apply(lambda x: is_touch(x['ed'],x['contig_ed']), axis=1)

	try:
		vars_to_keep = ['index','Match_addr','Status','Mblk','Ref_ID',
			'address','hn','fullname','type','state','city','ed','ed_1','is_touch']
		df_merge = df_merge[vars_to_keep]
	except:
		vars_to_keep = ['index','Match_addr','Status','mblk','Ref_ID',
			'address','hn','fullname','type','state','city','ed','ed_1','is_touch']
		df_merge = df_merge[vars_to_keep]

	# Function to save Pandas DF as DBF file 
	def save_dbf_geo(df, shapefile_name, field_map=False):
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
			field_mapping = """index "index" true true false 10 Long 0 0 ,First,#,%s,index,-1,-1;
			Match_addr "Match_addr" true true false 100 Text 0 0 ,First,#,%s,Match_addr,-1,-1;
			Status "Status" true true false 1 Text 0 0 ,First,#,%s,Status,-1,-1;
			mblk "mblk" true true false 10 Long 0 0 ,First,#,%s,mblk,-1,-1;
			Ref_ID "Ref_ID" true true false 10 Long 0 0 ,First,#,%s,Ref_ID,-1,-1;
			address "address" true true false 100 Text 0 0 ,First,#,%s,address,-1,-1;
			hn "hn" true true false 10 Long 0 0 ,First,#,%s,hn,-1,-1;
			fullname "fullname" true true false 100 Text 0 0 ,First,#,%s,fullname,-1,-1;
			type "type" true true false 10 Text 0 10 ,First,#,%s,type,-1,-1;
			state "state" true true false 2 Text 0 0 ,First,#,%s,state,-1,-1;
			city "city" true true false 50 Text 0 0 ,First,#,%s,city,-1,-1;
			ed "ed" true true false 10 Long 0 0 ,First,#,%s,ed,-1,-1;
			ed_1 "ed_1" true true false 10 Long 0 0 ,First,#,%s,ed_1,-1,-1;
			is_touch "is_touch" true true false 1 Long 0 0 ,First,#,%s,is_touch,-1,-1""" % tuple(14*[file])
		else:
			field_map = None

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=geo_path, 
			out_name="temp_for_shp"+rand_post+".dbf",
			field_mapping=field_mapping)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		#os.remove(csv_file)
		os.rename(geo_path+"/temp_for_shp"+rand_post+".dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(geo_path+"/temp_for_shp"+rand_post+".dbf.xml")
		os.remove(geo_path+"/temp_for_shp"+rand_post+".cpg")

	save_dbf_geo(df_merge, spatjoin, field_map=True)

	print "selecting the correct geocodes"
	# Process: Select correct geocodes
	arcpy.Select_analysis(in_features=spatjoin, 
		out_feature_class=cor, 
		where_clause="\"is_touch\" =1")

	print "selecting the incorrect geocodes"
	# Process: Select (Not geocoded or not geocoded correctly)
	if slow:
		arcpy.Select_analysis(in_features=spatjoin, 
			out_feature_class=notcor, 
			where_clause="\"is_touch\" = 0  OR \"Status\" = 'U'")
		df_notcor = dbf2DF(notcor.replace('.shp','.dbf'))
	else:
		df_notcor = df_merge.loc[(df_merge['is_touch']==0)|(df_merge['Status']=='U')] 
	# Process: Delete Fields and Save Table
	to_del = ['Match_addr','Ref_ID','Status','ed_1','is_touch']
	vars_to_keep = [i for i in df_notcor.columns.tolist() if i not in to_del]
	df_notcor_togeocode = df_notcor[vars_to_keep]

	rand_post = str(random.randint(1,100001))
	csv_file = geo_path+"temp"+rand_post+".csv"
	df_notcor_togeocode.to_csv(csv_file,index=False)
	residual_file_name = residual_file.split('/')[-1]
	arcpy.TableToTable_conversion(in_rows=csv_file, out_path=geo_path, out_name=residual_file_name)
	os.remove(csv_file)

# Combine geocodes
def combine_geocodes(geo_path, city_name, state_abbr, list_of_shp, notcor, outfile):

	post = outfile.split('/')[-1].split('.')[0].split('_GeocodeFinal')[1]

	def merge_and_tag_geocoded(list_of_shp):
		for shp in list_of_shp:
			arcpy.AddField_management(in_table=shp, 
				field_name="geocoded", 
				field_type="TEXT")			
			if "_GeocodedCorrect" in shp:
				arcpy.CalculateField_management(in_table=shp, 
					field="geocoded", 
					expression="'Yes'",
					expression_type="PYTHON_9.3")
			else:
				arcpy.CalculateField_management(in_table=shp, 
					field="geocoded", 
					expression="'No'",
					expression_type="PYTHON_9.3")
		arcpy.Merge_management(list_of_shp, outfile)
		df_merge = dbf2DF(outfile)
		try:
			df_merge_collapse = df_merge.groupby(['fullname','address','Mblk','ed','ed_1','geocoded']).size().reset_index(name='count')
		except:
			df_merge_collapse = df_merge.groupby(['fullname','address','mblk','ed','ed_1','geocoded']).size().reset_index(name='count')
		outfile_excel = geo_path + "StLouisMO_GeocodeFinal"+post+".xlsx"
		writer = pd.ExcelWriter(outfile_excel, engine='xlsxwriter')
		df_merge_collapse.to_excel(writer, sheet_name='Sheet1', index=False)
		writer.save()

	merge_and_tag_geocoded(list_of_shp)

	# Create list of streets from ungeocoded points that are not in the grid
	df_ungeocoded = dbf2DF(notcor)
	df_ungeocoded_st_ed = df_ungeocoded.loc[df_ungeocoded['fullname']!='.',['fullname','ed']]
	df_ungeocoded_st_ed = df_ungeocoded_st_ed.groupby(['fullname','ed']).size().reset_index(name='count')

	grid_file = geo_path + city_name + state_abbr + "_1930_stgrid_edit_Uns2.shp"
	df_grid = dbf2DF(grid_file)
	grid_streets_list = df_grid['FULLNAME'].drop_duplicates().tolist()

	df_ungeocoded_st_ed_tocheck = df_ungeocoded_st_ed[~df_ungeocoded_st_ed['fullname'].isin(grid_streets_list)].sort_values(['ed'])

	# Create a Pandas Excel writer using XlsxWriter as the engine.
	file_name = geo_path + '/' + city_name + state_abbr + '_ungeocoded_not_in_grid'+post+'.xlsx'
	writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

	# Convert the dataframe to an XlsxWriter Excel object.
	df_ungeocoded_st_ed_tocheck.to_excel(writer, sheet_name='Sheet1', index=False)

	# Close the Pandas Excel writer and output the Excel file.
	writer.save()
