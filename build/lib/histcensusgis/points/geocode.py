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

from histcensusgis.microdata.misc import create_addresses
from histcensusgis.lines.street import process_raw_grid
from histcensusgis.polygons.block import *
from histcensusgis.s4utils.AmoryUtils import *
from histcensusgis.s4utils.IOutils import *
import arcpy
import os
import subprocess
import pandas as pd
arcpy.env.overwriteOutput=True

# Performs initial geocode on contemporary grid
def initial_geocode(city_info, geo_path, hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD']):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	state_abbr = state_abbr.upper()

	min_l, max_l, min_r, max_r = hn_ranges

	# Files
	add_locator = geo_path + city_name + "_addloc_" + str(decade)
	addresses = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	address_fields="Street address; City city; State state"
	points = geo_path + city_name + "_" + str(decade) + "_Points.shp"
	reference_data = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp 'Primary Table'"

	# Fix addresses for use in geocoding
	try:
		arcpy.Delete_management(geo_path + "temp.gdb")
	except:
		pass
	arcpy.CreateFileGDB_management(geo_path,"temp.gdb")
	df_addresses_csv = pd.read_csv(addresses)
	df_addresses_dbf = df_addresses_csv.replace(np.nan,'',regex=True)
	x = np.array(np.rec.fromrecords(df_addresses_dbf.values))
	names = df_addresses_dbf.dtypes.index.tolist()
	x.dtype.names = tuple(names)
	arcpy.da.NumPyArrayToTable(x,geo_path + "temp.gdb/" + city_name + "_" + str(decade) + "_Addresses")
	arcpy.env.workspace = geo_path + "temp.gdb"

	field_map="'Feature ID' FID VISIBLE NONE; \
	'*From Left' %s VISIBLE NONE; \
	'*To Left' %s  VISIBLE NONE; \
	'*From Right' %s  VISIBLE NONE; \
	'*To Right' %s  VISIBLE NONE; \
	'Prefix Direction' <None> VISIBLE NONE; \
	'Prefix Type' <None> VISIBLE NONE; \
	'*Street Name' FULLNAME VISIBLE NONE; \
	'Suffix Type' '' VISIBLE NONE; \
	'Suffix Direction' <None> VISIBLE NONE; \
	'Left City or Place' CITY VISIBLE NONE; \
	'Right City or Place' CITY VISIBLE NONE; \
	'Left ZIP Code' <None> VISIBLE NONE; \
	'Right ZIP Code' <None> VISIBLE NONE; \
	'Left State' STATE VISIBLE NONE; \
	'Right State' STATE VISIBLE NONE; \
	'Left Street ID' <None> VISIBLE NONE; \
	'Right Street ID' <None> VISIBLE NONE; \
	'Display X' <None> VISIBLE NONE; \
	'Display Y' <None> VISIBLE NONE; \
	'Min X value for extent' <None> VISIBLE NONE; \
	'Max X value for extent' <None> VISIBLE NONE; \
	'Min Y value for extent' <None> VISIBLE NONE; \
	'Max Y value for extent' <None> VISIBLE NONE; \
	'Left parity' <None> VISIBLE NONE; \
	'Right parity' <None> VISIBLE NONE; \
	'Left Additional Field' <None> VISIBLE NONE; \
	'Right Additional Field' <None> VISIBLE NONE; \
	'Altname JoinID' <None> VISIBLE NONE" % (min_l, max_l, min_r, max_r)

	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith(city_name+"_addloc")]
	for f in add_loc_files:
			 if os.path.isfile(f):
				 os.remove(f)

	print("The script is executing the 'CreateAddressLocator' tool")
	#Create Address Locator
	arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", 
		in_reference_data=reference_data, 
		in_field_map=field_map, 
		out_address_locator=add_locator, 
		config_keyword="")
	#Change side offset to maximize quality of physical block matches
	locator_fn = geo_path+'/'+city_name+'_addloc_'+str(decade)+'.loc'
	locator_file = open(locator_fn,'a')  # open for appending
	locator_file.writelines('SideOffset = 1')
	locator_file.writelines('SideOffsetUnits = Feet')
	locator_file.close()
	print("The script has finished executing the 'CreateAddressLocator' tool and has begun executing the 'GeocodeAddress' tool")
	#Geocode Points
	arcpy.GeocodeAddresses_geocoding(in_table=city_name + "_" + str(decade) + "_Addresses", 
		address_locator=add_locator, 
		in_address_fields=address_fields, 
		out_feature_class=points)
	#Delete temporary.gdb
	arcpy.Delete_management(geo_path + "temp.gdb/" + city_name + "_" + str(decade) + "_Addresses")
	arcpy.Delete_management(geo_path + "temp.gdb")
	print("The script has finished executing the 'GeocodeAddress' tool and has begun executing the 'SpatialJoin' tool")

