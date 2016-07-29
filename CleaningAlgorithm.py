import urllib
import re
import os
import sys
import time
import numpy as np
import pandas as pd
from fuzzywuzzy import process

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

file_name = sys.argv[1] 
#file_name = 'NewHaven'
#sm_web_abbr = 'nhct'

city_name_dict = {
	'NewHaven':'New Haven',
	'Chicago1930reduced':'Chicago',
	'Yonkers':'Yonkers'}
city_name = city_name_dict[file_name]

sm_web_abbr_dict = {
	'NewHaven':'nhct',
	'Chicago1930reduced':'chil',
	'Yonkers':'yony'
}
sm_web_abbr = sm_web_abbr_dict[file_name]

print(color.BOLD + '%s Automated Cleaning\n' % (city_name) + color.END)

#Function for reporting compute time
def compute_time(t):
	return '%s seconds (%s minutes)' % (round(t,0),round(float(t)/60,1))

#
#	Import data
#
start = time.time()
df = pd.read_stata('%sStata13.dta' % (file_name))
end = time.time()
print(color.DARKCYAN + 'Loading data for %s took %s' % (city_name,compute_time(end-start)) + color.END)

#Save a pristine copy for debugging
df_save = df

#The original variable names will likely change from city to city
df['street'] = df['self_residence_place_streetaddre']
df['ed'] = df['indexed_enumeration_district']
df['ed'] = df['ed'].astype(str)
df['ed'] = df['ed'].str.split('.').str[0]
df['ed'] = df['ed'].str.lstrip('0')

#
#	Function to clean street direction and street type
#
#	Author: Amory Kisch
#	Date:	7/17/16
#

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

print(color.DARKCYAN + 'Precleaning street names for %s took %s\n' % (city_name,compute_time(end-start)) + color.END)

##
##	Identify matches using Steve Morse data
##

print(color.UNDERLINE + "Exact matching algorithm\n" + color.END)

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
df['sm_type'] = df['sm_type'].replace(micro_type_to_sm_type_dict,regex=False)

#Rearrange street address to match Steve Morse format
df['sm_st'] = df['NAME'] + ' ' + df['sm_type'] + ' ' + df['DIR']
df['sm_st'] = df['sm_st'].replace({' +':' '},regex=True)
df['sm_st'] = df['sm_st'].str.strip()

##
## 	Get Steve Morse street-EDs
##

url = "http://www.stevemorse.org/census/1930cities/%s.htm" % (sm_web_abbr) 

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
print("Exact matches before ED validation: "+str(sm_exact_matches)+" of "+str(len(df))+" cases ("+str(round(100*float(sm_exact_matches)/float(len(df)),1))+"%)")

#
# Validate exact matches by comparing Steve Morse ED to microdata ED
#

#Helper function for checking that microdata ED is in Steve Morse list of EDs for street name
def check_ed_match(microdata_ed,sm_st):
	if (sm_st is None) or (sm_st_ed_dict[sm_st] is None):
		return False
	else:
		if microdata_ed in sm_st_ed_dict[sm_st]:
			return True
		else:
			return False

df['sm_st_ed_match_bool'] = df.apply(lambda s: check_ed_match(s['ed'],s['sm_st']), axis=1)
np.sum(df['sm_st_ed_match_bool'])

#Validation of exact match fails if microdata ED and Steve Morse ED do not match
failed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_st_ed_match_bool==False)]
#Validation of exact match succeeds if microdata ED and Steve Morse ED are the same
passed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_st_ed_match_bool==True)]

#Keep track of unique street-ED pairs that have failed versus passed validation
pairs_failed_validation = len(failed_validation.groupby(['ed','sm_st']).count())
pairs_passed_validation = len(passed_validation.groupby(['ed','sm_st']).count())
total_pairs = pairs_passed_validation + pairs_failed_validation
end = time.time()

print(color.RED + "Failed ED validation: "+str(len(failed_validation))+" of "+str(sm_exact_matches)+" cases with exact name matches ("+str(round(100*float(len(failed_validation))/float(sm_exact_matches),1))+"%)" + color.END)
print("Exact matches after ED validation: "+str(len(passed_validation))+" of "+str(len(df))+" cases ("+str(round(100*float(len(passed_validation))/float(len(df)),1))+"%)")
print(color.YELLOW + "Cases failing ED validation represent "+str(pairs_failed_validation)+" of "+str(total_pairs)+" total Street-ED pairs ("+str(round(100*float(pairs_failed_validation)/float(total_pairs),1))+"%)\n" + color.END)
print(color.DARKCYAN + 'Exact matching and ED validation for %s took %s\n' % (city_name,compute_time(end-start)) + color.END)

##
##	Identify fuzzy matches
##

print(color.UNDERLINE + "Fuzzy matching algorithm \n" + color.END)

start = time.time()

#
# Find the best matching Steve Morse street name
#

