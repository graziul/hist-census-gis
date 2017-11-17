# Build ED and block maps based on manual and automatic cleaning

# File where everything has been edited is EmptyBlockToFillNumbers2.shp for St Louis

import re
import arcpy
import pandas as pd
import pysal as ps
import os

arcpy.env.overwriteOutput=True

def dbf2DF(dbfile, upper=False): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile) #Pysal to open DBF
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    #pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    if upper == True: #Make columns uppercase if wanted 
        pandasDF.columns = map(str.upper, db.header) 
    db.close() 
    return pandasDF

file_path = "S:\\Projects\\1940Census\\StLouis" 
city_name = "StLouis"
state_abbr = "MO"
dir_path = file_path + "\\GIS_edited\\"
edit_shp_file = dir_path + "EmptyBlockToFillNumbers2.shp"
block_shp_file = dir_path + city_name + "_1930_block_ED_checked.shp"
temp_shp_file = dir_path + city_name + "_1930_block_temp.shp"

arcpy.CopyFeatures_management(edit_shp_file,temp_shp_file)

dbf_file = dir_path + city_name + "_1930_block_temp.dbf"
df = dbf2DF(dbf_file,upper=False)

#Code to clean up automatic block numbers

#Turn ED=0 into blank 
df['ed1'] = df['ed'].astype(str).replace('0','')
#Add ED to manual block numbers
df['block1'] = df['ed1'] + '-' + df['block']
df['block1'] = df['block1'].replace('^-|-$','',regex=True)
df.loc[df['block']=='','block1'] = ''
df.loc[df['ed']==0,'block1'] = ''

#Replace spaces and "and" with "-"
df['auto_bn1'] = df['auto_bn'].str.replace(' ','-')
df['auto_bn1'] = df['auto_bn1'].str.replace('and','-')
df['auto_bn1'] = df['auto_bn1'].replace('-+','-',regex=True)

#Start with manual block numbers (some automatic block numbers have been fixed)
df['am_bn'] = df['block1']
#Add automatic block numbers where there is no manual block number
df.loc[df['D']==0,'am_bn'] = df['auto_bn1']

# Save as dbf via csv
csv_file = dir_path + "\\temp_for_dbf.csv"
df.to_csv(csv_file)
arcpy.TableToTable_conversion(csv_file,dir_path,"temp_for_shp.dbf")
os.remove(dbf_file)
os.remove(csv_file)
os.rename(dir_path+"\\temp_for_shp.dbf",dbf_file)
os.remove(dir_path+"\\temp_for_shp.dbf.xml")
os.remove(dir_path+"\\temp_for_shp.cpg")

arcpy.MakeFeatureLayer_management(temp_shp_file,"edit_lyr")
arcpy.SelectLayerByAttribute_management("edit_lyr", "", ' "am_bn" <> \'\' ')
arcpy.CopyFeatures_management("edit_lyr",block_shp_file)
arcpy.DeleteFeatures_management(temp_shp_file)

#Dissolve by "am_bn"
arcpy.Dissolve_management(in_features=block_shp_file, out_feature_class=temp_shp_file, dissolve_field=["am_bn","ed"], statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
#Generate unique block ID
expression="!FID! + 1"
arcpy.AddField_management(temp_shp_file, "pblk_id", "LONG", 4, "", "","", "", "")
arcpy.CalculateField_management(temp_shp_file, "pblk_id", expression, "PYTHON_9.3")
arcpy.CopyFeatures_management(temp_shp_file,block_shp_file)
arcpy.DeleteFeatures_management(temp_shp_file)



#### Could write dictionary to assign blocks {block:ed} that could then be used to fill in ED

# Next script is FixDirUsingED.py