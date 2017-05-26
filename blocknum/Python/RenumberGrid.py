import pysal as ps
import pandas as pd
import arcpy
import os
import pickle
arcpy.env.overwriteOutput=True

'''
Arguments
---------
dbfile  : DBF file - Input to be imported
upper   : Condition - If true, make column heads upper case
'''
def dbf2DF(dbfile, upper=True): #Reads in DBF files and returns Pandas DF
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

block_dbf_file = dir_path + city_name + "_1930_Block_Choice_Map2.dbf"
stgrid_file = dir_path + city_name + state_abbr + "_1940_stgrid_edit_Uns2.shp"
out_file = dir_path + city_name + state_abbr + "_1930_stgrid_renumbered.shp"
block_shp_file = dir_path + city_name + "_1930_Block_Choice_Map2.shp"
pblk_grid_dict_file = dir_path + city_name + "_map_block_dict.pkl"
add_locator_updated = dir_path + name + "_addloc_updated"
addresses = dir_path + name + "_1930_Addresses.csv"
address_fields="Street address; City city; State state; ZIP <None>"
points30 = dir_path + name + "_1930_Points_updated.shp"

# Load
arcpy.CopyFeatures_management(stgrid_file,out_file)
df_grid = dbf2DF(out_file.replace(".shp",".dbf"),upper=False)
df_block = dbf2DF(block_dbf_file,upper=False)
df_micro = load_large_dta(microdata_file)

vars_of_interest = ['ed','hn','autostud_street','block']
df_micro = df_micro[vars_of_interest]
df_micro = df_micro.dropna(how='any')
df_micro['hn'] = df_micro['hn'].astype(int)
df_micro['edblock'] = df_micro['ed'].astype(str)+'-'+df_micro['block']

# Get house number ranges for block-street combinations from microdata
df_micro_byblkst = df_micro.groupby(['edblock','autostud_street'])
blkst_hn_dict = {}
for group, group_data in df_micro_byblkst:
	blkst_hn_dict[group] = {'min_hn':group_data['hn'].min(), 'max_hn':group_data['hn'].max()}

# Get dictionary linking edblock to pblk_id
bn_var = 'auto_bn'
temp = df_block.loc[df_block[bn_var]!='',[bn_var,'pblk_id']]
pblk_edblock_dict = temp.set_index('pblk_id')[bn_var].to_dict()

# Load dictionary linking pblk_id to grid_id
pblk_grid_dict = pickle.load(pblk_grid_dict_file)

# Create dictionary linking grid_id to edblock
grid_edblock_dict = {}
for pblk, grid_id_list in pblk_grid_dict.items():
	for grid_id in grid_id_list:
		grid_edblock_dict[grid_id] = pblk_edblock_dict[pblk]

# Use edblock to assign street ranges
arcpy.AddField_management(out_file,'L_FROM','TEXT')
arcpy.AddField_management(out_file,'L_TO','TEXT')
arcpy.AddField_management(out_file,'R_FROM','TEXT')
arcpy.AddField_management(out_file,'R_TO','TEXT')

cursor = arcpy.UpdateCursor(out_file)
for row in cursor:
	grid_id = row.getValue('grid_id')
	st_name = row.getValue('FULLNAME')
	try:
		blkst_hn = blkst_hn_dict[edblock,st_name]
		blkst_hn_range = range(blkst_hn['min_hn'],blkst_hn['max_hn']+1)
		evensList = [x for x in blkst_hn_range if x % 2 == 0]
		oddsList = [x for x in blkst_hn_range if x % 2 != 0]
		row.setValue('L_FROM',min(evensList))
		row.setValue('L_TO',max(evensList))
		row.setValue('R_FROM',min(oddsList))
		row.setValue('R_TO',max(oddsList))
	except:
		pass
	cursor.updateRow(row)
del(cursor)

#Recreate Address Locator
arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", in_reference_data=out_file, in_field_map=field_map, out_address_locator=add_locator_updated, config_keyword="")
#Geocode Points
arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
