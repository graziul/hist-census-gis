#
# Name: Create Blocks and Block Points.py
#
# Author(s):Matt Martinez (adapted for AssignBlockNums.py by Chris Graziul, seperated into seperate functions by Joey Danko)
#
# Purpose: Use street grid and microdata to create blocks and perform initial geocode
#
# Usage: python "Create Blocks and Block Points.py" [path] [city_name] [state abbreviation]  
#
# File types:  Edited street grid shapefiles
# StudAuto microdata files
#

#from blocknum.blocknum import *

#dir_path = "S:/Projects/1940Census/StLouis/GIS_edited/"
#name = "StLouis"
#state = "MO"
#geocode_file = ""

#print("Start") # ERASE LATER

dir_path = sys.argv[1] + "/GIS_edited/"
name = sys.argv[2]
state = sys.argv[3]
geocode_file = sys.argv[4]

different_geocode = False
if geocode_file != None:
	different_geocode = True

# overwrite output
arcpy.env.overwriteOutput=True

print("The script has started to work and is running the 'street' function")

problem_segments = street(dir_path, name, state)
print("The script has finished executing the 'street' function and has now started executing 'physical_blocks' function")

physical_blocks(dir_path, name)
print("The script has finished executing the 'physical_blocks' function and has now started executing 'geocode' function")

geocode(dir_path, name)
print("The script has finished executing the 'geocode' function and has now started excuting 'attach_pblk_id'")

if different_geocode:
	points30 = geocode_file
	print("Different geocode")
else:
	points30 = dir_path + name + "_1930_Points.shp"

attach_pblk_id(dir_path, name, points30)
print("The script has finished executing the 'attach_pblk_id' function and the entire script is complete")
