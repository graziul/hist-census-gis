#
# All the functions for performing block numbering (includes many things)
#

import arcpy
import os
import sys
import re
from operator import itemgetter
import pandas as pd
import pysal as ps
import subprocess
from microclean.STstandardize import *

#
# Helper functions
#

# Helper functions

# Function to load large Stata files
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

# Function to reads in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=False):
	dbfile = dbfile.replace('.shp','.dbf')
	db = ps.open(dbfile) #Pysal to open DBF
	d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
	#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
	pandasDF = pd.DataFrame(d) #Convert to Pandas DF
	if upper == True: #Make columns uppercase if wanted 
		pandasDF.columns = map(str.upper, db.header) 
	db.close() 
	return pandasDF

'''
# Function to standardize street name
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
 #		print("Something went a bit wrong while trying to pre-standardize stnames.")
 #		print("orig was: "+orig_st)
 #		print("st is: \""+st+"\"")
 #		print("components: ["+(DIR+','+NAME+','+TYPE).strip()+"]")
		pass
	if runAgain :
		return standardize_street(st)
	else :
		return st, DIR, NAME, TYPE
'''

# Function to save Pandas DF as DBF file 
def save_dbf(df, shapefile, dir_path):
	shapefile_name = dir_path + shapefile
	csv_file = dir_path + "\\temp_for_dbf.csv"
	df.to_csv(csv_file,index=False)
	try:
		os.remove(dir_path + "\\schema.ini")
	except:
		pass
	arcpy.TableToTable_conversion(csv_file,dir_path,"temp_for_shp.dbf")
	os.remove(shapefile_name.replace('.shp','.dbf'))
	os.remove(csv_file)
	os.rename(dir_path+"\\temp_for_shp.dbf",shapefile_name.replace('.shp','.dbf'))
	os.remove(dir_path+"\\temp_for_shp.dbf.xml")
	os.remove(dir_path+"\\temp_for_shp.cpg")


#
# Functions for calling R scripts 
#

def create_1930_addresses(city_name, state_abbr, file_name, paths):
	r_path, script_path, file_path = paths
	print("Creating 1930 addresses\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Create 1930 Address.R',file_path,city_name,file_name,state_abbr])
	if t != 0:
		print("Error generating 1930 addresses for "+city_name+"\n")
	else:
		print("OK!\n")

def identify_1930_eds(city_name, paths):
	r_path, script_path, file_path = paths
	print("Identifying 1930 EDs\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 EDs.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying 1930 EDs for "+city_name+"\n")
	else:
		print("OK!\n")

def analyzing_microdata_and_grid(city_name, state_abbr, paths):
	r_path, script_path, file_path = paths
	print("Analyzing microdata and grids\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Analyzing Microdata and Grid.R',file_path,city_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error analyzing microdata and grid for "+city_name+"\n")
	else:
		print("OK!\n")

def add_ranges_to_new_grid(city_name, state_abbr, file_name, paths):
	r_path, script_path, file_path = paths
	print("Adding ranges to new grid\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Add Ranges to New Grid.R',file_path,city_name,file_name,state_abbr], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error adding ranges to new grid for "+city_name+"\n")
	else:
		print("OK!\n")

def identify_1930_blocks(city_name, paths):
	r_path, script_path, file_path = paths
	print("Identifying 1930 blocks\n")
	t = subprocess.call([r_path,'--vanilla',script_path+'\\blocknum\\R\\Identify 1930 Blocks.R',file_path,city_name], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	if t != 0:
		print("Error identifying 1930 blocks for "+city_name+"\n")
	else:
		print("OK!\n")

#
# Functions for calling Python scripts (code/functions should get pulled into here)
#

def get_block_desription_guesses(city_name, state_abbr, paths):
	r_path, script_path, file_path = paths
	print("Getting block numbers using block descriptions from microdata\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunBlockDesc.py",file_path,city_name,state_abbr])
	if t != 0:
		print("Error getting block description guesses for "+city_name+"\n")
	else:
		print("OK!\n")

def run_ocr(city_name, paths):
	r_path, script_path, file_path = paths
	print("Runing Matlab script\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\RunOCR.py",file_path,script_path],stdout=open(os.devnull, 'wb'))
	if t != 0:
		print("Error running Matlab OCR script for "+city_name+"\n")
	else:
		print("OK!\n")

