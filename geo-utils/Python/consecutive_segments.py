# -*- coding: utf-8 -*-

import arcpy
import re
import copy


#targ = r"C:\Users\akisch\Desktop\Streetgrid Automation Scripts\Address Fixing Tools\StLouis\StLouisMO_1930_stgrid_edit_Uns2.shp"
#targ = r"C:\Users\akisch\Documents\ArcGIS\Default.gdb\consec_test"
#targ = r"C:\Users\akisch\Desktop\Streetgrid Automation Scripts\Address Fixing Tools\Providence_1940.shp"
targ = r"S:\Projects\1940Census\StLouis\GIS_edited\StLouisMO_1930_stgrid_edit_Uns2.shp"


#Not "FULLNAME":
#fullname_var = 'FIRST_FULL'
fullname_var = 'FULLNAME'

fields = arcpy.ListFields(targ)

for f in fields :
    if f.type == "OID" :
        fid_var = f.name

#This should be the new standard for segment IDs:
#fid_var = "grid_id"

field_names = [x.name for x in fields]

# Version of Dict_append that only accepts unique v(alues) for each k(ey)
def Dict_append_unique(Dict, k, v) :
    if not k in Dict :
        Dict[k] = [v]
    else :
        if not v in Dict[k] :
            Dict[k].append(v)

#Return all unique values of field found in table
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as search_cursor:
        return sorted({row[0] for row in search_cursor})

#Returns just the NAME and TYPE components of the street phrase, if any#
def remove_st_dir(st) :
    if (st == None or st == '' or st == ' ' or st == -1) or not (isinstance(st, str) or isinstance(st, unicode)) :
        return "" #.shp files do not support NULL !!!
    else :
        DIR = re.search("^[NSEW]+ ",st)
        if(DIR) :
            DIR = DIR.group(0)
            st = re.sub("^"+DIR, "",st)
            DIR = DIR.strip()
        st = st.strip()
        return st

#function to make sure fids aren't accidentally looping through nexts
#returns True if there is no loop. fnd = fid_next_dict
def test_fid_loop(fnd,fid) :
    n = fid
    for i in range(0,len(fnd.keys())+1) :
        
        try :
            n = fnd[n]
        except KeyError :
            return True
        except TypeError :
            pass #BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD#BAD
        if n == fid :
            return False
    print("ran out of fids?")
    return False

#returns a tuple of lists comprising all discrete runs of consequent FIDs. fnd = fid_next_dict
def find_fid_runs(fnd) :
    run_starts = [x for x in fnd.keys() if not x in fnd.values()]
    runs = ()
    if len(run_starts) == 0 :
        print("FIDS ARE A LOOP AND WE CAN TELL FROM TRYING TO FIND RUNS!")
    for f in run_starts :
        runs += (fid_run_recurse(fnd, f),)
    return runs
#recursion function called by find_fid_runs
def fid_run_recurse(fnd, fid) :
    #if fid == None :
    #    return []
    try :
        next_fid = fnd[fid]
    except KeyError :
        return [fid]
    except TypeError :
        return [fid]
    else :
        return [fid]+fid_run_recurse(fnd,next_fid)

#given a graph in the form of a dict: node -> [child_nodes]
#return a list containing the nodes of the longest possible path
#from a start node to an end 
def longest_path(G) :
    keys = G.keys()
    values = []
    for v in G.values() :
        if isinstance(v,list) :
            values += v
        else :
            values.append(v)
    starts = set([x for x in keys if not x in values])
    ends = set([x for x in values if not x in keys])
    Gd = dict(G)
    #create new dict structure with entries for child vertices (v) and whether
    #current node is "discovered" (d)
    for k in Gd.keys() :
        if not isinstance(Gd[k],list) :
            Gd[k] = [Gd[k]]
        Gd[k] = {'v':Gd[k],'d':False}
    for e in ends :
        Gd[e] = {'v':[],'d':False}
    paths = []
    for s in starts :
        paths.append(depth_first_search(dict(Gd),s))
    return max(paths,key=len)
#recursive search function called by longest_path
def depth_first_search(G,v) :
    Gd = copy.deepcopy(G)
    #create an entirely new data structure in memory so that nodes' "discovered" 
    #values do not propagate backward to parent nodes!
    Gd[v]['d'] = True
    longest_subpath = []
    subpaths = []
    for n in Gd[v]['v'] :
        if not Gd[n]['d'] :
            subpaths.append(depth_first_search(Gd,n))
    if not subpaths == [] :
        longest_subpath = max(subpaths,key=len)
    return [v]+longest_subpath


