#
#	EDblocks.py
#
#	
#

from histcensusgis.microdata.misc import create_addresses
from histcensusgis.polygons.block import *
from histcensusgis.polygons.ed import *
from histcensusgis.points.geocode import *
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
	if city_state in ['KansasCityKS','KansasCityKS','RichmondVA','RichmondNY']:
		dir_path = data_path + city_state
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
		set_blocknum_confidence(city_info, paths)
	else:
		print("Cannot automatically assign Census block numbers for 1940 using current data sources")

def combine_ed_block_maps(city_info, paths):

	city_name, state_abbr, decade = city_info
	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'
	
	#edit_shp_file = geo_path + "EmptyBlockToFillNumbers2.shp"
	block_shp = geo_path + city_name + "_" + str(decade) + "_block_guess.shp"
	ed_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ed_guess.shp'
	ed_block_shp = geo_path + city_name + state_abbr + '_' + str(decade) '_ed_block_guess.shp'
	
	# Load block guess file and clean up
	df_block_shp = load_shp(block_shp)
	df_block_shp['pblk_id'] = df_block_shp['pblk_id'].astype(int)
	#Replace spaces and "and" with "-"
	df_block_shp['auto_bn'] = df_block_shp['auto_bn'].str.replace(' ','-')
	df_block_shp['auto_bn'] = df_block_shp['auto_bn'].str.replace('and','-')
	df_block_shp['auto_bn'] = df_block_shp['auto_bn'].replace('-+','-',regex=True)
	df_block_shp['auto_bn'] = df_block_shp['auto_bn'].str.replace('None','')
	df_block_shp['ed_alt'], df_block_shp['blk_guess'] = df_block_shp['auto_bn'].str.split('-',1).str
	df_block_shp['blk_guess'] = df_block_shp['blk_guess'].astype(str).str.replace('nan','')

	# Load ED guses file and clean up
	df_ed_shp = load_shp(ed_shp)
	#Turn ED=0 into blank 
	df_ed_shp['ed_guess'] = df_ed_shp['ed_guess'].astype(str).replace('0','')

	df = df_ed_shp.merge(df_block_shp.loc[:,df_block_shp.columns!='geometry'], on='pblk_id')

	def generate_ed_block_guesses():
		

	df['am_bn'] = df.apply(lambda x: generate_ed_block_guesses(x[]), axis=1)

	save_shp(df, ed_block_shp)

	#Add ED to manual block numbers
	df['block1'] = df['ed1'] + '-' + df['block']
	df['block1'] = df['block1'].replace('^-|-$','',regex=True)
	df.loc[df['block']=='','block1'] = ''
	df.loc[df['ed']==0,'block1'] = ''

	#Replace spaces and "and" with "-"
	df['auto_bn'] = df['auto_bn'].str.replace(' ','-')
	df['auto_bn'] = df['auto_bn'].str.replace('and','-')
	df['auto_bn'] = df['auto_bn'].replace('-+','-',regex=True)

	save_shp(df, ed_block_shp)
	'''
	###
	### THIS CODE INVOLVED INCLUDING MANUAL BLOCK NUMBERING BUT IS NOT USED CURRENTLY
	###

	#Start with manual block numbers (some automatic block numbers have been fixed)
	df['am_bn'] = df['block1']
	#Add automatic block numbers where there is no manual block number
	df.loc[df['D']==0,'am_bn'] = df['auto_bn1']

	# Save as dbf via csv
	csv_file = dir_path + "\\temp_for_dbf.csv"
	df.to_csv(csv_file)
	arcpy.TableToTable_conversion(csv_file,dir_path,"temp_for_shp.dbf")
	os.remove(dbf_file)
	os.remove(csv_file)
	os.rename(dir_path+"\\temp_for_shp.dbf",dbf_file)
	os.remove(dir_path+"\\temp_for_shp.dbf.xml")
	os.remove(dir_path+"\\temp_for_shp.cpg")

	#Select non-missing block numbers
	arcpy.MakeFeatureLayer_management(temp_shp_file,"edit_lyr")
	arcpy.SelectLayerByAttribute_management("edit_lyr", "", ' "am_bn" <> \'\' ')
	arcpy.CopyFeatures_management("edit_lyr",block_shp)
	arcpy.DeleteFeatures_management(temp_shp_file)

	#Dissolve by "am_bn"
	arcpy.Dissolve_management(in_features=block_shp, out_feature_class=temp_shp_file, dissolve_field=["am_bn","ed"], statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
	#Generate unique block ID
	expression="!FID! + 1"
	arcpy.AddField_management(temp_shp_file, "pblk_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(temp_shp_file, "pblk_id", expression, "PYTHON_9.3")
	arcpy.CopyFeatures_management(temp_shp_file, block_shp)
	arcpy.DeleteFeatures_management(temp_shp_file)

	#Select non-missing EDs
	arcpy.CopyFeatures_management(edit_shp_file,temp_shp_file)
	arcpy.MakeFeatureLayer_management(temp_shp_file,"edit_lyr")
	arcpy.SelectLayerByAttribute_management("edit_lyr", "", ' "ed" <> 0 ')
	arcpy.CopyFeatures_management("edit_lyr",ed_shp_file)
	arcpy.DeleteFeatures_management(temp_shp_file)

	#Dissolve by "ed"
	arcpy.Dissolve_management(in_features=ed_shp_file, out_feature_class=temp_shp_file, dissolve_field=["ed"], statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
	arcpy.CopyFeatures_management(temp_shp_file,ed_shp_file)
	arcpy.DeleteFeatures_management(temp_shp_file)
	'''


