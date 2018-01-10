from operator import itemgetter
from itertools import groupby
from blocknum.blocknum import *
import math

# overwrite output
arcpy.env.overwriteOutput=True

# Function to load large Stata files
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

# Outlier detection
def get_cray_z_scores(arr) :
    debug = False
    if not None in arr :
        inc_arr = np.unique(arr) #returns sorted array of unique values
        if(len(inc_arr)>2) :
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

            return dict(zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score)>8))
    return None

#def fill_blank_segs(city_name, state_abbr, paths, df_micro=None):

##
## Strategy: Produce renamed grids after filling blanks, use those to do geocoding, preserve orig
##

city_name = 'StLouis'
state_abbr = 'MO'
dir_path = "S:/Projects/1940Census/" + city_name #TO DO: Directories need to be city_name+state_abbr
geo_path = dir_path + "/GIS_edited/"

# Variable names for ranges
min_l = 'MIN_LFROMA'
max_l = 'MAX_LTOADD'
min_r = 'MIN_RFROMA'
max_r = 'MAX_RTOADD'
hn_ranges = [min_l, max_l, min_r, max_r]
grid_street_var = 'FULLNAME'

old_grid_file=geo_path + city_name + state_abbr + "_1930_stgrid_renumbered.shp"
#old_grid_file = geo_path + city_name + state_abbr + "_1930_stgrid_edit_Uns2.shp"

