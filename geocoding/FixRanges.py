from operator import itemgetter
from itertools import groupby
import pandas as pd
import pysal as ps
import pickle
import arcpy
import os

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

# Flip ranges when min > max
def flip_ranges(hn_ranges):

	min_l, max_l, min_r, max_r = hn_ranges

	if min_l > max_l:
		true_min_l = max_l
		true_max_l = min_l
	else:
		true_min_l = min_l
		true_max_l = max_l

	if min_r > max_r:
		true_min_r = max_r
		true_max_r = min_r
	else:
		true_min_r = min_r
		true_max_r = max_r
		
	return [true_min_l, true_max_l, true_min_r, true_max_r]

# Fix blanks
def fix_blanks(name, group, hn_ranges, blanks_dict):

	def get_ids(side):
		ranges = []
		data = blanks_dict[name][side]
		for k, g in groupby(enumerate(data), lambda (i,x): i-x):
			ranges.append(map(itemgetter(1), g))
		return ranges

	def get_value(id_val, var):
		try:
			return int(group.loc[group['order']==id_val,var].values[0])
		except:
			return None

	def fix_side(min_side, max_side):

		# Get sequences of blanks 
		ranges_min = get_ids(min_side)
		ranges_max = get_ids(max_side)

		# Count blanks that are fixable vs. fixed
		blanks_fixable = 0
		blanks_fixed = 0

		# Do something only if blanks are the same for from/to (simplest case):
		if ranges_min == ranges_max:
			blank_seqs = ranges_min
			for seq in blank_seqs:
				# Get dictionary linking seq to FID_str 
				order_fid_dict = group[['order','grid_id']].set_index('order')['grid_id'].to_dict()
				# Initialize dictionary {FID_str:{min_side:hn, max_side:hn}}
				for k,v in order_fid_dict.items():
					list_of_blanks = [i for s in blank_seqs for i in s]
					if k in list_of_blanks:
						fix_blanks_dict_temp.setdefault(v,{})
				# Get the start and end of the sequence
				max_id = max(seq)
				min_id = min(seq)
				# Get starting and ending house numbers based on available data	
				seq_start = get_value(min_id-1, max_side)
				seq_end = get_value(max_id+1, min_side)
				# Check order and reverse start/end if seq_start > seq_end (i.e. order is reversed)
				if seq_start > seq_end:
					start = seq_end
					end = seq_start
				else:
					start = seq_start
					end = seq_end
				# If no house number before or after sequence, do nothing
				if start is None or end is None:
					fix_blanks_dict_temp.update({})
				# Otherwise, break up by range number of segments and assign values
				else:
					num_segs = len(seq)
					blanks_fixable += num_segs
					# Create dictionary for assigning ranges to blanks
					if (num_segs == 1) & ((end-start)>4):
						fix_blanks_dict_temp[order_fid_dict[seq[0]]].update({min_side:start+2, max_side:end-2})
						blanks_fixed += num_segs
					if (num_segs > 1) & (end-start)>4:
						interval = (end - start - 2)/num_segs - 1
						max_cuts = [start+i*interval+2 for i in range(0,num_segs+1)]
						cuts = max_cuts + [i+2 for i in max_cuts[1:-1]]
						cuts.sort()
						cuts[-1] = cuts[-1]+2
						for i in range(len(cuts)/2):
							fix_blanks_dict_temp[order_fid_dict[seq[i]]].update({min_side:cuts[2*i], max_side:cuts[2*i+1]})
						blanks_fixed += num_segs
			return fix_blanks_dict_temp, blanks_fixable, blanks_fixed
		else:
			return fix_blanks_dict_temp, blanks_fixable, blanks_fixed

	min_l, max_l, min_r, max_r = hn_ranges

	# Fixes each side independently, overwriting what was once there
	fix_blanks_dict_temp = {}
	fix_blanks_dict_temp, blanks_fixable_l, blanks_fixed_l = fix_side(min_l, max_l)
	fix_blanks_dict_temp, blanks_fixable_r, blanks_fixed_r= fix_side(min_r, max_r)

	blanks_fixable = blanks_fixable_l + blanks_fixable_r
	blanks_fixed = blanks_fixed_l + blanks_fixed_r

	return fix_blanks_dict_temp, blanks_fixable, blanks_fixed

