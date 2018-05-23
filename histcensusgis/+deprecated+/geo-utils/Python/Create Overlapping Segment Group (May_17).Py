#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys

# overwrite output
arcpy.env.overwriteOutput=True

for name in ["StLouis"]:
    print "Working On: " + name + ".shp"
    target_features = "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_1930_stgrid_Split.shp"
    join_features = "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_1930_stgrid_Split.shp"
    SegGr_grid = "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_SegGr.shp"                 # This is Segment Group File
    SegGr_grid_c = "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_SegGr_c.shp"
    ExtSegGr_grid = "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_ExtSegGr.shp"            # This is Extented Segment Group File
    expression_Seg_ID="!FID!"
    expression_SegGr="!JOIN_FID!"
    expression_ExtSegGr="\"{}{}\".format(!TARGET_FID!, !JOIN_FID!)"
    expression_Out_Join_2="\"{}{}\".format(!JOIN_FID!, !SegGrID_1!)"
    expression_Final="!SegGrID_1!"
    Out_Join= "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_Join.shp"
    Out_Join_2= "Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_Join_2.shp"
    Out_Join_2_c="Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_Join_2_c.shp"
    Out_Join_2_Layer="Z:\Projects\\1940Census\\" + name + "\GIS_edited\\" + name + "_Out_Join_2.lyr"
    
    
    #Create a list of fields so that they are maintained throughout the join and creating new shapefile procedure
    arcpy.env.qualifiedFieldNames = False
    fields= arcpy.ListFields(SegGr_grid)
    fieldinfo= arcpy.FieldInfo()
    fieldmappings = arcpy.FieldMappings()

    #JUST FOR CHRIS
 #   arcpy.AddField_management(target_features, "Seg_ID", "LONG", 10, "", "","", "", "")
 #   arcpy.CalculateField_management(target_features, "Seg_ID", expression_Seg_ID, "PYTHON_9.3")

    #### STEP 1 #### - Overlapping Segment Groups
    #Join the segment shapefile to itself by 'intersect'
    arcpy.SpatialJoin_analysis(target_features, join_features, Out_Join, "JOIN_ONE_TO_MANY", "KEEP_ALL", fieldmappings, "INTERSECT")
    #Add Field Name called "UniqID" to result in Step 1
    arcpy.AddField_management(Out_Join, "UniqID", "TEXT", "", "", "","", "", "")
    arcpy.CalculateField_management(Out_Join, "UniqID", expression_ExtSegGr, "PYTHON_9.3")
    #Disolve by JOIN_FID
    arcpy.Dissolve_management(Out_Join, SegGr_grid, "JOIN_FID")
    #Add Field Name "SegGrID=JOIN_FID"
    arcpy.AddField_management(SegGr_grid, "SegGrID", "LONG", "", "", "","", "", "")
    arcpy.CalculateField_management(SegGr_grid, "SegGrID", expression_SegGr, "PYTHON_9.3")

    print "Finished:" + name + "SegGr_grid.shp"

    #### STEP 2 #### - Overlapping Extended Segment Groups
    #Create New Shapefile to Join to Itself
    arcpy.CopyFeatures_management(SegGr_grid, SegGr_grid_c)
    #Join SegGr shapefile to itself by 'intersect'
    arcpy.SpatialJoin_analysis(SegGr_grid, SegGr_grid_c, Out_Join_2, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
    #Add Field Name called "UniqID"
    arcpy.AddField_management(Out_Join_2, "UniqID", "TEXT", "", "", "","", "", "")
    arcpy.CalculateField_management(Out_Join_2, "UniqID", expression_Out_Join_2, "PYTHON_9.3")

    
    print "Starting SegGr to SegGr Join Procedure"
    
    ### Join SegGr shapefile to Out_Join_2 by 'UniqID' - Keep Only Mattching Records ###
    #Make Feature Layer to use for Join procedure
    arcpy.MakeFeatureLayer_management(Out_Join_2, Out_Join_2_Layer, "", "", fieldinfo)
    #Join table to layer
    arcpy.AddJoin_management(Out_Join_2_Layer, "UniqID", Out_Join, "UniqID", "KEEP_COMMON")
    #Create new shapefile to be used in Dissolve Procedure
    arcpy.CopyFeatures_management(Out_Join_2_Layer, Out_Join_2_c)

    print "Starting Dissolve Procedure"
    
    #Dissolve Join Result
    arcpy.Dissolve_management(Out_Join_2_c, ExtSegGr_grid, "SegGrID_1")
    #Add Field Name "ExtSegGrID = SegGrID_1"
    arcpy.AddField_management(ExtSegGr_grid, "ExtSegGrID", "LONG", "", "", "","", "", "")
    arcpy.CalculateField_management(ExtSegGr_grid, "ExtSegGrID", expression_Final, "PYTHON_9.3")

    #Delete Unecessary Files
    arcpy.Delete_management(Out_Join)
    arcpy.Delete_management(Out_Join_2_c)
    arcpy.Delete_management(SegGr_grid_c)
    arcpy.Delete_management(Out_Join_2_Layer)
    arcpy.Delete_management(Out_Join_2)  
    
    print "Finished: " + name + "ExSegGr.shp"

