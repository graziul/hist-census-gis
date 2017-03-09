#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys

####WORKS    arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", "'Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_1930_stgrid.shp' 'Primary Table'", "'Feature ID' FID VISIBLE NONE;'*From Left' LFROMADD VISIBLE NONE;'*To Left' LTOADD VISIBLE NONE;'*From Right' RFROMADD VISIBLE NONE;'*To Right' RTOADD VISIBLE NONE;'Prefix Direction' <None> VISIBLE NONE;'Prefix Type' <None> VISIBLE NONE;'*Street Name' FULLNAME VISIBLE NONE;'Suffix Type' <None> VISIBLE NONE;'Suffix Direction' <None> VISIBLE NONE;'Left City or Place' CITY VISIBLE NONE;'Right City or Place' CITY VISIBLE NONE;'Left ZIP Code' <None> VISIBLE NONE;'Right ZIP Code' <None> VISIBLE NONE;'Left State' state VISIBLE NONE;'Right State' state VISIBLE NONE;'Left Street ID' <None> VISIBLE NONE;'Right Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;'Max Y value for extent' <None> VISIBLE NONE;'Left parity' <None> VISIBLE NONE;'Right parity' <None> VISIBLE NONE;'Left Additional Field' <None> VISIBLE NONE;'Right Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE", "Z:\Projects\\1940Census\Block Creation\San Antonio\SanAntonio_addloc","")

# overwrite output
arcpy.env.overwriteOutput=True

for name in ["San Antonio"]:
    print "Working On: " + name
    #Create Paths to be used throughout Process
    reference_data = "'Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_stgrid.shp' 'Primary Table'"
    grid = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_stgrid.shp"
    dissolve_grid = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_stgrid_Dissolve.shp"
    split_grid = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_stgrid_Split.shp"
    pblocks = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_Pblk.shp"
    in_field_map='''
    "'Feature ID' FID VISIBLE NONE;'*From Left' LFROMADD VISIBLE NONE;'*To Left' LTOADD VISIBLE NONE;'*From Right' RFROMADD VISIBLE NONE;
    '*To Right' RTOADD VISIBLE NONE;'Prefix Direction' <None> VISIBLE NONE;'Prefix Type' <None> VISIBLE NONE;'*Street Name' FULLNAME VISIBLE NONE;
    'Suffix Type' <None> VISIBLE NONE;'Suffix Direction' <None> VISIBLE NONE;'Left City or Place' CITY VISIBLE NONE;'Right City or Place' CITY VISIBLE NONE;
    'Left ZIP Code' <None> VISIBLE NONE;'Right ZIP Code' <None> VISIBLE NONE;'Left State' state VISIBLE NONE;'Right State' state VISIBLE NONE;'Left Street ID' <None> VISIBLE NONE;
    'Right Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;
    'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;'Max Y value for extent' <None> VISIBLE NONE;'Left parity' <None> VISIBLE NONE;
    'Right parity' <None> VISIBLE NONE;'Left Additional Field' <None> VISIBLE NONE;'Right Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE;'''
    add_locator = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_addloc"
    #'Add_30' originates from 'Create 1930 and 1940 Address Files.R' code
    addresses = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\Add_30.csv"
    address_fields="Street address;City city;State state"
    points30 = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_Points30.shp"
    pblk_points = "Z:\Projects\\1940Census\Block Creation\\" + name + "\\" + name + "_1930_Pblk_Points.shp"

    print "Working On: " + name + " Creating Physical Blocks"
    ##### #Create Physical Blocks# #####
    #First Dissolve St_Grid lines
    arcpy.Dissolve_management(grid, dissolve_grid, "FULLNAME")
    #Second Split Lines at Intersections
    arcpy.FeatureToLine_management(dissolve_grid, split_grid)
    #Third Create Physical Blocks using Feature to Polygon
    arcpy.FeatureToPolygon_management(split_grid, pblocks)
    #Finally Add a Physical Block ID
    expression="!FID! + 1"
    arcpy.AddField_management(pblocks, "pblk_id", "LONG", 4, "", "","", "", "")
    arcpy.CalculateField_management(pblocks, "pblk_id", expression, "PYTHON_9.3")


    print "Working On: " + name + " Geocode"
    ##### #Geocode Points# #####
    #Create Address Locator
    arcpy.CreateAddressLocator_geocoding("US Address - Dual Ranges", reference_data, in_field_map, add_locator,"")
    #Geocode Points
    arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
    #Attach Pblk ids to points
    arcpy.SpatialJoin_analysis(points30, pblocks, pblk_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")

    print "Finished: " + name
