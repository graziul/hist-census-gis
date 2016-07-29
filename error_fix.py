import os
import re
from collections import Counter
import numpy as np
import time
import sys

sys.setrecursionlimit(1500)

os.chdir(r'C:\Users\akisch\Desktop')

file_data = open('chicago_std.txt','r')
data = file_data.readlines()[1:] ### WHOLE FILE OR EXCLUDE FIRST LINE?!?!?!?!?!?!?!?! ###
Data = []
for ind, line in enumerate(data) :
    
    Data.append(line.split(';'))
    Data[ind][-1] = Data[ind][-1].strip()
    try :
        Data[ind][1] = int(Data[ind][1])
    except ValueError:
        Data[ind][1] = None
    # IGNORE 1/2 etc. #
    Data[ind][2] = re.sub('[0-9]/[0-9]','',Data[ind][2])
    Data[ind][2] = Data[ind][2].strip()
    try :
        Data[ind][2] = int(Data[ind][2])
    except ValueError:
        Data[ind][2] = None



def preclean_dir_type(st):
    runAgain = False
    st = st.rstrip('\n')
    orig_st = st
    

    #Check if st is empty or blank and return empty to [st,DIR,NAME,TYPE]
    if st == '' or st == ' ':
        return ['','','','']

    ###Remove Punctuation, extraneous words at end of stname###
    st = re.sub(r'[\.,]','',st)
    st = re.sub(r' \(?([Cc]on[\'t]*d?|[Cc]ontinued)\)?$','',st)
    #consider extended a diff stname#
    #st = re.sub(r' [Ee][XxsS][tdDT]+[^ ]*$','',st)
    
    ###stname part analysis###
    DIR = ''
    NAME = ''
    TYPE = ''
    
    #First check if DIR is at end of stname. make sure that it's the DIR and not actually the NAME (e.g. "North Ave" or "Avenue E")#
    if re.search(r' (N|No|No|[Nn][Oo][Rr][Tt][Hh])$',st) and not re.match('^[Nn][Oo][Rr][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+N$',st) :
        st = "N "+re.sub(r' (N|No|[Nn][Oo][Rr][Tt][Hh])$','',st)
        DIR = 'N'
    if re.search(r' (S|So|So|[Ss][Oo][Uu][Tt][Hh])$',st) and not re.search('^[Ss][Oo][Uu][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+S$',st) :
        st = "S "+re.sub(r' (S|So|[Ss][Oo][Uu][Tt][Hh])$','',st)
        DIR = 'S'
    if re.search(r' ([Ww][Ee][Ss][Tt]|W)$',st) and not re.search('^[Ww][Ee][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+W$',st) :
        st = "W "+re.sub(r' ([Ww][Ee][Ss][Tt]|W)$','',st)
        DIR = 'W'
    if re.search(r' ([Ee][Aa][Ss][Tt]|E)$',st) and not re.search('^[Ee][Aa][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+E$',st) :
        st = "E "+re.sub(r' ([Ee][Aa][Ss][Tt]|E)$','',st)
        DIR = 'E'

    #See if a st TYPE can be identified#
    st = re.sub(r'[ \-]+([Ss][Tt][Rr][Ee]?[Ee]?[Tt]?[Ss]?|[Ss][tT]|[Ss]trete|[Ss][\.][Tt]|[Ss][Tt]?.?[Rr][Ee][Ee][Tt])$',' St',st)
    st = re.sub(r'[ \-]+([Aa][Vv]|[Aa][VvBb][Ee][Nn][Uu]?[EesS]?|Aveenue|Avn[e]?ue|[Aa][Vv][Ee])$',' Ave',st)
    st = re.sub(r'[ \-]+(Blv\'d|Bl\'v\'d|Blv|Blvi|Bly|Bldv|Bvld|Bol\'d|[Bb]oul[ea]?vard)$',' Blvd',st)
    st = re.sub(r'[ \-]+([Rr][Dd]|[Rr][Oo][Aa][Dd])$',' Road',st)
    st = re.sub(r'[ \-]+[Dd][Rr]$',' Drive',st)
    st = re.sub(r'[ \-]+([Cc][Oo][Uu]?[Rr][Tt]|[Cc][Tt])$',' Ct',st)
    st = re.sub(r'[ \-]+([Pp]lace|[Pp][Ll])$',' Pl',st)
    st = re.sub(r'[ \-]+([Ss]quare|[Ss][Qq])$',' Sq',st)
    st = re.sub(r'[ \-]+[Cc]ircle$',' Cir',st)
    st = re.sub(r'[ \-]+([Pp]rkway|[Pp]arkway|[Pp]ark [Ww]ay|[Pp]kway|[Pp]ky|[Pp]arkwy|[Pp]rakway|[Pp]rkwy|[Pp]wy)$',' Pkwy',st)
    st = re.sub(r'[ \-]+[Ww][Aa][Yy]$',' Way',st)
    st = re.sub(r'[ \-]+[Aa][Ll][Ll]?[Ee]?[Yy]?$',' Aly',st)
    st = re.sub(r'[ \-]+[Tt](err|errace)$',' Ter',st)
    st = re.sub(r'[ \-]+[Ll][Aa][Nn][Ee]$',' Ln',st)
    st = re.sub(r'[ \-]+([Pp]lzaz|[Pp][Ll][Aa][Zz][Aa])$',' Plaza',st)

    # "Park" is not considered a valid TYPE because it should probably actually be part of NAME #
    match = re.search(r' (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$',st)
    if match :
        TYPE = match.group(1)
        
    #See if there is a st DIR. again, make sure that it's the DIR and not actually the NAME (e.g. North Ave)
    match =  re.search(r'^([nN]|N\.|No|No\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'North'
        else :
            st = "N "+re.sub(r'^([nN]|N\.|No|No\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+','',st)
            DIR = 'N'
    match =  re.search(r'^([sS]|S\.|So|So\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'South'
        else :
            st = "S "+re.sub(r'^([sS]|S\.|So|So\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+','',st)
            DIR = 'S'
    match =  re.search(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'West'
        else :
            st = "W "+re.sub(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+','',st)
            DIR = 'W'
    match =  re.search(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|Ea[Ss]?)[ \-]+',st)
    if match :
        if st==match.group(0)+TYPE:
            NAME = 'East'
        else :
            st = "E "+re.sub(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|Ea[Ss]?)[ \-]+','',st)
            DIR = 'E'

    
    #get the st NAME and standardize it
    #convert written-out numbers to digits
    #TODO: Make these work for all exceptions (go thru text file with find)
    if re.search("[Tt]enth|Eleven(th)?|[Tt]wel[f]?th|[Tt]hirteen(th)?|Fourt[h]?een(th)?|[Ff]ift[h]?een(th)?|[Ss]event[h]?een(th)?|[Ss]event[h]?een(th)?|[eE]ighteen(th)?|[Nn]inet[h]?een(th)?|[Tt]wentieth|[Tt]hirtieth|[Ff]o[u]?rtieth|[Ff]iftieth|[Ss]ixtieth|[Ss]eventieth|[Ee]ightieth|[Nn]inetieth|Twenty[ \-]?|Thirty[ \-]?|Forty[ \-]?|Fifty[ \-]?|Sixty[ \-]?|Seventy[ \-]?|Eighty[ \-]?|Ninety[ \-]?|[Ff]irst|[Ss]econd|[Tt]hird|[Ff]ourth|[Ff]ifth|[Ss]ixth|[Ss]eventh|[Ee]ighth|[Nn]inth",st) :
        st = re.sub("[Tt]enth","10th",st)
        st = re.sub("[Ee]leven(th)?","11th",st)
        st = re.sub("[Tt]wel[f]?th","12th",st)
        st = re.sub("[Tt]hirteen(th)?","13th",st)
        st = re.sub("[Ff]ourt[h]?een(th)?","14th",st)
        st = re.sub("[Ff]ift[h]?een(th)?","15th",st)
        st = re.sub("[Ss]ixt[h]?een(th)?","16th",st)
        st = re.sub("[Ss]event[h]?een(th)?","17th",st)
        st = re.sub("[eE]ighteen(th)?","18th",st)
        st = re.sub("[Nn]inet[h]?een(th)?","19th",st)
        st = re.sub("[Tt]wentieth","20th",st)
        st = re.sub("[Tt]hirtieth","30th",st)
        st = re.sub("[Ff]o[u]?rtieth","40th",st)
        st = re.sub("[Ff]iftieth", "50th",st)
        st = re.sub("[Ss]ixtieth", "60th",st)
        st = re.sub("[Ss]eventieth", "70th",st)
        st = re.sub("[Ee]ightieth", "80th",st)
        st = re.sub("[Nn]inetieth", "90th",st)

        st = re.sub("Twenty[ \-]?","2",st)
        st = re.sub("Thirty[ \-]?","3",st)
        st = re.sub("Forty[ \-]?","4",st)
        st = re.sub("Fifty[ \-]?","5",st)
        st = re.sub("Sixty[ \-]?","6",st)
        st = re.sub("Seventy[ \-]?","7",st)
        st = re.sub("Eighty[ \-]?","8",st)
        st = re.sub("Ninety[ \-]?","9",st)
        st = re.sub("[Ff]irst","1st",st)
        st = re.sub("[Ss]econd","2nd",st)
        st = re.sub("[Tt]hird","3rd",st)
        st = re.sub("[Ff]our(th)?","4th",st)
        st = re.sub("[Ff]ifth","5th",st)
        st = re.sub("[Ss]ix(th)?","6th",st)
        st = re.sub("[Ss]even(th)?","7th",st)
        st = re.sub("[Ee]ighth?","8th",st)
        st = re.sub("[Nn]in(th|e)","9th",st)

    match = re.search(DIR+'(.+)'+TYPE,st)
    if NAME=='' :
        if match :
            NAME = match.group(1).strip()
            if re.search("[0-9]+",NAME) :
                # TODO: Fix incorrect suffixes e.g. "73d St"
                # TODO: identify corner cases with numbers e.g. "51 and S- Hermit"
                if re.search("^[0-9]+$",NAME) : #if NAME is only numbers (no suffix)
                    foo = True
                    suffixes = {'1':'1st','2':'2nd','3':'3rd','4':'4th','5':'5th','6':'6th','7':'7th','8':'8th','9':'9th','0':'0th'}
                    num = re.search("[0-9]$",NAME)
                    NAME = re.sub("[0-9]$",suffixes[num.group(0)],NAME)
                hnum = re.search("^([0-9]+[ \-]+).+",NAME) #housenum in stname?
                if hnum : 
                    NAME = re.sub(hnum.group(1),"",NAME) #remove housenum. May want to update housenum field, maybe not though.
                    runAgain = True
            else :
                NAME = NAME.title()
            
        else :
            assert(False)
    st = re.sub(re.escape(match.group(1).strip()),NAME,st)
    try :
        assert st == (DIR+' '+NAME+' '+TYPE).strip()
    except AssertionError :
        print("Something went horribly wrong while trying to pre-standardize stnames.")
        print("orig was: "+orig_st)
        print("st is: \""+st+"\"")
        print("components: \""+(DIR+' '+NAME+' '+TYPE).strip()+"\"")
    
    if runAgain :
        return preclean_dir_type(st)
    else :
        return [st, DIR, NAME, TYPE]


#output pre-standardized text file

def foo() :
    output = open('chicago_std.txt','w')
    for d in Data :
        #output.write(d[0]+';'+str(d[1])+';'+str(d[2])+';'+preclean_dir_type(d[3])[0]+';'+d[4]+';'+d[5]+'\n')
        output.write(d[0]+';'+str(d[1])+';'+str(d[2])+';'+preclean_dir_type(d[3])[0]+';'+d[3]+'\n')

##start_time = time.time()
##foo()
##print("--- %s seconds ---" % (time.time() - start_time))


HN_SEQ = []
ST_SEQ = []
INCONS = []
SINGLE_HN_ERRORS = []

MAX_GAP = 100

def get_hn(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][2]
    else :
        return None

def get_name(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][3]
    else :
        return None

def get_linenum(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][1]
    else :
        return None

#evaluative function to determine HN sequences#
def seq_end_chk(cur_num,chk_num) : #returns true if cur_num and chk_num are in different SEQs
    
    return cur_num == None or not (cur_num+chk_num) % 2 == 0 or abs(cur_num-chk_num) > MAX_GAP #if housenum undefined, consider it the end of seq
        
#recursive function to walk through HN sequences#
def num_seq(ind,chk_num,chk_dir) : #chk_dir = 1|-1 depending on the direction to look
    cur_num = get_hn(ind)
    if(seq_end_chk(cur_num,chk_num)) : #if cur num doesn't fit in SEQ...
        end = seq_end_chk(get_hn(ind+chk_dir),chk_num) #...see if next num does
        if(end) :
            return ind-chk_dir
        else :
            SINGLE_HN_ERRORS.append(ind)
            return num_seq(ind+chk_dir,chk_num,chk_dir)
    else :
        return num_seq(ind+chk_dir,cur_num,chk_dir)

#wrapper function for num_seq recursion#
def seq_match_num(ind) : 
    num = get_hn(ind)
    if num == None : #if housenum undefined, consider it a singleton seq
        return [ind,ind,num,num]
    seq_start = num_seq(ind-1,num,-1)
    seq_end = num_seq(ind+1,num,1)
    return [seq_start,seq_end]#[seq_start,seq_end,get_hn(seq_start),get_hn(seq_end)]

def st_seq(ind) :
    name = get_name(ind)
    if name==None :
        return []
    i=ind
    while(get_name(i-1)==name) :
        i = i-1
    start = i
    while(get_name(ind+1)==name) :
        ind = ind+1
    return [start,ind]#[start,ind,name]

def get_cray_z_scores(arr) :
    debug = False
    inc_arr = np.unique(arr) #returns sorted array of unique values
    
    if not None in arr and len(inc_arr)>2:
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
        
        return zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score))
        
    
ind = 0
while ind<len(Data) :
    try:
        HN_SEQ.append(seq_match_num(ind))
    except RuntimeError :
        print("STACK OVERFLOW...? ind was: "+str(ind)+", which is linenum "+str(get_linenum(ind))+" on page "+Data[ind][0])
    ind = HN_SEQ[len(HN_SEQ)-1][1]+1

ind = 0
while ind<len(Data) :
    ST_SEQ.append(st_seq(ind))
    ind = ST_SEQ[len(ST_SEQ)-1][1]+1

print("single hn (literally) errors: "+str(len(SINGLE_HN_ERRORS)))

##ind = 0
##for sw in ST_SEQ[:100] :
##    end = sw[1]
##    num_sw = (x for x in HN_SEQ[ind:] if x[1]<=end)
##    print("st swatch ending at %d has following HN swatches: " %end)
##    for sw_n in num_sw :
##        ind= ind+1
##        print sw_n
##    if Data[sw[0]][1]==51 :
##        print("classic hangover at %d" %sw[0])
        
    

### ERROR CHECKING LOOP: check swatches that do not match up ###

s = set(map(tuple,HN_SEQ))
INCONS = [x for x in map(tuple,ST_SEQ) if x not in s] #st swatches that lack a corresponding HN swatch

s1 = set(map(tuple,ST_SEQ))
INCONS1 = [x for x in map(tuple,HN_SEQ) if x not in s1] #HN swatches that lack a corresponding st swatch

errors = 0

for inc in INCONS[:0] :
    #find housenums that are outliers within a st-swatch (or otherwise normal housenum swatch - only one address diff)
    #compute standard deviation, median of housenums within st swatch
    #also take into account even/odd-ness
    #Standard Deviation should be calculated with respect to how much housenum deviates from previous num, as opposed
    # to how much it deviates from the distribution as a whole
    
    #HOW WILL USING ALL HOUSENUMS AND NOT JUST 1 FOR EACH HOUSEHOLD AFFECT RESULTS?
    inc_nums = [row[2] for row in Data[inc[0]:inc[1]+1]]
    z = get_cray_z_scores(inc_nums)
    print(inc_nums)
    print(z)
        
        #if z_score > 4, consider an outlier?
    
last = INCONS1[0]
print("# of incons "+ str(len(INCONS1)))
for inc in INCONS1[:0] :
    if True : ### inc[0] - last[1] == 1 : #consecutive unmatched swatches: what kind of error defines these??
        print(str(last)+" & "+str(inc)+" : ")
        inc_STs = Data[inc[0]:inc[1]+1]
        last_ST = inc_STs[0]
##        for st in inc_STs : #check if address is same but dwelling num different.
##            if st[2] == last_ST[2] and st[3] == last_ST[3] and not st[4] == last_ST[4] :
##                print("Found a probable wrong housenum, dwelling nums are: "+str(st[4])+" & "+str(last_ST[4]))
##            last_ST = st
        STs_freq = Counter([row[3] for row in inc_STs]).most_common()
        if len(STs_freq) == 2 :
            print(STs_freq)
            ratio = float(STs_freq[1][1])/float(STs_freq[0][1])
            if ratio <= .1 :
                errors = errors+1
                print("found a probable wrong stname, ratio: "+str(ratio))
    last = inc

print(errors)