def integrate_ocr(city_name, file_name, paths):
	r_path, script_path, file_path = paths
	print("Integrating OCR block numbering results\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\MapOCRintegration.py",file_path,city_name,file_name])
	if t != 0:
		print("Error integrating OCR block numbering results for "+city_name+"\n")
	else:
		print("OK!\n")

def set_blocknum_confidence(city_name, paths):
	r_path, script_path, file_path = paths
	print("Setting confidence\n")
	t = subprocess.call(["python",script_path+"\\blocknum\\Python\\SetConfidence.py",file_path,city_name])
	if t != 0:
		print("Error setting confidence for for "+city_name+"\n")
	else:
		print("OK!\n")


#
# Create Blocks and Block Points.py
#

# Head script calling individual functions
def create_blocks_and_block_points(name, state, paths, geocode_file=None):
	
	_, _, dir_path = paths
	dir_path = dir_path + "/GIS_edited/"

	different_geocode = False
	if geocode_file != None:
		different_geocode = True

	# overwrite output
	arcpy.env.overwriteOutput=True

	print("The script has started to work and is running the 'street' function")

	problem_segments = street(dir_path, name, state)
	print("The script has finished executing the 'street' function and has now started executing 'physical_blocks' function")

	physical_blocks(dir_path, name)
	print("The script has finished executing the 'physical_blocks' function and has now started executing 'geocode' function")

	geocode(dir_path, name, state)
	print("The script has finished executing the 'geocode' function and has now started excuting 'attach_pblk_id'")

	if different_geocode:
		points30 = geocode_file
		print("Different geocode")
	else:
		points30 = dir_path + name + "_1930_Points.shp"

	attach_pblk_id(dir_path, name, points30)
	print("The script has finished executing the 'attach_pblk_id' function and the entire script is complete")

