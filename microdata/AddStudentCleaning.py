#
# Name:			AddStudentCleaning.py
#
# Purpose:		Integrate student cleaning into autocleaning results 
#
# Usage:		python AddStudentCleaning.py [city] [state_abbr] [student file name] [autoclean version] [year]
#					
#				ex: 
#	 
#				python AddStudentCleaning.py Albany NY AlbanyNY_ForStudentsV1_ashley.dta 1 1930
#
# Note:			Student file MUST BE ON RHEA SERVER in the "studentcleaned" directory
#
#				ex:	"/LatestCities/1930/studentcleaned"

import os, sys, subprocess
import unicodecsv as csv
import pandas as pd
import numpy as np
import re
import pickle
import fuzzyset

csv.field_size_limit(sys.maxsize)

# These capture information from the command prompt
c = sys.argv[1]
s = sys.argv[2]
student_file = sys.argv[3]
version = sys.argv[4]
year = sys.argv[5]

#c = "St Louis"
#s = "MO"
#student_file = "StLouisMO_ForStudentsV4_rush.dta"
#version = 6
#year = 1930

c_spaces = c
c = c.replace(' ','')
s = s.upper()
city = c + s

# Set path and data file names
file_path = '/home/s4-data/LatestCities' 
studentcleaned_file_name = file_path + '/%s/studentcleaned/%s' % (str(year),student_file)
autostud_file_name = file_path + '/%s/autostudcleaned/%s' % (str(year),city.replace(' ','') + '_StudAuto.csv')
autostud_file_stata = file_path + '/%s/autostudcleaned/%s' % (str(year),city.replace(' ','') + '_StudAuto.dta')

# NOTE: There was a significant error in V1 and V2 where DIR = TYPE for some reason5
if int(version) < 3:
	autocleaned_file_name = file_path + '/%s/autocleaned/V5/%s_AutoCleanedV5.csv' % (str(year),city.replace(' ',''))
else:
	autocleaned_file_name = file_path + '/%s/autocleaned/V%s/%s_AutoCleanedV%s.csv' % (str(year),str(version),city.replace(' ',''),str(version))
if ~os.path.isfile(autocleaned_file_name):
	autocleaned_file_name = file_path + '/%s/autocleaned/V4/%s_AutoCleanedV4.csv' % (str(year),city.replace(' ',''))
if ~os.path.isfile(autocleaned_file_name):
	autocleaned_file_name = file_path + '/%s/autocleaned/V3/%s_AutoCleanedV3.csv' % (str(year),city.replace(' ',''))

#
# Helper functions
#

#Function to load large Stata files
def load_large_dta(fname):

    reader = pd.read_stata(fname, iterator=True)
    df = pd.DataFrame()

    try:
        chunk = reader.get_chunk(100*1000)
        while len(chunk) > 0:
            df = df.append(chunk, ignore_index=True)
            chunk = reader.get_chunk(100*1000)
            print '.',
            sys.stdout.flush()
    except (StopIteration, KeyboardInterrupt):
        pass

    print '\nloaded {} rows\n'.format(len(df))

    return df

#Function to standardize street name
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
			NAME = re.sub("^[Tt]wel[f]?th","12th",NAME)
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

#Function to load Steve Morse data
def load_steve_morse(city,state,year):

	#NOTE: This dictionary must be built independently of this script
	sm_st_ed_dict_file = pickle.load(open(file_path + '/%s/sm_st_ed_dict%s.pickle' % (str(year),str(year)),'rb'))
	sm_st_ed_dict_nested = sm_st_ed_dict_file[(city,'%s' % (state.lower()))]

	#Flatten dictionary
	temp = {k:v for d in [v for k,v in sm_st_ed_dict_nested.items()] for k,v in d.items()}

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