# Ensure geocode data exist for Matt's ED/block algorithms
def check_matt_dependencies(city_info, paths, geocode_file=None):

	# Attach physical block IDs to geocoded points 
	def attach_pblk_id(city_info, geo_path, points_shp):

		city_name, state_abbr, decade = city_info
		city_name = city_name.replace(' ','')
		state_abbr = state_abbr.upper()

		# Files
		pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
		pblk_points_shp = geo_path + city_name + "_" + str(decade) + "_Pblk_Points.shp"

		#Attach Pblk ids to points
		arcpy.SpatialJoin_analysis(points_shp, 
			pblk_shp, 
			pblk_points_shp, 
			"JOIN_ONE_TO_MANY", 
			"KEEP_ALL", 
			"#", 
			"INTERSECT")
		print("The script has finished executing the 'SpatialJoin' tool")

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')

	_, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	# Ensure that address file exists
	address_file = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	if not os.path.isfile(address_file):
		create_addresses(city_info, paths)

	# Ensure that processed street grid exists
	grid_uns2 = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	if not os.path.isfile(grid_uns2):
		_ = process_raw_grid(city_info, geo_path)

	# Ensure that physical block shapefile exists
	pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
	if not os.path.isfile(pblk_shp):
		create_pblks(city_info, geo_path)	

	# Call initial geocoding function
	initial_geocode(city_info, geo_path)
	print("The script has finished executing the 'geocode' function and has now started excuting 'attach_pblk_id'")

	if geocode_file != None:
		points = geocode_file
		print("Different geocode")
	else:
		points_shp = geo_path + city_name + "_" + str(decade) + "_Points.shp"

	attach_pblk_id(city_info, geo_path, points_shp)
	print("The script has finished executing the 'attach_pblk_id' function and the entire script is complete")

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
def validate(geo_path, city_name, state_abbr, gr, vm, spatjoin, notcor, cor, decade, residual_file, slow=False):

	fe = geo_path + city_name + state_abbr + "_" + str(decade) + "_formattedEDs.dbf"

	# Process: Spatial Join
	arcpy.SpatialJoin_analysis(target_features=gr, 
		join_features=vm, 
		out_feature_class=spatjoin, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL")
	print "spatial join has finished"

	print "joining the swm"
	# Process: Join field using Pandas and not ArcPy (since it's super slow)

	df_fe = load_shp(fe)
	del df_fe['Field1']

	df_spatjoin = load_shp(spatjoin)
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

	save_shp(df_merge, spatjoin)

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
		df_notcor = load_shp(notcor)
	else:
		df_notcor = df_merge.loc[(df_merge['is_touch']==0)|(df_merge['Status']=='U')] 
	# Process: Delete Fields and Save Table
	to_del = ['Match_addr','Ref_ID','Status','ed_1','is_touch']
	vars_to_keep = [i for i in df_notcor.columns.tolist() if i not in to_del]
	df_notcor_togeocode = df_notcor[vars_to_keep]

	rand_post = str(random.randint(1,100001))
	csv_file = geo_path+"temp.csv"
	df_notcor_togeocode.to_csv(csv_file,index=False)
	residual_file_name = residual_file.split('/')[-1]
	arcpy.TableToTable_conversion(in_rows=csv_file, out_path=geo_path, out_name=residual_file_name)
	os.remove(csv_file)

# Combine geocodes
def combine_geocodes(geo_path, city_name, state_abbr, list_of_shp, notcor, outfile, decade):

	post = outfile.split('/')[-1].split('.')[0].split('_GeocodeFinal')[1]

	# Merge shapefiles and tag geocoded
	merge_and_tag_geocoded(geo_path, city_name, state_abbr, list_of_shp, post)

	# Create list of streets from ungeocoded points that are not in the grid
	df_ungeocoded = load_shp(notcor)
	grid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	df_grid = load_shp(grid_file)
	get_st_in_micro_not_grid(geo_path, df_ungeocoded, df_grid, city_name, state_abbr, decade, post)

def merge_and_tag_geocoded(geo_path, city_name, state_abbr, list_of_shp, post):
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
	df_merge = load_shp(outfile)
	try:
		df_merge_collapse = df_merge.groupby(['fullname','address','Mblk','ed','ed_1','geocoded']).size().reset_index(name='count')
	except:
		df_merge_collapse = df_merge.groupby(['fullname','address','mblk','ed','ed_1','geocoded']).size().reset_index(name='count')
	outfile_excel = geo_path + "StLouisMO_GeocodeFinal"+post+".xlsx"
	writer = pd.ExcelWriter(outfile_excel, engine='xlsxwriter')
	df_merge_collapse.to_excel(writer, sheet_name='Sheet1', index=False)
	writer.save()