# Code to import and "fix up" the street grid (calls Amory's code below)
def street(dir_path, name, state):

	#Create Paths to be used throughout Process
	grid = dir_path + name + state + "_1940_stgrid_edit.shp"
	grid_1940 = "S:/Projects/1940Census/DirAdd/" + name + state + "_1940_stgrid_diradd.shp"
	dissolve_grid = dir_path + name + "_1930_stgrid_Dissolve.shp"
	temp = dir_path + name + "_temp.shp"
	split_grid = dir_path + name + "_1930_stgrid_Split.shp"
	grid_uns =  dir_path + name + state + "_1930_stgrid_edit_Uns.shp"
	grid_uns2 =  dir_path + name + state + "_1930_stgrid_edit_Uns2.shp"

	# Function to reads in DBF files and return Pandas DF
	def dbf2DF(dbfile, upper=False): 
		if dbfile.split('.')[1] == 'shp':
			dbfile = dbfile.replace('.shp','.dbf')
		db = ps.open(dbfile) #Pysal to open DBF
		d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
		#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
		pandasDF = pd.DataFrame(d) #Convert to Pandas DF
		if upper == True: #Make columns uppercase if wanted 
			pandasDF.columns = map(str.upper, db.header) 
		db.close() 
		return pandasDF

	# Function to save Pandas DF as DBF file 
	def save_dbf(df, shapefile_name, field_map = False):
		dir_temp = '/'.join(shapefile_name.split('/')[:-1])
		file_temp = shapefile_name.split('/')[-1]
		csv_file = dir_temp + "/temp_for_dbf.csv"
		df.to_csv(csv_file,index=False)
		try:
			os.remove(dir_temp + "/schema.ini")
		except:
			pass

		# Add a specific field mapping for a special case
		if field_map:
			file = csv_file
			field_map = """FULLNAME "FULLNAME" true true false 80 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
			CITY "CITY" true true false 30 Text 0 0 ,First,#,%s,CITY,-1,-1;
			STATE "STATE" true true false 30 Text 0 0 ,First,#,%s,STATE,-1,-1;
			MIN_LFROMA "MIN_LFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_LFROMA,-1,-1;
			MAX_LTOADD "MAX_LTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_LTOADD,-1,-1;
			MIN_RFROMA "MIN_RFROMA" true true false 10 Text 0 0 ,First,#,%s,MIN_RFROMA,-1,-1;
			MAX_RTOADD "MAX_RTOADD" true true false 10 Text 0 0 ,First,#,%s,MAX_RTOADD,-1,-1;
			grid_id "grid_id" true true false 10 Long 0 10 ,First,#,%s,grid_id,-1,-1""" % (file, file, file, file, file, file, file, file)
		else:
			field_map = None

		arcpy.TableToTable_conversion(in_rows=csv_file, 
			out_path=dir_temp, 
			out_name="temp_for_shp.dbf",
			field_mapping=field_map)
		os.remove(shapefile_name.replace('.shp','.dbf'))
		os.remove(csv_file)
		os.rename(dir_temp+"/temp_for_shp.dbf",shapefile_name.replace('.shp','.dbf'))
		os.remove(dir_temp+"/temp_for_shp.dbf.xml")
		os.remove(dir_temp+"/temp_for_shp.cpg")

	#Create copy of "diradd" file to use as grid
	arcpy.CopyFeatures_management(grid_1940, grid)

	#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MIN replace with big number
	codeblock_min = """def replace(x):
		if x == ' ':
			return 999999
		else:
			return x"""
	fieldName = "LFROMADD"
	expression = "replace(!LFROMADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

	fieldName = "RFROMADD"
	expression = "replace(!RFROMADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_min)

	#Can't <null> blank values, so when Dissolve Unsplit lines aggregates MAX replace with small number
	codeblock_max = """def replace(x):
		if x == ' ':
			return -1
		else:
			return x"""
	fieldName = "LTOADD"
	expression = "replace(!LTOADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

	fieldName = "RTOADD"
	expression = "replace(!RTOADD!)"
	arcpy.CalculateField_management(grid, fieldName, expression, "PYTHON", codeblock_max)

	#First Dissolve to create split_grid (no multi-part segments, split at intersections)
	arcpy.Dissolve_management(grid, split_grid, 
		multi_part="SINGLE_PART", 
		unsplit_lines="DISSOLVE_LINES")

	#Add a unique, static identifier (so ranges can be changed later)
	expression="!FID! + 1"
	arcpy.AddField_management(split_grid, "grid_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(split_grid, "grid_id", expression, "PYTHON_9.3")

	#Intersect with grid
	temp = dir_path + 'temp_step.shp'
	arcpy.CopyFeatures_management(grid, temp)
	arcpy.Intersect_analysis([temp, split_grid], grid)
	arcpy.DeleteFeatures_management(temp)
	#arcpy.DeleteFeatures_management(split_grid)

	#Second Dissolve St_Grid lines
	arcpy.Dissolve_management(in_features=grid, 
		out_feature_class=grid_uns, 
		dissolve_field="grid_id", 
		statistics_fields="LFROMADD MIN;LTOADD MAX;RFROMADD MIN;RTOADD MAX", 
		unsplit_lines="UNSPLIT_LINES")

	#Get the longest street name from multi-part segments
	df_grid = dbf2DF(grid)
	longest_name_dict = {}
	problem_segments = {}
	for grid_id, group in df_grid.groupby(['grid_id']):
		max_chars = group['FULLNAME'].str.len().max()
		longest_name = group.loc[group['FULLNAME'].str.len()==max_chars,'FULLNAME'].drop_duplicates().tolist()
		if len(longest_name) > 1:
			problem_segments[grid_id] = longest_name
		# Always returns first entry in longest name (a list of names equal in length to max_chars)
		longest_name_dict[grid_id] = longest_name[0]

	#Assign longest street name by grid_id (also add city and state for geolocator)
	df_grid_uns = dbf2DF(grid_uns)
	df_grid_uns['CITY'] = name
	df_grid_uns['STATE'] = state
	df_grid_uns['FULLNAME'] = df_grid_uns.apply(lambda x: longest_name_dict[x['grid_id']], axis=1)

	#Blank out the big/small numbers now that aggregation is done

	# Function to blank out big/small numbers
	def replace_nums(x):
		if x == "999999" or x == "-1":
			return ' '
		else:
			return x

	hn_ranges = ["MIN_LFROMA", "MIN_RFROMA", "MAX_LTOADD", "MAX_RTOADD"]
	for field in hn_ranges:
		df_grid_uns[field] = df_grid_uns[field].astype(str)
		df_grid_uns[field] = df_grid_uns.apply(lambda x: replace_nums(x[field]), axis=1)

	save_dbf(df_grid_uns, grid_uns, field_map=True)

	#Add a unique, static identifier (so ranges can be changed later)
	arcpy.DeleteField_management(grid_uns, "grid_id")
	expression="!FID! + 1"
	arcpy.AddField_management(grid_uns, "grid_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(grid_uns, "grid_id", expression, "PYTHON_9.3")

	#Fix duplicate address ranges
	t = fix_dup_address_ranges(grid_uns)
	print(t)

	return problem_segments

# Amory's code for fixing duplicate address ranges
def fix_dup_address_ranges(grid_uns):
	shp = grid_uns
	## ENTER ALTERNATE FIELD NAMES ## ENTER ALTERNATE FIELD NAMES ## ENTER ALTERNATE FIELD NAMES ##
	LFROMADD = "MIN_LFROMA"  
	LTOADD = "MAX_LTOADD" 
	RFROMADD = "MIN_RFROMA"  
	RTOADD = "MAX_RTOADD" 
	OBJECTID = "FID"
	## ENTER ALTERNATE FIELD NAMES ## ENTER ALTERNATE FIELD NAMES ## ENTER ALTERNATE FIELD NAMES ## 

	# Calculate starting and ending coordinates and length for each line segment
	arcpy.AddGeometryAttributes_management(shp, "LENGTH_GEODESIC;LINE_START_MID_END")

	data = []

	fields = arcpy.ListFields(shp)
	field_names = [field.name for field in fields]

	for row in arcpy.SearchCursor(shp):
		data.append([row.getValue(field.name) for field in fields])

	df = pd.DataFrame(data, columns=field_names)

	grouped = df.groupby(["FULLNAME",LFROMADD,LTOADD,RFROMADD,RTOADD])
	
	df["IN_FID"] = grouped.grouper.group_info[0]

	#There is no simple way to assign _n of each group to a variable in the dataframe
	# so use Chris Graziul's dict workaround.
	foo = {}
	#create dict: keys: group IDs ; values: number of items in group
	for g, d in grouped:
		foo[g] = d[OBJECTID].count()
	df['size'] = df.apply(lambda x : foo[x["FULLNAME"],x[LFROMADD],x[LTOADD],x[RFROMADD],x[RTOADD]], axis=1)

	df = df[[OBJECTID,LFROMADD,LTOADD,RFROMADD,RTOADD,"IN_FID","LENGTH_GEO","size","START_X","END_X","START_Y","END_Y"]]

	addresses = open('new_addresses.csv', 'wt') #this is deprecated, although topo errors are still output here.
	addresses.write("fid,l_f_add,l_t_add,r_f_add,r_t_add,short_segment\n")

	df = df.sort_values('IN_FID')

	for col in df:
		df[col] = df[col].astype(str)
	DList = df.values.tolist()

	TopoErrors = []

	ind = 0

	#master list for corrected data
	Data = []

	#input data should be in format :
	#fid;l_f_add;l_t_add;r_f_add;r_t_add;in_fid;new_length;num_identical;start_x;end_x;start_y;end_y

	appInd = 0

	while ind < len(DList):
		if(appInd != ind):
			print("len of Data: %sind: %s" % (appInd,ind))
		feat_seq = DList[ind][5] # actually in_fid, as feat_seq was unreliable.
		feat_num = int(DList[ind][7]) # number of features
		feat_list = DList[ind : ind+feat_num] #list of features that comprised the original feature
		if feat_num > 1:
			##find beginning segment##
			start_segment = False
			i=0
			topology_error = False
			while start_segment == False and i<feat_num:
				start_segment = True
				start = (DList[ind+i][8]+" "+DList[ind+i][10]).strip()
				for feat in feat_list:
					end = (feat[9]+" "+feat[11]).strip()
					if end == start:
						start_segment = False
						i= i +1
						#print "found a connexion. i is now %d",i
						break
			if start_segment==False : #could not find a start segment
				#print "PANIC"
				#probably topology or parsing error; or we are dealing with a circular street segment
				#pretend that the first segment in the input order is the start segment
				i=0
			##put feat list in order of street direction##
			o_feat_list = []
			o_feat_list.append(DList[ind+i])
			order_num = 1
			end = (o_feat_list[0][9]+" "+o_feat_list[0][11]).strip()
			feat_length = float(o_feat_list[0][6])
			while order_num < feat_num:
				for j,feat in enumerate(feat_list):
					start = (feat[8]+" "+feat[10]).strip()
					if start == end:
						end = (feat[9]+" "+feat[11]).strip()
						order_num= order_num + 1
						feat_length = feat_length + float(feat[6])
						o_feat_list.append(feat)
						break
					if j==feat_num-1:
	#					print ("topological error (there is a gap)~~~~~~~~~~~~~~!!!!!!!!!!!!!!~~~~~~~~~~~~~~")
						TopoErrors.append(DList[ind+order_num])
						topology_error = True
						order_num= order_num + 1
			if topology_error==False:
				try:
					LFAdd = int(o_feat_list[0][1])
				except ValueError:
					LFAdd = 0
				try:
					LTAdd = int(o_feat_list[0][2])
				except ValueError:
					LTAdd = 0
				try:
					RFAdd = int(o_feat_list[0][3])
				except ValueError:
					RFAdd = 0
				try:
					RTAdd = int(o_feat_list[0][4])
				except ValueError:
					RTAdd = 0
				debug = False
				if debug==True:
					addresses.write("feat_seq: "+str(feat_seq)+", name: "+o_feat_list[0][5]+", num segments: "+str(feat_num)+", add range: "+str(LFAdd)+"-"+str(LTAdd)+" "+str(RFAdd)+"-"+str(RTAdd)+"\n")

				RRange = (RTAdd - RFAdd)
				LRange = (LTAdd - LFAdd)
				ORange = RRange
				OLange = LRange
				RDir, LDir = 0,0 #Dir: direction addresses are going in.

				final_feat_list = []
				for feat in o_feat_list:
					if round(abs((float(feat[6])/feat_length)*LRange)) < 2 and LRange!= 0 and round(abs((float(feat[6])/feat_length)*RRange)) < 2 and RRange!= 0:
						#if feat is too short to contain even a single address (on either side) in its range...
						feat[1]=feat[2]=feat[3]=feat[4]=0
						feat_num = feat_num - 1
						feat_length = feat_length - float(feat[6])
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+",1")
						if debug==True:
							addresses.write(" length is "+feat[6]+"/"+str(feat_length)+" which WAS too short\n")
						else:
							addresses.write("\n")
					else:
						final_feat_list.append(feat)

				o_feat_list = final_feat_list

				ShortRange = False
				if RRange!=0:
					RDir = RRange/abs(RRange)
				if LRange!=0:
					LDir = LRange/abs(LRange)
				if abs(RRange)>2*feat_num : #if address range is NOT too small in comparison to number of segments
					RRange -= 2*(feat_num-1)*RDir #account for the hidden extra 2 address range each time we change segments
				else:
					ShortRange = True
					if debug==True:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				if abs(LRange)>2*feat_num:
					LRange -= 2*(feat_num-1)*LDir
				else:
					ShortRange = True
					if debug==True:
						addresses.write("WOAH SUPER SHORT ADDRESS RANGE / LOTS OF SEGMENTS!!!\n")
				assignedLength = 0

				for j, feat in enumerate(o_feat_list):
					segmentLength = float(feat[6])
					assignedLength+=segmentLength
					tooShort = False
					if debug==True:
						addresses.write(str(int(round(((segmentLength/feat_length)*LRange)/2)*2))+" is more than 2. RRange is "+str(RRange)+"\n")
					if j == 0:
						feat[1] = LFAdd
						feat[3] = RFAdd
					else:
						feat[1] = int(o_feat_list[j-1][2])+2*LDir
						feat[3] = int(o_feat_list[j-1][4])+2*RDir
	#				print "left range",round(((segmentLength/feat_length)*LRange)/2)*2
					if j == feat_num-1:
						feat[2] = LTAdd
						feat[4] = RTAdd
					else:
						feat[2] = feat[1] + int(round(((segmentLength/feat_length)*LRange)/2)*2)
						feat[4] = feat[3] + int(round(((segmentLength/feat_length)*RRange)/2)*2)
						if feat[2] > LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2) and LDir>0 or LDir<0 and feat[2] < LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2):
							feat[2] = LFAdd + int(round(((assignedLength/feat_length)*OLange)/2)*2)
							if debug==True:
								addresses.write("HAD TO ADJUST on LEFT\n")
						if feat[4] > RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2) and RDir>0 or RDir<0 and feat[4] < RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2):
							if debug==True:
								addresses.write("HAD TO ADJUST on RIGHT\n")
							feat[4] = RFAdd + int(round(((assignedLength/feat_length)*ORange)/2)*2)
					if RRange == 0:
						feat[3] = feat[4] = RFAdd
					if LRange == 0:
						feat[1] = feat[2] = LFAdd

					if debug == True:
						if LDir > 0 and (feat[1] > LTAdd or feat[2] > LTAdd) or LDir < 0 and (feat[1] < LTAdd or feat[2] < LTAdd) or RDir > 0 and (feat[3] > RTAdd or feat[4] > RTAdd) or RDir < 0 and (feat[3] < RTAdd or feat[4] < RTAdd):
							addresses.write("THIS SHOULD NOT HAPPEN!\n")
						addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+" length is "+feat[6]+"/"+str(feat_length)+" which was NOT too short\n")
					else:
						#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
						Data.append(feat)
						appInd =appInd+1

			else : #if topo error
				for feat in feat_list:
					Data.append(feat) #add just the fid of all segments to Data if topo error
					appInd =appInd+1

		else : #if feature was not split
			feat = DList[ind]
			#addresses.write(str(feat[0])+","+str(feat[1])+","+str(feat[2])+","+str(feat[3])+","+str(feat[4])+"\n")
			Data.append(feat)
			appInd =appInd+1

		ind+=feat_num

	Data.sort(key=itemgetter(0)) #sort both by OBJECTID (both are text so the sorting is weird but consistently so!)
	newShp = os.path.splitext(shp)[0]+"2.shp"
	#have to create a new FID field because Arc won't let you sort on fields of type Object ID
	arcpy.AddField_management(in_table = shp, field_name="FID_str", field_type="TEXT", field_precision="", field_scale="", field_length="", field_alias="",
		field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
	arcpy.CalculateField_management(in_table = shp, field="FID_str", expression="!"+OBJECTID+"!", expression_type="PYTHON_9.3", code_block="")
	arcpy.Sort_management(shp, newShp, [["FID_str", "ASCENDING"]])

	with arcpy.da.UpdateCursor(newShp,[LFROMADD,LTOADD,RFROMADD,RTOADD]) as cursor:
		for i,row in enumerate(cursor):
			row[0] = Data[i][1]
			row[1] = Data[i][2]
			row[2] = Data[i][3]
			row[3] = Data[i][4]
			cursor.updateRow(row)
	addresses.write("Topology Errors. Must be fixed and re-run script or re-address manually.\n")

	for err in TopoErrors:
		addresses.write(str(err[0])+"\n")
	addresses.close()

	return "\nFixed duplicate address ranges"

# Creates physical blocks shapefile 
def physical_blocks(dir_path, name):
	pblocks = dir_path + name + "_1930_Pblk.shp"
	split_grid = dir_path + name + "_1930_stgrid_Split.shp"

	#if int(start_from) = 1930:
	#arcpy.AddField_management(grid, 'FULLNAME', 'TEXT')
	#arcpy.CalculateField_management(grid, "FULLNAME","!Strt_Fx!", "PYTHON_9.3")

	#Create Physical Blocks# #####
	arcpy.FeatureToPolygon_management(split_grid, pblocks)
	#Add a Physical Block ID
	expression="!FID! + 1"
	arcpy.AddField_management(pblocks, "pblk_id", "LONG", 4, "", "","", "", "")
	arcpy.CalculateField_management(pblocks, "pblk_id", expression, "PYTHON_9.3")

# Performs initial geocode on contemporary grid
def geocode(dir_path, name, state):
	add_locator = dir_path + name + "_addloc"
	#'_1930_Addresses.csv' originates from 'Create 1930 and 1940 Address Files.R' code
	addresses = dir_path + name + "_1930_Addresses.csv"
	address_fields="Street address; City city; State state"
	points30 = dir_path + name + "_1930_Points.shp"
	reference_data = dir_path + name + state + "_1930_stgrid_edit_Uns2.shp 'Primary Table'"

	field_map="'Feature ID' FID VISIBLE NONE; \
	'*From Left' MIN_LFROMA VISIBLE NONE; \
	'*To Left' MAX_LTOADD VISIBLE NONE; \
	'*From Right' MIN_RFROMA VISIBLE NONE; \
	'*To Right' MAX_RTOADD VISIBLE NONE; \
	'Prefix Direction' <None> VISIBLE NONE; \
	'Prefix Type' <None> VISIBLE NONE; \
	'*Street Name' FULLNAME VISIBLE NONE; \
	'Suffix Type' '' VISIBLE NONE; \
	'Suffix Direction' <None> VISIBLE NONE; \
	'Left City or Place' CITY VISIBLE NONE; \
	'Right City or Place' CITY VISIBLE NONE; \
	'Left ZIP Code' <None> VISIBLE NONE; \
	'Right ZIP Code' <None> VISIBLE NONE; \
	'Left State' STATE VISIBLE NONE; \
	'Right State' STATE VISIBLE NONE; \
	'Left Street ID' <None> VISIBLE NONE; \
	'Right Street ID' <None> VISIBLE NONE; \
	'Display X' <None> VISIBLE NONE; \
	'Display Y' <None> VISIBLE NONE; \
	'Min X value for extent' <None> VISIBLE NONE; \
	'Max X value for extent' <None> VISIBLE NONE; \
	'Min Y value for extent' <None> VISIBLE NONE; \
	'Max Y value for extent' <None> VISIBLE NONE; \
	'Left parity' <None> VISIBLE NONE; \
	'Right parity' <None> VISIBLE NONE; \
	'Left Additional Field' <None> VISIBLE NONE; \
	'Right Additional Field' <None> VISIBLE NONE; \
	'Altname JoinID' <None> VISIBLE NONE"

	#Make sure address locator doesn't already exist - if it does, delete it
	add_loc_files = [dir_path+'\\'+x for x in os.listdir(dir_path) if x.startswith(name+"_addloc")]
	for f in add_loc_files:
			 if os.path.isfile(f):
				 os.remove(f)

	print("The script is executing the 'CreateAddressLocator' tool")
	#Create Address Locator
	arcpy.CreateAddressLocator_geocoding(in_address_locator_style="US Address - Dual Ranges", in_reference_data=reference_data, in_field_map=field_map, out_address_locator=add_locator, config_keyword="")
	print("The script has finished executing the 'CreateAddressLocator' tool and has begun executing the 'GeocodeAddress' tool")
	#Geocode Points
	arcpy.GeocodeAddresses_geocoding(addresses, add_locator, address_fields, points30)
	print("The script has finished executing the 'GeocodeAddress' tool and has begun executing the 'SpatialJoin' tool")

# Attach physical block IDs to geocoded points 
def attach_pblk_id(dir_path, name, points30):
	#Define paths
	pblk_points = dir_path + name + "_1930_Pblk_Points.shp"
	pblocks = dir_path + name + "_1930_Pblk.shp"
	#Attach Pblk ids to points
	arcpy.SpatialJoin_analysis(points30, pblocks, pblk_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT")
	print("The script has finished executing the 'SpatialJoin' tool")

#
# 
#
