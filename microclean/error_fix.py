from __future__ import print_function
import os
import re
from collections import Counter, defaultdict
import numpy as np
import time
import sys
import pandas as pd
import math

### THIS IS A CITYWIDE LIMIT ON THE NUMBER OF PEOPLE THAT CAN LIVE AT A SINGLE ADDRESS ###
sys.setrecursionlimit(2000)

os.chdir(r'C:\Users\akisch\Desktop\Micro_Cleaning')

file_data = open('Chicago_Fuzzy_Section.txt','r')
data = file_data.readlines()[1:] ### WHOLE FILE OR EXCLUDE FIRST LINE?!?!?!?!?!?!?!?! ###
Data = []
for ind, line in enumerate(data) :
    
    Data.append(line.split(';'))
    Data[ind][-1] = Data[ind][-1].strip()
##    if(Data[ind][3] == "") :
##        Data[ind][3] = None
    try :
        Data[ind][1] = int(Data[ind][1])
    except ValueError:
        Data[ind][1] = None

    # CLEAN UP HOUSENUM FIELD #
    # REMOVE 1/2, Rear etc. #
    # If there is a HN range, only the first # is kept: e.g. 1220-1222 becomes 1220
    # TODO: RECORD RECORD RECORD!!! AND EXPAND THESE CHANGES!!! #
    # '[0-9]+\-[0-9]+'
    Data[ind][2] = re.sub('[0-9]/[0-9]|[Rr]ear','',Data[ind][2])

    debug = False
    contHN = re.search("-?\(?([Cc]ontinued|[Cc][Oo][Nn][\'Tte]*[Dd]?\.?)\)?-?",Data[ind][2])
    rangeHN = re.search("([0-9]+)([\- ]+| [Tt][Oo] )[0-9]+",Data[ind][2])
    
    Data[ind][2] = re.sub("-?\(?([Cc]ontinued|[Cc][Oo][Nn][\'Tte]*[Dd]?\.?)\)?",'',Data[ind][2])
    rangeHN = re.search("([0-9]+)([\- ]+| [Tt][Oo] )[0-9]+",Data[ind][2])
    if(rangeHN) :
        Data[ind][2] = rangeHN.group(1)
    Data[ind][2] = Data[ind][2].strip()
    
    try :
        Data[ind][2] = int(Data[ind][2])
    except ValueError:
        Data[ind][2] = None
        

