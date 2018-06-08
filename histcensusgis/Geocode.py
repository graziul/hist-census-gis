#
# Geocode.py
#

import time
from blocknum.blocknum import *
from geocoding.GeocodeFunctions import *
# overwrite output
arcpy.env.overwriteOutput=True

#city_spaces = 'St Louis'
#city = city_spaces.replace(' ','')
#state = 'MO'
#micro_street_var = 'st_best_guess'
#grid_street_var = 'FULLNAME'
#decade = 1930

#geocode_file = ""
#different_geocode = False
#if geocode_file != "":
#	different_geocode = True

# Paths
#dir_path = "C:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr
#r_path = "C:/Program Files/R/R-3.4.2/bin/Rscript"
#paths = [r_path, dir_path]
#hn_ranges = ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD']

start = time.time()

#
# Step 1: Get a good ED map, good street grid, and initial geocode on contemporary ranges
#

microdata_file = dir_path + "/StataFiles_Other/" + str(decade) + "/" + city + state + "_StudAuto.dta"
df = load_large_dta(microdata_file)
df.loc[:,('index')] = df.index
#df1 = df[['index','hn','dir','name','type',micro_street_var,'ed','block']]

# Create 1930 addresses
create_addresses(city_name=city, 
	state_abbr=state, 
	paths=paths, 
	decade=decade,
	df=df)

# Create blocks and block points (gets Uns2 and points30)
create_blocks_and_block_points(city_name=city, 
	state_abbr=state, 
	paths=paths)

# Identify 1930 EDs 

# Matt's code
# Amory's code
# Combination code
#identify_1930_eds(city_name, paths)

# Manual process of filling in EDs 

#
# Step 2: Use ED map to fix DIR in microdata using initial geocode on contemporary ranges
#

df_micro = fix_micro_dir_using_ed_map(city_name=city, 
	state_abbr=state,
	micro_street_var=micro_street_var, 
	grid_street_var=grid_street_var,
	paths=paths,
	decade=decade,
	df_micro=df)

#
# Step 3: Use microdata to fix street grid names
#

fix_st_grid_names(city_spaces=city_spaces, 
	state_abbr=state, 
	micro_street_var=micro_street_var, 
	grid_street_var=grid_street_var,
	paths=paths, 
	decade=decade,
	df_micro=df_micro)

#
# Step 4: Use ED map and contemporary geocode to fix microdata block numbers
#

# Step 4a: Update addresses and contemporary geocode

# Create 1930 addresses (now uses updated addresses in df_micro)
create_addresses(city_name=city, 
	state_abbr=state, 
	paths=paths,
	decade=decade, 
	df=df_micro)

# Step 4b: Get updated contemporary geocode (using updated adresses from df_micro)
initial_geocode(geo_path=dir_path+'/GIS_edited/', 
	city_name=city, 
	state_abbr=state,
	hn_ranges=hn_ranges)

# Save current
file_name_students = dir_path + '/StataFiles_Other/%s/%s%s_StudAutoDirFixed.csv' % (str(decade),city, state)
df_micro2.to_csv(file_name_students)
dofile = script_path + "/utils/ConvertCsvToDta.do"
cmd = ["C:/Program Files (x86)/Stata15/StataSE-64","/e","do", dofile, file_name_students, file_name_students.replace('.csv','.dta')]
subprocess.call(cmd) 

# Step 4c: Get block numbers

identify_blocks_geocode(city_name, paths, decade)
identify_blocks_microdata(city_name, state_abbr, micro_street_var, paths, decade)


# Step 4d: Fix microdata block numbers using updated geocode and microdata (requires block map)

df_micro2 = fix_micro_blocks_using_ed_map(city_name=city, 
	state_abbr=state, 
	paths=paths, 
	decade=decade,
	df_micro=df_micro)

# If we want, save the microdata file 
save = False
if save:
	file_name_students = dir_path + '/StataFiles_Other/1930/%s%s_StudAutoDirBlockFixed.csv' % (city, state)
	df_micro2.to_csv(file_name_students)
	dofile = script_path + "/utils/ConvertCsvToDta.do"
	cmd = ["C:/Program Files (x86)/Stata15/StataSE-64","/e","do", dofile, file_name_students, file_name_students.replace('.csv','.dta')]
	subprocess.call(cmd) 

end = time.time()

print(str(float(end-start)/60)+" minutes")

#
# Step 5: Renumber grid based on updated 1930 microdata and street grid (requires block map)
#

renumber_grid(city_name=city, 
	state_abbr=state, 
	paths=paths, 
	decade=decade,
	df=df_micro2)

#
# Step 6: Fill in blanks
#

'''
fill_blank_segs(city_name=city, 
	state_abbr=state, 
	paths=paths, 
	df=df_micro)
'''

#
# Step 7: Perform geocode
#

# Path
geo_path = dir_path + '/GIS_edited/'

# Get adjacent EDs
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

