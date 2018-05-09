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