#Function to find fuzzy street name matches using Steve Morse data
def find_fuzzy_matches(df,city,street,sm_all_streets,sm_ed_st_dict):

	num_records = df['st_edit'].notnull().sum()

	#
	# Identify exact matches to exclude from fuzzy match search
	#

	df['st_edit_exact_match'] = df[street].apply(lambda s: s in sm_all_streets)
	print("Exact matches: %s of %s" % (str(df['st_edit_exact_match'].sum()),str(num_records)))

	#
	# Find the best matching Steve Morse street name
	#

	#Create a set of all streets for fuzzy matching (create once, call on)
	sm_all_streets_fuzzyset = fuzzyset.FuzzySet(sm_all_streets)

	#Keep track of problem EDs
	problem_EDs = []

	#Fuzzy matching algorithm
	def sm_fuzzy_match(street,ed):

		if ed != str:		
			ed = str(int(ed))

		#Return null if street is blank
		if street == '':
			return ['','',False]

		#Microdata ED may not be in Steve Morse, if so then add it to problem ED list and return null
		try:
			sm_ed_streets = sm_ed_st_dict[ed]
			sm_ed_streets_fuzzyset = fuzzyset.FuzzySet(sm_ed_streets)
		except:
			problem_EDs.append(ed)
			return ['','',False]
		
		#Step 1: Find best match among streets associated with microdata ED
		try:
			best_match_ed = sm_ed_streets_fuzzyset[street][0]
		except:
			return ['','',False]

		#Step 2: Find best match among all streets
		try:
			best_match_all = sm_all_streets_fuzzyset[street][0]
		except:
			return ['','',False]    

		#Step 3: If both best matches are the same, return as best match
		if (best_match_ed[1] == best_match_all[1]) & (best_match_ed[0] >= 0.5):
			return [best_match_ed[1],best_match_ed[0],True]
		else:
			return ['','',False]

	#Create dictionary based on Street-ED pairs for faster lookup using helper function
	df_st_edit = df[~df['st_edit_exact_match']]
	df_grouped = df_st_edit.groupby([street,'ed'])
	sm_fuzzy_match_dict = {}
	for st_ed,_ in df_grouped:
		sm_fuzzy_match_dict[st_ed] = sm_fuzzy_match(st_ed[0],st_ed[1])

	#Helper function (necessary since dictionary built only for cases without validated exact matches)
	def get_fuzzy_match(exact_match,street,ed):
		#Only look at cases without validated exact match 
		if not (exact_match):
			#Need to make sure "Unnamed" street doesn't get fuzzy matched
			if 'Unnamed' in street:
				return ['','',False]
			#Get fuzzy match    
			else:
				return sm_fuzzy_match_dict[street,ed]
		#Return null if exact validated match
		else:
			return ['','',False]

	#Get fuzzy matches 
	df['st_edit_fuzzy_match'], df['st_edit_fuzzy_match_score'], df['st_edit_fuzzy_match_bool'] = zip(*df.apply(lambda x: get_fuzzy_match(x['st_edit_exact_match'],x[street],x['ed']), axis=1))

	print("Fuzzy matches: %s of %s" % (str(df['st_edit_fuzzy_match_bool'].sum()),str(len(df))))
	print("Unmatched cases: %s of %s" % (str(len(df)-df['st_edit_fuzzy_match_bool'].sum()-df['st_edit_exact_match'].sum()),str(len(df))))

	df['st_edit_matched'] = df['st_edit']
	df.loc[~df['st_edit_exact_match'] & df['st_edit_fuzzy_match_bool'],'st_edit_matched'] = df['st_edit_fuzzy_match']

	return df

#
# Step 0: Open both files and merge
#

# Load data and merge
sc = load_large_dta(studentcleaned_file_name)
if int(version) == 2:
	sc['st'] = ''
tp = pd.read_csv(autocleaned_file_name, iterator=True, chunksize=10000,low_memory=False)
ac = pd.concat(tp, ignore_index=True)

vars_formerge = ['image_id','line_num','clean_priority','street_raw',
	'street_precleanedhn','st','stname_flag','checked_st','checked_hn','inst','nonstreet',
	'ed_edit','hn_edit','institution_edit','block_edit','st_edit']

sc_formerge = sc[vars_formerge].drop_duplicates(['image_id','line_num','st_edit'])

try:
	mc = ac.merge(sc_formerge,on=['image_id','line_num','clean_priority'],indicator=True)
except:
	mc = ac.merge(sc_formerge,on=['image_id','line_num'],indicator=True)

if len(mc) != sum(mc['_merge'] == 'both'):
	print('Merge error')
del mc['_merge']

#
# Step 1: Add TYPE (from raw/autoclean) if no TYPE_stud (from student) amd TYPE exists
#

#Function to look for np.nan
def nan_equal(a,b):
	try:
		np.testing.assert_equal(a,b)
	except AssertionError:
		return False
	return True

#Function to add TYPE
def add_type(TYPE,TYPE_stud,st_edit):
	if ~nan_equal(TYPE,np.NaN) & (TYPE_stud == ''):
		return str(st_edit) + ' ' + TYPE
	else:
		return st_edit

#Function to blank st_edit if st_edit==TYPE
def blank_st_edit(st_edit, TYPE):
	if st_edit.strip() == TYPE:
		return ''
	else:
		return st_edit

# Get TYPE from student cleaned street names
_, _, _, mc['TYPE_stud'] = zip(*mc['st_edit'].map(standardize_street))
# Add TYPE (from raw/autoclean) if no TYPE_stud (from student) amd TYPE exists
mc['st_edit'] = mc.apply(lambda x: add_type(x['TYPE'],x['TYPE_stud'],x['st_edit']),axis=1)
# Now replace st_edit with '' if st_edit == TYPE (e.g. st_edit == "Road")
mc['st_edit'] = mc.apply(lambda x: blank_st_edit(x['st_edit'],x['TYPE']), axis=1)

#
# Step 2: Re-add DIR to autoclean if it was removed
#

def readd_dir(overall_match, DIR):
	if str(DIR) != 'nan' and str(overall_match) != 'nan':
		if not overall_match.startswith(DIR+' '):
			return DIR + ' ' + overall_match
		else:
			return overall_match			
	else:
		return overall_match

