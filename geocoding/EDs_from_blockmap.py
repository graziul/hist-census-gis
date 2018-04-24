# -*- coding: utf-8 -*-
import re
import csv
import numpy as np
from codecs import open
import copy
import arcpy
import os

arcpy.env.overwriteOutput = True

city = "ProvidenceRI"

with open(r"S:\Projects\1940Census\city_directory.csv",'rb') as csvfile :
    reader = list(csv.reader(csvfile))
    directory = reader[[x[0] for x in reader].index(city)][1]

stgrid_file = directory+"\\GIS_edited\\"+city+"_1940_stgrid_edit_Uns2.shp"
if not os.path.isfile(stgrid_file) :
    stgrid_file = directory+"\\GIS_edited\\"+city+"_1930_stgrid_edit_Uns2.shp"

city_name = city[:-2]
with open(directory+"\\Textfile\\"+city_name+"_Block_lines_edit.txt",'r',encoding='utf-8-sig', errors='ignore') as blk_txt_file :
    blk_lines = blk_txt_file.readlines()
with open(directory+"\\Textfile\\"+city_name+"_ED_lines_edit.txt",'r',encoding='utf-8-sig', errors='ignore') as ed_txt_file :
    ed_lines = ed_txt_file.readlines()


# Dict: add v(alue) to k(ey), create k if it doesn't exist
def Dict_append(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        Dict[k].append(v)

line_blk_dict = {} #lookup line number -> blk descript
ed_line_dict = {} #lookup ed -> which line numbers
ed_tract_dict = {} #lookup ed -> which tract/area/precinct

#for line in ed_lines :
# FIND BLOCK LINES IN ED LINES???  


for line in blk_lines :
    if line.strip() == "" :
        continue
    if re.search("that part [ceo]f",line.lower()) :
        # Found an ED Line in the Block Line file - insert it into ed_lines in appropriate place
        try :
            line_num = re.search("\(\*([0-9]+)\*\): ?",line).group(1)
            for ind, ed_line in enumerate(ed_lines) :
                ed_line_num = re.search("\(\*([0-9]+)\*\): ?",ed_line).group(1)
                if int(ed_line_num) > int(line_num) :
                    ed_lines.insert(ind,line)
                    #print(str(ind)+": inserted line '"+line.strip()+"' at ind "+str(ind))
                    break
        except Exception as e :
            print("error handling line '"+line.strip()+"'")
            print(e)
            pass
        continue
    line_num = re.search("\(\*([0-9]+)\*\):? ",line)
    try :
        descript = re.sub(re.escape(line_num.group(0)),"",line)
        line_num = int(line_num.group(1))
        if line_num in line_blk_dict :
            print("duplicate line num: "+str(line_num))
        Dict_append(line_blk_dict,line_num, descript.strip())
    except AttributeError:
        print line
        continue
        #assert False




prev_line_num = ""
prev_descript = ""
for ind,line in enumerate(ed_lines) :
    line = line.strip()
    if line == "" or line == "\n" :
        continue

    line_num = re.search("\(\*([0-9]+)\*\): ?",line)
    try :
        descript = re.sub(re.escape(line_num.group(0)),"",line)
    except :
        print(repr(line))
        assert False

    if prev_line_num == "" :
        prev_line_num = int(line_num.group(1))
        prev_descript = descript
        continue
    try :
        ed = re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower()
    except :
        print(prev_descript)
        print(ind)
        assert False
    line_num = int(line_num.group(1))

    Dict_append(ed_line_dict, ed, (prev_line_num+1,line_num-1))

    tract = re.search("\(?(?:Area|Tra[co]?t) ([^\s)]+)",prev_descript)
    try :
        tract = tract.group(1)
        # replace 'l' with '1' where appropriate
        find_l = re.search("l(.+)",tract)
        if find_l :
            tract = re.sub("l(.+)",'1'+find_l.group(1),tract)
        ed_tract_dict[ed] = tract.lower()
    except :
        print "No tract found: "+prev_descript

    prev_line_num = line_num
    prev_descript = descript

#finish adding last ED line to dicts
try :
    Dict_append(ed_line_dict, re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower(), (prev_line_num+1,max(line_blk_dict.keys())))
    ed_tract_dict[re.search("^[\-0-9A-Za-z]+",prev_descript).group(0).lower()] = re.search("\(?(?:Area|Tra[co]?t) (\S+)",prev_descript).group(1).lower()
except :
    print "Problem with last line in ED lines"

tract_blk_ed_dict = {} # lookup tract+" "+census block -> ed

for ed, blk_list in ed_line_dict.items() :
    for blk in blk_list :
        for line in range(blk[0],blk[1]+1) :
            try :
                blk_list = line_blk_dict[line]
            except KeyError :
                continue
            for blk_line in blk_list :
                if re.search("Block|Image",blk_line) :
                    continue
                blk_num = re.search("^([0-9A-Za-z]+)[\-\— ]+",blk_line)
                if blk_num :
                    blk_num = blk_num.group(1)
                    tract = ed_tract_dict[ed]
                    tract_blk_ed_dict[(tract+" "+blk_num).lower()] = ed

##with open(r'C:\Users\akisch\Desktop\StLouis_Missing_EDs.csv','r') as sfile :
##    reader = csv.reader(sfile)
##    reader.next()
##    for line in reader :
##        ed = line[0]
##        tract = line[2]
##        blocks = line[3].split(',')
##        for block in blocks :
##            block = block.strip()
##            tract_blk_ed_dict[(tract+" "+block).lower()] = ed

def assign_EDs() :
    with arcpy.da.UpdateCursor(r'C:\Users\akisch\Desktop\Export_Output.shp',['block','TRACT','SUFFIX','aggr_ed']) as cursor :
        for row in cursor:
            block = row[0]
            TRACT = row[1]
            SUFFIX = row[2]
            try :
                ed = tract_blk_ed_dict[(str(TRACT)[:-2].strip()+""+SUFFIX.strip()+" "+block.strip()).lower()]
                row[3] = ed
                cursor.updateRow(row)
            except KeyError :
                print ("could not find "+"Tract "+(str(TRACT)[:-2].strip()+""+SUFFIX.strip()+" "+block.strip()).lower())


