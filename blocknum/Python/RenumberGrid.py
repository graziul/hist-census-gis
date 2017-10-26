import pysal as ps
import pandas as pd
import numpy as np
import arcpy
import os
import pickle
arcpy.env.overwriteOutput=True

# Function to reads in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=True): 
	db = ps.open(dbfile) #Pysal to open DBF
	d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
	#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
	pandasDF = pd.DataFrame(d) #Convert to Pandas DF
	if upper == True: #Make columns uppercase if wanted 
		pandasDF.columns = map(str.upper, db.header) 
	db.close() 
	return pandasDF

def load_large_dta(fname):

	reader = pd.read_stata(fname, iterator=True)
	df = pd.DataFrame()

	try:
		chunk = reader.get_chunk(100*1000)
		while len(chunk) > 0:
			df = df.append(chunk, ignore_index=True)
			chunk = reader.get_chunk(100*1000)
			print '.',
			sys.stdout.flush()
	except (StopIteration, KeyboardInterrupt):
		pass

	print '\nloaded {} rows\n'.format(len(df))

	return df

#file_path = sys.argv[1]
#city_name = sys.argv[2]
#state_abbr = sys.argv[2]

file_path = "S:\\Projects\\1940Census\\StLouis" 
city_name = "StLouis"
state_abbr = "MO"
microdata_file = file_path + "\\StataFiles_Other\\1930\\" + city_name + state_abbr + "_StudAuto.dta"
dir_path = file_path + "\\GIS_edited\\"

#block_dbf_file = dir_path + city_name + "_1930_Block_Choice_Map2test.dbf"
block_dbf_file = dir_path + city_name + "_1930_block_ED_checked.dbf"
#stgrid_file = dir_path + city_name + state_abbr + "_1930_stgrid_editFtoL.shp"
stgrid_file = dir_path + name + state + "_1930_stgrid_edit_Uns2_dupAddrFixed.shp"
out_file = dir_path + city_name + state_abbr + "_1930_stgrid_renumbered.shp"
block_shp_file = dir_path + city_name + "_1930_block_ED_checked.shp"
addresses = dir_path + city_name + "_1930_Addresses.csv"
points30 = dir_path + city_name + "_1930_Points_updated.shp"

pblk_file = block_shp_file #Note: This is the manually edited block file
pblk_grid_file2 = dir_path + city_name + state_abbr + "_1930_Pblk_Grid_SJ2.shp"

# Load
df_grid = dbf2DF(out_file.replace(".shp",".dbf"),upper=False)
df_block = dbf2DF(block_dbf_file,upper=False)
df_micro = load_large_dta(microdata_file)

vars_of_interest = ['ed','hn','autostud_street','block']
df_micro = df_micro[vars_of_interest]
df_micro = df_micro.dropna(how='any')
df_micro['hn'] = df_micro['hn'].astype(int)

#Create ED-block variable (standardized against block map)
#Turn ED=0 into blank 
df_micro['ed1'] = df_micro['ed'].astype(str).replace('0','')

df_micro['block1'] = df_micro['block'].str.replace(' ','-')
df_micro['block1'] = df_micro['block1'].str.replace('and','-')
df_micro['block1'] = df_micro['block1'].str.replace('.','-')
df_micro['block1'] = df_micro['block1'].replace('-+','-',regex=True)

df_micro['edblock'] = df_micro['ed1'] + '-' + df_micro['block1']
df_micro['edblock'] = df_micro['edblock'].replace('^-|-$','',regex=True)
df_micro.loc[df_micro['block']=='','edblock'] = ''
df_micro.loc[df_micro['ed']==0,'edblock'] = ''

def get_cray_z_scores(arr) :
	debug = False
	if not None in arr :
		inc_arr = np.unique(arr) #returns sorted array of unique values
		if(len(inc_arr)>=2) :
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

			return dict(zip(inc_arr, meanified_z_score * modified_z_score > 16))    
	try:
		return {inc_arr[0]:False}
	except:
		pass

# Get house number ranges for block-street combinations from microdata
df_micro_byblkst = df_micro.groupby(['edblock','autostud_street'])
blkst_hn_dict = {}
bad_blkst = []
for group, group_data in df_micro_byblkst:
	try:
		cray_dict = get_cray_z_scores(group_data['hn'])
		hn_range = [k for k,v in cray_dict.items() if not v]
		blkst_hn_dict[group] = {'min_hn':min(hn_range), 'max_hn':max(hn_range)}
	except:
		bad_blkst.append(group)


# Get dictionary linking edblock to pblk_id
bn_var = 'am_bn'
temp = df_block.loc[df_block[bn_var]!='',[bn_var,'ed','pblk_id']]
pblk_edblock_dict = temp.set_index('pblk_id')[bn_var].to_dict()
pblk_ed_dict = temp.set_index('pblk_id')['ed'].to_dict()