def geocode_city(city_info, paths):

	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')

	r_path, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'

	df_micro = fix_micro_dir_using_ed_map(city_info=city_info, 
		paths=paths)

	df_micro2 = fix_micro_blocks_using_ed_map(city_info=city_info, 
		paths=paths, 
		df_micro=df_micro)

	block_guess_shp = geo_path + city_name + "_" + str(decade) + "_block_guess.shp"
	if not os.path.isfile(block_guess_shp):
		get_block_map(city_info, paths)

	renumber_grid(city_name=city_name, 
		state_abbr=state_abbr, 
		paths=paths, 
		decade=decade,
		df=df_micro2)

	get_adjacent_eds(city_info=city_info,
		geo_path=geo_path)

	# Common variables

	# "vm" is the verified map (e.g., ED or block map)
	vm = geo_path + city_name + "_" + str(decade) + "_ED.shp"
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
	add = geo_path + city_name + "_" + str(decade) + "_Addresses.csv"
	# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
	sg = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_renumberedbf.shp"
	# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
	al = geo_path + city_name + "_addloc_" + str(decade) + "_ED"
	# "gr" is the filename of the geocoding results
	gr = geo_path + city_name + state_abbr + "_" + str(decade) + "_geocode_renumberedEDbf.shp"
	# "sg_vm" is the filename of the intersection of the street grid and the verified map
	sg_vm = geo_path + city_name + state_abbr + "_grid_poly_intersect.shp"
	#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
	spatjoin = geo_path + city_name + state_abbr + "_" + str(decade) + "_geo_map_spatjoin.shp"
	# Not correct geocode
	notcor = geo_path + city_name + state_abbr + "_" + str(decade) + "_NotGeocodedCorrect.shp"
	# Correct geocode
	cor = geo_path + city_name + state_abbr + "_" + str(decade) + "_GeocodedCorrect.shp"
	# Ungeocoded addresses
	resid_add = geo_path + city_name + "_" + str(decade) + "_AddNotGeocoded.dbf"

	geocode(geo_path, city_name, add, sg, vm, sg_vm, fl, tl, fr, tr, cal_street, cal_city, cal_state, addfield, al, g_address, g_city, g_state, gr)
	validate(geo_path, city_name, state_abbr, gr, vm, spatjoin, notcor, cor, decade, residual_file=resid_add)

	#
	# Geocode on contemporary house number ranges
	#

	# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
	# "add" is resid_add from above
	# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
	sg = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
	al = geo_path + city_name + "_addloc_" + str(decade) + "_ED_Contemp"
	# "gr" is the filename of the geocoding results
	gr = geo_path + city_name + state_abbr + "_" + str(decade) + "_geocode_renumberedED_Contemp.shp"
	# "sg_vm" is the filename of the intersection of the street grid and the verified map
	sg_vm = geo_path + city_name + state_abbr + "_grid_poly_intersect_Contemp.shp"
	#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
	spatjoin = geo_path + city_name + state_abbr + "_" + str(decade) + "_geo_map_spatjoin_Contemp.shp"
	# Not correct geocode
	notcor = geo_path + city_name + state_abbr + "_" + str(decade) + "_NotGeocodedCorrect_Contemp.shp"
	# Correct geocode
	cor = geo_path + city_name + state_abbr + "_" + str(decade) + "_GeocodedCorrect_Contemp.shp"
	# Ungeocoded addresses
	resid_add_contemp = geo_path + city_name + "_" + str(decade) + "_AddNotGeocoded_Contemp.dbf"

	geocode(geo_path, city_name, resid_add, sg, vm, sg_vm, fl, tl, fr, tr, cal_street, cal_city, cal_state, addfield, al, g_address, g_city, g_state, gr)
	validate(geo_path, city_name, state_abbr, gr, vm, spatjoin, notcor, cor, decade, residual_file=resid_add_contemp)

	#
	# Combine both geocodes to get the best geocode
	#

	combine_geocodes(geo_path, city_name, state_abbr, decade)