#Keep track of problem EDs
problem_EDs = []
def sm_fuzzy_match(sm_st,ed):
	
	#Return null if sm_st is blank
	if sm_st == '':
		return ['','',False]

	#Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
	try:
		sm_ed_streets = sm_ed_st_dict[ed]
	except:
		problem_EDs.append(ed)
		return ['','',False]
    
	#Step 1: Find best match among streets associated with microdata ED
	best_match_ed = process.extractOne(sm_st,sm_ed_streets)
	#Step 2: Find best match among all streets
	best_match_all = process.extractOne(sm_st,sm_all_streets)
	#Step 3: If both best matches are the same, return as best match
	if (best_match_ed == best_match_all):
		return [best_match_ed[0][0],best_match_ed[0][1],True]
	else:
		return ['','',False]

#Create dictionary based on Street-ED pairs for faster lookup using helper function
df_no_validated_exact_match = df[(df.sm_st_exact_match_bool==False) | (df.sm_st_ed_match_bool==False)]
df_grouped = df_no_validated_exact_match.groupby(['sm_st','ed'])
sm_fuzzy_match_dict = {}
for sm_st_ed,_ in df_grouped:
	sm_fuzzy_match_dict[sm_st_ed] = sm_fuzzy_match(sm_st_ed[0],sm_st_ed[1])

#Helper function (necessary since dictionary built only for cases without validated exact matches)
def get_fuzzy_match(sm_st,ed):
	try:
		return sm_fuzzy_match_dict[sm_st,ed]
	except:
		return ['','',False]

#Get fuzzy matches and replace missing data with null values
df['sm_st_fuzzy_match'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[0], axis=1)
df['sm_st_fuzzy_match_score'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[1], axis=1)
df['sm_st_fuzzy_match_bool'] = df.apply(lambda s: get_fuzzy_match(s['sm_st'],s['ed'])[2], axis=1)
sm_fuzzy_matches = np.sum(df['sm_st_fuzzy_match_bool'])

end = time.time()

#Compute number of residual cases without validated exact match
leftover_cases = len(df)-len(passed_validation)

print("Fuzzy matches (using microdata ED): "+str(sm_fuzzy_matches)+" of "+str(leftover_cases)+" unmatched cases ("+str(round(100*float(sm_fuzzy_matches)/float(leftover_cases),1))+"%)\n")
print(color.DARKCYAN + 'Fuzzy matching for %s took %s\n' % (city_name,compute_time(end-start)) + color.END)

##
##	Overall matches
##

print(color.UNDERLINE + "Overall matches of any kind\n" + color.END)

df['sm_st_overall_match'] = ''
df['overall_match_type'] = 'NoMatch'
df['sm_st_overall_match_bool'] = False

df.loc[df['sm_st_exact_match_bool'] & df['sm_st_ed_match_bool'],'sm_st_overall_match'] = df['sm_st']
df.loc[df['sm_st_fuzzy_match_bool'],'sm_st_overall_match'] = df['sm_st_fuzzy_match']

df.loc[df['sm_st_exact_match_bool'] & df['sm_st_ed_match_bool'],'overall_match_type'] = 'ExactSM'
df.loc[df['sm_st_fuzzy_match_bool'],'overall_match_type'] = 'FuzzySM'

df.loc[(df['overall_match_type'] == 'ExactSM') | (df['overall_match_type'] == 'FuzzySM'),'sm_st_overall_match_bool'] = True 

#df = pd.concat([df,df.apply(lambda s: overall_match(s['sm_st'],s['sm_st_exact_match_bool'],s['sm_st_ed_match_bool'],s['sm_st_fuzzy_match_bool'],s['sm_st_fuzzy_match']), axis=1)],axis=1)
sm_st_overall_matches = np.sum(df['sm_st_overall_match_bool'])
print("Overall matches: "+str(sm_st_overall_matches)+" of "+str(len(df))+" total cases ("+str(round(100*float(sm_st_overall_matches)/float(len(df)),1))+"%)")

df.to_csv('%s_AutoCleaned.csv' % (city_name))
'''
##
## House number sequences
##

hcount=0
max_gap = 100

HN_SEQ = []
ST_SEQ = []
INCONS = []

def num_seq(ind,chk_num,chk_dir) : #chk_dir = 1|-1 depending on the direction to look
    cur_num = get_hn(ind)
    if cur_num == None : #if housenum undefined, consider it the end of seq
        return ind-chk_dir
    if(not (cur_num+chk_num) % 2 == 0 or abs(cur_num-chk_num) > max_gap) :
        return ind-chk_dir
    else :
        return num_seq(ind+chk_dir,cur_num,chk_dir)

def seq_match_num(ind) : #wrapper function for num_seq recursion
    num = get_hn(ind) # num = house number
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
    HN_SEQ.append(seq_match_num(ind))
    ind = HN_SEQ[len(HN_SEQ)-1][1]+1

ind = 0
while ind<len(Data) :
    ST_SEQ.append(st_seq(ind))
    ind = ST_SEQ[len(ST_SEQ)-1][1]+1


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

for inc in INCONS[99:200] :
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
for inc in INCONS1[:0] :
    if inc[0] - last[1] == 1 : #consecutive unmatched swatches: what kind of error defines these??
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
'''