#
# FixBlockNumsUsingMap.py
#
# Process:
#  1. Obtain ED map
#  2. Obtain block map (preliminary or final)
#  3. Obtain street grid with 1930 HN ranges derived from microdata
#  4. Geocode using street grid with 1930 HN ranges
#  5. Geocode residuals using street grid with contemporary HN ranges
#  6. Check if points are in correct ED
#  7. Intersect points in correct ED with block map
#  8. Assign correct block numbers to microdata points
#  9. Reassign 1930 HN ranges based on improved/validated microdata blocks
#

import arcpy
import os
import pandas as pd
import pysal as ps
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


dir_path = "S:\\Projects\\1940Census\\StLouis\\GIS_edited\\"
name = "StLouis"
state = "MO"

# Geocode using street grid with 1930 HN ranges (should be done already)
add_locator_old = dir_path + name + "_addlocOld"
addresses = dir_path + name + "_1930_Addresses.csv"
address_fields_old="Street address; City CITY; State STATE; ZIP <None>"
points30 = dir_path + name + "_1930_Points_updated.shp"
#arcpy.GeocodeAddresses_geocoding(addresses, add_locator_old, address_fields_old, points30)

# Obtain residuals
residual_addresses = dir_path + name + "_1930_Addresses_residual.csv"
temp = dir_path + "temp.shp"
arcpy.MakeFeatureLayer_management(points30, "geocodelyr")
arcpy.SelectLayerByAttribute_management("geocodelyr", "NEW_SELECTION", """ "Status" <> 'M' """)
arcpy.CopyFeatures_management("geocodelyr",temp)
df = dbf2DF(temp.replace('.shp','.dbf'))
resid_vars = ['index','ed','fullname','state','city','address']
df_resid = df[resid_vars]
file_name = dir_path + name + "_1930_Addresses_residual.csv"
if os.path.isfile(file_name):
	os.remove(file_name)
df_resid.to_csv(file_name)
if os.path.isfile(file_name.replace('.csv','.dbf')):
	os.remove(file_name.replace('.csv','.dbf'))
arcpy.TableToTable_conversion(file_name,dir_path,name + "_1930_Addresses_residual.dbf")
temp_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith("temp")]
for f in temp_files:
    if os.path.isfile(f):
        os.remove(f)

# Geocode residuals using street grid with contemporary HN ranges
add_locator_contemp = dir_path + name + "_addloc"
addresses_resid = dir_path + name + "_1930_Addresses_residual.dbf"
address_fields_contemp="Street address; City city; State state"
points30_resid = dir_path + name + "_1930_ResidPoints.shp"
arcpy.GeocodeAddresses_geocoding(addresses_resid, add_locator_contemp, address_fields_contemp, points30_resid)

# Intersect geocoded points with ED map
ed_map = dir_path + name + "_1930_ED.shp"
intersect_resid_ed = dir_path + name + "_1930_intersect_resid_ed.shp"
arcpy.Intersect_analysis([ed_map, points30_resid], intersect_resid_ed)

# Identify points in the correct ED
inrighted = dir_path + "_1930_ResidPoints_inRightED.shp"
arcpy.MakeFeatureLayer_management(intersect_resid_ed, "geocodelyr1")
arcpy.SelectLayerByAttribute_management("geocodelyr1", "NEW_SELECTION", """ "ed" = "ed_1" """)
arcpy.CopyFeatures_management("geocodelyr1",inrighted)

# Intersect points in the correct ED with block map
intersect_correct_ed = dir_path + name + "_1930_intersect_correct_ed.shp"
block_shp_file = dir_path + name + "_1930_block_ED_checked.shp"
arcpy.Intersect_analysis([block_shp_file, inrighted], intersect_correct_ed)

# Get correct block number based on block map and geocoded in correct ED
df_correct_ed = dbf2DF(intersect_correct_ed.replace('.shp','.dbf'))
df_correct_ed['block'] = df_correct_ed['am_bn'].str.split('-').str[1:].str.join('-')
fix_block_dict = df_correct_ed[['index','block']].set_index('index')['block'].to_dict()

# Replace microdata block number with block map block number
microdata_file = "S:\\Projects\\1940Census\\" + name + "\\StataFiles_other\\1930\\"  + name + state + "_StudAuto.dta"
df_micro = load_large_dta(microdata_file)
df_micro['block_old'] = df_micro['block']

def fix_block(index, block):
	try:
		fix_block = fix_block_dict[index]
		return fix_block
	except:
		return block

df_micro['block'] = df_micro[['index','block_old']].apply(lambda x: fix_block(x['index'], x['block_old']), axis=1)
df_micro['changed_Block'] = df_micro['block'] != df_micro['block_old']


print(df_micro['changed_Block'].sum())

# Save microdata file
df_micro.to_csv(microdata_file.replace('.dta','.csv'))

# Manually convert to .dta in Stata

# Next script: RenumberGrid.py