def run_cleaning_w_ed(city_info, overwrite=False, iterate=True, unix_path='/home/s4-data/LatestCities', server='pstc-cs1.pstc.brown.edu', grid_street_var='FULLNAME', hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD']):

	overwrite=False
	iterate=False
	unix_path='/home/s4-data/LatestCities'
	server='pstc-cs1.pstc.brown.edu'
	grid_street_var='FULLNAME'
	hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD']
	city_info = ['Omaha','NE',1930]

	user = raw_input("Username:")
	passwd = getpass.getpass("Password for " + user + ":")

	# user = sys.argv[1]
	# pw = sys.argv[2]
	city_name, state_abbr, decade = city_info
	city_name = city_name.replace(' ','')
	r_path, dir_path = get_paths(city_info)
	geo_path = dir_path + '/GIS_edited/'

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.load_system_host_keys
	server = 'pstc-cs1.pstc.brown.edu'

	def upload_file(user, passwd, local_file_name, remote_file_name):
		# Connect to server via SSH
		ssh.connect(server,username=user,password=passwd)
		sftp = ssh.open_sftp()
		# Make sure the target directory exists (or else create it)
		target_path = '/'.join(remote_file_name.split('/')[:-1])
		try:
			sftp.listdir(target_path)
		except IOError:
			mkdir_p(sftp, target_path)
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

	def mkdir_p(sftp, remote_directory):
	    """Change to this directory, recursively making new folders if needed.
	    Returns True if any folders were created."""
	    if remote_directory == '/':
	        # absolute path so change directory to root
	        sftp.chdir('/')
	        return
	    if remote_directory == '':
	        # top-level relative directory must exist
	        return
	    try:
	        sftp.chdir(remote_directory) # sub-directory exists
	    except IOError:
	        dirname, basename = os.path.split(remote_directory.rstrip('/'))
	        mkdir_p(sftp, dirname) # make parent directories
	        sftp.mkdir(basename) # sub-directory missing, so created it
	        sftp.chdir(basename)
	        return True

	def download_file(user, passwd, remote_file_name, local_file_name):
		# Connect to server via SSH
		ssh.connect(server,username=user,password=passwd)
		sftp = ssh.open_sftp()
		# Download the file
		sftp.get(remote_file_name, local_file_name)
		# Close the connection
		sftp.close()
		ssh.close()

	# Step 0: Fix stgrid and get pblks (make this a check when iterative function working)
	get_pblks(city_info, paths)

	# Step 1: Run ED descriptions-based algorithm once (does not change with microdata changes)
	ed_desc_algo(city_info, paths, grid_street_var)	

	# Step 2: Function to run intersections and geocoding-baseds algorithms, thencombine results 
	def get_ed_inter_geo_combine():
		# Run Amory's intersections-based algorithm
		ed_inter_algo(city_info, paths, grid_street_var)
		# Run Matt's geocoding algorithm
		ed_geocode_algo(city_info, paths)
		# Combine results and print relevant informatino
		combine_ed_maps(city_info, geo_path, hn_ranges)
		print(get_ed_guess_stats(city_info, paths, hn_ranges))

	# Step 3: Upload street grid to server (prepare to clean microdata)
	grid_local_file_name = geo_path + city_name + state_abbr + "_" + str(decade) + "_stgrid_edit_Uns2.shp"
	grid_remote_file_name = unix_path + '/%s/shp/%s%s/%s' % (str(decade), city_name, state_abbr, grid_local_file_name.split('/')[-1])
	upload_file(user, passwd, grid_local_file_name, grid_remote_file_name)

	# Step 4: Set information for microdata cleaning
	version = 7
	microdata_remote_filename = unix_path + '/%s/autocleaned/V%s/%s%s_AutoCleanedV%s.csv' % (str(decade), str(version), city_name, state_abbr, str(version))
	microdata_local_filename = dir_path + '/StataFiles_Other/%s/%s%s_AutoCleanedV%s.csv' % (str(decade), city_name, state_abbr, str(version))

	def print_cleaning_results(ssh_stdout):
		exit_status = ssh_stdout.channel.recv_exit_status()
		for line in iter(ssh_stdout.readline,""):
			print(line)

	# Step 5a: If no iteration, run through once (clean -> ed guess -> clean -> ed guess)
	if not iterate:
		# Run cleaning algorithm on unix server 
		ssh.connect(server, username=user, password=passwd)
		if overwrite:
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python ~/.local/bin/RunClean.py %s %s %s %s" % (city_name, state_abbr, decade, False), get_pty=True)
			print_cleaning_results(ssh_stdout)
		else:
			try:
				sftp = ssh.open_sftp()
				print(sftp.stat(microdata_remote_filename))
				sftp.close()
			except:
				ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python ~/.local/bin/RunClean.py %s %s %s %s" % (city_name, state_abbr, decade, False), get_pty=True)
				print_cleaning_results(ssh_stdout)
		# Download cleaned microdata 
		download_file(user, passwd, microdata_remote_filename, microdata_local_filename)
		# Tabulate results
		df_micro = load_cleaned_microdata(city_info, dir_path)
		tot_micro = len(df_micro)
		cases_w_street_label = len(df_micro[df_micro['overall_match']!=''])
		# Run get_ed_inter_geo_combine
		get_ed_inter_geo_combine()
		# Tabulate results
		ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
		df_ed_guess = load_shp(ed_guess_shp)
		tot_pblks = len(df_ed_guess)
		cases_w_ed_guess = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
		# Spatial join stgrid and ED map
		pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
		sj_shp = geo_path + city_name + state_abbr + '_1940_stgrid_ED_sj.shp' 
		arcpy.SpatialJoin_analysis(target_features=pblk_shp, 
			join_features=grid_local_file_name, 
			out_feature_class=sj_shp, 
			join_operation="JOIN_ONE_TO_MANY", 
			join_type="KEEP_ALL",
			match_option="SHARE_A_LINE_SEGMENT_WITH")
		# Upload Spatial join file to unix server
		sj_remote_file_name = unix_path + '/%s/shp/%s%s/%s' % (str(decade), city_name_ns, state_abbr, sj_shp.split('/')[-1])
		upload_file(user, passwd, sj_shp, sj_remote_file_name)
		# Run cleaning algorithm on unix server (with ED map)
		ssh = paramiko.SSHClient()
		ssh.connect(server, username=username, password=password)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python RunClean %s %s %s %s" % (city_name, state_abbr, decade, True))
		ssh.close()
		print_cleaning_results(ssh_stdout)
		# Get final cleaned microdata
		download_file(user, passwd, microdata_remote_filename, microdata_local_filename)
		# Tabulate results
		df_micro = load_cleaned_microdata(city_info, dir_path)
		tot_micro = len(df_micro)
		cases_w_street_label2 = len(df_micro[df_micro['overall_match']!=''])
		# Run get_ed_inter_geo_combine
		get_ed_inter_geo_combine()
		# Tabulate results
		ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
		df_ed_guess = load_shp(ed_guess_shp)
		cases_w_ed_guess2 = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
		# Report improvement
		print("\nOverall matches gained %s" % (str(cases_w_street_label2-cases_w_street_label)))
		print("ED guesses gained %s" % (str(cases_w_ed_guess2-cases_w_ed_guess)))
		# Report how well we did
		print("\nOverall match found for %s of %s cases (%s%)" % (str(cases_w_street_label), str(tot_micro), float(cases_w_street_label)/tot_micro))
		print("ED guess found for %s of %s physical blocks (%s%)\n" % (str(cases_w_ed_label), str(tot_pblks), float(cases_w_ed_label)/tot_pblks))
		return

	# Step 6b: Loop to iteratively run cleaning (unix server) and ED mapping (local) until thresholds met
	else:
		first = True
		num_new_street_labels = 999999
		num_new_ed_guesses = 999999
		# Keep looping until number of new streets labeled and number of new ED guesses fall below threshold
		while num_new_street_labels >= 100 and num_new_ed_guesses >= 10:
			# Run cleaning algorithm on unix server 
			ssh.connect(server, username=user, password=passwd)
			if first:
				if overwrite:
					ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python ~/.local/bin/RunClean.py %s %s %s %s" % (city_name, state_abbr, decade, False), get_pty=True)
					print_cleaning_results(ssh_stdout)
				else:
					try:
						sftp = ssh.open_sftp()
						print(sftp.stat(microdata_remote_filename))
						sftp.close()
					except:
						ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python ~/.local/bin/RunClean.py %s %s %s %s" % (city_name, state_abbr, decade, False), get_pty=True)
						print_cleaning_results(ssh_stdout)
			else:
				ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python ~/.local/bin/RunClean.py %s %s %s %s" % (city_name, state_abbr, decade, True), get_pty=True)
				print_cleaning_results(ssh_stdout)
			ssh.close()
			# Download cleaned microdata file 
			download_file(user, passwd, microdata_remote_filename, microdata_local_filename)
			# Tabulate results
			df_micro = load_cleaned_microdata(city_info, dir_path)
			tot_micro = len(df_micro)
			cases_w_street_label = len(df_micro[df_micro['overall_match']!=''])
			# Run get_ed_inter_geo_combine
			get_ed_inter_geo_combine()
			# Tabulate results
			ed_guess_shp = geo_path + city_name + state_abbr + '_' + str(decade) + '_ED_guess_map.shp'
			df_ed_guess = load_shp(ed_guess_shp)
			tot_pblks = len(df_ed_guess)
			cases_w_ed_guess = len(df_ed_guess[df_ed_guess['ed_conf']!='-1. No guess'])
			# Spatial join stgrid and ED map
			pblk_shp = geo_path + city_name + "_" + str(decade) + "_Pblk.shp"
			sj_shp = geo_path + city_name + state_abbr + '_1940_stgrid_ED_sj.shp' 
			arcpy.SpatialJoin_analysis(target_features=pblk_shp, 
				join_features=grid_local_file_name, 
				out_feature_class=sj_shp, 
				join_operation="JOIN_ONE_TO_MANY", 
				join_type="KEEP_ALL",
				match_option="SHARE_A_LINE_SEGMENT_WITH")
			# Upload Spatial join file to unix server
			sj_remote_file_name = unix_path + '/%s/shp/%s%s/%s' % (str(decade), city_name, state_abbr, sj_shp.split('/')[-1])
			upload_file(user, passwd, sj_shp, sj_remote_file_name)
			# Update label/guess stats
			if first:
				num_new_street_labels = cases_w_street_label
				num_new_ed_guesses = cases_w_ed_guess
				first = False
			else:
				num_new_street_labels = cases_w_street_label - num_new_street_labels
				num_new_ed_guesses = cases_w_ed_guess - num_new_ed_guesses
			print("Number new streets labeled: " + str(num_new_street_labels))
			print("Number new ED guesses: " + str(num_new_ed_guesses) + "\n")

	# Download final microdata after iterations
	download_file(user, passwd, microdata_remote_filename, microdata_local_filename)

	# Report how well we did
	print("\nOverall match found for %s of %s cases (%s%)" % (str(cases_w_street_label), str(tot_micro), float(cases_w_street_label)/tot_micro))
	print("ED guess found for %s of %s physical blocks (%s%)\n" % (str(cases_w_ed_label), str(tot_pblks), float(cases_w_ed_label)/tot_pblks))

'''
from histcensusgis.EDblocks import *
city_info=['Omaha','NE',1930]
paths=get_paths(city_info)
get_ed_map(city_info, paths)
get_block_map(city_info, paths)
geocode_city(city_info, paths)
'''