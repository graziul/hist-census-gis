import os, sys
import arcpy
import arcpy.mapping
import pandas as pd
import glob
import shapefile
import simpledbf

dir_path = sys.argv[1]
city = sys.argv[2]
file_name = sys.argv[3]

gis_path = dir_path + "\\GIS_edited\\"
image_path = dir_path + "\\GIS_edited\\1930 ED Maps\\"
files_txt = image_path+'georeferenced_images.txt'

def convert_block(block):
	try:
		new_block = int(block)
		return new_block
	except:
		return None

def remove_fields(shp,keep_field_list):
	if type(keep_field_list) is not list:
		keep_field_list = [keep_field_list]
	if "FID" not in keep_field_list:
		keep_field_list.append("FID")
	if "Shape" not in keep_field_list:
		keep_field_list.append("Shape")

	input_fields = arcpy.ListFields(shp)
	for field in input_fields:
		if field.name not in keep_field_list:
			arcpy.DeleteField_management(shp,field.name)

#print "Working On: " + city
#Create Paths to be used throughout Process
reference_data = gis_path + city + "_1930_stgrid.shp' 'Primary Table'"
grid = gis_path + city + "_1930_stgrid.shp"
dissolve_grid = gis_path+ city + "_1930_stgrid_Dissolve.shp"
split_grid = gis_path+ city + "_1930_stgrid_Split.shp"
pblocks = gis_path+ city + "_1930_Pblk.shp"
in_field_map='''
"'Feature ID' FID VISIBLE NONE;'*From Left' LFROMADD VISIBLE NONE;'*To Left' LTOADD VISIBLE NONE;'*From Right' RFROMADD VISIBLE NONE;
'*To Right' RTOADD VISIBLE NONE;'Prefix Direction' <None> VISIBLE NONE;'Prefix Type' <None> VISIBLE NONE;'*Street Name' FULLNAME VISIBLE NONE;
'Suffix Type' <None> VISIBLE NONE;'Suffix Direction' <None> VISIBLE NONE;'Left City or Place' CITY VISIBLE NONE;'Right City or Place' CITY VISIBLE NONE;
'Left ZIP Code' <None> VISIBLE NONE;'Right ZIP Code' <None> VISIBLE NONE;'Left State' state VISIBLE NONE;'Right State' state VISIBLE NONE;'Left Street ID' <None> VISIBLE NONE;
'Right Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;
'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;'Max Y value for extent' <None> VISIBLE NONE;'Left parity' <None> VISIBLE NONE;
'Right parity' <None> VISIBLE NONE;'Left Additional Field' <None> VISIBLE NONE;'Right Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE;'''
add_locator = gis_path+ city + "_addloc"
#'Add_30' originates from 'Create 1930 and 1940 Address Files.R' code
addresses = gis_path + city + "_1930_Addresses.csv"
address_fields="Street address;City city;State state"
points30 = gis_path+ city + "_Points30.shp"
pblk_points = gis_path+ city + "_1930_Pblk_Points.shp"
blocks_algo_file = gis_path + city + "_1930_Block_Choice_Map2.shp"
eds_algo_file = gis_path + city + "_1930_ED_Choice_Map.shp"
ocr_pblk = gis_path + city + "_OCR_Pblk.shp"
ocr_ed = gis_path+ city + "_OCR_ED.shp"
temp = gis_path + city + "_temp.shp"

try:
	df = pd.read_stata(file_name)
except:
	df = pd.read_csv(file_name)

#Get block list from microdata
df_no_empty_blocks = df[df['block']!="."]
blocks_micro = df_no_empty_blocks.ed.astype(str).str.cat(df_no_empty_blocks.block.astype(str),sep='-')
blocks_micro = blocks_micro.unique().tolist()
print("Unique blocks (micro): " + str(len(blocks_micro)))
df['block_numeric'] = df['block'].apply(convert_block) 
df['ed_numeric'] = df['ed'].apply(convert_block) 
df_numeric_blocks = df[df['block_numeric'].notnull() & df['ed_numeric'].notnull()]
blocks_micro_numeric = df_numeric_blocks.ed.astype(str).str.cat(df_numeric_blocks.block.astype(str),sep='-')
blocks_micro_numeric = blocks_micro_numeric.unique().tolist()
print("Entirely numeric blocks (micro): " + str(len(blocks_micro_numeric)) + "\n")
#print(blocks_micro_numeric)

#Load blocks shapefile to get block list
sf_blocks = shapefile.Reader(blocks_algo_file)
fields = sf_blocks.fields[1:] 
for i, item in enumerate(fields):
	if item[0] == 'MBID':
		position = i

