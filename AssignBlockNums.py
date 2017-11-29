#
#	AssignBlockNums.py
#
#	
#

import os
import subprocess
import sys

city_name = "St Louis"
state_abbr = "MO"
#r_path = "C:\Program Files\\R\\R-3.3.2\\bin\Rscript"
#script_path = "C:\Users\\cgraziul\\hist-census-gis"
r_path = "C:\Program Files\\R\\R-3.4.2\\bin\Rscript"
script_path = "C:\Users\\cgraziul\\Documents\\GitHub\\hist-census-gis"

#city_name = sys.argv[1]
#state_abbr = sys.argv[2]
#r_path = sys.argv[3]
#script_path = sys.argv[4]

city_name = city_name.replace(" ","")
file_path = "S:\Projects\\1940Census\\%s" % (city_name) #TO DO: Directories need to be city_name+state_abbr
file_name = file_path + "\\StataFiles_Other\\1930\\" + city_name + state_abbr + "_StudAuto.dta"

print("Combined script for automated block numbering (%s)\n" % (city_name))

# Functions

def create_1930_addresses(r_path, script_path, file_path, city_name, file_name, state_abbr):
	print("Creating 1930 addresses\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Create 1930 Address.R',file_path,city_name,file_name,state_abbr])
	if t != 0:
		print("Error generating 1930 addresses for "+city_name+"\n")
	else:
		print("OK!\n")

def create_blocks_and_block_points(script_path, file_path, city_name, state_abbr):
	print("Creating blocks and block points\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\Create Blocks and Block Points.py",file_path,city_name,state_abbr])
	if t != 0:
		print("Error creating blocks and block points for "+city_name+"\n")
	else:
		print("OK!\n")

def identify_1930_eds(r_path, script_path, file_path, city_name):
	print("Identifying 1930 EDs\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 EDs.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying 1930 EDs for "+city_name+"\n")
	else:
		print("OK!\n")

def analyzing_microdata_and_grid(r_path, script_path, file_path, city_name, state_abbr):
	print("Analyzing microdata and grids\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Analyzing Microdata and Grid.R',file_path,city_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error analyzing microdata and grid for "+city_name+"\n")
	else:
		print("OK!\n")

def add_ranges_to_new_grid(r_path, script_path, file_path, city_name, file_name, state_abbr):
	print("Adding ranges to new grid\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Add Ranges to New Grid.R',file_path,city_name,file_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error adding ranges to new grid for "+city_name+"\n")
	else:
		print("OK!\n")

def identify_1930_blocks(r_path, script_path, file_path, city_name):
	print("Identifying 1930 blocks\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 Blocks.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying 1930 blocks for "+city_name+"\n")
	else:
		print("OK!\n")

def get_block_desription_guesses(script_path, file_path, city_name, state_abbr):
	print("Getting block numbers using block descriptions from microdata\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunBlockDesc.py",file_path,city_name,state_abbr])
	if t != 0:
		print("Error getting block description guesses for "+city_name+"\n")
	else:
		print("OK!\n")

def run_ocr(script_path, file_path, city_name):
	print("Runing Matlab script\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
	if t != 0:
		print("Error running Matlab OCR script for "+city_name+"\n")
	else:
		print("OK!\n")

def integrate_ocr(script_path, file_path, city_name, file_name):
	print("Integrating OCR block numbering results\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\MapOCRintegration.py",file_path,city_name,file_name])
	if t != 0:
		print("Error integrating OCR block numbering results for "+city_name+"\n")
	else:
		print("OK!\n")

def set_blocknum_confidence(script_path, file_path, city_name):
	print("Setting confidence\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\SetConfidence.py",file_path,city_name])
	if t != 0:
		print("Error setting confidence for for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Step 1: Apply R algorithm (Author: Matt Martinez)
#

print("Step 1: Apply R algorithm\n")

# Assigns block numbers using microdata blocks. Examines proportion of cases that geocode 
# onto the same physical block and decides  

# Create 1930 addresses
create_1930_addresses(r_path, script_path, file_path, city_name, file_name, state_abbr)

# Create blocks and block points
create_blocks_and_block_points(script_path, file_path, city_name, state_abbr)

# Identify 1930 EDs
identify_1930_eds(r_path, script_path, file_path, city_name)

# Analyze microdata and grid
analyzing_microdata_and_grid(r_path, script_path, file_path, city_name, state_abbr)

# Add ranges to new grid
#add_ranges_to_new_grid(r_path, script_path, file_path, city_name, file_name, state_abbr)		

# Identify 1930 blocks
identify_1930_blocks(r_path, script_path, file_path, city_name)

#
# Step 2: Create and apply "block descriptions" based on microdata
#

# Assigns block numbers using microdata blocks. Uses results from Step 1 and derived 
# block descriptions (i.e. streets associated with block in microdata) to make educated
# guesses about block numbers

print("Step 2: Block descriptions from microdata\n")

# Get block description guesses
get_block_desription_guesses(script_path, file_path, city_name, state_abbr)

#
# Step 3: Apply Matlab (OCR) algorithm (Author: Chris Graziul)
#

# Assigns block numbers using 1930 block maps. Applies custom built OCR engine 
# and Matlab toolboxes to produce shapefiles.  

print("Step 3: Runing OCR script\n")

# Run OCR script
#run_ocr(script_path, file_path, city_name)

# Integrate OCR block numbering results
#integrate_ocr(script_path, file_path, city_name, file_name)

#
# Step 4: Set confidence
#

# Condenses automated block numbering into one column of best guesses with confidence
# for each guess and as few other image columns as possible  

print("Step 4: Set confidence\n")

# Integrate OCR block numbering results
set_blocknum_confidence(script_path, file_path, city_name)
