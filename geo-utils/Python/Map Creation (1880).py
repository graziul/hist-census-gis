#Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.

import arcpy
import os
import sys
import csv

#Set Workspace

#Line 10 #FINISHED "Albany", "Allegheny", "Atlanta", "Baltimore", "Boston", "Brooklyn", "Buffalo", "Charleston",
# "Chicago", "Cincinnati", "Cleveland", "Columbus", "Denver", "Detroit", "Hartford", "Indianapolis", "JerseyCity", "KansasCity", "Louisville", "Memphis", "Milwaukee",
# "Minneapolis", "Mobile", "Nashville","New_Haven", "Newark", "Oakland", "Omaha", "Philadelphia", "Pittsburgh","Providence", "Richmond", "Rochester", "San Francisco",
# "St_Louis", "St_Paul", "NYC_Bronx", "NYC_Manhattan", "Washington", "Indianapolis", "New_Orleans"

#Needs Work 

# overwrite output
arcpy.env.overwriteOutput=True

#"Omaha", "Washington", "NewHaven"
#"ForeignBorn", "German", "Male-Female_SEI"

for name in ["Omaha", "Washington", "NewHaven"]:
    for maptype in ["ForeignBorn", "German", "Male-Female_SEI"]:
        print "Working On: " + name + " - " + maptype + ".mxd"
        
        Addresses = "Z:\Projects\\Preparing 1880 Files\Online Maps\Data\City_Summary - Address\\Address_sum_" + name + ".csv"    
        M = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Multi Unit\\" + name + "_MultiUnit.shp"
        M2 = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Multi Unit\\" + name + "_MultiUnit_2.shp"
        M_Layer= "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Multi Unit\\" + name + "_MultiUnit.lyr"
        Multi = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Multi Unit\\" + name + "_MultiUnit_Data.shp"
        arcpy.CopyFeatures_management(M, M2) # Create Copy of Original Shapefile So it Remains Untouched
        expression_serial="!serial! * 1"
        arcpy.AddField_management(M2, "serial_n", "LONG", "", "", "","", "", "")
        arcpy.CalculateField_management(M2, "serial_n", expression_serial, "PYTHON_9.3")
        #Create a list of fields so that they are maintained throughout creating new shapefile procedure
        arcpy.env.qualifiedFieldNames = False
        fields= arcpy.ListFields(M2)
        fieldinfo= arcpy.FieldInfo()
        fieldmappings = arcpy.FieldMappings()
        fieldinfo= arcpy.FieldInfo()
        arcpy.MakeFeatureLayer_management(M2, M_Layer, "", "", fieldinfo)
        arcpy.AddJoin_management(M_Layer, "serial_n", Addresses, "serial", "KEEP_COMMON")
        arcpy.CopyFeatures_management(M_Layer, Multi)
        
        S = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Single Unit\\" + name + "_SingleUnit.shp"
        S2 = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Single Unit\\" + name + "_SingleUnit_2.shp"
        S_Layer = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Single Unit\\" + name + "_SingleUnit.lyr"
        Single = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Single Unit\\" + name + "_SingleUnit_Data.shp"
        arcpy.CopyFeatures_management(S, S2) # Create Copy of Original Shapefile So it Remains Untouched
        expression_serial="!serial! * 1"
        arcpy.AddField_management(S2, "serial_n", "LONG", "", "", "","", "", "")
        arcpy.CalculateField_management(S2, "serial_n", expression_serial, "PYTHON_9.3")
        #Create a list of fields so that they are maintained throughout creating new shapefile procedure
        arcpy.env.qualifiedFieldNames = False
        fields= arcpy.ListFields(S2)
        fieldinfo= arcpy.FieldInfo()
        fieldmappings = arcpy.FieldMappings()
        fieldinfo= arcpy.FieldInfo()
        arcpy.MakeFeatureLayer_management(S2, S_Layer, "", "", fieldinfo)
        arcpy.AddJoin_management(S_Layer, "serial_n", Addresses, "serial", "KEEP_COMMON")
        arcpy.CopyFeatures_management(S_Layer, Single)

        Segment = "Z:\Projects\\Preparing 1880 Files\Online Maps\Data\City_Summary - Segment\\Segment_sum_" + name + ".csv"
        SG = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Street Grids\\" + name + "_StreetGrid.shp"
        SG2 = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Street Grids\\" + name + "_StreetGrid_2.shp"
        SG_Layer = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Street Grids\\" + name + "_StreetGrid.lyr"
        StreetGrid = "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\Street Grids\\" + name + "_StreetGrid_Data.shp"
        arcpy.CopyFeatures_management(SG, SG2) # Create Copy of Original Shapefile So it Remains Untouched
        expression_segid="!seg_id! * 1"
        arcpy.AddField_management(SG2, "seg_id_n", "LONG", "", "", "","", "", "")
        arcpy.CalculateField_management(SG2, "seg_id_n", expression_segid, "PYTHON_9.3")
        #Create a list of fields so that they are maintained throughout creating new shapefile procedure
        arcpy.env.qualifiedFieldNames = False
        fields= arcpy.ListFields(SG2)
        fieldinfo= arcpy.FieldInfo()
        fieldmappings = arcpy.FieldMappings()
        fieldinfo= arcpy.FieldInfo()
        arcpy.MakeFeatureLayer_management(SG2, SG_Layer, "", "", fieldinfo)
        arcpy.AddJoin_management(SG_Layer, "seg_id_n", Segment, "segment_id", "KEEP_COMMON")
        arcpy.CopyFeatures_management(SG_Layer, StreetGrid)

        ED= "Z:\Projects\\Preparing 1880 Files\Online Maps\Shapefiles\ED\\" + name + "_ED.shp"
        
    # ED Templates #
        temp_ed_online="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\ED_Template_" + maptype + "_New.lyr"
        #temp_ed_new="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\ED_Template_" + maptype + "_New.lyr"
    # Street Grid Templates #
        temp_st_missing="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\StreetGrid_Template_Missing.lyr"
        temp_st="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\Street_Template_" + maptype + ".lyr"
    # Single Unit Templates #
        temp_su="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\SingleUnit_Template_" + maptype + ".lyr"
        temp_su_leg="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\For Legend\\SingleUnit_Template_" + maptype + ".lyr"
    # Multi Unit Templates #
        temp_mu="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\\MultiUnit_Template_" + maptype + ".lyr"
        temp_mu_leg="Z:\Projects\\Preparing 1880 Files\Online Maps\Templates\For Legend\\MultiUnit_Template_" + maptype + ".lyr"
    # MXD Template #                        
        mxd = arcpy.mapping.MapDocument("Z:\Projects\Preparing 1880 Files\Online Maps\\MXDs\\Working_Legend.mxd")
        data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
    #Switch to data view  
        mxd.activeView = data_frame.name

    ##### Bring in Layer Files #####
    #Load ED
        Layer_ED=arcpy.mapping.Layer(ED)
    #Bring In Template Symbology for EDs
        arcpy.ApplySymbologyFromLayer_management(Layer_ED, temp_ed_online) #CHANGE THIS TO ONLINE FOR SECOND SET OF MAPS
    #Zoom To Extent of Newly Added Data
        ext=Layer_ED.getExtent()
        data_frame.extent=ext

    #Load Missing Street Grid
        Layer_Missing_St=arcpy.mapping.Layer(SG)
    #Bring In Template Symbology for Lines
        arcpy.ApplySymbologyFromLayer_management(Layer_Missing_St, temp_st_missing)
    #Place and Edit Labels
        if Layer_Missing_St.supports("LABELCLASSES"):
            for lblclass in Layer_Missing_St.labelClasses:
                lblclass.className = "Street"
                lblclass.expression = '"%s" & [Street] & VBNewLine & "%s"' % ("<FNT name='Arial' size='1'>", "</FNT>")
                lblclass.showClassLabels = True
        Layer_Missing_St.showLabels = True
        arcpy.RefreshActiveView()
    #Load Street Grid
        Layer_L=arcpy.mapping.Layer(StreetGrid)
    #Bring In Template Symbology for Street Grid
        arcpy.ApplySymbologyFromLayer_management(Layer_L, temp_st)
    #Bring In Single Unit Points
        Layer_Single=arcpy.mapping.Layer(Single)
        Layer_Single_Leg=arcpy.mapping.Layer(Single)
    #Bring In Template Symbology for Single Unit Points
        arcpy.ApplySymbologyFromLayer_management(Layer_Single, temp_su)
        arcpy.ApplySymbologyFromLayer_management(Layer_Single_Leg, temp_su_leg)
    #Bring In Multi-Unit Points
        Layer_Multi=arcpy.mapping.Layer(Multi)
        Layer_Multi_Leg=arcpy.mapping.Layer(Multi)
    #Bring In Template Symbology for Single Unit Points
        arcpy.ApplySymbologyFromLayer_management(Layer_Multi, temp_mu)
        arcpy.ApplySymbologyFromLayer_management(Layer_Multi_Leg, temp_mu_leg)

    #Add Legend
        legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]
        legend.autoAdd=True
    #Add ED Layer to MXD
        Layer_ED.name= "ED"
        arcpy.mapping.AddLayer(data_frame, Layer_ED, "TOP") 
    #Add Missing Street Grid Layer to MXD
        Layer_Missing_St.name= ""
        arcpy.mapping.AddLayer(data_frame, Layer_Missing_St, "TOP")
    #Add Street Grid Layer to MXD
        Layer_L.name= "Segments"
        arcpy.mapping.AddLayer(data_frame, Layer_L, "TOP")
        legend.autoAdd=False
    #Add Single Points Layer to MXD
        arcpy.mapping.AddLayer(data_frame, Layer_Single, "TOP")
    #Add Single Points Layer to MXD
        arcpy.mapping.AddLayer(data_frame, Layer_Multi, "TOP")
        legend.autoAdd=True
    #Add Single Points Layer to MXD - LEGEND ONLY
        Layer_Single_Leg.visible=False
        Layer_Single_Leg.name= "Single-Unit Building"
        arcpy.mapping.AddLayer(data_frame, Layer_Single_Leg, "TOP")
    #Add Single Points Layer to MXD - LEGEND ONLY
        Layer_Multi_Leg.visible=False
        Layer_Multi_Leg.name= "Multi-Unit Building"
        arcpy.mapping.AddLayer(data_frame, Layer_Multi_Leg, "TOP")

    #Make Fixes to Legend        
        styleItem_all = arcpy.mapping.ListStyleItems("Z:\Projects\\Preparing 1880 Files\Online Maps\Legend_Style.style", "Legend Items", "")[0]
        for lyr in legend.listLegendItemLayers():
            legend.updateItem(lyr, styleItem_all)
        legend.adjustColumnCount(2)

    #Add Legend Title to Map
        for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                if elm.text == "Label_Title": # whatever your Label element is named here
                    elm.text = maptype + " Composition in:"
                    break
    #Add Title to Map
        for elm2 in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                if elm2.text == "Title": # whatever your text element is named here
                    elm2.text = maptype + " Composition of " + name + " in 1880"
                    break
        print "Writing PDF"

    #Delete Layers Used in Map Creation
        arcpy.Delete_management(M2)
        arcpy.Delete_management(M_Layer)
        arcpy.Delete_management(S2)
        arcpy.Delete_management(S_Layer)
        arcpy.Delete_management(SG2)
        arcpy.Delete_management(SG_Layer)

    #Create PDF 
        arcpy.mapping.ExportToPDF(mxd, "Z:\Projects\\Preparing 1880 Files\Online Maps\Maps\\" + name + "_" + maptype + "_New.pdf",resolution="300",image_quality="BEST",layers_attributes="LAYERS_ONLY")
    #Save MXD File For Each City
        mxd.saveACopy("Z:\Projects\\Preparing 1880 Files\Online Maps\\MXDs\\" + name + "_" + maptype + "_New.mxd")
        
    print "Finished: " + name