field_mapSJ = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
ed "ed" true true false 10 Long 0 10 ,First,#,%s,ed,-1,-1;
FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (pblk_file, pblk_file, stgrid_file, stgrid_file)
arcpy.SpatialJoin_analysis(target_features=pblk_file, join_features=stgrid_file, out_feature_class=pblk_grid_file2, 
	join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
	match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
df_pblk_grid = dbf2DF(pblk_grid_file2.replace(".shp",".dbf"),upper=False)

# Create dictionary linking grid_id to pblk
grid_pblk_dict = {}
grouped_grid = df_pblk_grid.groupby(['grid_id'])
for grid_id, pblk_df in grouped_grid:
	grid_pblk_dict[grid_id] = pblk_df['pblk_id'].tolist()

# Create dictionary linking grid_id to fullname
grid_fullname_dict = df_pblk_grid.set_index('grid_id').to_dict()['FULLNAME']

# Create dictionary linking grid_id to list of edblocks it intersects
grid_edblock_dict = {grid_id:[pblk_edblock_dict[int(pblk_id)] for pblk_id in pblk_id_list] for grid_id, pblk_id_list in grid_pblk_dict.items()}

grid_hn_dict = {}
for grid_id, edblock_list in grid_edblock_dict.items():
	try:
		min_hn = max([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['min_hn'] for i in edblock_list])
		max_hn = min([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['max_hn'] for i in edblock_list])
		eds = [i.split("-")[0] for i in edblock_list] 
		grid_hn_dict[grid_id] = {'min_hn':min_hn, 'max_hn':max_hn, 'ed':max(set(eds), key=eds.count)}
	except:
		pass

arcpy.CopyFeatures_management(stgrid_file,out_file)

#Add ED field
arcpy.AddField_management(out_file, "ed", "TEXT", 5, "", "","", "", "")
cursor = arcpy.UpdateCursor(out_file)
for row in cursor:
	grid_id = row.getValue('grid_id')
	st_name = row.getValue('FULLNAME')
	try:
		hn_range = range(grid_hn_dict[grid_id]['min_hn'],grid_hn_dict[grid_id]['max_hn']+1)
		evensList = [x for x in hn_range if x % 2 == 0]
		oddsList = [x for x in hn_range if x % 2 != 0]
		row.setValue('MIN_LFROMA', min(evensList))
		row.setValue('MAX_LTOADD', max(evensList))
		row.setValue('MIN_RFROMA', min(oddsList))
		row.setValue('MAX_RTOADD', max(oddsList))
		row.setValue('ed', int(grid_hn_dict[grid_id]['ed']))
	except:
		pass
	cursor.updateRow(row)
del(cursor)

old = True

if old:
	add_locator = dir_path + city_name + "_addlocOld"
	arcpy.DeleteField_management(out_file, ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD'])
	arcpy.AddField_management(out_file, "MIN_LFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_LTOADD", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MIN_RFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_RTOADD", "TEXT", 5, "", "","", "", "")
	# Use edblock to assign street ranges
	cursor = arcpy.UpdateCursor(out_file)
	for row in cursor:
		grid_id = row.getValue('grid_id')
		st_name = row.getValue('FULLNAME')
		try:
			hn_range = range(grid_hn_dict[grid_id]['min_hn'],grid_hn_dict[grid_id]['max_hn']+1)
			evensList = [x for x in hn_range if x % 2 == 0]
			oddsList = [x for x in hn_range if x % 2 != 0]
			row.setValue('MIN_LFROMA', min(evensList))
			row.setValue('MAX_LTOADD', max(evensList))
			row.setValue('MIN_RFROMA', min(oddsList))
			row.setValue('MAX_RTOADD', max(oddsList))
			row.setValue('ed', int(grid_hn_dict[grid_id]['ed']))
		except:
			pass
		cursor.updateRow(row)
	del(cursor)
else:
	# Use edblock to assign street ranges
	cursor = arcpy.UpdateCursor(out_file)
	for row in cursor:
		grid_id = row.getValue('grid_id')
		st_name = row.getValue('FULLNAME')
		try:
			row.setValue('ed', int(grid_hn_dict[grid_id]['ed']))
		except:
			pass
		cursor.updateRow(row)
	del(cursor)
	add_locator = dir_path + city_name + "_addlocContemp"

#Make sure address locator doesn't already exist - if it does, delete it
if old:
	add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(city_name+"_addlocOld2017_09_01")]
else:
	add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(city_name+"_addlocContemp")]

for f in add_loc_files:
	if os.path.isfile(f):
		os.remove(f)

#Recreate Address Locator
field_map="'Feature ID' FID VISIBLE NONE; \
'*From Left' MIN_LFROMA VISIBLE NONE; \
'*To Left' MAX_LTOADD VISIBLE NONE; \
'*From Right' MIN_RFROMA VISIBLE NONE; \
'*To Right' MAX_RTOADD VISIBLE NONE; \
'Prefix Direction' <None> VISIBLE NONE; \
'Prefix Type' <None> VISIBLE NONE; \
'*Street Name' FULLNAME VISIBLE NONE; \
'Suffix Type' '' VISIBLE NONE; \
'Suffix Direction' <None> VISIBLE NONE; \
'Left City or Place' CITY VISIBLE NONE; \
'Right City or Place' CITY VISIBLE NONE; \
'Left ZIP Code' ed VISIBLE NONE; \
'Right ZIP Code' ed VISIBLE NONE; \
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
'Altname JoinID' <None> VISIBLE NONE"
address_fields= "Street address; City city; State state"
arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", 
	in_reference_data=out_file, 
	in_field_map=field_map, 
	out_address_locator=add_locator, 
	config_keyword="")


#Geocode Points
#arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