def fill_addr_gaps(targ) :
    pass
    #Chris is working on this...

# converts a stname -> [fid_sequence] dict into a fid -> [prev_fid, next_fid] dict
def flatten_seq_dict(name_sequence_dict) :
    fid_prevnext_dict = {}
    for name, seq in name_sequence_dict.items() :
        for ind, fid in enumerate(seq) :
            if ind == 0 :
                prev_fid = None
            else :
                prev_fid = seq[ind-1]
            if ind == len(seq) - 1 :
                next_fid = None
            else :
                next_fid = seq[ind+1]
            fid_prevnext_dict[fid] = [prev_fid,next_fid]
    return fid_prevnext_dict


#assumes that name_sequence_dict was created with ignore_dir = True
def consec_to_arc(targ,name_sequence_dict,exact_next_dict) :
    fid_prevnext_dict = flatten_seq_dict(name_sequence_dict)
    #try : arcpy.AddField_management (targ, "flipLine", "SHORT"); except : pass
    with arcpy.da.UpdateCursor(targ, [fid_var,"consecPrev","consecNext","exact_Prev",
                                      "exact_Next"]) as up_cursor:
        for row in up_cursor :
            fid = row[0]
            try :
                prev_next = fid_prevnext_dict[fid]
            except KeyError :
                continue
            print("row: "+str(row))
            row[1] = prev_next[0]
            row[2] = prev_next[1]
            try :
                print("prev_next: "+str(prev_next))
                row[3] = exact_next_dict[prev_next[0]] == fid
            except KeyError :
                row[3] = False
            try :
                row[4] = exact_next_dict[fid] == prev_next[1]
            except KeyError :
                row[4] = False
            up_cursor.updateRow(row)




#have to pass in a .shp
#include_non_exact: True or False
#logic: organize streets one stname at a time
#       first find exactly consequent segments
#       then, separately, decide about inexact consequent segments