#Get 100% certainty block list from algorithm
#blocks_algo = [r.record[-7] for r in sf_blocks.shapeRecords()]
blocks_algo = [r.record[position] for r in sf_blocks.shapeRecords()]
blocks_algo = list(set(blocks_algo))
blocks_algo.sort()
blocks_algo.pop(0) #Blocks without numbers are whitespace, this removes that entry
print("Unique blocks (algo): " + str(len(blocks_algo)))
blocks_algo_numeric = [i for i in blocks_algo if convert_block(i.split('-')[-1]) is not None]
print("Entirely numeric blocks (algo): " + str(len(blocks_algo_numeric)) + "\n")

#Summarize algorithm results
numeric_algo = len(blocks_algo_numeric)
numeric_micro = len(blocks_micro_numeric)
per_algo_id = round(100*float(numeric_algo)/numeric_micro,1)
print("Algorithm identified " + str(numeric_algo) + " of " + str(numeric_micro) + " (" + str(per_algo_id) + "%) numeric microdata blocks\n")

#Create list of blocks in microdata but not identified by algorithm
blocks_to_find = [i for i in blocks_micro_numeric if i not in blocks_algo_numeric]
#print(blocks_to_find)

current_image = image_path + city + "_current_image.shp"

def add_ocr(image_num):

	# Spatial join OCR shapefile to (calculated) ED shapefile 
	arcpy.SpatialJoin_analysis(target_features=eds_algo_file, join_features=files[image_num], out_feature_class=current_image, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="INTERSECT",search_radius="", distance_field_name="")

	# Add field for block-ed and populate 
	arcpy.AddField_management(current_image,"im_blk%s" % (str(image_num+1)),"TEXT")
	block_ed_expression = 'str(int(!ED_ID!))+"-"+!block_ocr!.strip()'
	arcpy.CalculateField_management (current_image, "im_blk%s" % (str(image_num+1)), block_ed_expression,"PYTHON")

	# Make sure OCR block guess is in the list of blocks to find
	cursor = arcpy.da.UpdateCursor(current_image,["im_blk%s" % (str(image_num+1))])
	for row in cursor:
		ocr_blk = row[0]
		if ocr_blk not in blocks_to_find:
			row[0] = ''
		else:
			row[0] = ocr_blk
		cursor.updateRow(row)
	del row
	del cursor

	# Remove extraneous fields
	keep_field_list = "im_blk%s" % (str(image_num+1))
	remove_fields(current_image,keep_field_list)

	# If first image, use current_image to create base ocr_pblk shapefil
	if image_num == 0:
		arcpy.CopyFeatures_management(current_image,ocr_pblk)
	else:
		arcpy.JoinField_management(in_data=ocr_pblk,in_field="FID",join_table=current_image,join_field="FID")
	arcpy.Delete_management(current_image)

	# If it's the last image, add OCR shapefiles to algo shapefile 
	if image_num+1 == len(files):
		arcpy.CopyFeatures_management(blocks_algo_file,temp)
		arcpy.JoinField_management(in_data=temp,in_field="FID",join_table=ocr_pblk, join_field="FID")
		arcpy.Delete_management(ocr_pblk)
		arcpy.CopyFeatures_management(temp,ocr_pblk)
		arcpy.Delete_management(temp)

with open(files_txt,'r') as f:
	files = f.read().splitlines()
	files = [f.replace(".tif",".shp") for f in files]

for i in range(len(files)):
	add_ocr(i)

ocr_pblk_dbf = ocr_pblk.replace(".shp",".dbf")
dbf = simpledbf.Dbf5(ocr_pblk_dbf)
df = dbf.to_dataframe()

print("OCR blocks identified")
total = 0
to_guess = df[df['MBID'].isnull()]
#to_guess = df[df['FirstE'].isnull()]

for i in range(len(files)):
	img_tot = to_guess['im_blk%s' % (str(i+1))].notnull().sum()
	print("Image %s: %s" % (str(i+1),str(img_tot)))
	total += img_tot
print("Total: %s\n" % (str(total)))

im_blks = [name for name in df.columns.values if "im_blk" in name]
df_im_blks = to_guess[im_blks]

guessed = df_im_blks.notnull().any(axis=1).sum()
per_guessed = round(100*float(guessed)/numeric_micro,1)
print("OCR returned plausible guesses for " + str(guessed) + " of " + str(numeric_micro) + " (" + str(per_guessed) + "%) numeric microdata blocks")

#tot_algos = guessed + numeric_algo
#per_tot_algos = round(100*float(tot_algos)/numeric_micro,1)
#print("\nTotal blocks identified/guessed: " + str(tot_algos) + " of " + str(numeric_micro) + " (" + str(per_tot_algos) + "%)"+"\n")
