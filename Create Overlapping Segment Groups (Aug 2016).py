#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys

#Set Workspace

#Finished "Atlanta", "Baltimore", "Charleston", "Louisville", "Memphis",
# "Mobile", "Nashville", "New Orleans", "Richmond", "Washington",
# "Albany", "Allegheny", "Boston", "Brooklyn", "Buffalo",  "Chicago", "Cincinnati", "Cleveland", "Columbus", "Denver", "Detroit", "Hartford",
# "Indianapolis", "JerseyCity", "KansasCity", "Milwaukee", "Minneapolis", "NYC_Manhattan", "NYC_Bronx", "Newark", "Oakland", "Omaha",
# "Philadelphia", "Pittsburgh","Providence", "Rochester", "San Francisco", "St_Louis", "St_Paul"
# "New Haven"

# overwrite output
arcpy.env.overwriteOutput=True

for name in ["Atlanta", "Baltimore", "Charleston", "Louisville", "Memphis",
"Mobile", "Nashville", "New Orleans", "Richmond", "Washington"]:
    
    print "Working On: " + name + ".shp"
#Join Segment File to Itself
    target_features = "Z:\Projects\Preparing 1880 Files\\" + name + "\Street Grid Without Ranges\\" + name + "_StreetGrid.shp"
    join_features = "Z:\Projects\Preparing 1880 Files\\" + name + "\Street Grid Without Ranges\\" + name + "_StreetGrid.shp"
    out_1="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Join.shp"
    arcpy.SpatialJoin_analysis(target_features, join_features, out_1, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
#Create unique id which is combination of the two segment ids
    Table="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Join.shp"
    expression="!Seg_id!" + "!Seg_id_1!"
    arcpy.AddField_management(Table, "UniqID", "TEXT", field_length=50)
    arcpy.CalculateField_management(Table, "UniqID", expression, "PYTHON_9.3")
#Dissolve by the unique segment id created in the last step
    out_2="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Dissolve.shp"
    arcpy.Dissolve_management(Table, out_2, "Seg_id_1")
#Create the Segment Group ID variable i.e. the overlapping segment group identifier
    Table_2="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Dissolve.shp"
    expression_2="!Seg_id_1!"
    arcpy.AddField_management(Table_2, "SegGrID", "LONG")
    arcpy.CalculateField_management(Table_2, "SegGrID", expression_2, "PYTHON_9.3")

#Create Extended Overlapping Segment Groups

#Join Segment Group File to Itself
    target_features_2 = "Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Dissolve.shp"
    join_features_2 = "Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Dissolve.shp"
    out_3="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Join.shp"
    arcpy.SpatialJoin_analysis(target_features_2, join_features_2, out_3, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
#Create unique id which is combination of the two segment ids
    Table_3="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Join.shp"
    expression_3="!Seg_id_1!" + "!SegGrID_1!"
    arcpy.AddField_management(Table_3, "UniqID", "TEXT", field_length=50)
    arcpy.CalculateField_management(Table_3, "UniqID", expression_3, "PYTHON_9.3")
#Join Segment group file (OverSeg_Join) with the Extended segment group file (ExtSeg_Join) by UniqID keeping only matching records.
    in_field="UniqID"
    in_data = "Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Join.shp"
    layername = "tempjoin"
    join_table = "Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_OverSeg_Join.shp"
    out_4="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Join2.shp"
    arcpy.MakeFeatureLayer_management(in_data, layername)
    arcpy.env.qualifiedFieldNames = False
    arcpy.AddJoin_management(layername, in_field, join_table, in_field, "KEEP_COMMON")
    arcpy.CopyFeatures_management(layername, out_4)
#Dissolve by the unique Segment Group id
    Table_4="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Join2.shp"
    out_5="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Dissolve.shp"
    arcpy.Dissolve_management(Table_4, out_5, "SegGrID_1")
#Create the Extended Segment Group ID variable i.e. the overlapping extended segment group identifier
    Table_5="Z:\Users\_Exchange\\1880 Stuff\AllCities\\" + name + "\\" + name + "_ExtSeg_Dissolve.shp"
    expression_3="!SegGrID_1!"
    arcpy.AddField_management(Table_5, "ExtSegGrID", "LONG")
    arcpy.CalculateField_management(Table_5, "ExtSegGrID", expression_3, "PYTHON_9.3")









    
