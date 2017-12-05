"""
Title: geocodefunction
Objective: automate our current (circa Nov. 2017) geocoding process
Notes:  Specifically intersects a user-specified street grid with a verified map (e.g., ED or block) to
		determine which street segments fall in which regions of the verified map (e.g., ED or block),
		creates an address locator using that grid and other user-specified parameters (e.g., use ED as city)
		and then execute the geocode using that address locator on a user-specified table of addresses (i.e.,
		full list of addresses for a specific city or a list of residual addresses from a previous geocode)
Author: Joseph Danko
Created: 11/3/2017
"""

# Import the ESRI library of tools into Python
import arcpy
import os
import pysal as ps
import pandas as pd

name = "StLouis"
state = "MO"

### USER-SPECIFIED INPUTS ###
# Specify the work place in which all the data is stored (e.g., a geodatabase is recommended)
#arcpy.env.workspace="S:/Users/_Exchange/To Joey/FromDaniel/Cincy.gdb"
dir_path = "S:/Projects/1940Census/StLouis/GIS_edited/"

# All Python to overwrite any ESRI output files (e.g., shapefiles)
arcpy.env.overwriteOutput=True

# "vm" is the verified map (e.g., ED or block map)
vm = dir_path + "StLouis_1930_ED.shp"
# Feature Class to Feature Class file
fc = "StLouisMO_1930_ED_Feature.shp"
# Spatial weights files:
swm_file = dir_path + "StLouisMO_1930_spatweight.swm"
swm_table = dir_path + "StLouisMO_1930_swmTab.dbf"
# "cal_street" is the name of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (hence "cal_"; REQUIRED)
cal_street = "FULLNAME" 
# "cal_city" is the name of the city as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (e.g., city or ED; NOT REQUIRED)
cal_city = "CITY"
# "cal_state" is the name of the state as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (NOT REQUIRED)
cal_state = "STATE"
# "addfield" is the name of the additional field as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (e.g., ED or city; NOT REQUIRED)
addfield = "<None>"
# "g_address" is the name of the column that stores the address of the property from the "add" list of address file
g_address = "ADDRESS"
# "g_city" is the name of the column that stores the city field from the "add" list of address file (e.g., city, ED or block), which should match the city field used in the address locator
g_city = "CITY"
# "g_state" is the name of the column that stores the state field from the "add" list of address file
g_state = "STATE"
# "fl" is the smallest house number on the left side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
# "tl" is the largest house number on the left side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
# "fr" is the smallest house number on the right side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
# "tr" is the largest house number on the right side of the street as noted in the output of  the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
fl = "MIN_LFROMA"
tl = "MAX_LTOADD"
fr = "MIN_RFROMA"
tr = "MAX_RTOADD"

# Helper functions

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
	if not k in Dict :
		Dict[k] = [v]
	else :
		if not v in Dict[k] :
			Dict[k].append(v)