# Readd DIR
mc['overall_match2'] = mc.apply(lambda x: readd_dir(x['overall_match'],x['DIR']),axis=1)

# Save list of streets with DIR
mc_readd_dir = mc[mc['overall_match']!=mc['overall_match2']]
mc_readd_dir = mc_readd_dir[mc_readd_dir['overall_match'].astype(str) != 'nan']
mc_readd_dir = mc_readd_dir[['overall_match','overall_match2']].drop_duplicates()
streets_w_dirs_file = file_path + '/%s/studentcleaned/streets_w_dirs%s%s.csv' % (str(year), c, s)
mc_readd_dir.to_csv(streets_w_dirs_file)

# Rename 'overall_match' variables to reflect which might not have DIR
mc['overall_match_wrong'] = mc['overall_match']
mc['overall_match'] = mc['overall_match2']

def fix_nan_st(st):
	if nan_equal(st,np.NaN):
		return ''
	else:
		return st
mc['overall_match'] = mc['overall_match'].apply(fix_nan_st)

#
# Step 3: Run fuzzy matching from autoclean to add TYPE to st_edit as needed (i.e. add "St")
#

sm_all_streets, sm_st_ed_dict_nested, sm_ed_st_dict = load_steve_morse(c_spaces,s,year)
mc = find_fuzzy_matches(mc,c,'st_edit',sm_all_streets,sm_ed_st_dict)

#
# Step 4: Find best street (autoclean vs student cleaned)
#

def find_best_street(overall_match, st_edit, st_edit_matched, checked_st, clean_priority):

	# Overall_match has DIR
	_, DIR_overall, NAME_overall, TYPE_overall = standardize_street(overall_match)
	overall_match_dir_bool = DIR_overall != ''
	# St_edit has DIR
	_, DIR_st_edit, NAME_st_edit, TYPE_st_edit = standardize_street(st_edit)
	st_edit_dir_bool = DIR_st_edit != ''
	# St_edit_matched has DIR
	_, DIR_st_edit_matched, NAME_st_edit_matched, TYPE_st_edit_matched = standardize_street(st_edit_matched)
	st_edit_matched_dir_bool = DIR_st_edit_matched != ''	

	# An overall_match exists
	overall_match_exists = (type(overall_match) == str) & (overall_match != '')
	# Unambiguously cleaned (manually)
	unambig_cleaned = (checked_st != 'c, ambiguous') & ~nan_equal(clean_priority,np.NaN)
	# No overall_match but manually cleaned (matched to Steve Morse)
	no_overall_but_manual_match = (type(overall_match) != str) & (st_edit_matched != '')

	# Use automated match if there is no unambiguously cleaned street name 
	if overall_match_exists & ~unambig_cleaned:
		return overall_match
	# If automated match and unambiguously cleaned street exists...
	if unambig_cleaned:
		# Return st_edit if st_edit_matched has DIR and st_edit_matched does not have DIR
		if st_edit_dir_bool & (st_edit_dir_bool != st_edit_matched_dir_bool):
			return st_edit
		# Return overall_match if NAME + TYPE are the same as st_edit/st_edit_matched but overall_match has DIR and st_edit does not
		# st_edit/st_edit_matched have no DIR, but overall_match has DIR
		overall_only_dir_bool = (~st_edit_dir_bool & ~st_edit_matched_dir_bool & overall_match_dir_bool)
		# overall_match NAME+TYPE is the same as st_edit_matched NAME+TYPE
		same_name_type = (NAME_st_edit_matched+TYPE_st_edit_matched).strip() == (NAME_st_edit_matched+TYPE_st_edit_matched).strip()
		if overall_only_dir_bool & same_name_type:
			return overall_match
		# Otherwise, return st_edit_matched
		else:
			return st_edit_matched
	else:
		return ''

mc['autostud_street'] = mc.apply(lambda x: find_best_street(x['overall_match'],x['st_edit'],x['st_edit_matched'],x['checked_st'],x['clean_priority']),axis=1)

def get_guess(autostud_street, street_precleanedhn):
	if autostud_street == '':
		return street_precleanedhn
	else:
		return autostud_street

mc['st_best_guess'] = mc.apply(lambda x: get_guess(x['autostud_street'],x['street_precleanedhn']), axis=1)

#
# Step 5 (final): Format and save file "CITY_StudAuto.dta"
#

# Change names for later use
mc.rename(columns={'overall_match':'overall_match_auto',
	'hn':'hn_auto',
	'hn_edit':'hn',
	'ed':'ed_orig',
	'ed_edit':'ed',
	'block':'block_orig',
	'block_edit':'block'}, inplace=True)
# Change "St " or "St. " at start of street into "Saint "

mc = mc.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('', '.')
mc.to_csv(autostud_file_name)

# Set do-file information
dofile = file_path + "/ConvertCsvToDta.do"
cmd = ["stata","-b","do", dofile, "%s" % (autostud_file_name), "%s" % (autostud_file_stata),"&"] 
# Run do-file
subprocess.call(cmd) 
# Cleanup .csv file
os.remove(autostud_file_name)
