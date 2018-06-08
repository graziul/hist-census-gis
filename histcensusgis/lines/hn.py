#
# Name: hn.py 
#
# Contents: Functions primarily associated with house numbers
#

from histcensusgis.s4utils.AmoryUtils import *
from histcensusgis.s4utils.IOutils import *
from histcensusgis.text.standardize import *
from operator import itemgetter
from itertools import groupby
import os
import arcpy
arcpy.env.overwriteOutput=True

# Amory's code for fixing duplicate address ranges
def fix_dup_address_ranges(shp, hn_ranges, debug_flag=False):
	# Set range names
	LFROMADD, LTOADD, RFROMADD, RTOADD = hn_ranges
	# Set OBJECTID (grid_id is FID+1)
	OBJECTID = "grid_id" 
	# Calculate starting and ending coordinates and length for each line segment
	arcpy.AddGeometryAttributes_management(shp, "LENGTH_GEODESIC;LINE_START_MID_END")

	data = []

	fields = arcpy.ListFields(shp)
	field_names = [field.name for field in fields]

	for row in arcpy.SearchCursor(shp):
		data.append([row.getValue(field.name) for field in fields])

	df = pd.DataFrame(data, columns=field_names)

	grouped = df.groupby(["FULLNAME",LFROMADD,LTOADD,RFROMADD,RTOADD])
	
	df["IN_FID"] = grouped.grouper.group_info[0]

	#There is no simple way to assign _n of each group to a variable in the dataframe
	# so use Chris Graziul's dict workaround.
	foo = {}
	#create dict: keys: group IDs ; values: number of items in group
	for g, d in grouped:
		foo[g] = d[OBJECTID].count()
	df['size'] = df.apply(lambda x : foo[x["FULLNAME"],x[LFROMADD],x[LTOADD],x[RFROMADD],x[RTOADD]], axis=1)

	df = df[[OBJECTID,LFROMADD,LTOADD,RFROMADD,RTOADD,"IN_FID","LENGTH_GEO","size","START_X","END_X","START_Y","END_Y"]]

	addresses = open('new_addresses.csv', 'wt') #this is deprecated, although topo errors are still output here.
	addresses.write("fid,l_f_add,l_t_add,r_f_add,r_t_add,short_segment\n")

	df = df.sort_values('IN_FID')

	for col in df:
		df[col] = df[col].astype(str)
	DList = df.values.tolist()

	TopoErrors = []

	ind = 0

	#master list for corrected data
	Data = []

	#input data should be in format :
	#fid;l_f_add;l_t_add;r_f_add;r_t_add;in_fid;new_length;num_identical;start_x;end_x;start_y;end_y

	appInd = 0

	while ind < len(DList):
		if(appInd != ind):
			print("len of Data: %sind: %s" % (appInd,ind))
		feat_seq = DList[ind][5] # actually in_fid, as feat_seq was unreliable.
		feat_num = int(DList[ind][7]) # number of features
		feat_list = DList[ind : ind+feat_num] #list of features that comprised the original feature
		if feat_num > 1:
			##find beginning segment##
			start_segment = False
			i=0
			topology_error = False
			while start_segment == False and i<feat_num:
				start_segment = True
				start = (DList[ind+i][8]+" "+DList[ind+i][10]).strip()
				for feat in feat_list:
					end = (feat[9]+" "+feat[11]).strip()
					if end == start:
						start_segment = False
						i= i +1
						#print "found a connexion. i is now %d",i
						break
			if start_segment==False : #could not find a start segment
				#print "PANIC"
				#probably topology or parsing error; or we are dealing with a circular street segment
				#pretend that the first segment in the input order is the start segment
				i=0
			##put feat list in order of street direction##
			o_feat_list = []
			o_feat_list.append(DList[ind+i])
			order_num = 1
			end = (o_feat_list[0][9]+" "+o_feat_list[0][11]).strip()
			feat_length = float(o_feat_list[0][6])
			while order_num < feat_num:
				for j,feat in enumerate(feat_list):
					start = (feat[8]+" "+feat[10]).strip()
					if start == end:
						end = (feat[9]+" "+feat[11]).strip()
						order_num= order_num + 1
						feat_length = feat_length + float(feat[6])
						o_feat_list.append(feat)
						break
					if j==feat_num-1:
	#					print ("topological error (there is a gap)~~~~~~~~~~~~~~!!!!!!!!!!!!!!~~~~~~~~~~~~~~")
						TopoErrors.append(DList[ind+order_num])
						topology_error = True
						order_num= order_num + 1
			if topology_error==False:
				try:
					LFAdd = int(o_feat_list[0][1])
				except ValueError:
					LFAdd = 0
				try:
					LTAdd = int(o_feat_list[0][2])
				except ValueError:
					LTAdd = 0
				try:
					RFAdd = int(o_feat_list[0][3])
				except ValueError:
					RFAdd = 0
				try:
					RTAdd = int(o_feat_list[0][4])
				except ValueError:
					RTAdd = 0
				if debug_flag:
					addresses.write("feat_seq: "+str(feat_seq)+", name: "+o_feat_list[0][5]+", num segments: "+str(feat_num)+", add range: "+str(LFAdd)+"-"+str(LTAdd)+" "+str(RFAdd)+"-"+str(RTAdd)+"\n")

				RRange = (RTAdd - RFAdd)
				LRange = (LTAdd - LFAdd)
				ORange = RRange
				OLange = LRange
				RDir, LDir = 0,0 #Dir: direction addresses are going in.

				final_feat_list = []
				for feat in o_feat_list:
					if round(abs((float(feat[6])/feat_length)*LRange)) < 2 and LRange!= 0 and round(abs((float(feat[6])/feat_length)*RRange)) < 2 and RRange!= 0:
						#if feat is too short to contain even a single address (on either side) in its range...
						feat[1]=feat[2]=feat[3]=feat[4]=0
						feat_num = feat_num - 1
						feat_length = feat_length - float(feat[6])
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+",1")
						if debug_flag:
							addresses.write(" length is "+feat[6]+"/"+str(feat_length)+" which WAS too short\n")
						else:
							addresses.write("\n")
					else:
						final_feat_list.append(feat)

				o_feat_list = final_feat_list

				ShortRange = False
				if RRange!=0:
					RDir = RRange/abs(RRange)
				if LRange!=0:
					LDir = LRange/abs(LRange)
				if abs(RRange)>2*feat_num : #if address range is NOT too small in comparison to number of segments
					RRange -= 2*(feat_num-1)*RDir #account for the hidden extra 2 address range each time we change segments
				else:
					ShortRange = True
					if debug_flag:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				if abs(LRange)>2*feat_num:
					LRange -= 2*(feat_num-1)*LDir
				else:
					ShortRange = True
					if debug_flag:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				assignedLength = 0

				for j, feat in enumerate(o_feat_list):
					segmentLength = float(feat[6])
					assignedLength+=segmentLength
					tooShort = False
					if debug_flag:
						addresses.write(str(int(round(((segmentLength/feat_length)*LRange)/2)*2))+" is more than 2. RRange is "+str(RRange)+"\n")
					if j == 0:
						feat[1] = LFAdd
						feat[3] = RFAdd
					else:
						feat[1] = int(o_feat_list[j-1][2])+2*LDir
						feat[3] = int(o_feat_list[j-1][4])+2*RDir
	#				print "left range",round(((segmentLength/feat_length)*LRange)/2)*2
					if j == feat_num-1:
						feat[2] = LTAdd
						feat[4] = RTAdd
					else:
						feat[2] = feat[1] + int(round(((segmentLength/feat_length)*LRange)/2)*2)
						feat[4] = feat[3] + int(round(((segmentLength/feat_length)*RRange)/2)*2)
						if feat[2] > LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2) and LDir>0 or LDir<0 and feat[2] < LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2):
							feat[2] = LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2)
							if debug_flag:
								addresses.write("HAD TO ADJUST on LEFT\n")
						if feat[4] > RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2) and RDir>0 or RDir<0 and feat[4] < RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2):
							if debug_flag:
								addresses.write("HAD TO ADJUST on RIGHT\n")
							feat[4] = RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2)
					if RRange == 0:
						feat[3] = feat[4] = RFAdd
					if LRange == 0:
						feat[1] = feat[2] = LFAdd

					if debug_flag:
						if LDir > 0 and (feat[1] > LTAdd or feat[2] > LTAdd) or LDir < 0 and (feat[1] < LTAdd or feat[2] < LTAdd) or RDir > 0 and (feat[3] > RTAdd or feat[4] > RTAdd) or RDir < 0 and (feat[3] < RTAdd or feat[4] < RTAdd):
							addresses.write("THIS SHOULD NOT HAPPEN!\n")
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+" length is "+feat[6]+"/"+str(feat_length)+" which was NOT too short\n")
					else:
						#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
						Data.append(feat)
						appInd =appInd+1

			else : #if topo error
				for feat in feat_list:
					Data.append(feat) #add just the fid of all segments to Data if topo error
					appInd =appInd+1

		else : #if feature was not split
			feat = DList[ind]
			#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
			Data.append(feat)
			appInd =appInd+1

		ind+=feat_num

	Data.sort(key=itemgetter(0)) #sort both by OBJECTID (both are text so the sorting is weird but consistently so!)
	newShp = os.path.splitext(shp)[0]+"2.shp"
	#have to create a new FID field because Arc won't let you sort on fields of type Object ID
	arcpy.AddField_management(in_table = shp, field_name="FID_str", field_type="TEXT", field_precision="", field_scale="", field_length="", field_alias="",
		field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
	arcpy.CalculateField_management(in_table = shp, field="FID_str", expression="!"+OBJECTID+"!", expression_type="PYTHON_9.3", code_block="")
	arcpy.Sort_management(shp, newShp, [["FID_str", "ASCENDING"]])

	with arcpy.da.UpdateCursor(newShp,[LFROMADD,LTOADD,RFROMADD,RTOADD]) as cursor:
		for i,row in enumerate(cursor):
			if Data[i][1] == 0:
				row[0] = ''
			else:
				row[0] = Data[i][1]
			if Data[i][2] == 0:
				row[1] = ''
			else:
				row[1] = Data[i][2]
			if Data[i][3] == 0:
				row[2] = ''
			else:
				row[2] = Data[i][3]
			if Data[i][4] == 0:
				row [3] = ''
			else:
				row[3] = Data[i][4]
			cursor.updateRow(row)
	addresses.write("Topology Errors. Must be fixed and re-run script or re-address manually.\n")

	for err in TopoErrors:
		addresses.write(str(err[0])+"\n")
	addresses.close()

	return "\nFixed duplicate address ranges"

# Adds new streets and ranges based on Steve Morse webpage that may or may not exist (R script)
def add_ranges_to_new_grid(city_name, state_abbr, file_name, paths):
	r_path, script_path, file_path = paths
	print("Adding ranges to new grid\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'/blocknum/R/Add Ranges to New Grid.R',file_path,city_name,file_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error adding ranges to new grid for "+city_name+"\n")
	else:
		print("OK!\n")

# Renumber grid using microdata
def renumber_grid(city_name, state_abbr, paths, decade, df=None, geocode=False):

	#Paths
	_, _, dir_path = paths
	geo_path = dir_path + "/GIS_edited/"

	#Files
	microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city_name + state_abbr + "_StudAutoDirBlockFixed.dta"
	stgrid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	out_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_renumbered.shp"
	block_shp_file = geo_path + city_name + "_" + str(decade) + "_block_ED_checked.shp"
	addresses = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	points = geo_path + city_name + "_" + str(decade) + "_Points_updated.shp"
	pblk_file = block_shp_file #Note: This is the manually edited block file
	pblk_grid_file = geo_path + city_name + state_abbr + "_" + str(decade) + "_Pblk_Grid_SJ2.shp"
	add_locator = geo_path + city_name + "_addlocOld" 

	# Load
	df_grid = load_shp(stgrid_file)
	df_block = load_shp(block_shp_file)
	if df is None:
		df_micro = load_large_dta(microdata_file)
	else:
		df_micro = df

	if 'st_best_guess' in df_micro.columns.values:
		micro_street_var = 'st_best_guess'
	else:
		micro_street_var = 'overall_match'
	try:
		block = 'block'
		vars_of_interest = ['ed','hn',micro_street_var,block]
		df_micro = df_micro[vars_of_interest]
	except:
		block = 'block_old'
		vars_of_interest = ['ed','hn',micro_street_var,block]
		df_micro = df_micro[vars_of_interest]
	df_micro = df_micro.dropna(how='any')
	df_micro['hn'] = df_micro['hn'].astype(int)

	#Create ED-block variable (standardized against block map)
	#Turn ED=0 into blank 
	df_micro['ed1'] = df_micro['ed'].astype(str).replace('0','')

	df_micro['block1'] = df_micro[block].str.replace(' ','-')
	df_micro['block1'] = df_micro['block1'].str.replace('and','-')
	df_micro['block1'] = df_micro['block1'].str.replace('.','-')
	df_micro['block1'] = df_micro['block1'].replace('-+','-',regex=True)

	df_micro['edblock'] = df_micro['ed1'] + '-' + df_micro['block1']
	df_micro['edblock'] = df_micro['edblock'].replace('^-|-$','',regex=True)
	df_micro.loc[df_micro[block]=='','edblock'] = ''
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
	df_micro_byblkst = df_micro.groupby(['edblock',micro_street_var])
	blkst_hn_dict = {}
	bad_blkst = []
	for group, group_data in df_micro_byblkst:
		try:
			cray_dict = get_cray_z_scores(group_data['hn'])
			hn_range = [k for k,v in cray_dict.items() if not v]
			blkst_hn_dict[group] = {'min_hn':min(hn_range), 'max_hn':max(hn_range)}
		except:
			bad_blkst.append(group)

	# Get dictionaries {pblk_id:edblock} and {pblk_id:ed} 
	bn_var = 'am_bn'
	temp = df_block.loc[df_block[bn_var]!='',[bn_var,'ed','pblk_id']]
	pblk_edblock_dict = temp.set_index('pblk_id')[bn_var].to_dict()
	pblk_ed_dict = temp.set_index('pblk_id')['ed'].to_dict()

	# Intersect block map and stgrid (needs to be manual block map because dissolved pblks)
	field_mapSJ = """pblk_id "pblk_id" true true false 10 Long 0 10 ,First,#,%s,pblk_id,-1,-1;
	ed "ed" true true false 10 Long 0 10 ,First,#,%s,ed,-1,-1;
	FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
	grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (block_shp_file, block_shp_file, stgrid_file, stgrid_file)
	arcpy.Intersect_analysis (in_features=[block_shp_file, stgrid_file], 
		out_feature_class=pblk_grid_file, 
		join_attributes="ALL")
	# Used spatial join before, but results in fewer cases (some streets not on block boundaries?)
	#arcpy.SpatialJoin_analysis(target_features=block_shp_file, join_features=stgrid_file, out_feature_class=pblk_grid_file, 
	#	join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", field_mapping=field_mapSJ, 
	#	match_option="SHARE_A_LINE_SEGMENT_WITH", search_radius="", distance_field_name="")
	df_pblk_grid = load_shp(pblk_grid_file)

	# Create dictionary linking grid_id to pblk_id
	grid_pblk_dict = {}
	grouped_grid = df_pblk_grid.groupby(['grid_id'])
	for grid_id, pblk_df in grouped_grid:
		grid_pblk_dict[grid_id] = pblk_df['pblk_id'].tolist()

	# Create dictionary linking grid_id to fullname
	# OLd WORKING: grid_fullname_dict = df_pblk_grid.set_index('grid_id').to_dict()['FULLNAME']
	grid_fullname_dict = df_grid.set_index('grid_id').to_dict()['FULLNAME']

	# Create dictionary linking grid_id to list of edblocks it intersects
	grid_edblock_dict = {grid_id:[pblk_edblock_dict[int(pblk_id)] for pblk_id in pblk_id_list] for grid_id, pblk_id_list in grid_pblk_dict.items()}

	# Create dictionary linking grid_id to min/max HN and ED
	grid_hn_dict = {}
	for grid_id, edblock_list in grid_edblock_dict.items():
		try:
			min_hn = max([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['min_hn'] for i in edblock_list])
			max_hn = min([blkst_hn_dict[i,grid_fullname_dict[grid_id]]['max_hn'] for i in edblock_list])
			eds = [i.split("-")[0] for i in edblock_list] 
			grid_hn_dict[grid_id] = {'min_hn':min_hn, 'max_hn':max_hn, 'ed':max(set(eds), key=eds.count)}
		except:
			pass

	#Create copy of st_grid to work on 
	arcpy.CopyFeatures_management(stgrid_file,out_file)

	#Add ED field
	arcpy.AddField_management(out_file, "ed", "TEXT", 5, "", "","", "", "")

	#Delete contemporary ranges and recreate HN range attributes
	arcpy.DeleteField_management(out_file, ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD'])
	arcpy.AddField_management(out_file, "MIN_LFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_LTOADD", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MIN_RFROMA", "TEXT", 5, "", "","", "", "")
	arcpy.AddField_management(out_file, "MAX_RTOADD", "TEXT", 5, "", "","", "", "")

	#Add HN ranges and ED based on grid_id
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

	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [geo_path+'/'+x for x in os.listdir(geo_path) if x.startswith(city_name+"_addlocOld.")]
	for f in add_loc_files:
		if os.path.isfile(f):
			os.remove(f)

	if geocode:

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
		'Altname JoinID' <None> VISIBLE NONE"
		address_fields= "Street address; City city; State state"
		arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", 
			in_reference_data=out_file, 
			in_field_map=field_map, 
			out_address_locator=add_locator, 
			config_keyword="")

		#Geocode Points
		arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points)

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

#def fill_blank_segs(city_name, state_abbr, paths, df_micro=None):

##
## Strategy: Produce renamed grids after filling blanks, use those to do geocoding, preserve orig
##
'''
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
'''

def fill_blank_segs(dir_path, city_name, state_abbr, hn_ranges, old_grid_file, grid_street_var):

	geo_path = dir_path + "/GIS_edited/"

	grid_file = old_grid_file.replace('.shp','bf.shp')
	arcpy.CopyFeatures_management(old_grid_file, grid_file)
	df_grid = load_shp(grid_file)

	#Load dataframe based on intersection of st_grid and ED map (attaches EDs to segments)
	st_grid_ed_shp = geo_path + city_name + state_abbr + '_1930_stgrid_ED_intersect.shp'
	df_grid_ed = load_shp(st_grid_ed_shp)
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

	save_shp(df, grid_file)

####
#### BELOW WAS COMMENTED OUT AT BOTTOM OF "HNclean.py"! 
####

#ST_SEQ = get_ST_SEQ()	
#print("missing TYPES: "+str(missingTypes))

### ERROR CHECKING LOOP: check swatches that do not match up ###
'''
hn_set = set(map(tuple,HN_SEQ))
INCONS_st = [x for x in map(tuple,ST_SEQ) if x not in hn_set] #st swatches that lack a corresponding HN swatch

st_set = set(map(tuple,ST_SEQ))
INCONS_hn = [x for x in map(tuple,HN_SEQ) if x not in st_set] #HN swatches that lack a corresponding st swatch

print("finished forming INCONS sets")

st_seq_starts = [row[0] for row in INCONS_st]
hn_seq_starts = [row[0] for row in INCONS_hn]
st_seq_ends = [row[1] for row in INCONS_st]
hn_seq_ends = [row[1] for row in INCONS_hn]
same_hh_chk
print("Finished making INCONS start and end lists")


CONS_starts = [x for x in st_seq_starts if x in hn_seq_starts]
CONS_ends = [x for x in st_seq_ends if x in hn_seq_ends]

print("Finished making CONS start and end lists")

CONS = list(zip(CONS_starts,CONS_ends))

print(INCONS_st[:10])
print(INCONS_hn[:10])
print(CONS[:10])

HANGOVERS = set()

#OVERLAP: ST and HN swatches intersect but do not contain each other exactly
OVERLAPS = [x for x in CONS if x not in INCONS_st and x not in INCONS_hn]
for o in OVERLAPS :
	debug = True
	st_swatches = INCONS_st[st_seq_starts.index(o[0]):st_seq_ends.index(o[1])+1]
	hn_swatches = INCONS_hn[hn_seq_starts.index(o[0]):hn_seq_ends.index(o[1])+1]
	if(True) : #len(st_swatches)==2 and len(hn_swatches)==2) :
		for s in st_swatches :
			for h in hn_swatches :
				#DO check that inconsistent observations are not mid-hh changes
				#Have to also identify hangovers where the start/end indices of the swatches do NOT EXACTLY line up
				#going along with this, eliminate the >1 obs restriction
				if(not(h[0]==h[1] or s[0]==s[1]) and (s[0]==h[1] or h[0]==s[1])) : #generalized hangover (FIX: only swatches longer than 1 household)
					if (debug) : print('Found a ', end="")
					if (s[0]==h[1]) : #hangover
						hang_ind = s[0]
						hang_dir = 1
					else : #reverse hangover
						hang_ind = h[0]
						hang_dir = -1
						if (debug) : print('reverse ', end="")
					if (debug) : print('hangover at %d, ' % hang_ind, end="")
					same_hh = same_hh_chk(hang_ind,hang_ind-hang_dir)
					if(same_hh[0]) :
						if (debug) : print('that passed same_hh_chk with all available vars, ', end="")
						
						#check to make sure abutting hn for (st that we are assuming is the correct stname) is not an outlier
						st_zscore = ed_hn_outlier_chk(get_ed(hang_ind-hang_dir),get_name(hang_ind-hang_dir),get_hn(hang_ind-hang_dir))
						if(st_zscore<4) :
							if(st_zscore==-1) :
								False
								#DO SOMETHING ABOUT THIS
							if (debug) : print('and was added to HANGOVERS.\n', end="")
							#All cases checked with these criteria were valid ready-to-be-fixed hangovers, except 86289
							test = HANGOVERS.copy()
							HANGOVERS.add(frozenset([hang_ind,hang_ind-hang_dir]))
							if(test == HANGOVERS) :
								print("OH DEAR, THE SAME HANGOVER WAS IDENTIFIED TWICE")
						else :
							if (debug) : print('but there was something suspicious about abutting hn: %s.\n' %st_zscore, end="")
					else :
						if (debug) : print('dwel: %s fam: %s rel: %s\n' %(same_hh[1],same_hh[2],same_hh[3]), end="")
						#if these are all false, we can still fix by seeing if there is another record with same
						#hn, dwel_id and fam_id as the hangover record. If there's nothing suspicious about the other
						#record, we can assume that one is the correct stname

						#Another Validation to think about: look at other HNs for the given st and Block
						#compare even-/odd-ness. Which decades do we have block ID for?
						
					#same hh chk works, but may be too restrictive?
					# for example, at line 18600 the dwelling is same but other two vars are different
					# and it is a valid hangover
					
					if(len(st_swatches)==2 and len(hn_swatches)==2) : #both guaranteed "otherwise well-defined" 
						print(str(o)+" "+str(hn_swatches[1][0]==st_swatches[0][1])+" "+str(hn_swatches[0][1]==st_swatches[1][0]))
					else :
						print(str(o)+" "+str(len(hn_swatches))+" "+str(len(st_swatches)))

##CONS = []
##ind = 0
##while ind<len(df) :
##    if 
print("Hangovers: "+str(len(HANGOVERS)))

errors = 0

#More useful outlier identification: outlying HH nums for a given st and ed
#e.g. St A in ED y has normal HN range 1000-2000. HN 5689 is flagged as outlier.
#This is then used as an additional piece of info when resolving Hangovers



for inc in INCONS_st[:0] :
	#find housenums that are outliers within a st-swatch (or otherwise normal housenum swatch - only one address diff)
	#compute standard deviation, median of housenums within st swatch
	#Standard Deviation should be calculated with respect to how much housenum deviates from previous num, as opposed
	# to how much it deviates from the distribution as a whole?
	
	#HOW WILL USING ALL HOUSENUMS AND NOT JUST 1 FOR EACH HOUSEHOLD AFFECT RESULTS?
	inc_nums = [row[2] for row in df[inc[0]:inc[1]+1]]
	print("inc nums: "+str(inc_nums))
	z = get_cray_z_scores(inc_nums)
	
		
		#if z_score > 4, consider an outlier?
	
last = INCONS_hn[0]
print("# of incons "+ str(len(INCONS_hn)))
for inc in INCONS_hn[:0] :
	if True : ### inc[0] - last[1] == 1 : #consecutive unmatched swatches: what kind of error defines these??
		print(str(last)+" & "+str(inc)+" : ")
		inc_STs = df[inc[0]:inc[1]+1]
		last_ST = inc_STs[0]
##        for st in inc_STs : #check if address is same but dwelling num different.
##            if st[2] == last_ST[2] and st[3] == last_ST[3] and not st[4] == last_ST[4] :
##                print("Found a probable wrong housenum, dwelling nums are: "+str(st[4])+" & "+str(last_ST[4]))
##            last_ST = st
		STs_freq = Counter([row[3] for row in inc_STs]).most_common()
		if len(STs_freq) == 2 :
			print(STs_freq)
			ratio = float(STs_freq[1][1])/float(STs_freq[0][1])
			if ratio <= .1 :
				errors = errors+1
				print("found a probable wrong stname, ratio: "+str(ratio))
	last = inc

print(errors)
'''
