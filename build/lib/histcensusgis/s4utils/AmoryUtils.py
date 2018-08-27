import numpy as np

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

def preserve_chars(s) :
    special_chars = u'\xa5'
    string = ""
    for char in s :
        if not char in special_chars :
            string += char.encode('ascii',errors='ignore')
        else :
            string += char
    return string

def Dict_append_flexible(Dict, k, v) :
    if not k in Dict :
        Dict[k] = v
    else :
        Dict[k] = [Dict[k]]
        Dict[k].append(v)

# Read a text file and return it as a list, removing the white space by default
def read_file_lines(d,remove_white_space = True) :
    with open(d,'r') as tfile :
        x = tfile.readlines()
        if remove_white_space :
            temp = []
            for line in x :
                temp.append(line.strip())
            x = temp
    return x

# Outlier detection
def get_cray_z_scores(arr, return_bool=False) :
    debug = False
    if not None in arr :
        inc_arr = np.unique(arr) #returns sorted array of unique values
        if(len(inc_arr)>2) :
            if debug : print("uniques: "+str(inc_arr))
            median = np.median(inc_arr,axis=0)
            diff = np.abs(inc_arr - median)
            med_abs_deviation = np.median(diff)
            mean_abs_deviation = np.mean(diff)
            meanified_z_score = diff / (1.253314 * mean_abs_deviation)

            if med_abs_deviation == 0 :
                    modified_z_score = diff / (1.253314 * mean_abs_deviation)
            else :
                    modified_z_score = diff / (1.4826 * med_abs_deviation)
            if debug : print ("MedAD Zs: "+str(modified_z_score))
            if debug : print("MeanAD Zs: "+str(meanified_z_score))
            if debug : print ("Results: "+str(meanified_z_score * modified_z_score > 16))
            
            if return_bool:
                return dict(zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score)>8))
            else:
                return dict(zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score)))
    return None

# looks for duplicate adjacent elements and deletes one
# iterate backwards to avoid problems with iterating and modifying list simultaneously...!
def f7(seq):
    rem_list = []
    if seq[0] == seq[-1]:
        del seq[len(seq)-1]
        rem_list = [len(seq)]
    ind = len(seq) - 2
    while ind >= 0 :
        if seq[ind] == seq[ind+1] :
            del seq[ind+1]
            rem_list.append(ind+1)
        ind -= 1
    return seq, rem_list

# Find mode of a list
def find_mode(l) :
    mode_dict = {}
    for i in l :
        if not i in mode_dict.keys() :
            mode_dict[i] = 1
        else :
           mode_dict[i] += 1
    try :
        max_freq = sorted(mode_dict.values())[-1]
    except :
        #print("max_freq prob")
        #print(l)
        return -999
    return [x[0] for x in mode_dict.items() if x[1]==max_freq]
