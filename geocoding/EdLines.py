#Automatic ED Boundary deducing program. Created by Amory Kisch.
import os
import csv
import xlrd
import sys
import numpy as np
import re
import math
from fuzzywuzzy import fuzz
import pickle
import arcpy


# (New) Program Logic #
# 1) Find all streets that intersect and share an ED #
# 2) Decide which intersections are ED boundaries vs. internal #
#     Resolve ambiguities* using microdata  #
# 3) To get ED boundaries, "connect" boundary intersections using #
#     existing street segments #
#
# *) 3-way intersections are always ambiguous - could be internal or boundary #
#    (even & odd = internal)


# Ideas to (Consider) Implement
# - Supplement Steve Morse ED data with microdata - which STs in which ED (SM incomplete!!) - DONE
# - Do address ambiguity resolution for 4-way intersections
#   - John's idea: analyze based on multiple EDs instead of only when there is one ED 
# - tweak even_or_odd(): either adjust threshold to .85, eliminate outliers from address list, or both - DONE
#   ->>> outlier detection was implemented. this changed the numbers although it's unclear if for the better!?
# - Do Fuzzymatching to match map names with morse&micro. DONE - improve results using TYPEs?
#   - only need to do this when name is not found, e.g. Potter's Ave from map does not match with Potters Ave from morse&micro
# - investigate using logic:
#   Intersection    A----B----C
#   ED              1    ?    2
#   Conclusion      B must be a boundary between 1 and 2
# - look at Matt's code and the results from it - how can approaches be combined (also '40 block descriptions,
#   '30 EDs that are coterminous with '40 EDs

# Problems:
# Directional Streets - fuzzy matching will match E Howard Ave w/ W Howard Ave instead of Howard Ave
# Numbered Streets - fuzzy matching will match S 27th St with S 17th St instead of 27th St
# ->->-> GO THRU CHRIS's fuzzy match, copy the code over

