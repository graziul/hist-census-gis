#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys

#Set Workspace

#Line 10 #FINISHED "Albany", "Allegheny", "Atlanta", "Baltimore", "Boston", "Brooklyn", "Buffalo", "Charleston",
# "Chicago", "Cincinnati", "Cleveland", "Columbus", "Denver", "Detroit", "Hartford", "Indianapolis", "JerseyCity", "KansasCity", "Louisville", "Memphis", "Milwaukee",
# "Minneapolis", "Mobile", "Nashville","New_Haven", "Newark", "Oakland", "Omaha", "Philadelphia", "Pittsburgh","Providence", "Richmond", "Rochester", "San Francisco",
# "St_Louis", "St_Paul", "NYC_Bronx", "NYC_Manhattan", "Washington", "Indianapolis", "New_Orleans"

#Needs Work 

# overwrite output
arcpy.env.overwriteOutput=True

for name in ["NYC_Bronx", "KansasCity","NYC_Manhattan", "New_Haven", "New_Orleans", "JerseyCity", "St_Paul", "St_Louis"]:
    print "Working On: " + name + ".mxd"
    Eth_Points = "Z:\Users\Matt\Segregation Project_Irish and Germans\Shapefiles\\" + name + "_Eth_Points.shp"
    Category_Pts = "Z:\Users\Matt\Segregation Project_Irish and Germans\Shapefiles\\" + name + "_Category_Pts.shp"
    Lines= "Z:\Projects\Preparing 1880 Files\\" + name + "\Street Grid Without Ranges\\" + name + "_StreetGrid.shp"
    temp_lines="Z:\Users\Matt\Segregation Project_Irish and Germans\MXDs\\template_lines.lyr"
    temp_points="Z:\Users\Matt\Segregation Project_Irish and Germans\MXDs\\template_points.lyr"
    mxd = arcpy.mapping.MapDocument("Z:\Users\Matt\Segregation Project_Irish and Germans\MXDs\Working.mxd")
    data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
#Switch to data view  
    mxd.activeView = data_frame.name
#Load Lines
    Layer_L=arcpy.mapping.Layer(Lines)
#Bring In Template Symbology for Lines
    arcpy.ApplySymbologyFromLayer_management(Layer_L,temp_lines)
#Place and Edit Labels
    if Layer_L.supports("LABELCLASSES"):
        for lblclass in Layer_L.labelClasses:
            lblclass.className = "Street"
            lblclass.expression = '"%s" & [Street] & VBNewLine & "%s"' % ("<FNT name='Arial' size='2'>", "</FNT>")
            lblclass.showClassLabels = True 
    Layer_L.showLabels = True
    arcpy.RefreshActiveView()
#Add Line Layer to MXD
    arcpy.mapping.AddLayer(data_frame, Layer_L, "TOP")
#Load Points
    Layer_P=arcpy.mapping.Layer(Eth_Points)
#Bring in Template Symbology for Points
    arcpy.ApplySymbologyFromLayer_management(Layer_P,temp_points)
#Add Points Layer to MXD
    arcpy.mapping.AddLayer(data_frame, Layer_P, "TOP")
#Add Title to Map
    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elm.text == "Text": # whatever your text element is named here
                elm.text = name + " 1880"
                break
    print "Writing PDF"
    
#Create PDF 
    arcpy.mapping.ExportToPDF(mxd, "Z:\Users\Matt\Segregation Project_Irish and Germans\\Output\\" + name + ".pdf",resolution="300",image_quality="BEST",layers_attributes="LAYERS_ONLY")
#Save MXD File For Each City
    mxd.saveACopy("Z:\Users\Matt\Segregation Project_Irish and Germans\\MXDs\\" + name + ".mxd")

    print "Finished: " + name
