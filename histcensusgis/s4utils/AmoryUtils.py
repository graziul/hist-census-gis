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