def standardize_street(st):
    runAgain = False
    st = st.rstrip('\n')
    orig_st = st
    
    st = st.lower()

    ###Remove Punctuation, extraneous words at end of stname###
    st = re.sub(r'[\.,]',' ',st)
    st = re.sub(' +',' ',st)
    st = st.strip()
    st = re.sub('\\\\','',st)
    st = re.sub(r' \(?([Cc][Oo][Nn][\'Tt]*d?|[Cc][Oo][Nn][Tt][Ii][Nn][Uu][Ee][Dd])\)?$','',st)
    #consider extended a diff stname#
    #st = re.sub(r' [Ee][XxsS][tdDT]+[^ ]*$','',st)

    #Check if st is empty or blank and return empty to [st,DIR,NAME,TYPE]
    if st == '' or st == ' ':
        return ['','','','']
    
    ###stname part analysis###
    DIR = ''
    NAME = ''
    TYPE = ''
 
    # Combinations of directions at end of stname (has to be run first)
    if re.search(r'[ \-]+([Nn][\.\-]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)$',st):
        st = "NE "+re.sub(r'[ \-]+([Nn][\.\-]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth[\s]+?[Ee]ast)$','',st)
        DIR = 'NE'
    if re.search(r'[ \-]+([Nn][\.\-]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$',st):
        st = "NW "+re.sub(r'[ \-]+([Nn][\.\-]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$','',st)
        DIR = 'NW'
    if re.search(r'[ \-]+([Ss][\.\-]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$',st):
        st = "SE "+re.sub(r'[ \-]+([Ss][\.\-]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$','',st)
        DIR = 'SE'
    if re.search(r'[ \-]+([Ss][\.\-]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$',st):
        st = "SW "+re.sub(r'[ \-]+([Ss][\.\-]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$','',st)
        DIR = 'SW'
   
    #First check if DIR is at end of stname. make sure that it's the DIR and not actually the NAME (e.g. "North Ave" or "Avenue E")#
    if re.search(r'[ \-]+([Nn]|[Nn][Oo][Rr]?[Tt]?[Hh]?)$',st) and not re.match('^[Nn][Oo][Rr][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+[Nn]$',st) :
        st = "N "+re.sub(r'[ \-]+([Nn]|[Nn][Oo][Rr]?[Tt]?[Hh]?)$','',st)
        DIR = 'N'
    if re.search(r'[ \-]+([Ss]|[Ss][Oo][Uu]?[Tt]?[Hh]?)$',st) and not re.search('^[Ss][Oo][Uu][Tt][Hh]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+[Ss]$',st) :
        st = "S "+re.sub(r'[ \-]+([Ss]|[Ss][Oo][Uu]?[Tt]?[Hh]?)$','',st)
        DIR = 'S'
    if re.search(r'[ \-]+([Ww][Ee][Ss][Tt]|[Ww])$',st) and not re.search('^[Ww][Ee][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+[Ww]$',st) :
        st = "W "+re.sub(r'[ \-]+([Ww][Ee][Ss][Tt]|[Ww])$','',st)
        DIR = 'W'
    if re.search(r'[ \-]+([Ee][Aa][Ss][Tt]|[Ee])$',st) and not re.search('^[Ee][Aa][Ss][Tt]$|[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+[Ee]$',st) :
        st = "E "+re.sub(r'[ \-]+([Ee][Aa][Ss][Tt]|[Ee])$','',st)
        DIR = 'E'

    #See if a st TYPE can be identified#
    st = re.sub(r'[ \-]+([Ss][Tt][Rr]?[Ee]?[Ee]?[Tt]?[SsEe]?|[Ss][\.][Tt]|[Ss][Tt]?.?[Rr][Ee][Ee][Tt])$',' St',st)
    #st = re.sub(r'[ \-]+[Ss]tr?e?e?t?[ \-]',' St ',st) # Fix things like "4th Street Place"
    st = re.sub(r'[ \-]+([Aa][Vv]|[Aa][VvBb][Ee][Nn][Uu]?[EesS]?|[aA]veenue|[Aa]vn[e]?ue|[Aa][Vv][Ee])$',' Ave',st)
    match = re.search("[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+([a-zA-Z])$",st)
    if match :
         st = re.sub("([a-zA-Z])$","",st)
         st = re.sub("[Aa][Vv][Ee]([Nn][Uu][Ee])?[ \-]+",match.group(2)+" Ave",st)
    st = re.sub(r'[ \-]+([Bb]\'?[Ll][Vv]\'?[Dd]|Bl\'?v\'?d|Blv|Blvi|Bly|Bldv|Bvld|Bol\'d|[Bb][Oo][Uu][Ll][EeAa]?[Vv]?[Aa]?[Rr]?[Dd]?)$',' Blvd',st)
    st = re.sub(r'[ \-]+([Rr][Dd]|[Rr][Oo][Aa][Dd])$',' Road',st)
    st = re.sub(r'[ \-]+[Dd][Rr][Ii]?[Vv]?[Ee]?$',' Drive',st)
    st = re.sub(r'[ \-]+([Cc][Oo][Uu]?[Rr][Tt]|[Cc][Tt])$',' Ct',st)
    st = re.sub(r'[ \-]+([Pp][Ll][Aa]?[Cc]?[Ee]?)$',' Pl',st)
    st = re.sub(r'[ \-]+([Ss][Qq][Uu]?[Aa]?[Rr]?[Ee]?)$',' Sq',st)
    st = re.sub(r'[ \-]+[Cc]ircle$',' Cir',st)
    st = re.sub(r'[ \-]+([Pp]rkway|[Pp]arkway|[Pp]ark [Ww]ay|[Pp]kway|[Pp]ky|[Pp]arkwy|[Pp]rakway|[Pp]rkwy|[Pp]wy)$',' Pkwy',st)
    st = re.sub(r'[ \-]+[Ww][Aa][Yy]$',' Way',st)
    st = re.sub(r'[ \-]+[Aa][Ll][Ll]?[Ee]?[Yy]?$',' Aly',st)
    st = re.sub(r'[ \-]+[Tt][Ee][Rr]+[EeAa]?[Cc]?[Ee]?$',' Ter',st)
    st = re.sub(r'[ \-]+([Ll][Aa][Nn][Ee]|[Ll][Nn])$',' Ln',st)
    st = re.sub(r'[ \-]+([Pp]lzaz|[Pp][Ll][Aa][Zz][Aa])$',' Plaza',st)
    st = re.sub(r'[ \-]+([Hh]ighway)$',' Hwy',st)
    st = re.sub(r'[ \-]+([Hh]eights?)$',' Heights',st)

    # "Park" is not considered a valid TYPE because it should probably actually be part of NAME #
    match = re.search(r' (St|Ave|Blvd|Pl|Drive|Road|Ct|Railway|CityLimits|Hwy|Fwy|Pkwy|Cir|Ter|Ln|Way|Trail|Sq|Aly|Bridge|Bridgeway|Walk|Heights|Crescent|Creek|River|Line|Plaza|Esplanade|[Cc]emetery|Viaduct|Trafficway|Trfy|Turnpike)$',st)
    if match :
        TYPE = match.group(1)

    #Combinations of directions
    
    match = re.search(r'^([Nn][Oo\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+',st)
    if match :
        if st == match.group(0)+TYPE :
            NAME = 'Northeast'
        else :
            st = "NE "+re.sub(r'^([Nn][Oo\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+','',st)
            DIR = 'NE'
    match = re.search(r'^([Nn][Oo\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+',st)
    if match :
        if st == match.group(0)+TYPE :
            NAME = 'Northwest'
        else :
            st = "NW "+re.sub(r'^([Nn][Oo\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+','',st)
            DIR = 'NW'
    match = re.search(r'^([Ss][Oo\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+',st)
    if match :
        if st == match.group(0)+TYPE :
            NAME = 'Southeast'
        else :
            st = "SE "+re.sub(r'^([Ss][Oo\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+','',st)
            DIR = 'SE'
    match = re.search(r'^([Ss][Oo\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+',st)
    if match :
        if st == match.group(0)+TYPE :
            NAME = 'Southwest'
        else :
            st = "SW "+re.sub(r'^([Ss][Oo\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+','',st)
            DIR = 'SW'
        
    #See if there is a st DIR. again, make sure that it's the DIR and not actually the NAME (e.g. North Ave, E St [not East St])
    if(DIR=='') :
        match =  re.search(r'^([nN]|[Nn]\.|[Nn]o|[nN]o\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+',st)
        if match :
            if st==match.group(0)+TYPE :
                if len(match.group(1))>1 :
                    NAME = 'North'
                else : NAME = 'N'
            else :
                st = "N "+re.sub(r'^([nN]|[Nn]\.|[Nn]o|[nN]o\.|[Nn][Oo][Rr][Tt]?[Hh]?)[ \-]+','',st)
                DIR = 'N'
        match =  re.search(r'^([sS]|[Ss]\.|[Ss]o|[Ss]o\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+',st)
        if match :
            if st==match.group(0)+TYPE :
                if len(match.group(1))>1:
                    NAME = 'South'
                else : NAME = 'S'
            else :
                st = "S "+re.sub(r'^([sS]|[Ss]\.|[Ss]o|[Ss]o\.|[Ss][Oo][Uu][Tt]?[Hh]?)[ \-]+','',st)
                DIR = 'S'
        match =  re.search(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+',st)
        if match :
            if st==match.group(0)+TYPE :
                if len(match.group(1))>1 :
                    NAME = 'West'
                else : NAME = 'W'
            else :
                st = "W "+re.sub(r'^([wW]|[Ww]\.|[Ww][Ee][Ss]?[Tt]?[\.]?)[ \-]+','',st)
                DIR = 'W'
        match =  re.search(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|[Ee]a[Ss]?)[ \-]+',st)
        if match :
            if st==match.group(0)+TYPE :
                if len(match.group(1))>1 :
                    NAME = 'East'
                else : NAME = 'E'
            else :
                st = "E "+re.sub(r'^([eE]|[Ee][\.\,]|[Ee][Ee]?[Aa]?[Ss][Tt][\.]?|[Ee]a[Ss]?)[ \-]+','',st)
                DIR = 'E'
                
    #get the st NAME and standardize it
            
    match = re.search('^'+DIR+'(.+)'+TYPE+'$',st)
    if NAME=='' :
        #If NAME is not 'North', 'West', etc...
        if match :
            NAME = match.group(1).strip()
            
            #convert written-out numbers to digits
            #TODO: Make these work for all exceptions (go thru text file with find)
            #if re.search("[Tt]enth|Eleven(th)?|[Tt]wel[f]?th|[Tt]hirteen(th)?|Fourt[h]?een(th)?|[Ff]ift[h]?een(th)?|[Ss]event[h]?een(th)?|[Ss]event[h]?een(th)?|[eE]ighteen(th)?|[Nn]inet[h]?een(th)?|[Tt]wentieth|[Tt]hirtieth|[Ff]o[u]?rtieth|[Ff]iftieth|[Ss]ixtieth|[Ss]eventieth|[Ee]ightieth|[Nn]inetieth|Twenty[ \-]?|Thirty[ \-]?|Forty[ \-]?|Fifty[ \-]?|Sixty[ \-]?|Seventy[ \-]?|Eighty[ \-]?|Ninety[ \-]?|[Ff]irst|[Ss]econd|[Tt]hird|[Ff]ourth|[Ff]ifth|[Ss]ixth|[Ss]eventh|[Ee]ighth|[Nn]inth",st) :
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
            
            if re.search("(^|[0-9]+.*)([Ff]irst|[Oo]ne)$",NAME) : NAME = re.sub("([Ff]irst|[Oo]ne)$","1st",NAME)
            if re.search("(^|[0-9]+.*)([Ss]econd|[Tt]wo)$",NAME) : NAME = re.sub("([Ss]econd|[Tt]wo)$","2nd",NAME)
            if re.search("(^|[0-9]+.*)([Tt]hird|[Tt]hree)$",NAME) : NAME = re.sub("([Tt]hird|[Tt]hree)$","3rd",NAME)
            if re.search("(^|[0-9]+.*)[Ff]our(th)?$",NAME) : NAME = re.sub("[Ff]our(th)?$","4th",NAME)
            if re.search("(^|[0-9]+.*)([Ff]ifth|[Ff]ive)$",NAME) : NAME = re.sub("([Ff]ifth|[Ff]ive)$","5th",NAME)
            if re.search("(^|[0-9]+.*)[Ss]ix(th)?$",NAME) : NAME = re.sub("[Ss]ix(th)?$","6th",NAME)
            if re.search("(^|[0-9]+.*)[Ss]even(th)?$",NAME) : NAME = re.sub("[Ss]even(th)?$","7th",NAME)
            if re.search("(^|[0-9]+.*)[Ee]igh?th?$",NAME) : NAME = re.sub("[Ee]igh?th?$","8th",NAME)
            if re.search("(^|[0-9]+.*)[Nn]in(th|e)+$",NAME) : NAME = re.sub("[Nn]in(th|e)+$","9th",NAME)
            
            if re.search("[0-9]+",NAME) :
                if re.search("^[0-9]+$",NAME) : #if NAME is only numbers (no suffix), add the correct suffix
                    foo = True
                    suffixes = {'11':'11th','12':'12th','13':'13th','1':'1st','2':'2nd','3':'3rd','4':'4th','5':'5th','6':'6th','7':'7th','8':'8th','9':'9th','0':'0th'}
                    num = re.search("[0-9]+$",NAME).group(0)
                    suff = ''
                    # if num is not found in suffixes dict, remove leftmost digit until it is found... 113 -> 13 -> 13th;    24 -> 4 -> 4th
                    while(suff=='') :
                        try :
                            suff = suffixes[num]
                        except KeyError :
                            num = num[1:]
                            if len(num) == 0 :
                                break
                    if not suff == '' :
                        NAME = re.sub(num+'$',suff,NAME)
                else :
                    # Fix incorrect suffixes e.g. "73d St" -> "73rd St"
                    if re.search("[23]d$",NAME) :
                        NAME = re.sub("3d","3rd",NAME)
                        NAME = re.sub("2d","2nd",NAME)
                    if re.search("1 [Ss]t|2 nd|3 rd|1[1-3] th|[04-9] th",NAME) :
                        try :
                            suff = re.search("[0-9] ([Sa-z][a-z])",NAME).group(1)
                        except :
                            print("NAME: "+NAME+", suff: "+suff+", st: "+st)
                        NAME = re.sub(" "+suff,suff,NAME)
                    # TODO: identify corner cases with numbers e.g. "51 and S- Hermit"
                
                # This \/ is a bit overzealous...! #
                hnum = re.search("^([0-9]+[ \-]+).+",NAME) #housenum in stname?
                if hnum : 
                    #False
                    NAME = re.sub(hnum.group(1),"",NAME) #remove housenum. May want to update housenum field, maybe not though.
                    runAgain = True
            else :
                NAME = NAME.title()
            
        else :
            assert(False)
        # Standardize "St ____ Ave" -> "Saint ____ Ave" #
        NAME = re.sub("^([Ss][Tt]\.?|[Ss][Aa][Ii][Nn][Tt])[ \-]","Saint ",NAME)
    st = re.sub(re.escape(match.group(1).strip()),NAME,st).strip()
    try :
        assert st == (DIR+' '+NAME+' '+TYPE).strip()
    except AssertionError :
        print("Something went a bit wrong while trying to pre-standardize stnames.")
        print("orig was: "+orig_st)
        print("st is: \""+st+"\"")
        print("components: ["+(DIR+','+NAME+','+TYPE).strip()+"]")
    
    if runAgain :
        return standardize_street(st)
    else :
        return [st, DIR, NAME, TYPE]



def csv_from_excel(excel_file, csv_name):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    for i,worksheet_name in enumerate(all_worksheets[:-1]) : #exclude last worksheet (1940 stnames)
        worksheet = workbook.sheet_by_name(worksheet_name)
        if i==0 :
            namename = csv_name
        elif i == 1 :
            namename = csv_name+"_ED"
        else :
            assert(True == False)
        with open('{}.csv'.format(namename), 'w+') as your_csv_file:
            for rownum in range(worksheet.nrows):
                rowstr = ""
                for v in worksheet.row_values(rownum) :
                    if v=="" :
                        break
                    rowstr = rowstr+v+","
                rowstr = rowstr[:-1] #remove trailing comma
                your_csv_file.write(rowstr+"\n")
                

SMLines = None
SMLines1 = None
InterLines = None
MicroLines = None

# Morse Dicts: #
ST_ED_DICT = {} # lookup ST -> which EDs
ED_ST_DICT = {} # lookup ED -> which STs

# Map Dicts: #
Intersect_ST_DICT = {} # lookup intersection -> which STs (names)
Intersect_BLOCK_DICT = {} # lookup intersection -> which BLOCKs
ST_Intersect_DICT = {} # lookup ST -> which intersections
BLOCK_Intersect_DICT = {} # lookup BLOCK ID -> which intersections

# Micro Dicts: #
ST_ED_Address_DICT = {} # lookup ST_ED -> list all addresses in ED
ST_Address_DICT = {} # lookup ST -> list all addresses in city
ST_ED_DICT_mi = {} # lookup ST -> which EDs
ED_ST_DICT_mi = {} # lookup ED -> which STs

# Derived Dict: #
Intersect_Info_DICT = {} # lookup intersection -> list of information


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
    NAME = re.sub("[Ff]ifty[ST_ED_DICT \-]*","5",NAME)
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


def morse_standardize(st) :
    if re.search('[Cc]ity [Ll]imits',st) :
        return 'City Limits'
    st = re.sub(" [Rr]iv($| St$)"," River",st)
    st = re.sub("^Mt ","Mount ",st)
    return st


def load_steve_morse(city, state, year):

    #NOTE: This dictionary must be built independently of this script
    sm_st_ed_dict_file = pickle.load(open(file_path + '/%s/sm_st_ed_dict%s.pickle' % (str(year), str(year)), 'rb'))
    sm_st_ed_dict_nested = sm_st_ed_dict_file[(city, '%s' % (state.lower()))]

    #Flatten dictionary
    temp = {k:v for d in [v for k, v in sm_st_ed_dict_nested.items()] for k, v in d.items()}

    #Capture all Steve Morse streets in one list
    sm_all_streets = temp.keys()

    #
    # Build a Steve Morse (sm) ED-to-Street (ed_st) dictionary (dict)
    #

    sm_ed_st_dict = {}
    #Initialize a list of street names without an ED in Steve Morse
    sm_ed_st_dict[''] = []
    for st, eds in temp.items():
        #If street name has no associated EDs (i.e. street name not found in Steve Morse) 
        #then add to dictionary entry for no ED
        if eds is None:
            sm_ed_st_dict[''].append(st)
        else:
            #For every ED associated with a street name...
            for ed in eds:
                #Initalize an empty list if ED has no list of street names yet
                sm_ed_st_dict[ed] = sm_ed_st_dict.setdefault(ed, [])
                #Add street name to the list of streets
                sm_ed_st_dict[ed].append(st)

    return sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict


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

# returns list of all EDs shared by all streets in st_ed_dict_chk
def ED_in_common(st_ed_dict_chk) :
    EDs = list(st_ed_dict_chk.values())
    in_common = set(EDs[0])
    for i in EDs[1:] :
        in_common = in_common & set(i)
    return list(in_common)

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

# Function that takes a list of streets and returns the street name that appears only once, if it exists
def find_unique_st(st_list) :
    unique_sts = []
    redundant_sts = []
    for st in st_list :
        if st not in unique_sts :
            if st not in redundant_sts :
                unique_sts.append(st)
        else :
            unique_sts.remove(st)
            redundant_sts.append(st)
    if not len(unique_sts) == 1 :
        raise ValueError("Failed to find a single unique street")
    else :
        return unique_sts,redundant_sts

#helper function for is_ED_boundary
#if >= 90% of addresses are even or odd, return 'even' or 'odd', respectively. Otherwise, return 'both'
def even_or_odd(Address_List) :
    even_cnt = 0
    odd_cnt = 0
    if len(Address_List) < 2 :
        return 'na'
    for a_str in Address_List :
        try :
            a = int(a_str)
            if a%2 == 0 :
                even_cnt = even_cnt+1
            else :
                odd_cnt = odd_cnt+1
        except ValueError :
            print("not an address #: "+str(a_str))

    if even_cnt / len(Address_List) >= .9 :
        return 'even'
    elif odd_cnt / len(Address_List) >= .9 :
        return 'odd'
    else :
        return 'both'
        
# function for resolving ambiguous 3-way intersections
def is_ED_boundary(st,ED) :
    #print("called ED boundary")
    try :
        temp_addresses_unfiltered = ST_ED_Address_DICT[st+ED]
    except KeyError : #st_ed from map+morse not found in micro
        return 'nfm'
    temp_addresses = list(filter(lambda x: not (x==None or x=='' or x==' ' or x=='nan'),temp_addresses_unfiltered))
    for a in list(temp_addresses) :
        try :
            float(a)
        except :
            temp_addresses.remove(a)
    ED_addr_outliers = get_cray_z_scores([int(x) for x in temp_addresses if not math.isnan(float(x))])
    if ED_addr_outliers == None : #this happens if there's only 1 or 2 addresses in temp_addresses
        ED_Addresses = temp_addresses
    else :
        ED_Addresses = list(filter(lambda x: ED_addr_outliers[int(x)]<4, temp_addresses))
        #print(temp_addresses)
        #print(ED_Addresses)

    City_Addresses = list(filter(lambda x: not (x==None or x=='' or x==' ' or x=='nan'),ST_Address_DICT[st]))
    city_even_odd = even_or_odd(City_Addresses)
    ED_even_odd = even_or_odd(ED_Addresses)
    if city_even_odd == 'na' or ED_even_odd == 'na' :
        return 'na'
    if city_even_odd == 'both' and not ED_even_odd == 'both' :
        return 'yes'
    else :
        return 'no'

# returns a list of all street phrases in st_dict that have the NAME name
# expects a dict with st_phrase -> st_name keys and values
def get_st_by_name(name, st_dict) :
    name_list = []
    for k,v in st_dict.items() :
        if v == name :
            name_list.append(k)
    return name_list

#Returns just the NAME component of the street phrase, if any#
#If second argument is True, return a list of all components 
def isolate_st_name(st,whole_phrase = False) :
    if (st == None or st == '' or st == -1) or (not isinstance(st, str)) :
        print("it is "+str(whole_phrase))
        print(str(st)+" is not a silly string")
        return None
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

# return all EDs associated with st according to st_ed_dict_chk
# st can be a string or an iterable of strings
def get_eds_by_st(st,st_ed_dict_chk) :
    if st == None :
        return None
    if isinstance(st,str) :
        return st_ed_dict_chk[st]
    ed_list = []
    for s in st :
        ed_list = ed_list + st_ed_dict_chk[s]
    return list(np.unique(ed_list))
        


# match based on entire street phrase, but favor matches with an exact match for NAME
##    principles:
##        don't return any match below 85 unless exact NAME match
##        don't return any match where TYPEs conflict (it's NOT OK if TYPE is missing from match)
##        if DIR does not match, favor matches with no DIR
##        always return highest scoring exact NAME match, unless it violates the above principles

##  --> the only time we eschew an exact NAME match for a non-exact NAME match is when the TYPE does not match
##  --> we may eschew an exact NAME match for a lower-scoring exact NAME match if the TYPEs or DIRs conflict in the higher-scoring match
def fuzzy_match(phrase,st_list) :
    if (not isinstance(phrase, str)) or (phrase == None or phrase == '' or phrase == -1):
        print(str(phrase)+" is not a gosh darn string")
        return None
    debug = False
    
    possible_match = []
    exact_name_match = []
    phrase_list = isolate_st_name(phrase,True)
    DIR = phrase_list[0]
    NAME = phrase_list[1]
    TYPE = phrase_list[2]
    for st in st_list: 
        if(not st=="") :
            score = fuzz.ratio(phrase,st)
            match_NAME = isolate_st_name(st)
            NAME_score = fuzz.ratio(NAME,match_NAME)
            
            if score >= 75 or NAME_score == 100 and score > 50 :
                if NAME_score == 100 :
                    exact_name_match.append((score,st))
                else :
                    possible_match.append((score,st))
    if debug :print("exact name matches: "+str(exact_name_match))
    if debug :print("other matches: "+str(possible_match))
    name_type_match = {}
    dir_name_match = []
    exact_name_dict = {}
    for score, st in exact_name_match :
        Dict_append_unique(exact_name_dict,score, st)
    for score in reversed(sorted(exact_name_dict)) :#iterate from highest to lowest score
        matches = exact_name_dict[score]
        matches_to_return = []
        for m in matches :
            m_list = isolate_st_name(m,True)
            m_DIR = m_list[0]
            m_TYPE = m_list[2]
            if m_DIR == None and m_TYPE == TYPE :
                matches_to_return.append(m)
            if m_TYPE == TYPE :
                Dict_append_unique(name_type_match,score,m)
            if m_DIR == DIR :
                dir_name_match.append((score,m))
        if matches_to_return :
            return set(matches_to_return)

    for score in reversed(sorted(name_type_match)) :
        return set(name_type_match[score]) # return highest score with name and type matching, if it exists
    
    possible_match.sort()
    for _,m in reversed(possible_match) :
        m_list = isolate_st_name(m,True)
        m_TYPE = m_list[2]
        if(m_TYPE == TYPE) :
            return m




# Main Program Loop - also outputs statistics and results to .txt files
def RunAnalysis(city_name) :
    #Put this  on  hold until it can be standardized or discarded, as necessary (based on the decade comparison of SM 10/30/40)
    #SM_st_corrections = pickle.load( open("SM_decade_compare_st_corrections.p","rb"))
    print("Processing Input Files")

    # Create Map DICTs
    for ind, iline in enumerate(InterLines) :
        IList = iline.rstrip().split(",")
        NAME = Num_Standardize(IList[6])
        Dict_append(Intersect_ST_DICT,IList[-1],NAME)
        Dict_append_unique(ST_Intersect_DICT,NAME,IList[-1])
        Dict_append_unique(Intersect_BLOCK_DICT,IList[-1],IList[7])
        Dict_append_unique(BLOCK_Intersect_DICT,IList[7],IList[-1])

        

    # Create Morse DICTs
    for ind, sline in enumerate(SMLines) : #
        st = morse_standardize(sline[0])
        EDList = list(filter(None,sline[1:]))
##        try :
##            temp = SM_st_corrections[("Hartford","ct")][st]
##            if not st == temp :
##                print("%s changed to %s" % (st,temp))
##                st = temp
##        except KeyError :
##            pass
        
        if not st=="" :
            ST_ED_DICT[st] = EDList
        for ed in EDList :
            Dict_append_unique(ED_ST_DICT,ed,st)

    # Create Micro DICTs
    for ind, mline in enumerate(MicroLines) :
        MList = mline.rstrip().split(",")
        NAME = standardize_street(MList[2])[0]
        ED = MList[3]
        ADDR = MList[6]
        Dict_append_unique(ST_ED_Address_DICT,NAME+ED,ADDR) # used to be Dict_append_unique!!!
        Dict_append_unique(ST_Address_DICT,NAME,ADDR) # used to be Dict_append_unique!!!
        
        Dict_append_unique(ST_ED_DICT_mi,NAME,ED)
        Dict_append_unique(ED_ST_DICT_mi,ED,NAME)



    SM_streets = ST_ED_DICT.keys()#all streets found in Steve Morse
    micro_streets = ST_ED_DICT_mi.keys() #all streets found in Micro

    print("Finished preparing files. Starting Intersections analysis.")
    # Intersections Analysis loop
    for i,slist in Intersect_ST_DICT.items() :
        debug = False
        # i is the current intersection ID
        #get list of STs in i, filter out blank STs
        STList = list(filter(lambda x: not x==' ' and not x=='',np.unique(slist))) #unique street names
        discrete_st_list = list(filter(lambda x: not x==' ' and not x=='',slist)) #all street names
        if len(STList) > 1 :
            proceed = True
            match_ed_dict = {}
            for st in STList :
                # for each street in intersection, find fuzzy matches with morse and micro and collect ED data for that street from both sources
                match_ed_dict[st] = []
                morse_match = fuzzy_match(st,SM_streets)
                if not morse_match == None :
                    match_ed_dict[st] = match_ed_dict[st] + get_eds_by_st(morse_match,ST_ED_DICT)
                micro_match = fuzzy_match(st,micro_streets)
                if not micro_match == None :
                    match_ed_dict[st] = match_ed_dict[st] + get_eds_by_st(micro_match,ST_ED_DICT_mi)
                match_ed_dict[st] = list(np.unique(match_ed_dict[st]))
            
            EDs = ED_in_common(match_ed_dict)

            if proceed :
                if "City Limits" in STList :
                    Intersect_Info_DICT[i] = ['b',[int(x) for x in EDs]]
                elif EDs == None or EDs == [] : #Steve Morse contradicts map
                    Intersect_Info_DICT[i] = ['mc',STList]
                    #print("no ED data: "+str(STList))
                else : #all streets in intersection share at least 1 ED
                    
                    BLOCKs = Intersect_BLOCK_DICT[i]
                    
                    if(len(EDs)==1 and len(BLOCKs)>3) :
                        Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal
                    else :
                        if(len(EDs)==1 and len(BLOCKs)==3) : # 3-way intersections #
                            # resolve ambiguity using addresses
                            try :
                                _,ambig_st = find_unique_st(discrete_st_list) #ambig_st is the non-unique st in the intersection
                            except ValueError :
                                if debug : print("couldn't find a unique st out of "+str(discrete_st_list))
                                Intersect_Info_DICT[i] = ['a'] #ambiguous
                            ED_bound_test = is_ED_boundary(ambig_st[0],EDs[0])
                            if ED_bound_test == "nfm" : #st_ed from map+morse not found in micro
                                Intersect_Info_DICT[i] = ['nfm',int(EDs[0])]
                            elif ED_bound_test == "na" :
                                Intersect_Info_DICT[i] = ['na',int(EDs[0])]
                            elif ED_bound_test == "yes" :
                                Intersect_Info_DICT[i] = ['b',int(EDs[0])] #boundary
                            else :
                                Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal
                        elif len(EDs)>1 :
                            Intersect_Info_DICT[i] = ['e',[int(x) for x in EDs]] #external (could include boundary intersections) - associated with more than one ED
                        elif len(EDs)==1 :
                            Intersect_Info_DICT[i] = ['i',int(EDs[0])] #internal, 2-way
                        else :
                            print("something is up with intersection "+str(i))
                            assert (False == True)
        

    internal_cnt = 0
    external_cnt = 0
    nf_cnt = 0
    boundary_cnt = 0
    contradiction_cnt = 0
    nf_micro_cnt = 0
    na_cnt = 0

    ED_Intersect_DICT = {}

    for i,info in Intersect_Info_DICT.items() :
        if(info[0] == 'e') :
           external_cnt = external_cnt+1
        if(info[0] == 'i') :
            internal_cnt=internal_cnt+1
            Dict_append(ED_Intersect_DICT,info[1],i)
        if(info[0] == 'nf') :
            nf_cnt = nf_cnt+1
            #print(str(i)+": 1 not found in Morse: "+str(Intersect_ST_DICT[i]))
        if(info[0] == 'b') :
            boundary_cnt = boundary_cnt+1
        if(info[0] == 'mc') :
            contradiction_cnt = contradiction_cnt+1
        if(info[0] == 'nfm') :
            nf_micro_cnt = nf_micro_cnt+1
        if(info[0] == 'na') :
            na_cnt = na_cnt+1
    print(city_name+" analysis finished.")
    print("internal: "+str(internal_cnt))
    print("external: "+str(external_cnt))
    print("boundary: "+str(boundary_cnt))
    print("not found in Morse or micro: "+str(nf_cnt))
    print("Morse contradicts map: "+str(contradiction_cnt))
    print("st_ed from map+morse not found in micro: "+str(nf_micro_cnt))
    print("not enough address data to resolve ambiguity: "+str(na_cnt))

    nf_list = []
    for i,info in Intersect_Info_DICT.items() :
        if(info[0]=='nf') :
            STlist = Intersect_ST_DICT[i]
            for st in STlist :
                try :
                    ST_ED_DICT[st]
                except KeyError :
                    nf_list.append(st)


    Output_TXT = open(city_name+'IntersectionsStatistics.txt','w+')
    Output_TXT.write("internal: "+str(internal_cnt)+"\n")
    Output_TXT.write("external: "+str(external_cnt)+"\n")
    Output_TXT.write("boundary: "+str(boundary_cnt)+"\n")
    Output_TXT.write("not found in Morse: "+str(nf_cnt)+"\n")
    Output_TXT.write("Morse contradicts map: "+str(contradiction_cnt)+"\n")
    Output_TXT.write("st_ed from map+morse not found in micro: "+str(nf_micro_cnt)+"\n")
    Output_TXT.write("not enough address data to resolve ambiguity: "+str(na_cnt))

    Output_TXT = open(city_name+'IntersectionsResults.csv','w+')
    for i,info in Intersect_Info_DICT.items() :
        if len(info)==2 :
            Output_TXT.write(i+","+info[0]+",\""+re.sub("[\[\]]",'',str(info[1]).replace(',','|'))+"\"\n")
        else :
            Output_TXT.write(i+","+info[0]+"\n")

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
        print("max_freq prob")
        print(l)
        return -999
    return [x[0] for x in mode_dict.items() if x[1]==max_freq]

# given a intersect->info dict for a particular block, return what ED the block should be in
def aggregate_blk_inter_data(inter_dict) :
    possible_eds = []
    for k,v in inter_dict.items() :
        if isinstance(v[1],int) :
            possible_eds += [v[1]]
        if isinstance(v[1],list) :
            try :
                possible_eds += [int(x) for x in v[1]]
            except :
                return 0
        mode = find_mode(possible_eds)
        if mode == -999 :
            print(inter_dict)
            return 0
        if len(mode) == 1 :
            return mode[0]
        else :
            return '|'.join([str(x) for x in mode])  
            

def draw_EDs(pblk_filename) :
    targ = path_to_city+"\\IntersectionsIntermediateFiles\\"+city+"_1930_stgrid_edit_Uns2_spatial_join.shp"
    targ1 = path_to_city+"\\"+pblk_filename
    try :
        inter = arcpy.Intersect_analysis(in_features=[targ,targ1], \
                             out_feature_class=path_to_city+"\\IntersectionsIntermediateFiles\\intersectToGetEDs.shp",join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")
    except :
        print("poo")
        #inter = "C:/Users/akisch/Documents/ArcGIS/Default.gdb/StLouisMO_1930_stgrid_edit_U2"
    field_names = [x.name for x in arcpy.ListFields(inter)]
    cursor = arcpy.da.SearchCursor(inter, field_names)
    inter_polyblk_dict = {}
    polyblk_inter_dict = {} #polygon block ID -> intersections in block
    
    for row in cursor :
        Dict_append_unique(inter_polyblk_dict, row[field_names.index("Interse_ID")], row[field_names.index("pblk_id")])
        Dict_append_unique(polyblk_inter_dict, row[field_names.index("pblk_id")], row[field_names.index("Interse_ID")])

    blk_ed_dict = {}
    for blk in polyblk_inter_dict.keys() :
            #retrieve a slice of Intersect_Info_DICT for just the intersections associated with blk
            blk_dict = {key: Intersect_Info_DICT[key] for key in Intersect_Info_DICT.viewkeys() if int(key) in polyblk_inter_dict[blk]}
            result = aggregate_blk_inter_data(blk_dict)
            blk_ed_dict[blk] = result
    try :
        arcpy.AddField_management (targ1, "AmoryED", "TEXT")
    except :
        pass
    with arcpy.da.UpdateCursor(targ1, ["pblk_id","AmoryED"]) as up_cursor:
        for row in up_cursor :
            row[1] = blk_ed_dict[row[0]]
            if row[1] == None :
                row[1] = 0
            up_cursor.updateRow(row)
    return polyblk_inter_dict
                

def prepare_map_intersections(stgrid_file) :
    print("Preparing Map Intersections File")
    arcpy.env.overwriteOutput = True
    
    os.chdir(path_to_city)
    if not os.path.exists("IntersectionsIntermediateFiles"):
        os.makedirs("IntersectionsIntermediateFiles")

    city_name, _ =  os.path.splitext(stgrid_file)

    latest_stage = path_to_city+"\\IntersectionsIntermediateFiles\\fullname_dissolve.shp"
    #dissolve all street segments based on FULLNAME
    arcpy.Dissolve_management(in_features = stgrid_file, out_feature_class = latest_stage,
                              dissolve_field="FULLNAME", statistics_fields="", multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES")

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
                               field_mapping="""FID_fullna "FID_fullna" true true false 10 Long 0 10 ,First,#,"""+target_feature_file+""",FID_fullna,-1,-1;FULLNAME "FULLNAME" true true false 100 Text 0 0 ,First,#,"""+target_feature_file+""",FULLNAME,-1,-1;ORIG_FID "ORIG_FID" true true false 10 Long 0 10 ,First,#,"""+target_feature_file+""",ORIG_FID,-1,-1;POINT_X "POINT_X" true true false 19 Double 0 0 ,First,#,"""+target_feature_file+""",POINT_X,-1,-1;POINT_Y "POINT_Y" true true false 19 Double 0 0 ,First,#,"""+target_feature_file+""",POINT_Y,-1,-1;POINT_X_1 "POINT_X_1" true true false 19 Double 0 0 ,First,#,"""+previous_stage+""",POINT_X,-1,-1;POINT_Y_1 "POINT_Y_1" true true false 19 Double 0 0 ,First,#,"""+previous_stage+""",POINT_Y,-1,-1;Interse_ID "Interse_ID" true true false 10 Long 0 10 ,First,#,"""+previous_stage+""",Interse_ID,-1,-1""",
                               match_option="INTERSECT", search_radius="", distance_field_name="")

    # EXPORT ATTRIBUTE TABLE
    arcpy.ExportXYv_stats(Input_Feature_Class = latest_stage, Value_Field="FID;Join_Count;TARGET_FID;FID_fullna;FULLNAME;ORIG_FID;POINT_X;POINT_Y;POINT_X_1;POINT_Y_1;Interse_ID", Delimiter="COMMA",
                          Output_ASCII_File = path_to_city+"\\IntersectionsIntermediateFiles\\"+city_name+"_Intersections.txt", Add_Field_Names_to_Output="ADD_FIELD_NAMES")

    

### THIS IS WHERE YOU ENTER THINGS:
# Change directory to the folder with the input text file:  

city = "StLouisMO"
decade = 1930



#for city in ["BostonMA","ChicagoIL","CincinnatiOH","PhiladelphiaPA","StLouisMO"] :

city_name = re.sub("[A-Z][A-Z]$","",city)
path_to_city = "S:\\Projects\\1940Census\\"+city_name+"\\GIS_edited"
Micro_TXT = open(path_to_city+"\\"+city_name+'_1930_Addresses.csv')

sm_path = r"S:\Projects\1940Census\SMlists"
os.chdir(sm_path+"\\"+str(decade))
csv_name = city+"_SM"
csv_from_excel(csv_name+".xlsx",csv_name)

SM_ED_TXT = open(csv_name+".csv",'r')
SM_ED_TXT1 = open(csv_name+"_ED.csv",'r')

prepare_map_intersections(city+'_1930_stgrid_edit_Uns2.shp')

Intersect_TXT = open(path_to_city+"\\IntersectionsIntermediateFiles\\"+city+'_1930_stgrid_edit_Uns2_Intersections.txt')
SMLines = csv.reader(SM_ED_TXT)
next(SMLines, None)  # skip header
SMLines1 = csv.reader(SM_ED_TXT1)
InterLines = Intersect_TXT.readlines()[1:]
MicroLines = Micro_TXT.readlines()[1:]

RunAnalysis(city)

print("Creating ED Map")
draw_EDs(city_name+"_1930_Pblk.shp")