def fill_blank_segs(dir_path, city_name, state_abbr, hn_ranges, old_grid_file, grid_street_var):

	geo_path = dir_path + "/GIS_edited/"

	grid_file = old_grid_file.replace('.shp','bf.shp')
	arcpy.CopyFeatures_management(old_grid_file, grid_file)
	df_grid = dbf2DF(grid_file.replace('.shp','.dbf'))

	#Load dataframe based on intersection of st_grid and ED map (attaches EDs to segments)
	st_grid_ed_shp = geo_path + city_name + state_abbr + '_1930_stgrid_ED_intersect.shp'
	df_grid_ed = dbf2DF(st_grid_ed_shp)
	df_grid_ed = df_grid_ed[['grid_id',grid_street_var,'CITY','STATE','ed']+hn_ranges]

	#Build {st_ed:[grid_ids]} dictionary based on street grid
	st_ed_grid_id_dict  = {}
	df_st_ed_grouped = df_grid_ed.groupby([grid_street_var,'ed'])
	for st_ed, grid_ids in df_st_ed_grouped:
		st_ed_grid_id_dict[st_ed] = grid_ids['grid_id'].tolist()

	#Build {st_ed:[hn_min,hn_max]} dictionary based on microdata
	if df_micro is None:
		microdata_file = dir_path + "/StataFiles_Other/1930/" + city_name + state_abbr + "_StudAuto.dta"
		df_micro = load_large_dta(microdata_file)
	if 'st_best_guess' in df_micro.columns.values:
		micro_street_var = 'st_best_guess'
	else:
		micro_street_var = 'overall_match'
	st_ed_hnrange_dict = {}
	for st_ed, group in df_micro.groupby([micro_street_var,'ed']):
		st, ed = st_ed
		if st != '.':
			hn_list = group['hn'].dropna().tolist() 
			outlier_dict = get_cray_z_scores(hn_list)
			if outlier_dict != None:
				hn_list_no_out = [i for i in hn_list if not outlier_dict[i]]
			try:
				st_ed_hnrange_dict[st_ed] = {'hn_min':min(hn_list_no_out), 'hn_max':max(hn_list_no_out)}
			except:
				st_ed_hnrange_dict[st_ed] = {'hn_min':'', 'hn_max':''}

	# Get {st:[grid_ids]} dictionary 
	print("Starting to find consecutive segments")
	name_sequence_dict, exact_next_dict = find_consecutive_segments(grid_file, grid_street_var)
	exact_previous_dict = {v:k for k,v in exact_next_dict.items()}

	#
	# Use microdata to get ED-based house number ranges and fill in missing st_grid ranges
	#

	def get_num_blanks(mi_l, ma_l, mi_r, ma_r):
		if mi_l==ma_l==mi_r==ma_r=='':
			return True
		else:
			return False

	num_blanks = df_grid.apply(lambda x: get_num_blanks(x[min_l],x[max_l],x[min_r],x[max_r]),axis=1).sum()

	def apply_ed_hn_ranges(df_grid, hn_ranges):	

		#
		# Get ED range fixes
		#

		# Function figures out whether first/last segment in ED is blank, then fills it in 
		def fix_min_max(df, st_ed_hn_min_max):
			grid_id_hn_change_list = []
			# Get hn_min and hn_min from microdata
			st_ed_hn_min = int(st_ed_hn_min_max['hn_min'])
			st_ed_hn_max = int(st_ed_hn_min_max['hn_max'])
			# Determine which side is even versus odd
			#print(df[[min_l,max_l]])
			even_l = np.mod([int(i) for i in df[[min_l,max_l]].values.flatten() if i != ''],2).mean() < 0.5
			even_min = np.mod(st_ed_hn_min,2) == 0
			even_max = np.mod(st_ed_hn_max,2) == 0
			# Get the first segment
			order_first = df['order'].min()
			first = df[df['order']==order_first]
			# Get the last segment		
			order_list = df['order'].max()
			last = df[df['order']==order_list]
			# If either first or last segment has missing, just replace 
			if first[hn_ranges].isin(['']).all().all() and st_ed_hn_min != '':
				if even_l == even_min:
					new_ranges_min = {min_l:st_ed_hn_min, max_l:st_ed_hn_min+2, min_r:st_ed_hn_min+1, max_r:st_ed_hn_min+3}
				else:
					new_ranges_min = {min_l:st_ed_hn_min+1, max_l:st_ed_hn_min+3, min_r:st_ed_hn_min, max_r:st_ed_hn_min+2}
				grid_id_hn_change_list.append({(first['grid_id'].values[0],'min'):new_ranges_min})
			if last[hn_ranges].isin(['']).all().all() and st_ed_hn_max != '':
				if even_l == even_max:
					new_ranges_max = {min_l:st_ed_hn_max, max_l:st_ed_hn_max-2, min_r:st_ed_hn_max-1, max_r:st_ed_hn_max-3}
				else:
					new_ranges_max = {min_l:st_ed_hn_max, max_l:st_ed_hn_max-2, min_r:st_ed_hn_max-1, max_r:st_ed_hn_max-3}
				grid_id_hn_change_list.append({(last['grid_id'].values[0],'max'):new_ranges_max})
			else:
				try:
					first_min_l = first[min_l].astype(int).get_values()[0] 
					first_min_r = first[min_r].astype(int).get_values()[0] 
					last_max_l = first[max_l].astype(int).get_values()[0] 
					last_max_r = first[max_r].astype(int).get_values()[0] 
				except:
					pass
			#if grid_id_hn_change_dict != {}: print(grid_id_hn_change_dict)
			return grid_id_hn_change_list

		# Assuming a whole bunch of conditions are met, use ED hn ranges to get potential ranges for blanks
		list_of_changes = []
		for st_ed, group in df_st_ed_grouped:
			st,ed = st_ed
			try:
				st_grid_ids_list = name_sequence_dict[st]
			except:
				#print("Street not found in name_sequence_dict")
				continue
			# Get list of grid_ids in st_ed from {st_ed:[grid_ids]} dictionary
			st_ed_grid_ids = st_ed_grid_id_dict[st_ed]
			if (len(st_ed_grid_ids)) > 1 and (type(st_grid_ids_list[0]) != list) and (len(st_grid_ids_list) > 1):
				# Create {grid_id:order} dictionary for st seq
				st_grid_ids_order_dict = {st_grid_ids_list[i]:i for i in range(len(st_grid_ids_list))}
				# Use list of grid_ids in st_ed to make a smaller {grid_id:order} specific to st_ed
				st_ed_grid_ids_order_dict = {k:v for k,v in st_grid_ids_order_dict.items() if k in st_ed_grid_ids}
				# Ensure that all the grid_is in the st_ed have an order (can be mismatch)
				if len(st_ed_grid_ids_order_dict)==len(st_ed_grid_ids):
					# Get df_grid data for st_ed
					df_grid_st_ed = df_grid.loc[df_grid['grid_id'].isin(st_ed_grid_ids)]
					if len(df_grid_st_ed) > 1:
						# Attach order of grid_ids and sort
						df_grid_st_ed.loc[:,'order'] = df_grid_st_ed.apply(lambda x: st_grid_ids_order_dict[x['grid_id']], axis=1)
						df_grid_st_ed = df_grid_st_ed.sort_values(by='order')
						# Assign hn_min and and hn_max for st_ed according to microdata (if called for)
						try:
							st_ed_hn_min_max = st_ed_hnrange_dict[st_ed]
							# Build up dict
							list_of_changes.append(fix_min_max(df_grid_st_ed, st_ed_hn_min_max))
						except:
							#print("Error fixing min/max")
							pass
		list_of_changes_backup = list_of_changes
		list_of_changes = [i for i in list_of_changes if i != []]
		list_of_changes = [i for s in list_of_changes for i in s]

		# NOTE: We first assume NO actual range in house numbers (ust min+2, max-2, etc.)
		
		#
		# Get unique grid_id changes
		#

		# Some grid_ids have multiple entries, so need to handle that case
		# and, in the process, we can often get some actual ranges on a segment

		def unique_grid_id_changes(list_changes):
			if len(list_changes)==1:
				unique_changes = list_changes[0]
			else:
				unique_changes = {}
				hn_ranges = list_changes[0].keys()
				for hn_range in hn_ranges:
					options = []
					for change in list_changes:
						options.append(change[hn_range])
					if 'MIN' in hn_range:
						unique_changes[hn_range] = min(options)
					if 'MAX' in hn_range:
						unique_changes[hn_range] = max(options)
			return unique_changes 

		# Get list of grid_ids whose hn ranges will change (takes two steps)
		list_of_changes_keys = [i.keys() for i in list_of_changes]
		list_of_grid_ids_to_change = [i.keys()[0][0] for i in list_of_changes]
		# Get list of changes for each grid_id (can have multiple for same grid_id)
		grid_id_changes_dict = {i:[s.values()[0] for s in list_of_changes if s.keys()[0][0] == i] for i in list_of_grid_ids_to_change}
		grid_id_changes_unique_dict = {k:unique_grid_id_changes(v) for k,v in grid_id_changes_dict.items()}

		#
		# Check for range overlap with adjacent segments (NOT WORKING)
		#

		# NOT FINISHED
		def check_for_overlap(grid_id, changes, hn_ranges):
			min_l, max_l, min_r, max_r = hn_ranges
			try:
				next_id = exact_next_dict[grid_id]
				next_ranges = df.iloc[df['grid_id']==next_id,hn_ranges].to_dict(orient='records')[0]
				is_next = True
			except:
				is_next = False
			try:
				previous_id = exact_previous_dict[grid_id]
				previous_ranges = df.iloc[df['grid_id']==previous_id,hn_ranges].to_dict(orient='records')[0]
				is_previous = True
			except:
				is_previous = False
			current_hn = changes
			# If previous and next both exist
			if is_next and is_previous:
				if previous_hn[max_l] < current_hn[min_l] < current_hn[max_l] < next_hn[min_l]:
					fix_min_l = previous_hn[max_l]+2
					fix_max_l = next_hn[min_l]-2
				if previous_hn[max_r] < current_hn[min_r] < current_hn[max_r] < next_hn[min_r]:
					fix_min_r = previous_hn[max_r]+2
					fix_max_r = next_hn[min_r]-2					
				if (current_hn[min_l] > previous_hn[max_l]) & (next_hn[max_l]-previous_hn[max_l]>2):
					fix_min_l = previous_hn[max_l]+2

				new_changes

			# If only previous exists
			if is_previous and ~is_next:
				if previous_hn[max_l] < current_hn[min_l]:
					fix_min_l = previous_hn[max_l]+2
				if previous_hn[max_r] < current_hn[min_r]:
					fix_min_r = previous_hn[max_r]+2

				new_changes = [fix_min_l, current_hn[max_l], fix_min_r, current_hn[max_r]]

			# If only next exists
			if is_next and ~is_previous:
				if current_hn[max_l] < next_hn[min_l]:
					fix_max_l = next_hn[min_l]-2
				if current_hn[max_r] < next_hn[min_r]:
					fix_max_r = next_hn[min_r]-2

				new_changes = [current_hn[min_l], fix_max_l, current_hn[min_r], fix_max_r]

			# If no previous or next
			if ~is_next and ~is_previous:
				new_changes = [current_hn[min_l], current_hn[max_l], current_hn[min_r], current_hn[max_r]]

			return new_changes

		#for grid_id, changes in grid_id_changes_dict.items():
		#	grid_id_changes_dict[grid_id] = check_for_overlap(grid_id, changes, hn_ranges)

		#	
		# Change hn ranges
		#

		def change_hns_ed_ranges(grid_id, mi_l, ma_l, mi_r, ma_r):
			try:
				temp = grid_id_changes_unique_dict[grid_id]
				new_ranges = [temp[min_l], temp[max_l], temp[min_r], temp[max_r]]
				#print(grid_id, new_ranges)
				return pd.Series(new_ranges + [True])
			except:
				old_ranges = [mi_l, ma_l, mi_r, ma_r]
				return pd.Series(old_ranges + [False])

		df_grid_ed_hn = df_grid	
		df_grid_ed_hn[hn_ranges+['hn_change']] = df_grid_ed_hn.apply(lambda x: change_hns_ed_ranges(x['grid_id'],x[min_l],x[max_l],x[min_r],x[max_r]), axis=1)

		blanks_fixed_ed_hn = df_grid_ed_hn['hn_change'].sum()
		per_blanks_fixed = '{:.1%}'.format(float(blanks_fixed_ed_hn)/num_blanks)
		print("Blanks fixed: " + str(blanks_fixed_ed_hn) + " of " + str(num_blanks) + " (" + per_blanks_fixed + ")")

		actual_ranges = len([k for k,v in grid_id_changes_dict.items() if len(v)>1])
		print("Blanks fixed with non-trivial ranges: " + str(actual_ranges))

		return df_grid, blanks_fixed_ed_hn

	df_grid_ed_hn, blanks_fixed_ed_hn = apply_ed_hn_ranges(df_grid, hn_ranges)

	#
	# Take care of flips and any zeroes leftover 
	#

	# Flip ranges when min > max
	def flip_ranges(hn_ranges):

		min_l, max_l, min_r, max_r = hn_ranges

		# Check for type (catches blanks)
		min_l_str = (type(min_l)==str) | (type(min_l)==unicode)
		max_l_str = (type(max_l)==str) | (type(max_l)==unicode)
		min_r_str = (type(min_r)==str) | (type(min_r)==unicode)
		max_r_str = (type(max_r)==str) | (type(max_r)==unicode)

		# Set default "true" range
		true_min_l = min_l
		true_max_l = max_l
		true_min_r = min_r
		true_max_r = max_r

		# Check if both have blank(s)
		if min_l_str | max_l_str | min_r_str | max_r_str:
			seg_status['Both have blank(s)'] += 1
			return [true_min_l, true_max_l, true_min_r, true_max_r]

		# Check if left has blank(s)
		if (min_l_str | max_l_str) & (~min_r_str & ~max_r_str):
			if min_r < max_r:
				seg_status['Right flipped, left has blank(s)'] += 1
				true_min_r = max_r
				true_max_r = min_r	
				return [true_min_l, true_max_l, true_min_r, true_max_r]
			else:
				seg_status['No flips, left has blank(s)'] += 1
				return [true_min_l, true_max_l, true_min_r, true_max_r]

		# Check if right has blank(s)
		if (min_r_str | max_r_str) & (~min_l_str & ~max_l_str):
			if min_l < max_l:
				seg_status['Left flipped, right has blank(s)'] += 1
				true_min_l = max_l
				true_max_l = min_l	
				return [true_min_l, true_max_l, true_min_r, true_max_r]
			else:
				seg_status['No flips, right has blank(s)'] += 1
				return [true_min_l, true_max_l, true_min_r, true_max_r]

		# At this point, blanks have been filtered out
		else:
			if min_l < max_l & min_r < max_r:
				seg_status['No flips'] += 1
				return [true_min_l, true_max_l, true_min_r, true_max_r]
			if min_l > max_l & min_r < max_r:
				seg_status['Left flipped'] += 1
				true_min_l = max_l
				true_max_l = min_l
				return [true_min_l, true_max_l, true_min_r, true_max_r]
			if min_r > max_r & min_l < max_l:
				seg_status['Right flipped'] += 1
				true_min_r = max_r
				true_max_r = min_r
				return [true_min_l, true_max_l, true_min_r, true_max_r]
			if min_l > max_l & min_r > max_r:
				seg_status['Both flipped'] += 1
				true_min_l = max_r
				true_max_l = min_r
				true_min_r = max_l
				true_max_r = min_l
				return [true_min_l, true_max_l, true_min_r, true_max_r]

	# Blanks out house numbers that are 0 and flips ranges 
	def preclean_ranges(df, hn_ranges):
		# Blank out zero house numbers
		for hn_range in hn_ranges:
			try:
				df.loc[df[hn_range]=='0',hn_range] = ''
			except:
				df.loc[df[hn_range]==0,hn_range] = ''
		# Fix flips
		#df[hn_ranges] = df[hn_ranges].apply(lambda x: flip_ranges(x),axis=1)
		# Report flips/blanks stats
		#print(pd.DataFrame(seg_status.items(), columns=['Status','Count']))
		return df

	# Keep track of flipping and blanks
	seg_status = {}
	seg_status['Both have blank(s)'] = 0
	seg_status['No flips, left has blank(s)'] = 0
	seg_status['No flips, right has blank(s)'] = 0
	seg_status['Right flipped, left has blank(s)'] = 0
	seg_status['Left flipped, right has blank(s)'] = 0
	seg_status['Left flipped'] = 0
	seg_status['Right flipped'] = 0
	seg_status['Both flipped'] = 0
	seg_status['No flips'] = 0
	
	df_grid_ed_hn_pc = preclean_ranges(df_grid_ed_hn, hn_ranges)

	#
	# Fix blanks for real
	#

	# Use precleaned grid data where ED ranges have been used to fill in blanks already
	df = df_grid_ed_hn_pc

	# Group by street name
	df_grouped = df.groupby([grid_street_var])

	#for name, seq in name_sequence_dict.items():
	#	df_temp = df_grid_ed_hn_pc.loc[df['grid_id'].isin(seq)]

	# Build dictionary for fixing blanks by looping through streets
	fix_blanks_dict = {}
	blanks_dict = {}
	blanks_fixable_total = 0
	blanks_fixed_total = 0
	for name in df[grid_street_var].drop_duplicates().tolist():
		# Get list of grid_id for each street name
		try:
			grid_id_list = name_sequence_dict[name]
		except:
			continue
		# Create a dictionary based on the sequence of segments
		try:
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
		except:
			continue
	fix_blanks_dict = {k:v for k,v in fix_blanks_dict.items() if v != {}}
	blanks_dict = {k:v for k,v in blanks_dict.items() if v != dict(zip(hn_ranges,[[],[],[],[]]))}

	# Number of blank block faces (missing either hn)
	df_r = df[((df[min_r]=='') | (df[max_r]==''))]
	df_l = df[((df[min_l]=='') | (df[max_l]==''))]
	blank_block_faces = len(df_r) + len(df_l)
	per_blanks_total = float(blank_block_faces)/(2*len(df))
	print("Total blank block faces: "+str(blank_block_faces)+" (" + '{:.1%}'.format(per_blanks_total) + " of " + str(2*len(df)) + " block faces)")

	per_blanks_fixable = float(blanks_fixable_total)/blank_block_faces
	per_blanks_fixed = float(blanks_fixed_total)/blanks_fixable_total

	print("Fixable blanks: " + str(blanks_fixable_total) + " (" + '{:.1%}'.format(per_blanks_fixable) + " of " + str(blank_block_faces) + " blank block faces)")
	print("Fixed blanks: " + str(blanks_fixed_total) + " (" + '{:.1%}'.format(per_blanks_fixed) + " of fixable blanks)")

	# Blank streets
	blank_streets = {}
	for name, group in df_grouped:
		unique_hns = []
		for hn_range in hn_ranges:
			unique_hns.append(group[hn_range].drop_duplicates().tolist())
			if unique_hns == [[''],[''],[''],['']]:
				blank_streets[name] = len(group)
	per_blanks_unfixable = float(2*sum(blank_streets.values()))/(blank_block_faces-blanks_fixable_total)
	per_blanks_st = float(2*sum(blank_streets.values()))/blank_block_faces

	print("There are "+str(len(blank_streets))+" streets with no house number ranges ("+str(2*sum(blank_streets.values()))+ " blank block faces total), representing "+ '{:.1%}'.format(per_blanks_unfixable) +" of unfixable blank block faces and "+'{:.1%}'.format(per_blanks_st)+" of total blank block faces")

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

	save_dbf(df, grid_file)

#### Not used

''' (only produces a few streets)
	def check_for_extra_zero(hn_list):
		new_hn_list = []
		change_dict = {}
		for hn in hn_list:
			if hn/10 in hn_list:
				list_without_hn = [i for i in hn_list if i != hn]
				avg_diff = np.mean([hn-i for i in list_without_hn])
				if avg_diff > 500:
					change_dict[st, ed] = {hn:hn/10}
		return change_dict

	hn_change_dict = {}
	for st_ed, group in df_micro.groupby([micro_street_var,'ed']):
		st, ed = st_ed
		micro_hns = group['hn'].tolist()
		hn_change_dict.update(check_for_extra_zero(micro_hns))
'''