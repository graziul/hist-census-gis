# Created: Amory Kisch, 1/8/2018
#
# Purpose: To convert Steve Morse ED text descriptions to ED polygons using historical street grid shapefiles.
#
# Method: For each ED description:
#           1) find an intersection in the street grid that exactly matches the full street phrases of two adjoining
#               streets in the description
#           2) for each of the remaining streets, select all segments that connect the preceding and following streets
#               in the description
#               - if exact matches do not exist, match using just street NAME, and then try fuzzy matching
#           3) create the ED polygon using feature_to_polygon on the selected segments
#               - if correct polygon cannot be created, flag ED for manual checking

from __future__ import print_function
import arcpy
import os
import re
from fuzzywuzzy import fuzz
import pandas as pd


arcpy.env.overwriteOutput = True


# Dict: add v(alue) to k(ey), create k if it doesn't exist
def Dict_append(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        Dict[k].append(v)

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        if not v in Dict[k] :
            Dict[k].append(v)

def Num_Standardize(NAME) :
    NAME = re.sub("^[Tt]enth","10th",NAME)
    NAME = re.sub("^[Ee]leven(th)?","11th",NAME)
    NAME = re.sub("^[Tt]wel[fv]?e?th","12th",NAME)
    NAME = re.sub("^[Tt]hirteen(th)?","13th",NAME)
    NAME = re.sub("^[Ff]ourt[h]?een(th)?","14th",NAME)
    NAME = re.sub("^[Ff]ift[h]?een(th)?","15th",NAME)
    NAME = re.sub("^[Ss]ixt[h]?een(th)?","16th",NAME)
    NAME = re.sub("^[Ss]event[h]?een(th)?","17th",NAME)
    NAME = re.sub("^[eE]ighteen(th)?","18th",NAME)
    NAME = re.sub("^[Nn]inet[h]?e+n(th)?","19th",NAME)
    NAME = re.sub("^[Tt]went[iy]eth","20th",NAME)
    NAME = re.sub("^[Tt]hirt[iy]eth","30th",NAME)
    NAME = re.sub("^[Ff]o[u]?rt[iy]eth","40th",NAME)
    NAME = re.sub("^[Ff]ift[iy]eth", "50th",NAME)
    NAME = re.sub("^[Ss]ixt[iy]eth", "60th",NAME)
    NAME = re.sub("^[Ss]event[iy]eth", "70th",NAME)
    NAME = re.sub("^[Ee]ight[iy]eth", "80th",NAME)
    NAME = re.sub("^[Nn]inet[iy]eth", "90th",NAME)

    NAME = re.sub("[Tt]wenty[ \-]*","2",NAME)
    NAME = re.sub("[Tt]hirty[ \-]*","3",NAME)
    NAME = re.sub("[Ff]orty[ \-]*","4",NAME)
    NAME = re.sub("[Ff]ifty[ \-]*","5",NAME)
    NAME = re.sub("[Ss]ixty[ \-]*","6",NAME)
    NAME = re.sub("[Ss]eventy[ \-]*","7",NAME)
    NAME = re.sub("[Ee]ighty[ \-]*","8",NAME)
    NAME = re.sub("[Nn]inety[ \-]*","9",NAME)
    
    if re.search("(^|[0-9]+.*)([Ff]irst|[Oo]ne)",NAME) : NAME = re.sub("([Ff]irst|[Oo]ne)","1st",NAME)
    if re.search("(^|[0-9]+.*)([Ss]econd|[Tt]wo)",NAME) : NAME = re.sub("([Ss]econd|[Tt]wo)","2nd",NAME)
    if re.search("(^|[0-9]+.*)([Tt]hird|[Tt]hree)",NAME) : NAME = re.sub("([Tt]hird|[Tt]hree)","3rd",NAME)
    if re.search("(^|[0-9]+.*)[Ff]our(th)?",NAME) : NAME = re.sub("[Ff]our(th)?","4th",NAME)
    if re.search("(^|[0-9]+.*)([Ff]ifth|[Ff]ive)",NAME) : NAME = re.sub("([Ff]ifth|[Ff]ive)","5th",NAME)
    if re.search("(^|[0-9]+.*)[Ss]ix(th)?",NAME) : NAME = re.sub("[Ss]ix(th)?","6th",NAME)
    if re.search("(^|[0-9]+.*)[Ss]even(th)?",NAME) : NAME = re.sub("[Ss]even(th)?","7th",NAME)
    if re.search("(^|[0-9]+.*)[Ee]igh?th?",NAME) : NAME = re.sub("[Ee]igh?th?","8th",NAME)
    if re.search("(^|[0-9]+.*)[Nn]in(th|e)+",NAME) : NAME = re.sub("[Nn]in(th|e)+","9th",NAME)
    
    return NAME

#Returns just the NAME component of the street phrase, if any#
#If second argument is True, return a list of all components 
def isolate_st_name(st,whole_phrase = False) :
    if (st == None or st == '' or st == -1) or (not isinstance(st, str)) :
        return ''
    else :
        TYPE = re.search(" (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$",st)
        if(TYPE) :
            TYPE = TYPE.group(0)
            st = re.sub(TYPE+"$", "",st)
            TYPE = TYPE.strip()
        DIR = re.search("^[NSEW]+ ",st)
        if(DIR) :
            DIR = DIR.group(0)
            st = re.sub("^"+DIR, "",st)
            DIR = DIR.strip()
        st = st.strip()
        
    if whole_phrase :
        return [DIR,st,TYPE]
    else :
        return st

def prepare_map_intersections(stgrid_file) :
    print("Preparing Map Intersections File")
    
    
    if not os.path.exists(path_to_city+"\\IntersectionsIntermediateFiles"):
        os.makedirs(path_to_city+"\\IntersectionsIntermediateFiles")

    city_name, _ =  os.path.splitext(stgrid_file)

    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\fullname_dissolve.shp"
    #dissolve all street segments based on FULLNAME
    arcpy.Dissolve_management(in_features = path_to_city+"\\"+stgrid_file, out_feature_class = latest_stage,
                              dissolve_field=fullname_var, statistics_fields="", multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES")

    previous_stage = latest_stage
    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\fullname_dissolve_split.shp"
    #split street segments at their intersections
    arcpy.FeatureToLine_management(in_features = previous_stage, out_feature_class = latest_stage,
                                   cluster_tolerance="", attributes="ATTRIBUTES")

    previous_stage = latest_stage
    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\split_endpoints.shp"
    #create points at both ends of every split segment
    arcpy.FeatureVerticesToPoints_management(in_features = previous_stage, out_feature_class = latest_stage,
                                             point_location="BOTH_ENDS")

    #calculate x and y coordinates of points
    arcpy.AddGeometryAttributes_management(latest_stage, "POINT_X_Y_Z_M")

    previous_stage = latest_stage
    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\xy_dissolve.shp"
    #dissolve points based on x and y
    arcpy.Dissolve_management(in_features = previous_stage, out_feature_class = latest_stage,
                              dissolve_field="POINT_X;POINT_Y", statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")

    arcpy.AddField_management(in_table = latest_stage, field_name="Interse_ID", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="",
                              field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    #preserve intersection ID field
    arcpy.CalculateField_management(in_table = latest_stage, field="Interse_ID", expression="!FID!", expression_type="PYTHON_9.3", code_block="")

    previous_stage = latest_stage
    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\"+city_name+"_spatial_join.shp"
    target_feature_file = path_to_city+"\\IntersectionsIntermediateFiles\\split_endpoints.shp"
    #join intersection ID back to points file with the rest of the data
    arcpy.SpatialJoin_analysis(target_features = target_feature_file, join_features = previous_stage,
                               out_feature_class = latest_stage, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                               field_mapping="""FID_fullna "FID_fullna" true true false 10 Long 0 10 ,First,#,"""+target_feature_file+""",FID_fullna,-1,-1;"""+fullname_var+""" \""""+fullname_var+"""" true true false 100 Text 0 0 ,First,#,"""+target_feature_file+""","""+fullname_var+""",-1,-1;ORIG_FID "ORIG_FID" true true false 10 Long 0 10 ,First,#,"""+target_feature_file+""",ORIG_FID,-1,-1;POINT_X "POINT_X" true true false 19 Double 0 0 ,First,#,"""+target_feature_file+""",POINT_X,-1,-1;POINT_Y "POINT_Y" true true false 19 Double 0 0 ,First,#,"""+target_feature_file+""",POINT_Y,-1,-1;POINT_X_1 "POINT_X_1" true true false 19 Double 0 0 ,First,#,"""+previous_stage+""",POINT_X,-1,-1;POINT_Y_1 "POINT_Y_1" true true false 19 Double 0 0 ,First,#,"""+previous_stage+""",POINT_Y,-1,-1;Interse_ID "Interse_ID" true true false 10 Long 0 10 ,First,#,"""+previous_stage+""",Interse_ID,-1,-1""",
                               match_option="INTERSECT", search_radius="", distance_field_name="")

    # EXPORT ATTRIBUTE TABLE
    arcpy.ExportXYv_stats(Input_Feature_Class = latest_stage, Value_Field="FID;Join_Count;TARGET_FID;FID_fullna;"+fullname_var+";ORIG_FID;POINT_X;POINT_Y;POINT_X_1;POINT_Y_1;Interse_ID", Delimiter="COMMA",
                          Output_ASCII_File = path_to_city+"\\IntersectionsIntermediateFiles\\"+city_name+"_Intersections.txt", Add_Field_Names_to_Output="ADD_FIELD_NAMES")

def get_intersect_by_stnames(stlist) :
    try :
        in_common = set(ST_Intersect_dict[stlist[0]])
    except KeyError :
        return []
    for st in stlist[1:] :
        try :
            in_common = in_common & set(ST_Intersect_dict[st])
        except KeyError :
            return []
    return list(in_common)

def get_block_by_intersections(i1,i2) :
    in_common = [x for x in Intersect_BLOCK_dict[i1] if x in Intersect_BLOCK_dict[i2]]
    if in_common :
        try :
            assert len(in_common) == 1
        except :
            print("Warning: More than one block "+str(in_common)+" associated with intersections "+str(i1)+" & "+str(i2))
        return in_common[0]
    else :
        print("NO BLOCK FOUND FOR INTERSECTIONS "+str(i1)+" and "+str(i2))

# looks for duplicate adjacent elements and deletes one
# iterate backwards to avoid problems with iterating and modifying list simultaneously...!
def f7(seq):
    ind = len(seq) - 2
    while ind >= 0 :
        if seq[ind] == seq[ind+1] :
            del seq[ind+1]
        ind -= 1
    return seq

#compares st1 with st2, which can be a string or a list of strings
#if list, return True if st1 matches with ANY string in st2
def fuzzy_st_test(st1,st2) :
    threshold = 80
    if isinstance(st2,str) :
        st1 = st1.lower()
        st2 = st2.lower()
        return fuzz.ratio(st1,st2) >= threshold
    if isinstance(st2,list) :
        st1 = st1.lower()
        for s in st2 :
            s = s.lower()
            if fuzz.ratio(st1,s) >= threshold :
                return True
        return False

#don't have to worry about KeyError because first vertex always has None as its parent
def get_predecessors(pre_dict,v) :
    orig_v = v
    l = []
    while pre_dict[v] and pre_dict[v] != orig_v :
        l.append(pre_dict[v])
        v = pre_dict[v]
    return l

def find_descript_segments1(descript,intersect,start_ind,start_streets,fuzzy = False,debug = False) :

    finished = False
    
    start = intersect[0]
    predecessor_dict = {start:None} #record path traversed by search: lookup intersection -> ID of prev intersection
    visited, queue = set(), [start]
    cur_name = isolate_st_name(start_streets[1])
    start_ind = (start_ind + 1) % len(descript)
    assert(cur_name == descript[start_ind])
    next_name = descript[(start_ind+1)%len(descript)]
    if debug:print("cur_name: "+cur_name)
    if debug:print("next_name: "+next_name)
    descript_ind = 1
    while queue :
        found_next = False
        vertex = queue.pop(0)
        if debug:print("vertex: "+str(vertex))
        if debug:print("rest of queue: "+str(queue))
        if vertex not in visited : #update visited to at least be the so-far path of correct intersections
            if vertex == start and descript_ind > 1 and descript_ind < len(descript) :
                return False,str(filter(None,predecessor_dict.values())).replace("'","").replace("[","(").replace("]",")")+" "+next_name
            if descript_ind == len(descript)+1 and vertex == start :
                if debug:print("THIS SHOULD NOT HAPPEN BECAUSE THE START VERTEX SHOULD ALREADY BE IN VISITED")
                if debug:print(predecessor_dict)
                #assert(False)
                queue = []
                finished = True
                if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
                pre = predecessor_dict[vertex]
                string = "("+str(pre)+","
                pre_ind = 0
                while pre != start and pre_ind <= len(predecessor_dict.items()) + 10:
                    pre = predecessor_dict[pre]
                    string+=str(pre)+","
                    pre_ind += 1
                string = string[:-1]+")"
                if pre == start :
                    return finished,string
                else :
                    return finished,"erroneous starting intersection: "+str(start)+string

            visited.add(vertex)
            new_vertices = []
            for block in Intersect_BLOCK_dict[vertex] :
                #if debug:print("block: "+str(block)+" ("+str(BLOCK_NAME_dict[block])+")")
                if BLOCK_NAME_dict[block] == cur_name or fuzzy and fuzzy_st_test(BLOCK_NAME_dict[block], cur_name) :
                    new_vertices.extend(BLOCK_Intersect_dict[block])
                    
            #if the correct next intersection is already in visited, don't filter it out!
            #check results if using descript_ind rather than x==start as the condition to satisfy this ^
            new_vertices = filter(lambda x : (not x == vertex or (next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x]))) and not x == predecessor_dict[vertex] and not x in queue and (not x in visited or (x==start and (next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x])))), new_vertices)
            #new_vertices = filter(lambda x : not x == vertex and not x == predecessor_dict[vertex] and not x in queue and (not x in visited or next_name in Intersect_NAME_dict[x] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[x])), new_vertices)
            if debug:print("new_vertices: "+str(new_vertices))
            for v in new_vertices :
                predecessor_dict[v] = vertex
            for v in new_vertices :
                if descript_ind == len(descript) and v == start :
                    queue = []
                    finished = True
                    if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
                    pre = predecessor_dict[v]
                    string = "("+str(pre)+","
                    while pre != start :
                        pre = predecessor_dict[pre]
                        string+=str(pre)+","
                    string = string[:-1]+")"
                    return finished,string
                if next_name in Intersect_NAME_dict[v] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[v]) :
                    if found_next :
                        queue.append(v)
                    else :
                        descript_ind += 1
                        queue = [v]
                    visited = set(get_predecessors(predecessor_dict,v))
                    if debug:print("FOUND THE NEXT STREET! (v = "+str(v)+")")
                    if debug:print("descript_ind: "+str(descript_ind))
                    if debug:print("visited: "+str(visited))
                    #check to see if any additional cur_name blocks intersect with next_name:
                    for block in Intersect_BLOCK_dict[v] :
                        if BLOCK_NAME_dict[block] == cur_name or fuzzy and fuzzy_st_test(BLOCK_NAME_dict[block], cur_name) :
                            aux_vertex = filter(lambda x : not x == v and not x == vertex,BLOCK_Intersect_dict[block])
                            if aux_vertex :
                                assert len(aux_vertex) == 1
                                aux_vertex = aux_vertex[0]
                                if next_name in Intersect_NAME_dict[aux_vertex] or fuzzy and fuzzy_st_test(next_name,Intersect_NAME_dict[aux_vertex]) :
                                    queue.append(aux_vertex)
                                    predecessor_dict[aux_vertex] = v
                                    if debug:print("FOUND ANOTHER CANDIDATE FOR THE NEXT STREET! (v = "+str(aux_vertex)+")")
                    found_next = True
                    #break ### GOOD IDEA???
            if found_next :
                cur_name = next_name
                next_name = descript[(start_ind+descript_ind)%len(descript)]
                if debug:print("cur_name: "+cur_name)
                if debug:print("next_name: "+next_name)
                continue
            else :
                queue.extend(new_vertices)
        elif next_name in Intersect_NAME_dict[vertex] :
            global discovered_problem
            discovered_problem += 1
            if debug:print("OH DEAR :( DISCOVERED PROBLEM :(")
        elif descript_ind == len(descript)+1 and vertex == start :
            queue = []
            finished = True
            if debug:print("FINISHED FINDING ALL STREETS IN ED!!!!!!!!!!")
            pre = predecessor_dict[vertex]
            string = "("+str(pre)+","
            while pre != start :
                pre = predecessor_dict[pre]
                string+=str(pre)+","
            string = string[:-1]+")"
            return finished,string

    return finished,str(filter(None,predecessor_dict.values())).replace("'","").replace("[","(").replace("]",")")+" "+str(vertex)+" "+next_name


