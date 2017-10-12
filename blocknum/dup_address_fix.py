#Automatic re-addressing program. Created by Amory Kisch.
#Input: a shapefile or geodatabase with identical street segments
#       "identical" in this case means same street name and same address ranges
#Output: a csv with corrected address ranges, where the duplicate ranges are distributed
#       across the segments proportional to their relative length

import arcpy, os
import pandas as pd


# Change directory to the folder with the input text file:  
os.chdir(r'C:\Users\akisch\Desktop')
shp = r'C:\Users\akisch\Documents\ArcGIS\Default.gdb\footemps'

#Calculate starting and ending coordinates and length for each line segment
arcpy.AddGeometryAttributes_management(shp, "LENGTH_GEODESIC;LINE_START_MID_END")

data = []

fields = arcpy.ListFields(shp)
field_names = [field.name for field in fields]

for row in arcpy.SearchCursor(shp) :
    data.append([row.getValue(field.name) for field in fields])

df = pd.DataFrame(data, columns=field_names)

# need dup_id, num_feat

grouped = df.groupby(["FULLNAME","LFROMADD","LTOADD","RFROMADD","RTOADD"])

df["IN_FID"] = grouped.grouper.group_info[0]

#There is no simple way to assign _n of each group to a variable in the dataframe
# so use Chris Graziul's dict workaround.
foo = {}
#create dict: keys: group IDs ; values: number of items in group
for g, d in grouped :
	foo[g] = d["OBJECTID"].count()
df['size'] = df.apply(lambda x : foo[x["FULLNAME"],x["LFROMADD"],x["LTOADD"],x["RFROMADD"],x["RTOADD"]], axis=1)


df = df[["OBJECTID","LFROMADD","LTOADD","RFROMADD","RTOADD","IN_FID","LENGTH_GEO","size","START_X","END_X","START_Y","END_Y"]]


addresses = open('new_addresses.csv', 'wt')
addresses.write("fid,l_f_add,l_t_add,r_f_add,r_t_add,short_segment\n")

df = df.sort_values('IN_FID')

for col in df :
    df[col] = df[col].astype(str)
DList = df.values.tolist()

TopoErrors = []

ind = 0

#########################################################
#input file should be in format :
#fid;l_f_add;l_t_add;r_f_add;r_t_add;in_fid;new_length;num_identical;start_x;end_x;start_y;end_y
#########################################################