# Function to reads in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=False): 
	if dbfile.split('.')[1] == 'shp':
		dbfile = dbfile.replace('.shp','.dbf')
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
	dir_temp = '/'.join(shapefile_name.split('/')[:-1])
	file_temp = shapefile_name.split('/')[-1]
	csv_file = dir_temp + "/temp_for_dbf.csv"
	df.to_csv(csv_file,index=False)
	try:
		os.remove(dir_temp + "/schema.ini")
	except:
		pass
	arcpy.TableToTable_conversion(in_rows=csv_file, out_path=dir_temp, out_name="temp_for_shp.dbf")
	os.remove(shapefile_name.replace('.shp','.dbf'))
	os.remove(csv_file)
	os.rename(dir_temp+"/temp_for_shp.dbf",shapefile_name.replace('.shp','.dbf'))
	os.remove(dir_temp+"/temp_for_shp.dbf.xml")
	os.remove(dir_temp+"/temp_for_shp.cpg")

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
def geocode(add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr):
	print("Step 1 of 3: The 'Geocode' function has started and the program has started to implement the intersect function")
	arcpy.Intersect_analysis (in_features=[sg, vm], 
		out_feature_class=sg_vm, 
		join_attributes="ALL")
	print("Step 2 of 3: The program has finished implementing the intersect function and has begun creating the address locator")
	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(name+"_addloc_ED")]
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
def validate(dir_path, gr, vm, spatjoin, fc, swm_file, swm_table, fe_file, notcor, cor, residual_file):

	fe = dir_path + fe_file

	# Process: Spatial Join
	arcpy.SpatialJoin_analysis(target_features=gr, 
		join_features=vm, 
		out_feature_class=spatjoin, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL")
	print "spatial join has finished"

	print "creating the swm"
	# Process: Feature Class to Feature Class
	ftc_mapping = """OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,%s,OBJECTID,-1,-1;
		ed \"ed\" true true false 19 Double 0 0 ,First,#,%s,ed,-1,-1;
		Shape_Leng \"Shape_Leng\" true true false 19 Double 0 0 ,First,#,%s,Shape_Leng,-1,-1;
		Shape_Area \"Shape_Area\" true true false 19 Double 0 0 ,First,#,%s,Shape_Area,-1,-1;
		ED_int \"ED_int\" true true false 5 Long 0 5 ,First,#,%s,ED_int,-1,-1;
		Ed_str \"Ed_str\" true true false 5 Text 0 0 ,First,#,%s,Ed_str,-1,-1""" % (vm, vm, vm, vm, vm, vm)
	arcpy.FeatureClassToFeatureClass_conversion(in_features=vm, 
		out_path=dir_path, 
		out_name=fc, 
		field_mapping=ftc_mapping)

		#Calculate some fields

	arcpy.CalculateField_management(in_table=dir_path+fc, 
		field="Shape_Leng", 
		expression="!SHAPE.LENGTH!",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=dir_path+fc, 
		field="Shape_Area", 
		expression="!SHAPE.AREA!",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=dir_path+fc, 
		field="ED_int", 
		expression="int(!ed!)",
		expression_type="PYTHON_9.3")
	arcpy.CalculateField_management(in_table=dir_path+fc, 
		field="Ed_str", 
		expression="str(int(!ed!))",
		expression_type="PYTHON_9.3")

	# Process: Generate Spatial Weights Matrix
	arcpy.GenerateSpatialWeightsMatrix_stats(Input_Feature_Class=dir_path+fc, 
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

	arcpy.CreateTable_management(out_path=dir_path, 
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

	vars_to_keep = ['index','Match_addr','Status','Mblk','Ref_ID',
		'address','hn','fullname','type','state','city','ed','ed_1','contig_ed','is_touch']
	df_merge = df_merge[vars_to_keep]

	save_dbf(df_merge, spatjoin)

	print "selecting the incorrect geocodes"
	# Process: Select (Not geocoded or not geocoded correctly)
	arcpy.Select_analysis(in_features=spatjoin, 
		out_feature_class=notcor, 
		where_clause="\"is_touch\" = 0  OR \"Status\" = 'U'")

	print "selecting the correct geocodes"
	# Process: Select correct geocodes
	arcpy.Select_analysis(in_features=spatjoin, 
		out_feature_class=cor, 
		where_clause="\"is_touch\" =1")

	# Process: Delete Fields and Save Table
	df_notcor = dbf2DF(notcor.replace('.shp','.dbf'))
	to_del = ['Match_addr','Ref_ID','Status','ed_1','is_touch','contig_ed']
	vars_to_keep = [i for i in df_notcor.columns.tolist() if i not in to_del]
	df_notcor_togeocode = df_notcor[vars_to_keep]

	csv_file = dir_path+"temp.csv"
	df_notcor_togeocode.to_csv(csv_file,index=False)
	arcpy.TableToTable_conversion(in_rows=csv_file, out_path=dir_path, out_name=residual_file)
	os.remove(csv_file)

#
# Renumbered grid
#

# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
add = dir_path + "StLouis_1930_Addresses.csv"
# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
sg = dir_path + "StLouisMO_1930_stgrid_renumbered.shp"
# Amory's formatted EDs dbf
fe = dir_path + "StLouisMO_1930_formattedEDs.dbf"
fe_file = "StLouisMO_1930_formattedEDs.dbf"
# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
al = dir_path + name + "_addloc_ED"
# "gr" is the filename of the geocoding results
gr = dir_path + "StLouisMO_1930_geocode_renumberedED.shp"
# "sg_vm" is the filename of the intersection of the street grid and the verified map
sg_vm = dir_path + "StLouisMO_grid_poly_intersect.shp"
#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
spatjoin = dir_path + "StLouisMO_1930_geo_map_spatjoin.shp"
# Not correct geocode
notcor = dir_path + "StLouisMO_1930_NotGeocodedCorrect.shp"
# Correct geocode
cor = dir_path + "StLouisMO_1930_GeocodedCorrect.shp"

geocode(add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr)

validate(dir_path, gr, vm, spatjoin, fc, swm_file, swm_table, fe_file, notcor, cor, residual_file="NotGeocoded.dbf")

#
# Contemporary grid
#

# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
add = dir_path + "NotGeocoded.dbf"
# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
sg = dir_path + "StLouisMO_1930_stgrid_edit_Uns2.shp"
# Amory's formatted EDs dbf
fe_file = "StLouisMO_1930_Contemp.dbf"
# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
al = dir_path + name + "_addloc_ED_Contemp"
# "gr" is the filename of the geocoding results
gr = dir_path + "StLouisMO_1930_geocode_renumberedED_Contemp.shp"
# "sg_vm" is the filename of the intersection of the street grid and the verified map
sg_vm = dir_path + "StLouisMO_grid_poly_intersect_Contemp.shp"
#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
spatjoin = dir_path + "StLouisMO_1930_geo_map_spatjoin_Contemp.shp"
# Not correct geocode
notcor = dir_path + "StLouisMO_1930_NotGeocodedCorrect_Contemp.shp"
# Correct geocode
cor = dir_path + "StLouisMO_1930_GeocodedCorrect_Contemp.shp"

geocode(add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr)

validate(dir_path, gr, vm, spatjoin, fc, swm_file, swm_table, fe_file, notcor, cor, residual_file="NotGeocoded_Contemp.dbf")

#
# Combine both geocodes to get the best geocode
#

def merge(list_of_shp):
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
	outfile = dir_path + "StLouisMO_GeocodeFinal.shp"
	arcpy.Merge_management(list_of_shp, outfile)
	df_merge = dbf2DF(outfile)
	df_merge_collapse = df_merge.groupby(['fullname','address','Mblk','ed','ed_1','contig_ed','geocoded']).size().reset_index(name='count')
	outfile_excel = dir_path + "StLouisMO_GeocodeFinal.xlsx"
	writer = pd.ExcelWriter(outfile_excel, engine='xlsxwriter')
	df_merge_collapse.to_excel(writer, sheet_name='Sheet1', index=False)
	writer.save()

first = dir_path + "StLouisMO_1930_GeocodedCorrect.shp"
second = dir_path + "StLouisMO_1930_NotGeocodedCorrect_Contemp.shp"
third = dir_path + "StLouisMO_1930_GeocodedCorrect_Contemp.shp"

list_of_shp = [first, second, third]

merge(list_of_shp)

# Create list of streets from ungeocoded points that are not in the grid
ungeocoded_shp = dir_path + "StLouisMO_1930_NotGeocodedCorrect_Contemp.shp"
df_ungeocoded = dbf2DF(ungeocoded_shp)
df_ungeocoded_st_ed = df_ungeocoded.loc[df_ungeocoded['fullname']!='.',['fullname','ed']]
df_ungeocoded_st_ed = df_ungeocoded_st_ed.groupby(['fullname','ed']).size().reset_index(name='count')

grid_file = dir_path + "StLouisMO_1930_stgrid_edit_Uns2.shp"
df_grid = dbf2DF(grid_file)
grid_streets_list = df_grid['FULLNAME'].drop_duplicates().tolist()

df_ungeocoded_st_ed_tocheck = df_ungeocoded_st_ed[~df_ungeocoded_st_ed['fullname'].isin(grid_streets_list)].sort_values(['ed'])

# Create a Pandas Excel writer using XlsxWriter as the engine.
file_name = dir_path + '/' + name + state + '_ungeocoded_not_in_grid.xlsx'
writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df_ungeocoded_st_ed_tocheck.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