#shp_file="S:/Projects/1940Census/StLouis/GIS_edited/StLouisMO_1930_stgrid_renumbered.shp"

shp_file = "S:/Projects/1940Census/StLouis/GIS_edited/StLouisMO_1930_stgrid_edit_Uns2.shp"
shp_file_fixed = shp_file.replace('.shp','bf.shp')
arcpy.CopyFeatures_management(shp_file, shp_file_fixed)
dbf_file=shp_file_fixed.replace('.shp','.dbf')

seq_dict = pickle.load(open('C:/Users/cgraziul/Documents/StLouis_consec.p','rb'))
df = dbf2DF(dbf_file)

# Variable names for ranges
min_l = 'MIN_LFROMA'
max_l = 'MAX_LTOADD'
min_r = 'MIN_RFROMA'
max_r = 'MAX_RTOADD'
hn_ranges = [min_l, max_l, min_r, max_r]

# Blank out zero house numbers
for hn_range in hn_ranges:
	df.loc[df[hn_range]=='0',hn_range] = ''

# Flip ranges when min > max
df[hn_ranges] = df[hn_ranges].apply(lambda x: flip_ranges(x),axis=1)

# Group by street name
df_grouped = df.groupby(['FULLNAME'])

# Build dictionary for fixing blanks by looping through streets
fix_blanks_dict = {}
blanks_dict = {}
blanks_fixable_total = 0
blanks_fixed_total = 0
for name in df['FULLNAME'].drop_duplicates().tolist():
	# Get list of grid_id for each street name
	try:
		grid_id_list = seq_dict[name]
	except:
		continue
	# Create a dictionary based on the sequence of segments
	grid_id_dict = {grid_id_list[i]:i for i in range(len(grid_id_list))}
	# Convert dictionary into a data frame 
	df_dict = pd.DataFrame(grid_id_dict.items(),columns=['grid_id','order'])
	group = df[df['grid_id'].isin(grid_id_list)]
	group = group.merge(df_dict, on='grid_id')
	group = group.sort_values(['order'])
	#Create list of blank sequences
	list_order = list(group['order'].values)
	#Get blanks
	blanks_dict[name] = {hn:list(group.loc[group[hn]=='','order'].values) for hn in hn_ranges}
	#Fix blanks
	fix_blanks_dict_temp, blanks_fixable, blanks_fixed = fix_blanks(name, group, hn_ranges, blanks_dict)
	blanks_fixable_total += blanks_fixable
	blanks_fixed_total += blanks_fixed
	fix_blanks_dict.update(fix_blanks_dict_temp)
fix_blanks_dict = {k:v for k,v in fix_blanks_dict.items() if v != {}}
blanks_dict = {k:v for k,v in blanks_dict.items() if v != dict(zip(hn_ranges,[[],[],[],[]]))}

per_blanks_fixable = float(blanks_fixable_total)/(2*len(df))
per_blanks_fixed = float(blanks_fixed_total)/blanks_fixable_total

print("Fixable blanks: " + str(blanks_fixable_total) + " (" + '{:.1%}'.format(per_blanks_fixable) + " of " + str(2*len(df)) + " segment-sides)")
print("Fixed blanks: " + str(blanks_fixed_total) + " (" + '{:.1%}'.format(per_blanks_fixed) + " of fixable blanks)")

def fill_in_blanks(x):
	grid_id, min_left, max_left, min_right, max_right = x
	orig = [min_left, max_left, min_right, max_right]
	try:
		temp_dict = fix_blanks_dict[grid_id]
		try:
			true_min_left = str(temp_dict[min_l])
		except:
			true_min_left = min_left
		try:
			true_max_left = str(temp_dict[max_l])
		except:
			true_max_left = max_left
		try:
			true_min_right = str(temp_dict[min_r])
		except:
			true_min_right = min_right
		try:
			true_max_right = str(temp_dict[max_r])
		except:
			true_max_right = max_right
		return [true_min_l, true_max_l, true_min_r, true_max_r]
	except:
		return orig

df[min_l], df[max_l], df[min_r], df[max_r] = zip(*df[['grid_id']+hn_ranges].apply(lambda x: fill_in_blanks(x), axis=1))


save_dbf(df, dbf_file.replace('.dbf','.shp'))
