import arcpy
import os
import sys
import pandas as pd
import csv
import time
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

arcpy.env.parallelProcessingFactor = "75%"
arcpy.env.overwriteOutput=True

city_path = sys.argv[1]
city_name = sys.argv[2]
microdata_file = sys.argv[3]
state_abbr = sys.argv[4]

#city_name = "Hartford"
#street = 'autostud_street'
#microdata_file = city_path + "\\StataFiles_Other\\1930\\HartfordCT_StudAuto.dta"

gis_path = city_path + "\\GIS_edited\\"
block_file = gis_path + city_name + "_1930_Block_Choice_Map.shp"
#stgrid_file = gis_path + city_name + "_1930_stgrid_edit.shp"
stgrid_file = "S:\\Projects\\1940Census\\StreetGrids\\" + city_name + state_abbr + "_1940_stgrid_edit.shp"
out_file = gis_path + city_name + "_1930_Block_Choice_Map2.shp"

#dir_path = sys.argv[1] + "\\GIS_edited\\"
#name = sys.argv[2]
#state = sys.argv[3]

cprint("Getting block description guesses\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))

#
# Step 1: Create "block descriptions" using microdata
#

#Load data
start = time.time()

if microdata_file.split('.')[1] == 'dta':
	street = 'autostud_street'
	df_pre = pd.read_stata(microdata_file)
	df_pre = df_pre[['ed','block',street]]
if microdata_file.split('.')[1] == 'csv':
	street = 'overall_match'
	with open(microdata_file) as f:
		reader = csv.reader(f)
		header = next(reader)
	ed_idx = header.index('ed')
	block_idx = header.index('block')
	street_idx = header.index(street)
	df_pre = pd.read_csv(microdata_file,usecols=[ed_idx,block_idx,street_idx])

end = time.time()
run_time = round(float(end-start)/60, 1)
cprint("Finished loading microdata (took " + str(run_time) + " minutes)", 'cyan', file=AnsiToWin32(sys.stdout))

#TO DO: Clean up block numbers
df_pre = df_pre[df_pre['block'].notnull() & df_pre['ed'].notnull()]
df_pre['ed_block'] = df_pre['ed'].astype(str) + '-' + df_pre['block'].astype(str)
del df_pre['ed']
del df_pre['block']

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

temp_file = gis_path + city_name + "_1930_Block_Choice_Map2.shp"

	#Get list of streets touching each physical block and turn into dictionary
map_blocks_dict = {}
for row in arcpy.da.SearchCursor(block_file,('OID@','SHAPE@')):
	map_blocks_dict[str(row[0])] = []
	for row2 in arcpy.da.SearchCursor(stgrid_file,('OID@','SHAPE@','fullname')):
		if not row[1].disjoint(row2[1]):
			if row[1].intersect(row2[1],1):
				map_blocks_dict[str(row[0])].append(row2[2])
exclude_list = ['City Limits']
	#Exclude certain street names "City Limits"
map_blocks_dict = {k:list(set([i for i in v if i not in exclude_list])) for k,v in map_blocks_dict.items()}
	#Remove streets that touch physical block only once (i.e. T-intersections)
#map_blocks_dict = {k:list(set(remove_single_point_touches(v))) for k,v in map_blocks_dict.items()}

end = time.time()
run_time = round(float(end-start)/60, 1)
cprint("Finished overlaying physical blocks and street grid (took " + str(run_time) + " minutes)"+"\n", 'cyan', file=AnsiToWin32(sys.stdout))

#Get number of physical blocks
num_physical_blocks = int(arcpy.GetCount_management(block_file).getOutput(0))

#Get block numbers already labeled in Step 1 (strict criteria)
def extract_step1_labels(fields):
	labels_step1 = []
	fid_labeled1 = []
	for field in fields:
		with arcpy.da.SearchCursor(block_file,['FID',field]) as cursor:
			for row in cursor:
				if row[1] != ' ':
					labels_step1.append(row[1])
					fid_labeled1.append(row[0])
	num_labels_step1 = len(labels_step1)
	per_physical_blocks = round(100*float(num_labels_step1)/num_physical_blocks, 1)
	cprint("Physical blocks labeled in Step 1: "+str(num_labels_step1)+" ("+str(per_physical_blocks)+r"% of physical blocks)"+"\n",'green',attrs=['bold'], file=AnsiToWin32(sys.stdout))
	return labels_step1, fid_labeled1, num_labels_step1

fields = ['MBID','MBID2']
labels_step1, fids_labeled_step1, num_labeled_step1 = extract_step1_labels(fields)

#Look for block description matches
def match_using_block_desc(thresh,fids_labeled,labels):
	temp_match_dict = {}
	for map_block, map_streets in map_blocks_dict.items():
		if len(map_streets) > 0 and (int(map_block) not in fids_labeled):
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
	per_physical_blocks = round(100*float(num_matches)/num_physical_blocks, 1)
	cprint("Matches based on block description: "+str(num_matches)+" ("+str(per_physical_blocks)+r"% of physical blocks)",file=AnsiToWin32(sys.stdout))
	return temp_match_dict, temp_fids_labeled, temp_labels, num_matches

exact_match_dict, fids_labeled_exact, labels_exact, num_exact_matches \
	= match_using_block_desc(1, fids_labeled_step1, labels_step1)

good_match_dict, fids_labeled_good, labels_good, num_good_matches \
	= match_using_block_desc(0.75, fids_labeled_step1+fids_labeled_exact, labels_step1+labels_exact)

num_labeled_step2 = num_exact_matches+num_good_matches
per_physical_blocks = round(100*float(num_labeled_step2)/num_physical_blocks, 1)
cprint("\n"+"Physical blocks labeled by Step 2: "+str(num_labeled_step2)+" ("+str(per_physical_blocks)+r"% of physical blocks)"+"\n",'green',attrs=['bold'],file=AnsiToWin32(sys.stdout))

num_labeled_steps1and2 = num_labeled_step1+num_labeled_step2
per_physical_blocks = round(100*float(num_labeled_steps1and2)/num_physical_blocks, 1)
cprint("Physical blocks labeled by Step 1 and Step 2: "+str(num_labeled_steps1and2)+" ("+str(per_physical_blocks)+r"% of physical blocks)"+"\n",attrs=['bold'], file=AnsiToWin32(sys.stdout))

#Add labels 

map_blocks = map_blocks_dict.keys()
for block in map_blocks:
	if block not in exact_match_dict.keys():
		exact_match_dict[block] = ''
	if block not in good_match_dict.keys():
		good_match_dict[block] = ''		

arcpy.CopyFeatures_management(block_file,out_file)
arcpy.AddField_management(out_file,'blockdesc','TEXT')
arcpy.AddField_management(out_file,'blockdesc2','TEXT')

cursor = arcpy.UpdateCursor(out_file)
for row in cursor:
	fid = row.getValue('FID')
	row.setValue('blockdesc',exact_match_dict[str(fid)])
	row.setValue('blockdesc2',good_match_dict[str(fid)])
	cursor.updateRow(row)
del(cursor)
