#
# Geocode.py
#

from blocknum.blocknum import *
from geocoding.GeocodeFunctions import *
# overwrite output
arcpy.env.overwriteOutput=True

city_spaces = 'St Louis'
city = city_spaces.replace(' ','')
state = 'MO'
micro_street_var = 'st_best_guess'
grid_street_var = 'FULLNAME'
year = 1930

geocode_file = ""
different_geocode = False
if geocode_file != "":
	different_geocode = True

# Paths
dir_path = "S:/Projects/1940Census/" + city #TO DO: Directories need to be city_name+state_abbr
r_path = "C:/Program Files/R/R-3.4.2/bin/Rscript"
script_path = "C:/Users/cgraziul/Documents/GitHub/hist-census-gis"
paths = [r_path, script_path, dir_path]

#
# Step 1: Get a good ED map, good street grid, and initial geocode on contemporary ranges
#

microdata_file = dir_path + "/StataFiles_Other/1930/" + city + state + "_StudAuto.dta"
df = load_large_dta(file_name)

# Create 1930 addresses
create_1930_addresses(city_name=city_name, 
	state_abbr=state_abbr, 
	paths=paths, 
	df=df)

# Create blocks and block points (gets Uns2 and points30)
create_blocks_and_block_points(city_name=city_name, 
	state_abbr=state_abbr, 
	paths=paths)

# Identify 1930 EDs (this will eventually incorporate Amory's ED map)
#identify_1930_eds(city_name, paths)

# Manual process of filling in EDs 

#
# Step 2: Use ED map to fix DIR in microdata using initial geocode on contemporary ranges
#

df_micro = fix_micro_dir_using_ed_map(city_name=city, 
	state_abbr=state, 
	street_var=grid_street_var,
	df_micro=df)

#
# Step 3: Use microdata to fix street grid names
#

fix_st_grid_names(city_name=city_spaces, 
	state_abbr=state, 
	grid_street_var=grid_street_var,
	paths=paths, 
	df_micro=df_micro)

#
# Step 4: Use ED map and contemporary geocode to fix microdata block numbers
#

# First, update addresses and contemporary geocode

# Create 1930 addresses (now uses updated addresses in df_micro)
create_1930_addresses(city_name=city_name, 
	state_abbr=state_abbr, 
	paths=paths, 
	df=df_micro)

# Create blocks and block points (gets Uns2 and points30)
create_blocks_and_block_points(city_name=city_name, 
	state_abbr=state_abbr, 
	paths=paths)

# Second, fix microdata block numbers using updated geocode/microdata

df_micro = fix_micro_blocks_using_ed_map(city_name=city_name, 
	state_abbr=state_abbr, 
	paths=paths, 
	df_micro=df_micro)

#
# Step 5: Renumber grid based on updated 1930 microdata and street grid
#

renumber_grid(name=city, 
	state=state, 
	df=df_micro)

#
# Step 6: Perform geocode
#

# Path
geo_path = dir_path + '/GIS_edited/'

# Common files

# "vm" is the verified map (e.g., ED or block map)
vm = geo_path + city_name + "_1930_ED.shp"
# Feature Class to Feature Class file
fc = city_name + state_abbr + "_1930_ED_Feature.shp"
# Spatial weights files:
swm_file = geo_path + city_name + state_abbr + "_1930_spatweight.swm"
swm_table = geo_path + city_name + state_abbr + "_1930_swmTab.dbf"

# Common variables

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
add = geo_path + city_name + "_1930_Addresses.csv"
# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
sg = geo_path + city_name + state_abbr + "_1930_stgrid_renumbered.shp"
# Amory's formatted EDs dbf
fe = geo_path + city_name + state_abbr + "_1930_formattedEDs.dbf"
fe_file = city_name + state_abbr + "_1930_formattedEDs.dbf"
# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
al = geo_path + city_name + "_addloc_ED"
# "gr" is the filename of the geocoding results
gr = geo_path + city_name + state_abbr + "_1930_geocode_renumberedED.shp"
# "sg_vm" is the filename of the intersection of the street grid and the verified map
sg_vm = geo_path + city_name + state_abbr + "_grid_poly_intersect.shp"
#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
spatjoin = geo_path + city_name + state_abbr + "_1930_geo_map_spatjoin.shp"
# Not correct geocode
notcor = geo_path + city_name + state_abbr + "_1930_NotGeocodedCorrect.shp"
# Correct geocode
cor = geo_path + city_name + state_abbr + "_1930_GeocodedCorrect.shp"

geocode(add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr)

validate(dir_path, gr, vm, spatjoin, fc, swm_file, swm_table, fe_file, notcor, cor, residual_file="NotGeocoded.dbf")

#
# Geocode on contemporary house number ranges
#

# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
add = geo_path + city_name + state_abbr + "_NotGeocoded.dbf"
# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
sg = geo_path + city_name + state_abbr + "_1930_stgrid_edit_Uns2.shp"
# Amory's formatted EDs dbf
fe_file = city_name + state_abbr + "_1930_Contemp.dbf"
# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
al = geo_path + city_name + "_addloc_ED_Contemp"
# "gr" is the filename of the geocoding results
gr = geo_path + city_name + state_abbr + "_1930_geocode_renumberedED_Contemp.shp"
# "sg_vm" is the filename of the intersection of the street grid and the verified map
sg_vm = geo_path + city_name + state_abbr + "_grid_poly_intersect_Contemp.shp"
#"spatjoin" is joining the geocode to the verified map (e.g., ED or block map)
spatjoin = geo_path + city_name + state_abbr + "_1930_geo_map_spatjoin_Contemp.shp"
# Not correct geocode
notcor = geo_path + city_name + state_abbr + "_1930_NotGeocodedCorrect_Contemp.shp"
# Correct geocode
cor = geo_path + city_name + state_abbr + "_1930_GeocodedCorrect_Contemp.shp"

geocode(add,sg,vm,sg_vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr)

validate(dir_path, gr, vm, spatjoin, fc, swm_file, swm_table, fe_file, notcor, cor, residual_file="NotGeocoded_Contemp.dbf")

#
# Combine both geocodes to get the best geocode
#

combine_geocodes(geo_path, city_name, state_abbr)

