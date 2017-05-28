import arcpy
import os
import sys
import pandas as pd
import pysal as ps
import csv
import time
import pickle
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from multiprocessing.dummy import Pool 
from _functools import partial

arcpy.env.parallelProcessingFactor = "75%"
arcpy.env.overwriteOutput=True
arcpy.env.workspace = "in_memory"

city_path = sys.argv[1]
city_name = sys.argv[2]
state_abbr = sys.argv[3]

#city_path = "S:\\Projects\\1940Census\\StLouis"
#city_name = "StLouis"
#state_abbr = "MO"

gis_path = city_path + "\\GIS_edited\\"
block_file = gis_path + city_name + "_1930_Block_Choice_Map.shp"
pblk_file = gis_path + city_name + "_1930_Pblk.shp"
#stgrid_file = gis_path + city_name + state_abbr + "_1930_stgrid_edit.shp"
stgrid_file = gis_path + city_name + state_abbr + "_1930_stgrid_edit_Uns2.shp"
pblk_grid_file = gis_path + city_name + state_abbr + "_1930_Pblk_Grid_SJ.shp"
out_file = gis_path + city_name + "_1930_Block_Choice_Map2.shp"
pblk_grid_dict_file = gis_path + city_name + "_pblk_grid_dict.pkl"
pblk_st_dict_file = gis_path + city_name + "_pblk_st_dict.pkl"
microdata_file = city_path + "\\StataFiles_Other\\1930\\" + city_name + state_abbr + "_StudAuto.dta"

cprint("Getting block description guesses\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))

#
# Step 1: Create "block descriptions" using microdata
#

#Load data
start = time.time()

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

def dbf2DF(dbfile, upper=False): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile) #Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    #pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    if upper == True: #Make columns uppercase if wanted 
        pandasDF.columns = map(str.upper, db.header) 
    db.close() 
    return pandasDF

street = 'autostud_street'
df_pre = load_large_dta(microdata_file)
df_pre = df_pre[['ed','block',street]]

end = time.time()
run_time = round(float(end-start)/60, 1)
cprint("Finished loading microdata (took " + str(run_time) + " minutes)", 'cyan', file=AnsiToWin32(sys.stdout))

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
df = df_pre.groupby(['ed_block',street]).size().to_frame('st_addresses').reset_index()
block_num_addresses_dict = df.groupby('ed_block').sum().to_dict().values()[0]
df['block_addresses'] = df.apply(lambda x: block_num_addresses_dict[x['ed_block']],axis=1)
df['prop_block'] = df['st_addresses']/df['block_addresses']
micro_blocks_dict = {group:streets[street].values.tolist() for group, streets in df.groupby('ed_block')}
	#TO DO: Remove blocks defined by a single street (too indeterminate)???
cprint("Finished building microdata block-street dictionary", 'cyan', file=AnsiToWin32(sys.stdout))

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
cprint("Finished overlaying physical blocks and street grid (took " + str(run_time) + " minutes)"+"\n", 'cyan', file=AnsiToWin32(sys.stdout))

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
	cprint("Physical blocks labeled in Step 1: "+str(num_labels_step1)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n",'green',attrs=['bold'], file=AnsiToWin32(sys.stdout))
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
	cprint("Matches based on block description: "+str(num_matches)+" ("+str(per_micro_blocks)+r"% of microdata blocks)",file=AnsiToWin32(sys.stdout))
	cprint("Matching took "+str(run_time)+" minutes to complete\n",'cyan',file=AnsiToWin32(sys.stdout))
	return temp_match_dict, list(temp_pblks_labeled), list(temp_labels), num_matches

thresh = 1
unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1}
exact_match_dict, pblks_labeled_exact, labels_exact, num_exact_matches = match_using_block_desc(pblks_labeled_step1)

thresh = 0.75
unknown_micro_blocks_dict = {k:v for k,v in micro_blocks_dict.items() if k not in labels_step1+labels_exact}
good_match_dict, pblks_labeled_good, labels_good, num_good_matches = match_using_block_desc(pblks_labeled_step1+pblks_labeled_exact)

num_labeled_step2 = num_exact_matches+num_good_matches
per_micro_blocks = round(100*float(num_labeled_step2)/num_micro_blocks, 1)
cprint("\n"+"Physical blocks labeled by Step 2: "+str(num_labeled_step2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

num_labeled_steps1and2 = num_labeled_step1+num_labeled_step2
per_micro_blocks = round(100*float(num_labeled_steps1and2)/num_micro_blocks, 1)
cprint("Physical blocks labeled by Step 1 and Step 2: "+str(num_labeled_steps1and2)+" ("+str(per_micro_blocks)+r"% of microdata blocks)"+"\n",attrs=['bold'], file=AnsiToWin32(sys.stdout))

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