def RunAnalysis(city) :

    output = open(city+"_EDs.txt","w+")
    problem_EDs = open(city+"_problem_EDs.txt","w+")

    debug = False

    print("Preparing Input Data for "+city)

    # Create Map DICTs
    for ind, iline in enumerate(InterLines) :
        IList = iline.rstrip().split(",")
        NAME = Num_Standardize(IList[6])
        Dict_append(Intersect_ST_dict,IList[-1],NAME)
        Dict_append(Intersect_NAME_dict,IList[-1],isolate_st_name(NAME))
        Dict_append_unique(ST_Intersect_dict,NAME,IList[-1])
        Dict_append_unique(Intersect_BLOCK_dict,IList[-1],IList[7])
        Dict_append_unique(BLOCK_Intersect_dict,IList[7],IList[-1])
        BLOCK_NAME_dict[IList[7]] = isolate_st_name(NAME)

    # Create Morse DICTs
    for line in Descriptions :
        line_list = line.split(',')
        ED_description_dict[line_list[0]] = [x.strip('"\' \n') for x in line_list[1:]]
        ED_NAME_description_dict[line_list[0]] = [isolate_st_name(x.strip('"\' \n')) for x in line_list[1:]]

    # Isolate St NAMEs
    arcpy.AddField_management (shp_targ, "NAME", "TEXT")
    with arcpy.da.UpdateCursor(shp_targ, [fullname_var,"NAME"]) as up_cursor:
        for row in up_cursor :
            row[1] = isolate_st_name(str(row[0]))
            up_cursor.updateRow(row)

    print("Analyzing ED Descriptions")

    good_EDs = []
    try_fuzzy_EDs = []

    for ED, descript in ED_description_dict.items() :
        #if ED != "486" and ED!="225" and ED!='152':
        #    continue

        #keep only unique street names, but preserve order in description
        descript = f7(descript)
        
        intersect = []
        start_ind = 0
        #find an exactly matching starting intersection
        while start_ind <= len(descript) - 1:
            start_streets = [descript[start_ind], descript[(start_ind+1)%len(descript)]]
            if debug:print("start_streets: "+str(start_streets))
            intersect = get_intersect_by_stnames(start_streets)
            if intersect == [] or start_streets[0] == start_streets[1] :
                start_ind += 1
            else :
                break
        if intersect == [] or start_streets[0] == start_streets[1] :
            if debug:print("Could not find any exactly matching intersections out of "+str(descript))
        else :
            #breadth-first search through block/intersection dicts to find
            #path to intersection with next street in the description

            #change descript to be just the NAMEs of the streets
            descript = ED_NAME_description_dict[ED]
            #keep only unique street names, but preserve order in description
            descript = f7(descript)
            if debug:print(str(ED)+": "+str(descript))

            success, string = find_descript_segments1(descript,intersect,start_ind,start_streets,debug=debug)
            if success :
                output.write(str(ED)+": "+string+"\n")
                ED_Intersect_ID_dict[ED] = string
            else :
                try_fuzzy_EDs.append(ED)

    
    
    for ED in try_fuzzy_EDs :
        descript = ED_description_dict[ED]
        intersect = []
        start_ind = 0

        #keep only unique street names, but preserve order in description
        descript = f7(descript)
        
        #find an exactly matching starting intersection
        while start_ind <= len(descript) - 1:
            start_streets = [descript[start_ind], descript[(start_ind+1)%len(descript)]]
            if debug:print("start_streets: "+str(start_streets))
            intersect = get_intersect_by_stnames(start_streets)
            if intersect == [] :
                start_ind += 1
            else :
                break
        if intersect == [] :
            if debug:print("Could not find any exactly matching intersections out of "+str(descript))
        else :
            #breadth-first search through block/intersection dicts to find
            #path to intersection with next street in the description

            #change descript to be just the NAMEs of the streets
            descript = ED_NAME_description_dict[ED]
            #keep only unique street names, but preserve order in description
            descript = f7(descript)
            if debug:print(str(ED)+": "+str(descript))

            success, string = find_descript_segments1(descript,intersect,start_ind,start_streets,fuzzy = True,debug=debug)
            if success :
                if debug:print("FUZZY WORKED FOR "+str(ED)+"!!!!!!!!!!!!!!!!!!!!!")
                output.write(str(ED)+": "+string+"\n")
                ED_Intersect_ID_dict[ED] = string
            else :
                problem_EDs.write(str(ED)+": "+string+"\n")
                

    if debug:print("discovered_problem: "+str(discovered_problem))

    
    #find_descript_segments(descript,intersect,start_ind,start_streets,fuzzy = True)


    #arcpy.MakeFeatureLayer_management(shp_targ,"lyr","FULLNAME IN ('John St','Liberty St')")

