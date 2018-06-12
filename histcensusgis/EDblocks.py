#
#	EDblocks.py
#
#	
#

from histcensusgis.microdata.misc import create_addresses
from histcensusgis.polygons.block import *
from histcensusgis.polygons.ed import *
from histcensusgis.lines.street import *
import arcpy
import getpass
import paramiko
arcpy.env.overwriteOutput = True

def get_paths(city_info, data_path="S:/Projects/1940Census/", r_path="C:/Program Files/R/R-3.4.2/bin/Rscript"):

	city_name, state_abbr, decade = city_info 
	city_spaces = city_name
	city_name = city_name.replace(' ','')

	city_state = city_name + state_abbr
	if city_state == "KansasCityKS":
		dir_path = data_path + "KansasCityKS"
	elif city_state == "KansasCityMO":
		dir_path = data_path + "KansasCityMO"
	elif city_state == "RichmondVA":
		dir_path = data_path + "RichmondVA"
	elif city_state == "RichmondNY":
		dir_path = data_path + "RichmondNY"
	else:
		dir_path = data_path + city_name #TO DO: Directories need to be city_name+state_abbr

	paths = [r_path, dir_path]

	return paths

def get_ed_map(city_info, paths, grid_street_var='FULLNAME', hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD']):

	city_name, state_abbr, decade = city_info
	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'
	
	# Step 0: Fix stgrid and get pblks (make this a check when iterative function working)
	get_pblks(city_info, paths)

	# Step 1: Run Amory's intersections-based algorithm
	ed_inter_algo(city_info, paths, grid_street_var)

	# Step 2: Run Matt's geocoding-based algorithm 
	ed_geocode_algo(city_info, paths)

	# Step 3: Run ED descriptions-based algorithm
	ed_desc_algo(city_info, paths, grid_street_var)	

	# Step 4: Combine algorithm results
	combine_ed_maps(city_info, geo_path, hn_ranges)
	print(get_ed_guess_stats(city_info, paths, hn_ranges))

	print("\nFinished ED map for %s %s, %s\n" % (str(decade), city_name, state_abbr))

def get_block_map(city_info, paths):

	city_name, state_abbr, decade = city_info
	r_path, dir_path = paths

	if decade != 1940:
		# Identify blocks using geocoding
		identify_blocks_geocode(city_info, paths)
		# Identify blocks using microdata alone (derived block descriptions)
		identify_blocks_microdata(city_info, paths)
		'''
		NOTE: These functions have worked in the past, but are not in use currently.
		# Add ranges to new grid 
		add_ranges_to_new_grid(city_name, state_abbr, file_name, paths)		
		# Run OCR script
		run_ocr(script_path, file_path, city_name)
		# Integrate OCR block numbering results
		integrate_ocr(city_name, file_name, paths)
		'''
		# Set confidence in block number guess [NEEDS TO BE GENERALIZED]
		set_blocknum_confidence(city_name, paths)
	
def get_ed_block_numbers(city_info, paths, grid_street_var="FULLNAME", hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD'], just_desc=False):

	_, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	get_pblks(city_info, paths)

	get_missing_streets(city_info, paths)

	get_ed_map(city_info, paths, grid_street_var, hn_ranges)

	fix_micro_dir_using_ed_map()
	
	fix_micro_blocks_using_ed_map()

	get_block_map(city_info, paths)

def do_geocode():

	get_ed_block_numbers()

	renumber_grid(city_name=city, 
		state_abbr=state, 
		paths=paths, 
		decade=decade,
		df=df_micro2)

	get_adjacent_eds(city_info=city_info,
		geo_path=geo_path)

	# Common variables

	# "vm" is the verified map (e.g., ED or block map)
	vm = geo_path + city + "_" + str(decade) + "_ED.shp"
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

	#
	# Geocode on 1930 house number ranges
	#

	# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
	add = geo_path + city + "_" + str(decade) + "_Addresses.csv"
	# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
	sg = geo_path + city + state + "_" + str(decade) + "_stgrid_renumberedbf.shp"
	# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
	al = geo_path + city + "_addloc_" + str(decade) + "_ED"
	# "gr" is the filename of the geocoding results
	gr = geo_path + city + state + "_" + str(decade) + "_geocode_renumberedEDbf.shp"
	# "sg_vm" is the filename of the intersection of the street grid and the verified map
	sg_vm = geo_path + city + state + "_grid_poly_intersect.shp"
	#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
	spatjoin = geo_path + city + state + "_" + str(decade) + "_geo_map_spatjoin.shp"
	# Not correct geocode
	notcor = geo_path + city + state + "_" + str(decade) + "_NotGeocodedCorrect.shp"
	# Correct geocode
	cor = geo_path + city + state + "_" + str(decade) + "_GeocodedCorrect.shp"
	# Ungeocoded addresses
	resid_add = geo_path + city + "_" + str(decade) + "_AddNotGeocoded.dbf"

	geocode(geo_path, city, add, sg, vm, sg_vm, fl, tl, fr, tr, cal_street, cal_city, cal_state, addfield, al, g_address, g_city, g_state, gr)

	validate(geo_path, city, state, gr, vm, spatjoin, notcor, cor, decade, residual_file=resid_add)

	#
	# Geocode on contemporary house number ranges
	#

	# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
	# "add" is resid_add from above
	# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
	sg = geo_path + city + state + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
	al = geo_path + city + "_addloc_" + str(decade) + "_ED_Contemp"
	# "gr" is the filename of the geocoding results
	gr = geo_path + city + state + "_" + str(decade) + "_geocode_renumberedED_Contemp.shp"
	# "sg_vm" is the filename of the intersection of the street grid and the verified map
	sg_vm = geo_path + city + state + "_grid_poly_intersect_Contemp.shp"
	#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
	spatjoin = geo_path + city + state + "_" + str(decade) + "_geo_map_spatjoin_Contemp.shp"
	# Not correct geocode
	notcor = geo_path + city + state + "_" + str(decade) + "_NotGeocodedCorrect_Contemp.shp"
	# Correct geocode
	cor = geo_path + city + state + "_" + str(decade) + "_GeocodedCorrect_Contemp.shp"
	# Ungeocoded addresses
	resid_add_contemp = geo_path + city + "_" + str(decade) + "_AddNotGeocoded_Contemp.dbf"

	geocode(geo_path, city, resid_add, sg, vm, sg_vm, fl, tl, fr, tr, cal_street, cal_city, cal_state, addfield, al, g_address, g_city, g_state, gr)

	validate(geo_path, city, state, gr, vm, spatjoin, notcor, cor, decade, residual_file=resid_add_contemp)

	#
	# Combine both geocodes to get the best geocode
	#

	combine_geocodes(geo_path, city, state, decade)


def run_cleaning_w_ed(city_info, paths, iterate=True, unix_path='/home/s4-data/LatestCities'):

	user = raw_input("Username:")
	passwd = getpass.getpass("Password for " + user + ":")

	# user = sys.argv[1]
	# pw = sys.argv[2]
	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	_, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	def upload_file(user, passwd, local_file_name, remote_file_name):
		# Connect to server via SSH
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys
		ssh.connect('pstc-cs1.pstc.brown.edu',username=user,password=passwd)
		sftp = ssh.open_sftp()
		# Make sure the target directory exists (or else create it)
		target_path = '/'.join(remote_file_name.split('/')[:-1])
		try:
			sftp.listdir(target_path)
		except IOError:
			sftp.mkdir(target_path)
		# Upload the file
		local_path = '/'.join(local_file_name.split('/')[:-1])
		if local_file_name.split('.')[-1] == 'shp':
			map_files = [x for x in os.listdir(local_path) if x.split('.')[0]==local_file_name.split('/')[-1].split('.')[0]]
			for item in map_files:
				remote_file_name = '%s/%s' % (target_path, item)
				local_file_name = '%s/%s' % (local_path, item)
				if os.path.isfile(remote_file_name):
					#Try to remove old file if it exist
					try: 
						sftp.remove(remote_file_name)
					except IOError:
						pass
					sftp.put(local_file_name, remote_file_name)
		else:
			sftp.put(local_file_name, remote_file_name)
		# Close the connection
		sftp.close()
		ssh.close()

	def download_file(user, passwd, remote_file_name, local_directory):
		# Connect to server via SSH
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys
		ssh.connect('pstc-cs1.pstc.brown.edu',username=user,password=passwd)
		sftp = ssh.open_sftp()
		# Download the file
		sftp.get(remote_file_name, local_directory)
		# Close the connection
		sftp.close()
		ssh.close()

	# Run get_pblks
	get_pblks(city_info, paths)

	# Upload street grid to server
	grid_local_file_name = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	grid_remote_file_name = unix_path + '/%s/stgrid/%s%s/%s' % (str(decade), city_name, state_abbr, grid_shp.split('/')[-1])
	upload_file(user, passwd, grid_local_file_name, grid_remote_file_name)

	# If no iteration, run once
	if not iterate:
		# Run cleaning algorithm on unix server 
		ssh = paramiko.SSHClient()
		ssh.connect(server, username=username, password=password)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python RunClean %s %s %s %s" % (city_name, state_abbr, decade, False))
		ssh.close()
		# Download results to proper local directory
		# 	- Store overall_match
		#	- Count number of overall_matches
		version = 7
		microdata_remote_filename = unix_path + '/%s/autocleaned/V%s/%s%s_AutoCleanedV%s.csv' % (str(decade), str(version), city_name, state_abbr, str(version))
		local_directory = dir_path + "/StataFiles_Other/" + str(decade) + "/"
		download_file(user, passwd, microdata_remote_filename, local_directory)
		df_micro = load_cleaned_microdata(city_info, dir_path)
		tot_micro = len(df_micro)
		cases_w_street_label = len(df_micro[df_micro['overall_match']!=''])
		# Run get_ed_map
		#	- Store pblk/ED
		# 	- Count number of pblks with ED guesses
		get_ed_map(city_info, paths, grid_street_var, hn_ranges)
		ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
		df_ed_guess = load_shp(ed_guess_shp)
		tot_pblks = len(df_ed_guess)
		cases_w_ed_label = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
		# Spatial join stgrid and ED map
		pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
		sj_shp = geo_path + city_name + state_abbr + '_1940_stgrid_ED_sj.shp' 
		arcpy.SpatialJoin_analysis(target_features=pblk_shp, 
			join_features=grid_local_file_name, 
			out_feature_class=sj_shp, 
			join_operation="JOIN_ONE_TO_MANY", 
			join_type="KEEP_ALL",
			match_option="SHARE_A_LINE_SEGMENT_WITH")
		# Upload Spatial join file
		sj_remote_file_name = unix_path + '/%s/stgrid/%s%s/%s' % (str(decade), city_name_ns, state_abbr, sj_shp.split('/')[-1])
		upload_file(user, passwd, sj_shp, sj_remote_file_name)
		# Run cleaning algorithm on unix server (with ED map)
		ssh = paramiko.SSHClient()
		ssh.connect(server, username=username, password=password)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python RunClean %s %s %s %s" % (city_name, state_abbr, decade, True))
		ssh.close()
		# Get final cleaned microdata
		microdata_remote_filename = unix_path + '/%s/autocleaned/V%s/%s%s_AutoCleanedV%s.csv' % (str(decade), str(version), city_name, state_abbr, str(version))
		local_directory = dir_path + "/StataFiles_Other/" + str(decade) + "/"
		download_file(user, passwd, microdata_remote_filename, local_directory)
		# Run get_ed_map one final time
		#	- Store pblk/ED
		# 	- Count number of pblks with ED guesses
		get_ed_map(city_info, paths, grid_street_var, hn_ranges)
		ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
		df_ed_guess = load_shp(ed_guess_shp)
		cases_w_ed_label = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
		# Account for improvement??
		# Report how well we did
		print("\nOverall match found for %s of %s cases (%s%)" % (str(cases_w_street_label), str(tot_micro), float(cases_w_street_label)/tot_micro))
		print("ED guess found for %s of %s physical blocks (%s%)\n" % (str(cases_w_ed_label), str(tot_pblks), float(cases_w_ed_label)/tot_pblks))
		return

	# Loop to iteratively run cleaning (unix server) and ED mapping (local) until thresholds met
	first = True
	while num_new_street_labels >= 100 and num_new_ed_guesses >= 10:
		# Run cleaning algorithm on unix server 
		ssh = paramiko.SSHClient()
		ssh.connect(server, username=username, password=password)
		if first:
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python RunClean %s %s %s %s" % (city_name, state_abbr, decade, False))
		else:
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python RunClean %s %s %s %s" % (city_name, state_abbr, decade, True))
		ssh.close()
		# Download results to proper local directory
		# 	- Store overall_match
		#	- Count number of overall_matches
		version = 7
		microdata_remote_filename = unix_path + '/%s/autocleaned/V%s/%s%s_AutoCleanedV%s.csv' % (str(decade), str(version), city_name, state_abbr, str(version))
		local_directory = dir_path + "/StataFiles_Other/" + str(decade) + "/"
		download_file(user, passwd, microdata_remote_filename, local_directory)
		df_micro = load_cleaned_microdata(city_info, dir_path)
		tot_micro = len(df_micro)
		cases_w_street_label = len(df_micro[df_micro['overall_match']!=''])
		# Run get_ed_map
		#	- Store pblk/ED
		# 	- Count number of pblks with ED guesses
		get_ed_map(city_info, paths, grid_street_var, hn_ranges)
		ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
		df_ed_guess = load_shp(ed_guess_shp)
		tot_pblks = len(df_ed_guess)
		cases_w_ed_label = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
		# Spatial join stgrid and ED map
		pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
		sj_shp = geo_path + city_name + state_abbr + '_1940_stgrid_ED_sj.shp' 
		arcpy.SpatialJoin_analysis(target_features=pblk_shp, 
			join_features=grid_local_file_name, 
			out_feature_class=sj_shp, 
			join_operation="JOIN_ONE_TO_MANY", 
			join_type="KEEP_ALL",
			match_option="SHARE_A_LINE_SEGMENT_WITH")
		# Upload Spatial join file
		sj_remote_file_name = unix_path + '/%s/stgrid/%s%s/%s' % (str(decade), city_name_ns, state_abbr, sj_shp.split('/')[-1])
		upload_file(user, passwd, sj_shp, sj_remote_file_name)
		# Keep track of how we're doing
		if first:
			num_new_street_labels = cases_w_street_label
			num_new_ed_guesses = cases_w_ed_label
			first = False
		else:
			num_new_street_labels = cases_w_street_label - num_new_street_labels
			num_new_ed_guesses = cases_w_ed_label - num_new_ed_guesses

	# Download final microdata after iterations
	microdata_remote_filename = unix_path + '/%s/autocleaned/V%s/%s%s_AutoCleanedV%s.csv' % (str(decade), str(version), city_name, state_abbr, str(version))
	local_directory = dir_path + "/StataFiles_Other/" + str(decade) + "/"
	download_file(user, passwd, microdata_remote_filename, local_directory)

	# Report how well we did
	print("\nOverall match found for %s of %s cases (%s%)" % (str(cases_w_street_label), str(tot_micro), float(cases_w_street_label)/tot_micro))
	print("ED guess found for %s of %s physical blocks (%s%)\n" % (str(cases_w_ed_label), str(tot_pblks), float(cases_w_ed_label)/tot_pblks))
