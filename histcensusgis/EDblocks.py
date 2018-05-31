#
#	EDblocks.py
#
#	
#

from histcensusgis.microdata.misc import create_addresses
from histcensusgis.lines.street import *
from histcensusgis.polygons.blocknum import *
from histcensusgis.polygons.ed import *
from histcensusgis.s4utils.AmoryUtils import *
from histcensusgis.s4utils.IOutils import *

r_path = "C:\Program Files\\R\\R-3.4.2\\bin\\Rscript"

def get_ed_block_numbers(city_info, paths, grid_street_var="FULLNAME", hn_ranges=['MIN_LFROMA','MIN_RFROMA','MAX_LTOADD','MAX_RTOADD'], just_desc=False):

	city_name, state_abbr, decade = city_info 
	city_spaces = city_name
	city_name = city_name.replace(' ','')

	city_state = city_name + state_abbr
	if city_state == "KansasCityKS":
		dir_path = "S:/Projects/1940Census/KansasCityKS"
	elif city_state == "KansasCityMO":
		dir_path = "S:/Projects/1940Census/KansasCityMO"
	elif city_state == "RichmondVA":
		dir_path = "S:/Projects/1940Census/RichmondVA"
	elif city_state == "RichmondNY":
		dir_path = "S:/Projects/1940Census/RichmondNY"
	else:
		dir_path = "S:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr

	paths = [r_path, dir_path]
	geo_path = dir_path + '/GIS_edited/'
	
	# Step 1: Get addresses, create physical blocks
	# Create addresses
	create_addresses(city_info, paths)
	# Create blocks and block points
	create_blocks_and_block_points(city_info, paths)

	# Step 2: Run Amory's intersections script
	ed_inter_algo(city_info, paths, grid_street_var)

	# Step 3: Run Matt's ED script (based on geocoding)
	ed_geocode_algo(city_info, paths)

	# Step 4: Run ED descriptions algorithm
	ed_desc_algo(city_info, paths, grid_street_var)	

	# Step 5: Combine ED map guesses
	combine_ed_maps(city_info, geo_path, hn_ranges)
	print(get_ed_guess_stats(city_info))
	print("\nFinished ED map for %s %s, %s\n" % (str(decade), city, state))

	# Step 6: Get block guesses if not 1940
	
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
	
