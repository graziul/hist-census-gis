#
#	AssignBlockNums.py
#
#	
#

import os
import subprocess
import sys
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

#city_name = "St Louis"
#state_abbr = "MO"
#r_path = "C:\Program Files\\R\\R-3.3.2\\bin\Rscript"
#script_path = "C:\Users\\cgraziul\\hist-census-gis"
r_path = "C:\Program Files\\R\\R-3.4.1\\bin\Rscript"
script_path = "C:\Users\\cgraziul\\hist-census-gis"

city_name = sys.argv[1]
state_abbr = sys.argv[2]
#r_path = sys.argv[3]
#script_path = sys.argv[4]

city_name = city_name.replace(" ","")
file_path = "S:\Projects\\1940Census\\%s" % (city_name) #TO DO: Directories need to be city_name+state_abbr
file_name = file_path + "\\StataFiles_Other\\1930\\" + city_name + state_abbr + "_StudAuto.dta"

cprint("Combined script for automated block numbering (%s)\n" % (city_name), 'yellow',attrs=['bold'], file=AnsiToWin32(sys.stdout))

#
# Step 1: Apply R algorithm (Author: Matt Martinez)
#

cprint("Step 1: Apply R algorithm\n", attrs=['bold','underline'], file=AnsiToWin32(sys.stdout))

# Assigns block numbers using microdata blocks. Examines proportion of cases that geocode 
# onto the same physical block and decides  

# Create 1930 addresses
cprint("Creating 1930 addresses\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Create 1930 Address.R',file_path,city_name,file_name,state_abbr])
if t != 0:
	cprint("Error generating 1930 addresses for "+city_name, 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

# Create blocks and block points
cprint("Creating blocks and block points\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call(["python",script_path+"\\blocknum\\Python\\Create Blocks and Block Points.py",file_path,city_name,state_abbr])
if t != 0:
	cprint("Error creating blocks and block points for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

# Identify 1930 EDs
cprint("Identifying 1930 EDs\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 EDs.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
if t != 0:
	cprint("Error identifying 1930 EDs for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

# Analyze microdata and grid
cprint("Analyzing microdata and grids\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Analyzing Microdata and Grid.R',file_path,city_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
if t != 0:
	cprint("Error analyzing microdata and grid for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

'''
# Add ranges to new grid
cprint("Adding ranges to new grid\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Add Ranges to New Grid.R',file_path,city_name,file_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
if t != 0:
	cprint("Error adding ranges to new grid for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))
'''

# Identify 1930 blocks
cprint("Identifying 1930 blocks\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 Blocks.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
if t != 0:
	cprint("Error identifying 1930 blocks for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

#
# Step 2: Create and apply "block descriptions" based on microdata
#

# Assigns block numbers using microdata blocks. Uses results from Step 1 and derived 
# block descriptions (i.e. streets associated with block in microdata) to make educated
# guesses about block numbers

cprint("Step 2: Block descriptions from microdata\n", attrs=['bold','underline'], file=AnsiToWin32(sys.stdout))

# Get block description guesses
t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunBlockDesc.py",file_path,city_name,state_abbr])
if t != 0:
	cprint("Error getting block description guesses for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

#
# Step 3: Apply Matlab (OCR) algorithm (Author: Chris Graziul)
#

# Assigns block numbers using 1930 block maps. Applies custom built OCR engine 
# and Matlab toolboxes to produce shapefiles.  
'''
cprint("Step 3: Runing OCR script\n", attrs=['bold','underline'], file=AnsiToWin32(sys.stdout))

# Run OCR script
cprint("Runing Matlab script\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
if t != 0:
	cprint("Error running Matlab OCR script for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))

# Integrate OCR block numbering results
cprint("Integrating OCR block numbering results\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call(["python",script_path+"\\blocknum\\Python\\MapOCRintegration.py",file_path,city_name,file_name])
if t != 0:
	cprint("Error integrating OCR block numbering results for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))
'''
#
# Step 4: Set confidence
#

# Condenses automated block numbering into one column of best guesses with confidence
# for each guess and as few other image columns as possible  

cprint("Step 4: Set confidence\n", attrs=['bold','underline'], file=AnsiToWin32(sys.stdout))

# Integrate OCR block numbering results
cprint("Setting confidence\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
t = subprocess.call(["python",script_path+"\\blocknum\\Python\\SetConfidence.py",file_path,city_name])
if t != 0:
	cprint("Error setting confidence for for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
else:
	cprint("OK!\n", 'green', file=AnsiToWin32(sys.stdout))