#ignore_dir determines whether streets with only differing directions are considered
#the same street for purposes of determining consecutive-ness:
def get_consecutive(targ,include_non_exact = True,ignore_dir = True) :

    debug = True
    
    arcpy.AddGeometryAttributes_management(targ, "LINE_START_MID_END")
    try :
        arcpy.AddField_management (targ, "consecPrev", "TEXT")
        arcpy.AddField_management (targ, "consecNext", "TEXT")
        arcpy.AddField_management (targ, "exact_Prev", "SHORT")
        arcpy.AddField_management (targ, "exact_Next", "SHORT")
    except :
        pass #just for debugging, as any .shp having this done will not have these fields
    fields = arcpy.ListFields(targ)
    field_names = [x.name for x in fields]
    name_sequence_dict = {} #dict: st_name -> sequential list of FIDs for all segments with st_name
    name_sequence_spur_dict = {} #same format as name_sequence_dict, but comprising spurs and other segments that connect to main sequence
    #how do we account for two different groups of segs with same name when include_non_exact is False?
    exact_next_dict = {}
    print("field_names"+str(field_names))
    if ignore_dir :
        arcpy.AddField_management (targ, "name_type", "TEXT")
        with arcpy.da.UpdateCursor(targ, [fullname_var,"name_type"]) as up_cursor:
            for row in up_cursor :
                row[1] = remove_st_dir(row[0])
                up_cursor.updateRow(row)
        unique_names = unique_values(targ,"name_type")
        name_var = "name_type"
    else :
        unique_names = unique_values(targ,fullname_var)
        name_var = fullname_var
    
    for name in unique_names :
        fid_coord_dict = {}
        if name != " " and name != "City Limits" :
            name_targ = name+"_lyr"
            name = name.replace("'","''") #replace apostrophe in name with two apostrophes (SQL-specific syntax)
            arcpy.MakeFeatureLayer_management(targ,name_targ,name_var+" = '"+name+"'")
            num_name_segments = int(arcpy.GetCount_management(name_targ).getOutput(0))
            if debug: print("examining "+str(num_name_segments)+" segments named "+name)
            if num_name_segments > 1 : #if more than 1 st segment with name
                next_fid_list = []#fids that should be considered for next of another segment
                all_fid_list = []
                with arcpy.da.SearchCursor(name_targ, [fid_var,'START_X', 'START_Y', 'END_X', 'END_Y']) as s_cursor :
                    for row in s_cursor :
                        #populate dict of fid -> coordinates_dict
                        all_fid_list.append(row[0])
                        next_fid_list.append(row[0])
                        fid_coord_dict[row[0]] = {}
                        fid_coord_dict[row[0]]['START_X'] = row[1]
                        fid_coord_dict[row[0]]['START_Y'] = row[2]
                        fid_coord_dict[row[0]]['END_X'] = row[3]
                        fid_coord_dict[row[0]]['END_Y'] = row[4]
                with arcpy.da.UpdateCursor(name_targ, [fid_var,"consecPrev","consecNext",
                                                       "exact_Prev","exact_Next"]) as up_cursor:
                    next_fid_linked_list = {} #dict: fid -> fid of next segment(s)
                    prev_fid_linked_list = {} #dict: fid -> fid of prev segment
                    coord_diff_start = {} #keeps track of the segment that is spatially closest to cur_seg
                    coord_diff_end = {}#for purposes of tracking down inexact next and prev segments
                    singleton_segments = ()
                    found_cyclic_loop = False
                    fork_segs = [] #not used
                    merge_segs = []#not used
                    for row in up_cursor :
                        cur_fid = row[0]
                        cur_seg = fid_coord_dict[cur_fid]
                        startx = round(cur_seg['START_X'],6) # Assuming units=decimal degrees,
                        starty = round(cur_seg['START_Y'],6) #this rounds to roughly the
                        endx = round(cur_seg['END_X'],6) # nearest inch.
                        endy = round(cur_seg['END_Y'],6) # i.e. negligible (but necessary. Because Arc.)
                        coord_diff_start[cur_fid] = []
                        coord_diff_end[cur_fid] = []
                        found_exact_prev = False
                        found_exact_next = False
                        next_fid_candidates = []
                        prev_fid_candidates = []
                        for fid, seg in fid_coord_dict.items() :
                            if not cur_fid == fid :#no segment can be the next or prev of itself...
                                if round(seg['END_X'],6) == startx and round(seg['END_Y'],6) == starty : #found exact prev
                                    found_exact_prev = True
                                    prev_fid_candidates.append(fid)
                                #print("cur_fid - endx: "+str(endx)+" endy:   "+str(endy)+" ("+str(fid)+")")
                                #print("fid -  START_X: "+str(seg['START_X'])+" START_Y: "+str(seg['START_Y']))
                                if round(seg['START_X'],6) == endx and round(seg['START_Y'],6) == endy : #found exact next
                                    if found_exact_next :
                                        ### cur_fid is the last segment before a fork:
                                        ###            \ /
                                        ###             |  <- cur_fid
                                        ###             ↑
                                        if debug:print(str(cur_fid)+" has multiple exact nexts!")
                                        fork_segs.append(cur_fid)#not used
                                    found_exact_next = True
                                    try :
                                        next_fid_list.remove(fid)
                                    except ValueError :
                                        ### cur_fid is the last segment before a merge:
                                        ###             ↑
                                        ###             |
                                        ###            / \  <- cur_fid
                                        if debug:print("an exact next is already the exact next of something else")
                                        merge_segs.append(fid)#not used
                                        
                                    next_fid_candidates.append(fid)
                                #record distance of start and end coordinates relative to start and end of cur_seg:
                                end_end_diff = math.sqrt((seg['END_X'] - endx)**2 + (seg['END_Y'] - endy)**2)
                                end_start_diff = math.sqrt((seg['START_X'] - endx)**2 + (seg['START_Y'] - endy)**2)
                                coord_diff_end[cur_fid].append((min(end_end_diff,end_start_diff), fid))
                                start_end_diff = math.sqrt((seg['END_X'] - startx)**2 + (seg['END_Y'] - starty)**2)
                                start_start_diff = math.sqrt((seg['START_X'] - startx)**2 + (seg['START_Y'] - starty)**2)
                                coord_diff_start[cur_fid].append((min(start_end_diff,start_start_diff), fid))
                        if not found_exact_prev and not found_exact_next :
                            singleton_segments += ([cur_fid],)
                        else :
                            if len(prev_fid_candidates) == 1 :
                                prev_fid_linked_list[cur_fid] = prev_fid_candidates[0]
                            if len(prev_fid_candidates) > 1 :
                                prev_fid_linked_list[cur_fid] = prev_fid_candidates
                            if len(next_fid_candidates) == 1 :
                                next_fid_linked_list[cur_fid] = next_fid_candidates[0]
                            if len(next_fid_candidates) > 1 :
                                next_fid_linked_list[cur_fid] = next_fid_candidates
                        
                        
                    if test_fid_loop(next_fid_linked_list,fid) :
                        pass
                    else :
                        print("Cyclic Loop detected.")
                        print("Name of segments: "+name)
                        print("FIDs of segments: "+str(all_fid_list))
                        found_cyclic_loop = True
                        #TODO: store this info somewhere?

                    cur_longest_path = []
                    
                    if not found_cyclic_loop :
                        if not next_fid_linked_list == {} :
                            #PROBLEM:#PROBLEM:#PROBLEM: 
                            #PROBLEM:#PROBLEM:#PROBLEM: test_fid_loop does not support lists in next_fid_linked_list
                            #PROBLEM:#PROBLEM:#PROBLEM:
                            #PROBLEM:#PROBLEM:#PROBLEM: CURRENTLY THIS IS BEING SILENCED WITH AN except TypeError!!!!
                            #PROBLEM:#PROBLEM:#PROBLEM: instead, should change longest_path to detect cycles
                            #PROBLEM:#PROBLEM:#PROBLEM:
                            cur_longest_path = longest_path(next_fid_linked_list)
                            if debug:
                                print("next_fid_linked_list is: "+str(next_fid_linked_list))
                                print("longest path is: "+str(cur_longest_path))
                                print("FIDs not in longest path: "+str([x for x in all_fid_list if not x in cur_longest_path]))

                            #modify next_fid_linked_list to conform to longest_path
                            for k,v in dict(next_fid_linked_list).items() :
                                if k in cur_longest_path :
                                    if isinstance(v,list) :
                                        next_fid_linked_list[k] = cur_longest_path[cur_longest_path.index(k)+1]

                        else :
                            print("no exact consecutive segments exist for "+name)

                        street_is_too_messed_up = False
                        for k, v in next_fid_linked_list.items() :
                            if isinstance(v, list) :
                                print("There is a fork on a non-central path for the street "+name)
                                print("This is not currently supported. Goodbye.")
                                street_is_too_messed_up = True
                                break
                        if street_is_too_messed_up :
                            continue

                        exact_next_dict = dict(copy.deepcopy(next_fid_linked_list), **exact_next_dict)
                        
                        #determine if segments that do not have an exact next/prev should have an inexact next/prev:
                        #start segment is somewhere in next_fid_list
                        #first, break down entire sequence of street segments into contiguous runs:
                        #then create a dict of possible connections (which will include end segment->start segment. we do not want this.)

                        runs = find_fid_runs(next_fid_linked_list)
                        runs += singleton_segments

                        if debug: print("runs: "+str(runs))

                        #set aside runs that are spurs/forks of cur_longest_path
                        #they will not be considered as candidates for inexact next/prev
                        for run in tuple(runs) :
                            if not run == cur_longest_path :
                                longest_path_overlap = [x for x in run if x in cur_longest_path]
                                if not longest_path_overlap == [] :
                                    temp = list(runs)
                                    temp.remove(run)
                                    runs = tuple(temp)
                                    for x in longest_path_overlap :
                                        run.remove(x)
                                    Dict_append_unique(name_sequence_spur_dict,name,run)
                                    for x in run :
                                        del next_fid_linked_list[x]
                                    if debug: print("added the spur "+str(run)+" to aux dict")       

                        possible_connexions = {}
                        for s_run in runs :
                            for e_run in runs :
                                if s_run != e_run :
                                    Dict_append_unique(possible_connexions,e_run[-1],s_run[0])
                        print("possible_connexions: "+str(possible_connexions))
                        #cumbersome magic to organize and sort the distances of each gap for which we want to (maybe)
                        #make a connexion based on the dicts created prior:
                        dist_fid_list = []
                        for k in possible_connexions.keys() :
                            coord_diff_start_list = []
                            coord_diff_end_list = []
                            for v in possible_connexions[k] :
                                coord_diff_start_list.append(list(filter(lambda x: x[1]==v, coord_diff_start[k])))
                                coord_diff_end_list.append(list(filter(lambda x: x[1]==v, coord_diff_end[k])))
                            shortest_gap = min(sorted(coord_diff_start_list)[0],sorted(coord_diff_end_list)[0])
                            if isinstance(shortest_gap,list) and len(shortest_gap) > 0:
                                if debug:print("shortest_gap is a list (yes, this is still happening)")
                                shortest_gap = shortest_gap[0]
                            elif debug:print("shortest_gap is NOT a list (not happening all the time)")

                            shortest_gap += (k,)
                            dist_fid_list.append(shortest_gap)
                        
                        #deal with cycles in inexact next gaps (this only applies to two-fid cycles)
                        ### have to find when there is a cycle in dist_fid_list 
                        ### when we have a cycle, we should remove the cyclic connexion that interferes with another connexion
                        
                        def deal_with_dist_fid_cycles() :
                            dist_fid_cycles = []
                            #identify cyclic gaps in dist_fid_list
                            for i in range(0,len(dist_fid_list)-1) :
                                for j in range(i+1,len(dist_fid_list)) :
                                    if dist_fid_list[i][1]==dist_fid_list[j][2] and dist_fid_list[i][2]==dist_fid_list[j][1] :
                                        dist_fid_cycles.append(dist_fid_list[i])
                                        dist_fid_cycles.append(dist_fid_list[j])
                                        break
                            #isolate cyclic gaps from the rest of dist_fid_list
                            for i in dist_fid_cycles :
                                dist_fid_list.remove(i)
                            print("dist_fid_cycles: "+str(dist_fid_cycles))
                            for i in dist_fid_list :
                                #iterate over a copy of dist_fid_cycles so we can modify the original
                                for j in list(dist_fid_cycles) :
                                    if i[1] == j[1] and i[2] != j[2] :
                                        #set distance to impossibly high value for the bad gap in the cycle
                                        dist_fid_cycles.remove(j)
                                        dist_fid_cycles.append((99999,)+j[1:])
                                        if debug:print(str(j)+" was a bad egg cuz of "+str(i))
                            for j in dist_fid_cycles :
                                #add values back to list
                                dist_fid_list.append(j)
                                
                        deal_with_dist_fid_cycles()

                        dist_fid_list = sorted(dist_fid_list)
                                            
                        if debug:print("now, dist_fid_list is: "+str(dist_fid_list))
                        while len(dist_fid_list) > 1 :
                            connexion = dist_fid_list.pop(0)
                            if debug:print("checking connexion "+str(connexion))
                            check_for_cycles_linked_list = dict(next_fid_linked_list)
                            check_for_cycles_linked_list[connexion[2]] = connexion[1]
                            if test_fid_loop(check_for_cycles_linked_list,connexion[2]) :
                                #only create the connection if it does not create a cyclical loop
                                next_fid_linked_list[connexion[2]] = connexion[1]
                        if debug:
                            if len(dist_fid_list) :     
                                print(name +": the last connexion (which was not made) was "+str(dist_fid_list[0]))
                            else :
                                print(name+" had no inexact connexions")
                            
                        #reconstruct order of segments and store in name_sequence_dict
                        start_fid = [x for x in next_fid_linked_list.keys() if not x in next_fid_linked_list.values()]
                        if debug:
                            wtf = [x for x in next_fid_linked_list.values() if not x in next_fid_linked_list.keys()]
                            print(name+": "+str(start_fid)+ " -> "+str(wtf))
                        if not len(start_fid) == 1 :
                            print("There is a spur (or sum'n') on the street "+name)
                            print("Have to deal with this manually!!!!!!!")
                        start_fid = start_fid[0]
                        fid_list = [start_fid]
                        if debug: print("There should be %s FIDs" %(len(next_fid_linked_list.keys())+1))
                            
                        while len(fid_list) <= len(next_fid_linked_list.keys()) :
                            try :
                                fid_list.append(next_fid_linked_list[fid_list[-1]])
                            except KeyError :
                                print("THIS SHOULD NOT HAPPEN CAUSE OF THE LEN AND STUFF")
                                break
                        if debug:print("adding fid_list: "+str(fid_list))
                        name_sequence_dict[name] = fid_list
    print("Finished.")
    return name_sequence_dict,exact_next_dict


### Unresolved Issues ###

# Broadway :
# --<--|--<--|--<--|-->--|-->--|-->--
#   6     5     4     1     2     3



name_sequence_dict, exact_next_dict = get_consecutive(targ)

