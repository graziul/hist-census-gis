import os
import subprocess
import sys
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

r_path = r"C:\Program Files\R\R-3.3.2\bin\Rscript"
script_path = r"C:\Users\cgraziul\hist-census-gis"

city_name = "St Louis"
city_name = city_name.replace(" ","")
state_abbr = "MO"
file_path = r"S:\Projects\1940Census\%s" % (city_name) #Needs to be city_name+state_abbr
file_name = file_path + r"\StataFiles_Other\1930\StLouisMO_AutoCleanedV4.csv"

cprint("Combined script for automated block numbering (%s)\n" % (city_name), 'yellow',attrs=['bold'], file=AnsiToWin32(sys.stdout))

# Step 1: Create 1930 addresses
cprint("Starting Step 1: Create 1930 addresses\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Create 1930 Address.R',file_path,city_name,file_name,state_abbr])
	cprint("Step 1 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error generating Add_30.csv for "+city_name, 'red', file=AnsiToWin32(sys.stdout))

# Step 2: Create blocks and block points
cprint("Starting Step 2: Create blocks and block points\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call(["python",script_path+"\\blocknum\\Python\\Create Blocks and Block Points.py",file_path,city_name,state_abbr])
	cprint("\nStep 2 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error creating blocks and block points for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 3: Identify 1930 EDs
cprint("Starting Step 3: Identify 1930 EDs\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 EDs.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	cprint("Step 3 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error identifying 1930 EDs for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 4: Analyze microdata and grid
cprint("Starting Step 4: Analyze microdata and grids\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Analyzing Microdata and Grid.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	cprint("Step 4 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error analyzing microdata and grid for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 5: Add ranges to new grid
cprint("Starting Step 5: Add ranges to new grid\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Add Ranges to New Grid.R',file_path,city_name,file_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	cprint("Step 5 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error adding ranges to new grid for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))
##ABOVE IS DONE

# Step 6: Create 1930 address (2nd round)
cprint("Starting Step 6: Create 1930 address (2nd round)\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Create 1930 Address_2nd.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	cprint("Step 6 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error creating 1930 address (2nd round) for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 7: Create blocks and block points (2nd round)
cprint("Starting Step 7: Create blocks and block points (2nd round)\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call(["python",script_path+"\\blocknum\\Python\\Blocks and Block Points_2nd.py",city_name,file_path])
	cprint("Step 7 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error creating blocks and block points (2nd round) for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 8: Identify 1930 blocks
cprint("Starting Step 8: Identify 1930 blocks\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 Blocks.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	cprint("Step 8 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error identifying 1930 blocks for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 9: Run Matlab OCR script
cprint("Starting Step 9: Run Matlab OCR script\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call(["python",script_path+"\\blocknum\\Python\\Create Blocks and Block Points.py",city_name,file_path])
	cprint("Step 9 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error running Matlab OCR script for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

# Step 10: Integrate R and Matlab block numbering results
cprint("Starting Step 10: Integrate R and Matlab block numbering results\n", attrs=['bold'], file=AnsiToWin32(sys.stdout))
try:
	subprocess.call(["python",script_path+"\\blocknum\\Python\\Create Blocks and Block Points.py",city_name,file_path])
	cprint("Step 10 completed for "+city_name+"\n", 'green', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error integrating R and Matlab block numbering results for "+city_name+"\n", 'red', file=AnsiToWin32(sys.stdout))

