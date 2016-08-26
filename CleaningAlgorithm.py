#
#	Name: 		CleaningAlgorithm.py
#	Authors: 	Chris Graziul, Amory Kisch
#
#	Input:		file_name - File name of city file, saved in Stata 13 (or below) format
#	Output:		<file_name>_autocleaned.csv - City file with addresses cleaned 
#
#	Purpose:	This is the master script for automatically cleaning addresses before
#				manually cleaning the file using Ancestry images. Large functions will
#				eventually become separate scripts that will be further refined and
#				called from this script.
#

import urllib
import re
import os
import sys
import time
import numpy as np
import pandas as pd
from multiprocessing import Pool
import fuzzyset
from termcolor import colored, cprint
from colorama import AnsiToWin32, init

year = int(sys.argv[1])

#Pretty output for easy reading
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#
#   Function to clean street direction and street type
#
#   Author: Amory Kisch
#   Date:   7/17/16
#

def preclean_dir_type(st):
    runAgain = False
    st = st.rstrip('\n')
    orig_st = st

    ###Remove Punctuation, extraneous words at end of stname###
    st = re.sub(r'[\.,]','',st)
    st = re.sub('\\\\','',st)
    st = re.sub(r' \(?([Cc]on[\'t]*d?|[Cc]ontinued)\)?$','',st)
    #consider extended a diff stname#
    #st = re.sub(r' [Ee][XxsS][tdDT]+[^ ]*$','',st)

    #Check if st is empty or blank and return empty to [st,DIR,NAME,TYPE]
    if st == '' or st == ' ':
        return ['','','','']
     
    ###stname part analysis###
    DIR = ''
    NAME = ''
    TYPE = ''
 
    # Combinations of directions (has to be run first)
    if re.search(r' ([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)$',st):
        st = "NE "+re.sub(r' ([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth[\s]+?[Ee]ast)$','',st)
        DIR = 'NE'
    if re.search(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$',st):
        st = "NW "+re.sub(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)$','',st)
        DIR = 'NW'
    if re.search(r' ([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$',st):
        st = "SE "+re.sub(r' ([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)$','',st)
        DIR = 'SE'
    if re.search(r' ([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$',st):
        st = "SW "+re.sub(r' ([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)$','',st)
        DIR = 'SW'
   
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

    #Combinations of directions (assumes no streets named "Northeast Ave" or similar)
    if re.search(r'^([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+',st):
        st = "NE "+re.sub(r'^([Nn][\.]?[\s]?[Ee][\.]?|[Nn]ortheast|[Nn]orth\s+?[Ee]ast)[ \-]+','',st)
        DIR = 'NE'
    if re.search(r'^([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+',st):
        st = "NW "+re.sub(r' ([Nn][\.]?[\s]?[Ww][\.]?|[Nn]orthwest|[Nn]orth\s+?[Ww]est)[ \-]+','',st)
        DIR = 'NW'
    if re.search(r'^([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+',st):
        st = "SE "+re.sub(r'^([Ss][\.]?[\s]?[Ee][\.]?|[Ss]outheast|[Ss]outh\s+?[Ee]ast)[ \-]+','',st)
        DIR = 'SE'
    if re.search(r'^([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+',st):
        st = "SW "+re.sub(r'^([Ss][\.]?[\s]?[Ww][\.]?|[Ss]outhwest|[Ss]outh\s+?[Ww]est)[ \-]+','',st)
        DIR = 'SW'
        
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

    if NAME=='' :
        match = re.search(DIR+'(.+)'+TYPE,st)
        if match :
            NAME = match.group(1).strip()
            if re.search("[0-9]+",NAME) :
                # TODO: Fix incorrect suffixes e.g. "73d St"
                '''
                if re.search("^[0-9]+[Ss][Tt]",NAME):
                    NAME = re.sub("[Ss][Tt]","st",NAME)
                if re.search("^[0-9]+[Rr][Dd]",NAME):
                    NAME = re.sub("[Rr][Dd]","rd",NAME)
                if re.search("^[0-9]+[Nn][Dd]",NAME):
                    NAME = re.sub("[Nn][Dd]","nd",NAME)
                if re.search("^[0-9]+[Tt][Hh]",NAME):
                    NAME = re.sub("[Tt][Hh]","th",NAME)     
                '''             
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
            st = re.sub(re.escape(match.group(1).strip()),NAME,st)
        else :
            assert(False)
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

def clean_microdata(city):

    city_name = city[2]
    state_abbr =city[3]
    year = city[5]
    if year == 1930:
        file_name = city[0].lower() + city[3]
    else:
        file_name = city[0] + city[3]
    sm_web_abbr = city[4]

    #Helper function for checking that microdata ED is in Steve Morse list of EDs for street name
    def check_ed_match(microdata_ed,sm_st):
        if (sm_st is None) or (sm_st_ed_dict[sm_st] is None):
            return False
        else:
            if microdata_ed in sm_st_ed_dict[sm_st]:
                return True
            else:
                return False

    def sm_fuzzy_match(sm_st,ed):
        
        #Return null if sm_st is blank
        if sm_st == '':
            return ['','',False]

        #Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
        try:
            sm_ed_streets = sm_ed_st_dict[ed]
            sm_ed_streets_fuzzyset = fuzzyset.FuzzySet(sm_ed_streets)
        except:
            problem_EDs.append(ed)
            return ['','',False]
        #
        #Step 1: Find best match among streets associated with microdata ED
        try:
            best_match_ed = sm_ed_streets_fuzzyset[sm_st][0]
        except:
            return ['','',False]
    #   best_match_ed = process.extractOne(sm_st,sm_ed_streets)
        #Step 2: Find best match among all streets
        try:
            best_match_all = sm_all_streets_fuzzyset[sm_st][0]
        except:
            return ['','',False]    
    #   best_match_all = process.extractOne(sm_st,sm_all_streets)
        #Step 3: If both best matches are the same, return as best match
        if (best_match_ed[1] == best_match_all[1]) & (best_match_ed[0] > 0.5):
            return [best_match_ed[1],best_match_ed[0],True]
        else:
            return ['','',False]

    #Helper function (necessary since dictionary built only for cases without validated exact matches)
    def get_fuzzy_match(sm_st,ed):
        try:
            return sm_fuzzy_match_dict[sm_st,ed]
        except:
            return ['','',False]

    #Save to logfile
    init()
    sys.stdout = open(file_path + "/logs/%s_Cleaning.log" % (city_name),'wb')

    cprint('%s Automated Cleaning\n' % (city_name), attrs=['bold'], file=AnsiToWin32(sys.stdout))

    start_total = time.time()

    #
    #	Import data
    #

    start = time.time()

    try:
        df = pd.read_stata(file_path + '/%s.dta' % (file_name), convert_categoricals=False)
    except:
        return [year, city_name, state_abbr, 0, 
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0, 0,
    0, 0, 0, 0, 0] 

    #df = pd.read_stata('%sStata13.dta' % (file_name))
    end = time.time()

    num_records = len(df)

    load_time = round(float(end-start)/60,1)
    cprint('Loading data for %s took %s' % (city_name,load_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

    #Save a pristine copy for debugging
    df_save = df

    #The original variable names change from census to census

    if year == 1930:
        df['street'] = df['self_residence_place_streetaddre']
    if year == 1920:
        df['street'] = df['indexed_street']
    if year == 1910:
        df['street'] = df['Street']
    
    if year == 1940:
        df['ed'] = df['derived_enumdist']
    if year == 1930:
        df['ed'] = df['indexed_enumeration_district']
    if year == 1920:
        df['ed'] = df['general_enumeration_district']
    if year == 1910:
        df['ed'] = df['EnumerationDistrict']
    
    #Strip leading zeroes from EDs
    df['ed'] = df['ed'].astype(str)
    df['ed'] = df['ed'].str.split('.').str[0]
    df['ed'] = df['ed'].str.lstrip('0')

    #
    # Pre-clean data
    #

    start = time.time()
    #Create dictionary for (and run precleaning on) unique street names
    grouped = df.groupby(['street'])
    cleaning_dict = {}
    for name,_ in grouped:
    	cleaning_dict[name] = preclean_dir_type(name)
    #Use dictionary create st (cleaned street), DIR (direction), NAME (street name), and TYPE (street type)
    df['st'] = df.street.apply(lambda s: cleaning_dict[s][0])
    df['DIR'] = df.street.apply(lambda s: cleaning_dict[s][1])
    df['NAME'] = df.street.apply(lambda s: cleaning_dict[s][2])
    df['TYPE'] = df.street.apply(lambda s: cleaning_dict[s][3])
    end = time.time()
    preclean_time = round(float(end-start)/60,1)

    cprint('Precleaning street names for %s took %s\n' % (city_name,preclean_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))


    ##
    ##	Identify matches using Steve Morse data
    ##

    cprint("Exact matching algorithm\n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

    start = time.time()

    #Steve Morse data has its own abbreviations for streets, alter TYPE for matching purposes
    df['sm_type'] = df['TYPE']
    micro_type_to_sm_type_dict = {
    	#These are changes
    	'Aly':'Alley',
    	'Ave':'Av',
    	'St':'',
    	'Road':'Dr',
    	'Ln':'Lane',
    	#These are not
    	'Pl':'Pl',
    	'Ter':'Ter',
    	'Ct':'Ct',
    	'Park':'Park',
    	'Pkwy':'Pkwy',
    	'Sq':'Sq',
    	'Blvd':'Blvd',
    	'Cir':'Cir',
    	'Way':'Way',
    	'Trail':'Trail',
    	'Crescent':'Crescent',
    	'River':'River',
    	'':''
    }

    #Idiosyncracies in Steve Morse
    ave_is_ave = ['Springfield',
        'Columbus',
        'Youngstown',
        'Trenton',
        'Jersey City',
        'Akron',
        'San Francisco',
        'Toledo',
        'Oakland',
        'Cincinnati',
        'St Louis',
        'Newark',
        'Dayton',
        'Long Beach',
        'Omaha',
        'Flint',
        'Grand Rapids',
        'San Antonio',
        'Chattanooga',
        'Richmond',
        'Tulsa',
        'Des Moines',
        'Oklahoma City',
        'Portland',
        'Miami',
        'San Diego']
    if city_name in ave_is_ave:
        micro_type_to_sm_type_dict['Ave'] = 'Ave'

    df['sm_type'] = df['sm_type'].replace(micro_type_to_sm_type_dict,regex=False)

    #Rearrange street address to match Steve Morse format
    df['sm_st'] = df['NAME'] + ' ' + df['sm_type'] + ' ' + df['DIR']
    df['sm_st'] = df['sm_st'].replace({' +':' '},regex=True)
    df['sm_st'] = df['sm_st'].str.strip()

    ##
    ## 	Get Steve Morse street-EDs
    ##

    url = "http://www.stevemorse.org/census/%scities/%s.htm" % (str(year),sm_web_abbr) 

    url_handle = urllib.urlopen(url)
    sourcetext = url_handle.readlines()
    url_handle.close()

    #Change the parsing strings if necessary (CG: Doesn't seem necessary yet)
    start_num = "value=" 
    end_num = ">"
    end_name = "</option>"

    #
    # Build a Steve Morse (sm) Street-to-EDs (st to eds) dictionary (dict)
    #

    sm_st_ed_dict = {}
    for line in sourcetext:
    	#If line has "value=" and "</option>" in it, do stuff
        if start_num in line and end_name in line:
        	#Ignore header line
            if "Select Street" in line:
                col_line = ""
            else:
            	#Extract street name between ">" and "</option>""
                streetname = line[line.find(end_num)+1:line.find(end_name)]
                #Extract EDs as one long string
                streetnum_str = line[line.find(start_num) + 7 : line.find(end_num)-1]
                #Split string of EDs into a list and assign to street name in dictionary
                sm_st_ed_dict[streetname] = list(streetnum_str.split(","))

    #Capture all Steve Morse streets in one list
    sm_all_streets = sm_st_ed_dict.keys()

    #For bookkeeping when validating matches using ED 
    microdata_all_streets = np.unique(df['sm_st'])
    for st in microdata_all_streets:
    	if st not in sm_all_streets:
    		sm_st_ed_dict[st] = None

    #
    # Build a Steve Morse (sm) ED-to-Street (ed to st) dictionary (dict)
    #

    sm_ed_st_dict = {}
    #Initialize a list of street names without an ED in Steve Morse
    sm_ed_st_dict[''] = []
    for st, eds in sm_st_ed_dict.items():
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

    #
    # Find exact matches
    #

    df['sm_st_exact_match_bool'] = df.sm_st.apply(lambda s: s in sm_all_streets)
    sm_exact_matches = np.sum(df['sm_st_exact_match_bool'])
    cprint("Exact matches before ED validation: "+str(sm_exact_matches)+" of "+str(num_records)+" cases ("+str(round(100*float(sm_exact_matches)/float(num_records),1))+"%)",file=AnsiToWin32(sys.stdout))

    #
    # Validate exact matches by comparing Steve Morse ED to microdata ED
    #

    df['sm_st_ed_match_bool'] = df.apply(lambda s: check_ed_match(s['ed'],s['sm_st']), axis=1)
    np.sum(df['sm_st_ed_match_bool'])

    #Validation of exact match fails if microdata ED and Steve Morse ED do not match
    failed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_st_ed_match_bool==False)]
    num_failed_validation = len(failed_validation)
    #Validation of exact match succeeds if microdata ED and Steve Morse ED are the same
    passed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_st_ed_match_bool==True)]
    num_passed_validation = len(passed_validation)

    #Keep track of unique street-ED pairs that have failed versus passed validation
    num_pairs_failed_validation = len(failed_validation.groupby(['ed','sm_st']).count())
    num_pairs_passed_validation = len(passed_validation.groupby(['ed','sm_st']).count())
    num_pairs = num_pairs_failed_validation + num_pairs_passed_validation
    end = time.time()
    exact_matching_time = round(float(end-start)/60,1)

    if sm_exact_matches == 0:
        sm_exact_matches += 1
    cprint("Failed ED validation: "+str(num_failed_validation)+" of "+str(sm_exact_matches)+" cases with exact name matches ("+str(round(100*float(len(failed_validation))/float(sm_exact_matches),1))+"%)",'red',file=AnsiToWin32(sys.stdout))
    cprint("Exact matches after ED validation: "+str(num_passed_validation)+" of "+str(num_records)+" cases ("+str(round(100*float(num_passed_validation)/float(num_records),1))+"%)",file=AnsiToWin32(sys.stdout))
    if num_pairs == 0:
        num_pairs += 1
    cprint("Cases failing ED validation represent "+str(num_pairs_failed_validation)+" of "+str(num_pairs)+" total Street-ED pairs ("+str(round(100*float(num_pairs_failed_validation)/float(num_pairs),1))+"%)\n",'yellow',file=AnsiToWin32(sys.stdout))
    cprint("Exact matching and ED validation for %s took %s\n" % (city_name,exact_matching_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

    ##
    ##	Identify fuzzy matches
    ##

    cprint("Fuzzy matching algorithm \n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

    start = time.time()

    #
    # Find the best matching Steve Morse street name
    #

    #Create a set of all streets for fuzzy matching (create once, call on)
    sm_all_streets_fuzzyset = fuzzyset.FuzzySet(sm_all_streets)

    #Keep track of problem EDs
    problem_EDs = []

    #Create dictionary based on Street-ED pairs for faster lookup using helper function
    df_no_validated_exact_match = df[(df.sm_st_exact_match_bool==False) | (df.sm_st_ed_match_bool==False)]
    df_grouped = df_no_validated_exact_match.groupby(['sm_st','ed'])
    sm_fuzzy_match_dict = {}
    for sm_st_ed,_ in df_grouped:
    	sm_fuzzy_match_dict[sm_st_ed] = sm_fuzzy_match(sm_st_ed[0],sm_st_ed[1])

    #Get fuzzy matches and replace missing data with null values
    df['sm_st_fuzzy_match'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[0], axis=1)
    df['sm_st_fuzzy_match_score'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[1], axis=1)
    df['sm_st_fuzzy_match_bool'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[2], axis=1)
    sm_fuzzy_matches = np.sum(df['sm_st_fuzzy_match_bool'])

    end = time.time()
    fuzzy_matching_time = round(float(end-start)/60,1)

    #Compute number of cases without validated exact match
    num_current_residual_cases = num_records - num_passed_validation

    cprint("Fuzzy matches (using microdata ED): "+str(sm_fuzzy_matches)+" of "+str(num_current_residual_cases)+" unmatched cases ("+str(round(100*float(sm_fuzzy_matches)/float(num_current_residual_cases),1))+"%)\n",file=AnsiToWin32(sys.stdout))
    cprint("Fuzzy matching for %s took %s\n" % (city_name,fuzzy_matching_time),'cyan',attrs=['dark'],file=AnsiToWin32(sys.stdout))

    ##
    ##	Overall matches
    ##

    cprint("Overall matches of any kind\n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

    df['sm_st_overall_match'] = ''
    df['overall_match_type'] = 'NoMatch'
    df['sm_st_overall_match_bool'] = False

    df.loc[df['sm_st_fuzzy_match_bool'],'sm_st_overall_match'] = df['sm_st_fuzzy_match']
    df.loc[df['sm_st_exact_match_bool'] & df['sm_st_ed_match_bool'],'sm_st_overall_match'] = df['sm_st']

    df.loc[df['sm_st_fuzzy_match_bool'],'overall_match_type'] = 'FuzzySM'
    df.loc[df['sm_st_exact_match_bool'] & df['sm_st_ed_match_bool'],'overall_match_type'] = 'ExactSM'

    df.loc[(df['overall_match_type'] == 'ExactSM') | (df['overall_match_type'] == 'FuzzySM'),'sm_st_overall_match_bool'] = True 

    #df = pd.concat([df,df.apply(lambda s: overall_match(s['sm_st'],s['sm_st_exact_match_bool'],s['sm_st_ed_match_bool'],s['sm_st_fuzzy_match_bool'],s['sm_st_fuzzy_match']), axis=1)],axis=1)
    sm_st_overall_matches = np.sum(df['sm_st_overall_match_bool'])
    cprint("Overall matches: "+str(sm_st_overall_matches)+" of "+str(num_records)+" total cases ("+str(round(100*float(sm_st_overall_matches)/float(num_records),1))+"%)\n",file=AnsiToWin32(sys.stdout))

    end_total = time.time()
    total_time = round(float(end_total-start_total)/60,1)

    cprint("Total processing time for %s: %s\n" % (city_name,total_time),'cyan',attrs=['bold'],file=AnsiToWin32(sys.stdout))
#    sys.stdout.close()

    problem_EDs = list(set(problem_EDs))
    print("Problem EDs: %s" % (problem_EDs))
    df.to_csv(file_path + '/autocleaned/%s_AutoCleaned.csv' % (file_name))

    num_residual_cases = num_records - sm_st_overall_matches

    prop_passed_validation = float(num_passed_validation)/float(num_records)
    prop_sm_fuzzy_matches = float(sm_fuzzy_matches)/float(num_records)
    prop_sm_st_overall_matches = float(sm_st_overall_matches)/float(num_records)
    prop_residual_cases = float(num_residual_cases)/float(num_records)
    prop_failed_validation = float(num_failed_validation)/float(num_records)
    prop_pairs_failed_validation = float(num_pairs_failed_validation)/float(num_pairs)
    
    return [year, city_name, state_abbr, num_records, 
    num_passed_validation, prop_passed_validation,
    sm_fuzzy_matches, prop_sm_fuzzy_matches,
    sm_st_overall_matches, prop_sm_st_overall_matches,
    num_residual_cases, prop_residual_cases,
    num_failed_validation, prop_failed_validation,
    num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation,
    load_time, preclean_time, exact_matching_time, fuzzy_matching_time, total_time] 

file_path = '/home/s4-data/LatestCities/%s' % (str(year))
city_info_file = file_path + '/CityInfo%s.csv' % (str(year))
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df.values.tolist()

for i in city_info_list:
    i.append(year)

pool = Pool(8)
temp = pool.map(clean_microdata, city_info_list)
pool.close()

names = ['Year', 'City', 'State', 'NumCases',
    'ExactMatchesValidated','propExactMatchesValidated',
    'FuzzyMatches','propFuzzyMatches',
    'OverallMatches','propOverallMatches',
    'ResidualCases','propResidualCases',
    'ExactMatchesFailed','propExactMatchesFailed',
    'StreetEDpairsFailed','StreetEDpairsTotal','propStreedEDpairsFailed',
    'LoadTime','PrecleanTime','ExactMatchingTime','FuzzyMatchingTime','TotalTime']

dashboard = pd.DataFrame(temp,columns=names)
csv_file = file_path + '/CleaningSummary%s.csv' % (str(year))
dashboard.to_csv(csv_file)