def draw_EDs() :
    arcpy.env.workspace = path_to_city
    output_shp = path_to_city+"\\"+city+"_EDs.shp"
    arcpy.CreateFeatureclass_management(path_to_city,city+"_EDs.shp")
    blk_file = path_to_city+"\\IntersectionsIntermediateFiles\\fullname_dissolve_split.shp"
    arcpy.MakeFeatureLayer_management(blk_file,"blk_lyr")
    arcpy.AddField_management(output_shp, "ED", "TEXT", "", "", 20)

    with arcpy.da.InsertCursor(output_shp, ("SHAPE@", "ED")) as cursor:
        for ED, inter in ED_Intersect_ID_dict.items() :
            inter = inter.replace("(","").replace(")","").split(",") #convert intersect string to list 
            block_list = []
            for ind,i in enumerate(inter) :
                i2 = inter[(ind+1)%len(inter)]
                block_list.append(get_block_by_intersections(i,i2))
            block_str = str(block_list).replace("'","").replace("[","(").replace("]",")")
            arcpy.SelectLayerByAttribute_management ("blk_lyr", "NEW_SELECTION", '"FID" IN '+block_str)
            #arcpy.CopyFeatures_management("blk_lyr", "lyr", "", "0", "0", "0")
            arcpy.FeatureToPolygon_management("blk_lyr", "poly_lyr.shp", "", "ATTRIBUTES", "")
            with arcpy.da.UpdateCursor("poly_lyr.shp",("SHAPE@", "Id")) as icursor:
                for irow in icursor:
                    irow[1]=ED
                    cursor.insertRow(irow)
            #ASSIGN ED # TO POLYGON
            arcpy.SelectLayerByAttribute_management("blk_lyr", "CLEAR_SELECTION")
            #feature_to_polygon on the selected segments
    arcpy.Delete_management ("poly_lyr.shp")

    