df = pd.DataFrame(Data,columns = ['imageid','indexed_line_number','general_house_number_in_cities_o','st','general_dwelling_number','general_family_number','general_relid','ed'])
df = df[['ed','st','general_house_number_in_cities_o']]

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
    st = re.sub(r'[ \-]+[Dd][Rr][Ii]?[Vv]?[Ee]?$',' Drive',st)
    st = re.sub(r'[ \-]+([Cc][Oo]?[Uu]?[Rr][Tt]|[Cc][Tt])$',' Ct',st)
    st = re.sub(r'[ \-]+([Pp][Ll][Aa][Cc][Ee]|[Pp][Ll])$',' Pl',st)
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
def pre_clean_write_to_file() :
    output = open('chicago_std_allvars.txt','w')
    start_time = time.time()
    output.write("imageid;indexed_line_number;general_house_number_in_cities_o;self_residence_place_streetaddre;general_dwelling_number;general_family_number;general_relid\n")
    for d in Data :
        #output.write(d[0]+';'+str(d[1])+';'+str(d[2])+';'+preclean_dir_type(d[3])[0]+'\n')
        output.write(d[0]+';'+str(d[1])+';'+str(d[2])+';'+preclean_dir_type(d[3])[0]+';'+d[4]+';'+d[5]+';'+d[6]+'\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    sys.exit("done")

#pre_clean_write_to_file()



HN_SEQ = []
ST_SEQ = []
DW_SEQ = []
INCONS_st = []
SINGLE_HN_ERRORS = []
ED_ST_HN_dict = {}
SUBUNIT_HN_ERRORS = []

MAX_GAP = 100

def get_linenum(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][1]
    else :
        return None

def get_hn(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][2]
    else :
        # SHOULD RETURN -1 HERE OR SOMETHING, CONSEQUENCES?
        return None

def get_name(ind) :
    if ind>=0 and ind<len(Data) :
        if Data[ind][3] == "" :
            return None
        else :
            return Data[ind][3]
    else :
        print ("GET NAME OUT OF BOUNDS "+str(ind))
        return -1 #different return values for out of bounds vs. stname missing

#Defaults to str for return value; returns -1 on fail, which is >1 away from any valid dwelling_num
#The value may be incorrect e.g. in apt buildings the apt. # may be in the dwelling field
#However in these cases the housenum is unlikely to be wrong also.
def get_dwelling(ind,numeric=False) : 
    if ind>=0 and ind<len(Data) :
        if(numeric) :
            debug = False
            dw = re.search('([0-9]+)([ \-/]*[A-Za-z.]|[ \-/]+[0-9]| 1/2)?([ \-/]+[Rr]ear)?$',Data[ind][4])
            if(not dw==None) :
                if(dw.group(1)!=Data[ind][4]) :
                    if(debug) : print("dwelling# %s was fixed to: " %Data[ind][4],end="")
                    dw = dw.group(1)
                else :
                    dw = dw.string
            else : dw = Data[ind][4]
            try :
                dw = int(dw)
                if(debug) : print(dw)
                return dw
            except ValueError :
                if(not dw=='') :
                    if(debug) : print("Exception. dwelling# at %s is: %s" %(ind,Data[ind][4]))
                return -1
        else :
            return Data[ind][4]
    else :
        #-2 is adjacent to -1. Use -3 instead.
        return -3

def get_fam(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][5]
    else :
        return -1

def get_relid(ind) :
    if ind>=0 and ind<len(Data) :
        return Data[ind][6]
    else :
        return -1

def get_ed(ind) :
    #ED can eventually go where imageid is in the input .txt varlist ([ind][0])
    if ind>=0 and ind<len(Data) :
        return Data[ind][7]
    else :
        return -1


def same_hh_chk(ind,chk) :
    dwel, fam, relid, ind_dwel, chk_dwel, ind_fam, chk_fam, ind_relid, chk_relid = (-1,)*9
    if(get_dwelling(ind)!="") :
        ind_dwel = get_dwelling(ind)
    if(get_dwelling(chk)!="") :
        chk_dwel = get_dwelling(chk)
    if(get_fam(ind)!="") :
        ind_fam = get_fam(ind)
    if(get_fam(chk)!="") :
        chk_fam = get_fam(chk)
    if(get_relid(ind)!="") :
        ind_relid = get_relid(ind)
    if(get_relid(chk)!="") :
        chk_relid = get_relid(chk)
    if(not -1==ind_dwel and not -1==chk_dwel) :
        dwel = (ind_dwel==chk_dwel)
    if(not -1==ind_fam and not -1==chk_fam) :
        fam = (ind_fam==chk_fam)
    if(not -1==ind_relid and not -1==chk_relid) :
        relid = (ind_relid==chk_relid)
    #if all available hh_chk vars check out, and they are not all undefined (-1)
    if(dwel==-1 and fam==-1 and relid==-1) :
        return -1
    else :
        return [(dwel==-1 or dwel) and (fam==-1 or fam) and (relid==-1 or relid),dwel,fam,relid]
    

#evaluative function to determine HN sequences#
def seq_end_chk(cur_num,chk_num) : #returns True if cur_num and chk_num are in DIFFERENT SEQs
    error_type = 0
    if(cur_num == None) : #if housenum undefined, consider it the end of seq
        error_type = 1
    elif (not (cur_num+chk_num) % 2 == 0) : #one num even, next odd; or vice-versa
        error_type = 2
    elif (abs(cur_num-chk_num) > MAX_GAP) : #gap between two nums exceeds MAX_GAP
        error_type = 3
    return (not error_type==0, error_type)

  
#recursive function to walk through HN sequences#
def num_seq(ind,chk_num,chk_dir) : #chk_dir = 1|-1 depending on the direction to look
    cur_num = get_hn(ind)
    end = seq_end_chk(cur_num,chk_num)
    if(end[0]) : #if cur num doesn't fit in SEQ...
        nextNum = seq_end_chk(get_hn(ind+chk_dir),chk_num) #...see if next num does
        if(not nextNum[0] and get_name(ind)==get_name(ind-1) and get_name(ind)==get_name(ind+1)) :
            #do we want to check sequence of dwelling nums? e.g. 4584230_01092
            #seems like an error but is actually correct because non-consecutive dwelling no.
            #YES. TODO: improve HN swatches using other vars. if stname AND imageid changes, it's probably
            #the end of the HN swatch even if it could keep going. same goes for stname AND dwelling_num_SEQ changing?
            #Likewise, if HN swatch would stop but the error is explained by dwelling_num_SEQ changing while stname stays the same
            
            SINGLE_HN_ERRORS.append([ind,end[1]])
            return num_seq(ind+chk_dir,chk_num,chk_dir)
        else :
            #check places where housenum seq changes, but dwelling# and stname are unchanged
            #if(False) :
            if(get_dwelling(ind+chk_dir)==get_dwelling(ind) and get_dwelling(ind-chk_dir)==get_dwelling(ind) and get_dwelling(ind)!=-1) :
                if(chk_dir==1 and get_name(ind+chk_dir)==get_name(ind) and get_name(ind-chk_dir)==get_name(ind)) :#HNs may only replace other HNs "downstream"
                    SUBUNIT_HN_ERRORS.append([ind,ed_hn_outlier_chk(get_ed(ind),get_name(ind),get_hn(ind))])
                    #HOW TO DEAL WITH THESE
                    #Reveals places where there are HN typos as well as apt/unit numbers in HN
                    #Therefore, we can fix based on whether one of the two addresses for a given dw# and stname is obviously an outlier
                    #However, must deal with false positive problem created by stupid dw#s. Sometimes enumerator just stops updating dw#
                    #for like a whole page, across multiple STs, etc.
                    #IF HN IS A SIGNIFICANT OUTLIER
                    
                    #This makes weird stuff happen with the Hangover Code, so put it on hold for now:
                    #return dwel_seq(ind,chk_dir)
                
            return ind-chk_dir
    else :
        return num_seq(ind+chk_dir,cur_num,chk_dir)

#wrapper function for num_seq recursion#
def seq_match_num(ind) : 
    num = get_hn(ind)
    if num == None : #if housenum undefined, consider it a singleton seq
        return [ind,ind]
    seq_start = num_seq(ind-1,num,-1)
    seq_end = num_seq(ind+1,num,1)
    
    return [seq_start,seq_end]#[seq_start,seq_end,get_hn(seq_start),get_hn(seq_end)]

def st_seq(ind) :
    name = get_name(ind)
    i=ind
    #TODO: Modify code so that it identifies and fixes "S Shore" and "S Shore Drive" being different stnames
    while(get_name(i-1)==name) :
        i = i-1
    start = i
    while(get_name(ind+1)==name) :
        ind = ind+1
    return [start,ind]#[start,ind,name]

#if chk_dir is -1 or 1, does a uni-directional search for end of sequence and returns index
#otherwise, checks in both directions and returns list of start and end indices
def dwel_seq(ind,chk_dir=0) :        
    start=ind
    if(chk_dir!=0) :
        while (abs(get_dwelling(start+chk_dir,numeric=True)-get_dwelling(start,numeric=True))<=1) :
            start = start+chk_dir
        return start
    else :
        while (abs(get_dwelling(start-1,numeric=True)-get_dwelling(start,numeric=True))<=1) :
            start = start-1
        end = ind
        while (abs(get_dwelling(end+1,numeric=True)-get_dwelling(end,numeric=True))<=1) :
            end = end+1
        return [start,end]
    

def get_cray_z_scores(arr) :
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
            
            return dict(zip(inc_arr, np.sqrt(meanified_z_score * modified_z_score)))
    return None

#try to fix single hn errors based on sequence before and after error

def hn_seq_err_fix(ind) :
    hn = str(get_hn(ind))
    p = str(get_hn(ind-1)) #prev num
    n = str(get_hn(ind+1)) #next num
    if(n==p) :
        print("thing: "+Data[ind][0]+" "+p+" "+hn+" "+n)
    #if dwelling num is same as previous or consecutive; if not, don't try to fix
    #also check if that dwelling num was enumerated elsewheres, compare if so
    #also check if the housenum is changing mid-household (should stay same obv)
    for i,digit in enumerate(hn) :
        False
        #even if we can't conclusively fix hn based on digit comparison, we should
        #still keep track of discrepancies with the rest of the sequence, which may also be wrong

def get_ed_hn_outliers() :
    start_time = time.time()
##    eds = [x[7] for x in Data]
##    for ed in np.unique(eds) :
##        ED = eds[eds.index(ed):len(eds) - list(reversed(eds)).index(ed)]
##        assert(len(np.unique(ED))==1)
    ED_HN_OUTLIERS = df.groupby(['ed','st'])
    
    for ED_ST,df_HN in ED_HN_OUTLIERS :        
        ED_ST_HN_dict[ED_ST] = get_cray_z_scores([x for x in df_HN['general_house_number_in_cities_o'] if not math.isnan(x)])
        if(ED_ST_HN_dict[ED_ST]==None) :
            False
            #do something about ED_STs that could not have z-scores calculated
            #this will consist of ED_STs that do not have more than 2 valid HNs
            
        
    print("Finding ED_ST_HN outliers took %s seconds ---" % (time.time() - start_time))
get_ed_hn_outliers()

def ed_hn_outlier_chk(ed,st,hn) :
    if(st is None or ED_ST_HN_dict[(ed,st)] is None or hn is None) :
        return -1
    else :
        return ED_ST_HN_dict[(ed,st)][hn]


ind = 1
while ind<len(Data) :
    DW_SEQ.append(dwel_seq(ind))
    ind = DW_SEQ[len(DW_SEQ)-1][1]+1

print(DW_SEQ[:20])
print(len(DW_SEQ))


ind = 0
while ind<len(Data) :
    try:
        HN_SEQ.append(seq_match_num(ind))
    except RuntimeError :
        print("STACK OVERFLOW...? ind was: "+str(ind)+", which is linenum "+str(get_linenum(ind))+" on page "+Data[ind][0])
    ind = HN_SEQ[len(HN_SEQ)-1][1]+1

print("subunit")
print(SUBUNIT_HN_ERRORS[:20])
print(len(SUBUNIT_HN_ERRORS))

ind = 0
while ind<len(Data) :
    ST_SEQ.append(st_seq(ind))
    ind = ST_SEQ[len(ST_SEQ)-1][1]+1
##
##
##print("single hn (literally) errors: "+str(len(SINGLE_HN_ERRORS)))
##for e in SINGLE_HN_ERRORS :
##    if(e[1]==3 or e[1]==2) :
##        hn_seq_err_fix(e[0])
##
##sys.exit("yay")        

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
INCONS_st = [x for x in map(tuple,ST_SEQ) if x not in s] #st swatches that lack a corresponding HN swatch

s1 = set(map(tuple,ST_SEQ))
INCONS_hn = [x for x in map(tuple,HN_SEQ) if x not in s1] #HN swatches that lack a corresponding st swatch

print("finished forming INCONS sets")

st_seq_starts = [row[0] for row in INCONS_st]
hn_seq_starts = [row[0] for row in INCONS_hn]
st_seq_ends = [row[1] for row in INCONS_st]
hn_seq_ends = [row[1] for row in INCONS_hn]
same_hh_chk
print("Finished making INCONS start and end lists")


CONS_starts = [x for x in st_seq_starts if x in hn_seq_starts]
CONS_ends = [x for x in st_seq_ends if x in hn_seq_ends]

print("Finished making CONS start and end lists")

CONS = list(zip(CONS_starts,CONS_ends))

print(INCONS_st[:10])
print(INCONS_hn[:10])
print(CONS[:10])

HANGOVERS = set()

#OVERLAP: ST and HN swatches intersect but do not contain each other exactly
OVERLAPS = [x for x in CONS if x not in INCONS_st and x not in INCONS_hn]
for o in OVERLAPS :
    debug = True
    st_swatches = INCONS_st[st_seq_starts.index(o[0]):st_seq_ends.index(o[1])+1]
    hn_swatches = INCONS_hn[hn_seq_starts.index(o[0]):hn_seq_ends.index(o[1])+1]
    if(True) : #len(st_swatches)==2 and len(hn_swatches)==2) :
        for s in st_swatches :
            for h in hn_swatches :
                #DO check that inconsistent observations are not mid-hh changes
                #Have to also identify hangovers where the start/end indices of the swatches do NOT EXACTLY line up
                #going along with this, eliminate the >1 obs restriction
                if(not(h[0]==h[1] or s[0]==s[1]) and (s[0]==h[1] or h[0]==s[1])) : #generalized hangover (FIX: only swatches longer than 1 household)
                    if (debug) : print('Found a ', end="")
                    if (s[0]==h[1]) : #hangover
                        hang_ind = s[0]
                        hang_dir = 1
                    else : #reverse hangover
                        hang_ind = h[0]
                        hang_dir = -1
                        if (debug) : print('reverse ', end="")
                    if (debug) : print('hangover at %d, ' % hang_ind, end="")
                    same_hh = same_hh_chk(hang_ind,hang_ind-hang_dir)
                    if(same_hh[0]) :
                        if (debug) : print('that passed same_hh_chk with all available vars, ', end="")
                        
                        #check to make sure abutting hn for (st that we are assuming is the correct stname) is not an outlier
                        st_zscore = ed_hn_outlier_chk(get_ed(hang_ind-hang_dir),get_name(hang_ind-hang_dir),get_hn(hang_ind-hang_dir))
                        if(st_zscore<4) :
                            if(st_zscore==-1) :
                                False
                                #DO SOMETHING ABOUT THIS
                            if (debug) : print('and was added to HANGOVERS.\n', end="")
                            #All cases checked with these criteria were valid ready-to-be-fixed hangovers, except 86289
                            test = HANGOVERS.copy()
                            HANGOVERS.add(frozenset([hang_ind,hang_ind-hang_dir]))
                            if(test == HANGOVERS) :
                                print("OH DEAR, THE SAME HANGOVER WAS IDENTIFIED TWICE")
                        else :
                            if (debug) : print('but there was something suspicious about abutting hn: %s.\n' %st_zscore, end="")
                    else :
                        if (debug) : print('dwel: %s fam: %s rel: %s\n' %(same_hh[1],same_hh[2],same_hh[3]), end="")
                        #if these are all false, we can still fix by seeing if there is another record with same
                        #hn, dwel_id and fam_id as the hangover record. If there's nothing suspicious about the other
                        #record, we can assume that one is the correct stname

                        #Another Validation to think about: look at other HNs for the given st and Block
                        #compare even-/odd-ness. Which decades do we have block ID for?
                        
                    #same hh chk works, but may be too restrictive?
                    # for example, at line 18600 the dwelling is same but other two vars are different
                    # and it is a valid hangover
                    
                    if(len(st_swatches)==2 and len(hn_swatches)==2) : #both guaranteed "otherwise well-defined" 
                        print(str(o)+" "+str(hn_swatches[1][0]==st_swatches[0][1])+" "+str(hn_swatches[0][1]==st_swatches[1][0]))
                    else :
                        print(str(o)+" "+str(len(hn_swatches))+" "+str(len(st_swatches)))


##CONS = []
##ind = 0
##while ind<len(Data) :
##    if 
print("Hangovers: "+str(len(HANGOVERS)))

errors = 0

#More useful outlier identification: outlying HH nums for a given st and ed
#e.g. St A in ED y has normal HN range 1000-2000. HN 5689 is flagged as outlier.
#This is then used as an additional piece of info when resolving Hangovers



for inc in INCONS_st[:0] :
    #find housenums that are outliers within a st-swatch (or otherwise normal housenum swatch - only one address diff)
    #compute standard deviation, median of housenums within st swatch
    #Standard Deviation should be calculated with respect to how much housenum deviates from previous num, as opposed
    # to how much it deviates from the distribution as a whole?
    
    #HOW WILL USING ALL HOUSENUMS AND NOT JUST 1 FOR EACH HOUSEHOLD AFFECT RESULTS?
    inc_nums = [row[2] for row in Data[inc[0]:inc[1]+1]]
    print("inc nums: "+str(inc_nums))
    z = get_cray_z_scores(inc_nums)
    
        
        #if z_score > 4, consider an outlier?
    
last = INCONS_hn[0]
print("# of incons "+ str(len(INCONS_hn)))
for inc in INCONS_hn[:0] :
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

