# Build ED and block maps based on manual and automatic cleaning

# File where everything has been edited is EmptyBlockToFillNumbers2.shp for St Louis

import arcpy

arcpy.env.overwriteOutput=True

file_path = "S:\\Projects\\1940Census\\StLouis" 
city_name = "StLouis"
state_abbr = "MO"
dir_path = file_path + "\\GIS_edited\\"
edit_shp_file = dir_path + "EmptyBlockToFillNumbers2.shp"
block_shp_file = dir_path + city_name + "_1930_block_ED_checked.shp"
ed_shp_file = dir_path + city_name + "_1930_ED.shp"
temp_shp_file = dir_path + city_name + "_1930_temp.shp"
dbf_file = dir_path + city_name + "_1930_temp.dbf"

arcpy.CopyFeatures_management(edit_shp_file,temp_shp_file)
df = load_shp(temp_shp_file)

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

# Save dataframe
save_shp(df, temp_shp_file)

#Select non-missing block numbers
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

#Select non-missing EDs
arcpy.CopyFeatures_management(edit_shp_file,temp_shp_file)
arcpy.MakeFeatureLayer_management(temp_shp_file,"edit_lyr")
arcpy.SelectLayerByAttribute_management("edit_lyr", "", ' "ed" <> 0 ')
arcpy.CopyFeatures_management("edit_lyr",ed_shp_file)
arcpy.DeleteFeatures_management(temp_shp_file)

#Dissolve by "ed"
arcpy.Dissolve_management(in_features=ed_shp_file, out_feature_class=temp_shp_file, dissolve_field=["ed"], statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
arcpy.CopyFeatures_management(temp_shp_file,ed_shp_file)
arcpy.DeleteFeatures_management(temp_shp_file)

#### Could write dictionary to assign blocks {block:ed} that could then be used to fill in ED