while ind < len(DList) :
    feat_seq = DList[ind][5] # actually in_fid, as feat_seq was unreliable.
    feat_num = int(DList[ind][7]) # number of features
    feat_list = DList[ind : ind+feat_num] #list of features that comprised the original feature
    if feat_num > 1 :
        ##find beginning segment##
        start_segment = False
        i=0
        topology_error = False
        while start_segment == False and i<feat_num:
            start_segment = True
            start = (DList[ind+i][8]+" "+DList[ind+i][10]).strip()
            for feat in feat_list :
                end = (feat[9]+" "+feat[11]).strip()
                if end == start :
                    start_segment = False
                    i= i +1
                    #print "found a connexion. i is now %d",i
                    break
        if start_segment==False : #could not find a start segment
            #print "PANIC"
            #probably topology or parsing error; or we are dealing with a circular street segment
            #pretend that the first segment in the input order is the start segment
            i=0        
        ##put feat list in order of street direction##
        o_feat_list = []
        o_feat_list.append(DList[ind+i])
        order_num = 1
        end = (o_feat_list[0][9]+" "+o_feat_list[0][11]).strip()
        feat_length = float(o_feat_list[0][6])
        while order_num < feat_num :
            for j,feat in enumerate(feat_list) :
                start = (feat[8]+" "+feat[10]).strip()
                if start == end :
                    end = (feat[9]+" "+feat[11]).strip()
                    order_num= order_num + 1
                    feat_length = feat_length + float(feat[6])
                    o_feat_list.append(feat)
                    
                    break
                if j==feat_num-1 :
                    print ("topological error (there is a gap)~~~~~~~~~~~~~~!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~")
                    TopoErrors.append(DList[ind+order_num])
                    topology_error = True
                    order_num= order_num + 1
        if topology_error==False :
            try :
                LFAdd = int(o_feat_list[0][1])
            except ValueError:
                LFAdd = 0
            try :
                LTAdd = int(o_feat_list[0][2])
            except ValueError:
                LTAdd = 0
            try :
                RFAdd = int(o_feat_list[0][3])
            except ValueError:
                RFAdd = 0
            try :
                RTAdd = int(o_feat_list[0][4])
            except ValueError:
                RTAdd = 0
            debug = False
            #print("feat_seq: "+str(feat_seq)+", num segments: "+str(feat_num)+", add range: "+str(LFAdd)+"-"+str(LTAdd)+" "+str(RFAdd)+"-"+str(RTAdd)+"\n")
            if debug==True:
                addresses.write("feat_seq: "+str(feat_seq)+", name: "+o_feat_list[0][5]+", num segments: "+str(feat_num)+", add range: "+str(LFAdd)+"-"+str(LTAdd)+" "+str(RFAdd)+"-"+str(RTAdd)+"\n")
            
            RRange = (RTAdd - RFAdd)
            LRange = (LTAdd - LFAdd)
            ORange = RRange
            OLange = LRange
            RDir, LDir = 0,0 #Dir: direction addresses are going in.

            final_feat_list = []
            for feat in o_feat_list :
                if round(abs((float(feat[6])/feat_length)*LRange)) < 2 and LRange!= 0 and round(abs((float(feat[6])/feat_length)*RRange)) < 2 and RRange!= 0 :
                    #if feat is too short to contain even a single address (on either side) in its range...
                    feat[1]=feat[2]=feat[3]=feat[4]=0
                    feat_num = feat_num - 1
                    feat_length = feat_length - float(feat[6])
                    addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+",1")
                    if debug==True :
                        addresses.write(" length is "+feat[6]+"/"+str(feat_length)+" which WAS too short\n")
                    else :
                        addresses.write("\n")
                else :
                    final_feat_list.append(feat)

            o_feat_list = final_feat_list
            
            ShortRange = False
            if RRange!=0 :
                RDir = RRange/abs(RRange)
            if LRange!=0 :
                LDir = LRange/abs(LRange)
            if abs(RRange)>2*feat_num : #if address range is NOT too small in comparison to number of segments
                RRange -= 2*(feat_num-1)*RDir #account for the hidden extra 2 address range each time we change segments
            else :
                ShortRange = True
                if debug==True:
                    addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
            if abs(LRange)>2*feat_num :
                LRange -= 2*(feat_num-1)*LDir
            else :
                ShortRange = True
                if debug==True:
                    addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
            assignedLength = 0

            
            
            for j, feat in enumerate(o_feat_list) :
                segmentLength = float(feat[6])
                assignedLength+=segmentLength
                tooShort = False
                if debug==True:
                    addresses.write(str(int(round(((segmentLength/feat_length)*LRange)/2)*2))+" is more than 2. RRange is "+str(RRange)+"\n")
                if j == 0 :
                    feat[1] = LFAdd
                    feat[3] = RFAdd
                else :
                    feat[1] = int(o_feat_list[j-1][2])+2*LDir #if o_feat_list[j-1][2]!=o_feat_list[j-1][1] else int(o_feat_list[j-1][2])
                    feat[3] = int(o_feat_list[j-1][4])+2*RDir #if o_feat_list[j-1][4]!=o_feat_list[j-1][3] else int(o_feat_list[j-1][4])
                    
                print "left range",round(((segmentLength/feat_length)*LRange)/2)*2
                if j == feat_num-1 :
                    feat[2] = LTAdd
                    feat[4] = RTAdd
                else :
                    feat[2] = feat[1] + int(round(((segmentLength/feat_length)*LRange)/2)*2)
                    feat[4] = feat[3] + int(round(((segmentLength/feat_length)*RRange)/2)*2)
                    if feat[2] > LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2) and LDir>0 or LDir<0 and feat[2] < LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2) :
                        feat[2] = LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2)
                        if debug==True:
                            addresses.write("HAD TO ADJUST on LEFT\n")
                    if feat[4] > RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2) and RDir>0 or RDir<0 and feat[4] < RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2):
                        if debug==True:
                            addresses.write("HAD TO ADJUST on RIGHT\n")
                        feat[4] = RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2)
                if RRange == 0 :
                    feat[3] = feat[4] = RFAdd
                if LRange == 0 :
                    feat[1] = feat[2] = LFAdd

                if debug == True :
                    if LDir > 0 and (feat[1] > LTAdd or feat[2] > LTAdd) or LDir < 0 and (feat[1] < LTAdd or feat[2] < LTAdd) or RDir > 0 and (feat[3] > RTAdd or feat[4] > RTAdd) or RDir < 0 and (feat[3] < RTAdd or feat[4] < RTAdd) :
                        addresses.write("THIS SHOULD NOT HAPPEN!\n")
                    addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+" length is "+feat[6]+"/"+str(feat_length)+" which was NOT too short\n")
                else :
                    addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")

    else : #if feature was not split
        feat = DList[ind]
        addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")

    ind+=feat_num


addresses.write("Topology Errors. Must be fixed and re-run script, or re-address manually.\n")
for err in TopoErrors :
    addresses.write(str(err[0])+"\n")

addresses.close()

