#
#	EDblocks.py
#
#	
#

from histcensusgis.microdata.misc import create_addresses
from histcensusgis.polygons.block import *
from histcensusgis.polygons.ed import *

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

def get_ed_map(city_info, paths, grid_street_var, hn_ranges=['LTOADD','LFROMADD','RTOADD','RFROMADD']):

	city_name, state_abbr, decade = city_info
	_, dir_path = paths
	geo_path = dir_path + '/GIS_edited/'
	
	# Step 1: Run Amory's intersections-based algorithm
	ed_inter_algo(city_info, paths, grid_street_var)

	# Step 2: Run Matt's geocoding-based algorithm 
	ed_geocode_algo(city_info, paths)

	# Step 3: Run ED descriptions-based algorithm
	ed_desc_algo(city_info, paths, grid_street_var)	

	# Step 4: Combine algorithm results
	combine_ed_maps(city_info, geo_path, hn_ranges)
	print(get_ed_guess_stats(city_info, hn_ranges))

	print("\nFinished ED map for %s %s, %s\n" % (str(decade), city_name, state_abbr))

def get_block_map(city_info, paths):

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

	get_pblks(city_info, paths)

	get_ed_map(city_info, paths, grid_street_var, hn_ranges)

	get_block_map(city_info, paths)