arcpy.env.overwriteOutput=True

### THIS IS WHERE YOU ENTER THINGS:
# Change directory to the folder with the input text file:  

fullname_var = "FULLNAME"
decade = 1930


file_path = r'S:\Projects\1940Census\SMdescriptions'

city_info_file = file_path + r'\city_list.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_df = city_info_df[city_info_df['city'].notnull()]
city_state_iterator = [tuple(x.split(', ')) for x in city_info_df['city'].str.lower().unique().tolist()]

# just do first 134 cities for now (138 including 5 borroughs). Also, no 1920 yet.
city_state_iterator = city_state_iterator[:138]

city_list = [x[0].replace("saint","st") for x in city_state_iterator]
state_list = [x[1] for x in city_state_iterator]

city_state_iterator = zip(city_list, state_list)

city_state_iterator = [('providence', 'ri')]

for city_state in city_state_iterator:
    city = city_state[0].title()+city_state[1].upper()
    city_name = city_state[0].title()


    discovered_problem = 0


    assert(city_name == re.sub("[A-Z][A-Z]$","",city))
    path_to_city = "S:\\Projects\\1940Census\\"+city_name+"\\GIS_edited"
    shp_targ = path_to_city+"\\"+city+"_1930_stgrid_edit_Uns2.shp"

    #path_to_city = r"S:\Users\_Exchange\To Amory\Albany"
    #shp_targ = path_to_city+"\\AlbanyNY_1930_edit.shp"

    # LOAD SM DESCRIPTIONS....
    if os.path.isfile(shp_targ) :
        #pass
        prepare_map_intersections(city+"_1930_stgrid_edit_Uns2.shp")
        #prepare_map_intersections("AlbanyNY_1930_edit.shp")
    else :
        print(city+": Error finding stgrid")
        continue

    Descriptions_path = 'S:\\Projects\\1940Census\\SMdescriptions\\'+city_name+'_EDdraw_test.txt'
    Intersect_TXT = open(path_to_city+"\\IntersectionsIntermediateFiles\\"+city+'_1930_stgrid_edit_Uns2_Intersections.txt')
    #Intersect_TXT = open(path_to_city+"\\IntersectionsIntermediateFiles\\AlbanyNY_1930_edit_Intersections.txt")
    InterLines = Intersect_TXT.readlines()[1:]
    Descriptions = open(Descriptions_path).readlines()

    # Morse Dicts: #
    ED_description_dict = {} # lookup ED -> list streets in order of description
    ED_NAME_description_dict = {} # lookup ED -> list street NAMEs in order of description

    # Map Dicts: #
    Intersect_ST_dict = {} # lookup intersection -> which STs (phrases)
    Intersect_BLOCK_dict = {} # lookup intersection -> which BLOCKs
    Intersect_NAME_dict = {} # lookup intersection -> which STs (NAMEs)
    ST_Intersect_dict = {} # lookup ST -> which intersections
    BLOCK_Intersect_dict = {} # lookup BLOCK ID -> which intersections
    BLOCK_NAME_dict = {} # lookup BLOCK ID -> NAME of segment

    # Derived Dict #
    ED_Intersect_ID_dict = {} # lookup ED -> string of Intersection IDs

    st_grid_exists = os.path.isfile(shp_targ)
    descriptions_exist = os.stat(Descriptions_path).st_size != 0
    if st_grid_exists and descriptions_exist:
        RunAnalysis(city)
    else :
        print(city+": Error finding stgrid ("+str(st_grid_exists)+") and/or descriptions ("+str(descriptions_exist)+")")
    
    print("Creating ED Map")
    draw_EDs()
