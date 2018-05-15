import arcpy
import numpy as np

#spatial join target=pblk file, join=Uns2, share_a_LINE_SEGMENT, join the grid_ids of all street segments for each block
#format the joined grid ID field so it is like: (1047,1048,1081,168,197,218,219)

with open('ed_blk_desc.txt','r') as blk_desc_file :
    blk_desc = blk_desc_file.readlines()

for ind,line in enumerate(blk_desc) :
    blk_desc[ind] = line.strip()    

join_file = r'C:\Users\akisch\Documents\ArcGIS\Default.gdb\Worcester_1930_Pblk_SpatialJ12'
st_file = r'C:\Users\akisch\Documents\ArcGIS\Default.gdb\Worcester_Uns2'

fullname_var = "FULLNAME"

blk_desc_dict = {} # lookup SM ed_blk identifier -> SM description of block
blk_gridID_dict = {} # lookup pblk_id -> string of grid_ids of streets comprising boundary of block
blk_fullname_dict = {} # lookup pblk_id -> list of fullnames of streets comprising boundary of block
fullname_blk_dict = {} # lookup alphabetical, unique tuple of streets comprising boundary of block -> pblk_id of block
pblk_ed_blk_dict = {} # lookup pblk_id -> SM ed_blk identifier

for line in blk_desc :
    line = line.split(', ')
    blk = line[1].split('-')[1]
    blk_desc_dict[blk] = list(np.unique(line[2:]))

arcpy.MakeFeatureLayer_management(st_file, "st_lyr")
with arcpy.da.SearchCursor(join_file,['pblk_id','grid_id_str']) as b_cursor :
    for b_row in b_cursor :
        blk = b_row[0]
        seg_str = b_row[1]
        blk_gridID_dict[blk] = seg_str
        arcpy.SelectLayerByAttribute_management("st_lyr", 'NEW_SELECTION', '"grid_id" IN '+seg_str)
        with arcpy.da.SearchCursor("st_lyr",['grid_id',fullname_var]) as s_cursor :
            stname_list = []
            for s_row in s_cursor :
                stname_list.append(str(s_row[1]))
            stname_list = list(np.unique(stname_list))
            blk_fullname_dict[blk] = stname_list
            fullname_blk_dict[tuple(stname_list)] = blk

def find_blk_by_stnames(stname_list) :
    try :
        return fullname_blk_dict[tuple(stname_list)]
    except KeyError :
        print(str(stname_list) +" not found")
        #work out some kind of inexact matching?

for ed_blk, stname_list in blk_desc_dict.items() :
    pblk = find_blk_by_stnames(stname_list)
    if pblk :
        pblk_ed_blk_dict[pblk] = ed_blk

arcpy.AddField_management(join_file, "ED", "TEXT", "", "", 20)
arcpy.AddField_management(join_file, "cblk_id", "TEXT", "", "", 20)
with arcpy.da.UpdateCursor(join_file,['pblk_id','ED','cblk_id']) as b_cursor :
    for row in b_cursor :
        try :
            ed_blk = pblk_ed_blk_dict[row[0]]
            row[1] = ed_blk.split('_')[0]
            row[2] = ed_blk.split('_')[1]
            b_cursor.updateRow(row)
        except KeyError :
            continue
        
