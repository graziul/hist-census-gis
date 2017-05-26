import arcpy
import os
import sys
import pandas as pd
import csv
import time
import pickle
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

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
#stgrid_file = gis_path + city_name + "_1930_stgrid_edit.shp"
stgrid_file = gis_path + city_name + state_abbr + "_1940_stgrid_edit_Uns2.shp"
out_file = gis_path + city_name + "_1930_Block_Choice_Map2test.shp"
pblk_grid_dict_file = gis_path + city_name + "_map_block_dict.pkl"
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

#Create {Census block:streets} dict from microdata 
df = df_pre.groupby(['ed_block',street]).size().to_frame('st_addresses').reset_index()
block_num_addresses_dict = df.groupby('ed_block').sum().to_dict().values()[0]
df['block_addresses'] = df.apply(lambda x: block_num_addresses_dict[x['ed_block']],axis=1)
df['prop_block'] = df['st_addresses']/df['block_addresses']
micro_blocks_dict = {group:streets[street].values.tolist() for group, streets in df.groupby('ed_block')}
	#TO DO: Remove blocks defined by a single street (too indeterminate)???
cprint("Finished building microdata block-street dictionary", 'cyan', file=AnsiToWin32(sys.stdout))

#Create {physical block:streets} dict from map

def remove_single_point_touches(street_list):
	touches = {i:street_list.count(i) for i in street_list}
	return [i for i in street_list if touches[i] > 1]

start = time.time()

arcpy.CopyFeatures_management(block_file, "block_file")
arcpy.CopyFeatures_management(stgrid_file, "stgrid_file")

	#Get list of streets touching each physical block and turn into dictionary
pblk_st_dict = {}
pblk_grid_dict = {}
#for row in arcpy.da.SearchCursor('in_memory\\block_file',('pblk_id','SHAPE@')):
block_sc = arcpy.da.SearchCursor('in_memory\\block_file',('pblk_id','SHAPE@'))
grid_sc = arcpy.da.SearchCursor('in_memory\\stgrid_file',('grid_id','SHAPE@','fullname'))

#for row in arcpy.da.SearchCursor(block_file,('pblk_id','SHAPE@')):
#	for row2 in arcpy.da.SearchCursor(stgrid_file,('grid_id','SHAPE@','fullname')):

for row in arcpy.da.SearchCursor('in_memory\\block_file',('pblk_id','SHAPE@')):
	pblk_st_dict[str(row[0])] = []
	pblk_grid_dict[str(row[0])] = []
	for row2 in arcpy.da.SearchCursor('in_memory\\stgrid_file',('grid_id','SHAPE@','fullname')):
		if not row[1].disjoint(row2[1]):
			if row[1].intersect(row2[1],1):
				pblk_st_dict[str(row[0])].append(row2[2])
				pblk_grid_dict[str(row[0])].append(row2[0])
exclude_list = ['City Limits']
	#Exclude certain street names "City Limits"
pblk_st_dict = {k:list(set([i for i in v if i not in exclude_list])) for k,v in pblk_st_dict.items()}
	#Save a copy for RenumberGrid.py
pickle.dump(pblk_grid_dict,open(pblk_grid_dict_file,'wb'))

end = time.time()
run_time = round(float(end-start)/60, 1)
cprint("Finished overlaying physical blocks and street grid (took " + str(run_time) + " minutes)"+"\n", 'cyan', file=AnsiToWin32(sys.stdout))

#Get number of physical blocks
num_physical_blocks = int(arcpy.GetCount_management(block_file).getOutput(0))
#Get number of microdata blocks
num_micro_blocks = len(df_pre['block'].unique())

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
fields = ['MBID']
labels_step1, pblks_labeled_step1, num_labeled_step1 = extract_step1_labels(fields)

#Look for block description matches
def match_using_block_desc(thresh,pblks_labeled,labels):
	temp_match_dict = {}
	for map_block, map_streets in pblk_st_dict.items():
		if len(map_streets) > 0 and (int(map_block) not in pblks_labeled):
			temp_match_dict[map_block] = temp_match_dict.setdefault(map_block, [])
			for micro_block, microdata_streets in micro_blocks_dict.items():
				if micro_block not in labels:
					u = [i.decode('utf-8') for i in microdata_streets]
					num_matching_streets = len(set(map_streets).intersection(set(u)))
					prop_matching_map = float(num_matching_streets)/len(map_streets)
					#Note: There are cases where prop_matching_map == 1 because all map streets
					#were found in microdata, but microdata may have additional streets
					if prop_matching_map >= thresh:
						temp_match_dict[map_block].append(micro_block)					
	temp_match_dict = {k:v[0] for k,v in temp_match_dict.items() if len(v)==1}
	temp_fids_labeled = [int(i) for i in temp_match_dict.keys()]
	temp_labels = temp_match_dict.values()
	num_matches = len(temp_match_dict)
	per_micro_blocks = round(100*float(num_matches)/num_micro_blocks, 1)
	cprint("Matches based on block description: "+str(num_matches)+" ("+str(per_micro_blocks)+r"% of microdata blocks)",file=AnsiToWin32(sys.stdout))
	return temp_match_dict, temp_fids_labeled, temp_labels, num_matches

exact_match_dict, pblks_labeled_exact, labels_exact, num_exact_matches \
	= match_using_block_desc(1, pblks_labeled_step1, labels_step1)

good_match_dict, pblks_labeled_good, labels_good, num_good_matches \
	= match_using_block_desc(0.75, pblks_labeled_step1+fids_labeled_exact, labels_step1+labels_exact)

num_labeled_step2 = num_exact_matches+num_good_matches
per_micro_blocks = round(100*float(num_labeled_step2)/num_micro_blocks, 1)
cprint("\n"+"Physical blocks labeled by Step 2: "+str(num_labeled_step2)+" ("+str(per_micro_blocks)+r"% of physical blocks)"+"\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

num_labeled_steps1and2 = num_labeled_step1+num_labeled_step2
per_micro_blocks = round(100*float(num_labeled_steps1and2)/num_micro_blocks, 1)
cprint("Physical blocks labeled by Step 1 and Step 2: "+str(num_labeled_steps1and2)+" ("+str(per_micro_blocks)+r"% of physical blocks)"+"\n",attrs=['bold'], file=AnsiToWin32(sys.stdout))

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
	row.setValue('blockdesc',exact_match_dict[str(pblk_id)])
	row.setValue('blockdesc2',good_match_dict[str(pblk_id)])
	cursor.updateRow(row)
del(cursor)
