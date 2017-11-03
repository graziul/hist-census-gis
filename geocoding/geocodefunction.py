"""
Title: geocodefunction
Objective: automate our current (circa Nov. 2017) geocoding process
Notes:  Specifically intersects a user-specified street grid with a verified map (e.g., ED or block) to
        determine which street segments fall in which regions of the verified map (e.g., ED or block),
        creates an address locator using that grid and other user-specified parameters (e.g., use ED as city)
        and then execute the geocode using that address locator on a user-specified table of addresses (i.e.,
        full list of addresses for a specific city or a list of residual addresses from a previous geocode)
Author: Joseph Danko
Created: 11/3/2017
"""

# Import the ESRI library of tools into Python
import arcpy


### USER-SPECIFIED INPUTS ###
# Specify the work place in which all the data is stored (e.g., a geodatabase is recommended)
arcpy.env.workspace="S:/Users/_Exchange/To Joey/FromDaniel/Cincy.gdb"

# All Python to overwrite any ESRI output files (e.g., shapefiles)
arcpy.env.overwriteOutput=True

# "add" is the list of addresses (e.g., .csv or table in a geodatabase) that will eventually be geocoded
add = "Cincinnati_OH_1930_microdata"

# "sg" is the name of the street grid on which the previous list of addresses will be geocoded
sg = "Cincinnati_OH_1930_streets"

# "vm" is the verified map (e.g., ED or block map)
vm = "Cincinnati_OH_1930_EDchi"

# "fl" is the smallest house number on the left side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
fl = "LFROMADD"

# "tl" is the largest house number on the left side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
tl = "LTOADD"

# "fr" is the smallest house number on the right side of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
fr = "RFROMADD"

# "tr" is the largest house number on the right side of the street as noted in the output of  the output of the intersect of the "sg" street grid and "vm" verified map, which is used when creating the address locator (REQUIRED)
tr = "RTOADD"

# "cal_street" is the name of the street as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (hence "cal_"; REQUIRED)
cal_street = "FULLNAME" 

# "cal_city" is the name of the city as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (e.g., city or ED; NOT REQUIRED)
cal_city = "ed"

# "cal_state" is the name of the state as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (NOT REQUIRED)
cal_state = "STATE"

# "addfield" is the name of the additional field as noted in the output of the intersect of the "sg" street grid and "vm" verified map, which is used in the create address locator (e.g., ED or city; NOT REQUIRED)
addfield = "<None>"

# "al" is the filename of the ESRI-generated address locator, which cannot be overwritten and must be changed if you are running multiple iterations of this tool
al = "address_locator"

# "g_address" is the name of the column that stores the address of the property from the "add" list of address file
g_address = "ADDRESS"

# "g_city" is the name of the column that stores the city field from the "add" list of address file (e.g., city, ED or block), which should match the city field used in the address locator
g_city = "ED"

# "g_state" is the name of the column that stores the state field from the "add" list of address file
g_state = "STATE"

# "gr" is the filename of the geocoding results
gr = "geocode_result"

def geocode(add,sg,vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr):
    print("Step 1 of 3: The 'Geocode' function has started and the program has started to implement the intersect function")
    arcpy.Intersect_analysis ([sg, vm], "sg_vm", "ALL", "", "")
    print("Step 2 of 3: The program has finished implementing the intersect function and has begun creating the address locator")
    arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges",
                                         "sg_vm","'Feature ID' <None> VISIBLE NONE;\
                                                    '*From Left' "+fl+" VISIBLE NONE;\
                                                    '*To Left' "+tl+" VISIBLE NONE;\
                                                    '*From Right' "+fr+" VISIBLE NONE;\
                                                    '*To Right' "+tr+" VISIBLE NONE;\
                                                    'Prefix Direction' <None> VISIBLE NONE;\
                                                    'Prefix Type' <None> VISIBLE NONE;\
                                                    '*Street Name' "+cal_street+" VISIBLE NONE;\
                                                    'Suffix Type' <None> VISIBLE NONE;\
                                                    'Suffix Direction' <None> VISIBLE NONE;\
                                                    'Left City or Place' "+cal_city+" VISIBLE NONE;\
                                                    'Right City or Place' "+cal_city+" VISIBLE NONE;\
                                                    'Left ZIP Code' <None> VISIBLE NONE;\
                                                    'Right ZIP Code' <None> VISIBLE NONE;\
                                                    'Left State' "+cal_state+" VISIBLE NONE;\
                                                    'Right State' "+cal_state+" VISIBLE NONE;\
                                                    'Left Street ID' <None> VISIBLE NONE;\
                                                    'Right Street ID' <None> VISIBLE NONE;\
                                                    'Display X' <None> VISIBLE NONE;\
                                                    'Display Y' <None> VISIBLE NONE;\
                                                    'Min X value for extent' <None> VISIBLE NONE;\
                                                    'Max X value for extent' <None> VISIBLE NONE;\
                                                    'Min Y value for extent' <None> VISIBLE NONE;\
                                                    'Max Y value for extent' <None> VISIBLE NONE;\
                                                    'Left parity' <None> VISIBLE NONE;\
                                                    'Right parity' <None> VISIBLE NONE;\
                                                    'Left Additional Field' "+addfield+" VISIBLE NONE;\
                                                    'Right Additional Field' "+addfield+" VISIBLE NONE;\
                                                    'Altname JoinID' <None> VISIBLE NONE",
                                         al, "")
    print("Step 3 of 3: The program has finished creating the address locator and has started the geocoding process")

    arcpy.GeocodeAddresses_geocoding(add, al,
                                     "Street "+g_address+" VISIBLE NONE;\
                                    City "+g_city+" VISIBLE NONE;\
                                    State "+g_state+" VISIBLE NONE",
                                     gr, "STATIC")
    print("The program has finished the geocoding process and 'Geocode' function is complete")

geocode(add,sg,vm,fl,tl,fr,tr,cal_street,cal_city,cal_state,addfield,al,g_address,g_city,g_state,gr)
