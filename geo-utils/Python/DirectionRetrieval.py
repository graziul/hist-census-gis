
#
# Name:			DirectionRetrieval.py
#
# Author(s):	Chris Graziul and Amory Kisch 
#
# Purpose:		Re-add street directions lost when creating 1940 street grids from contemporary Tiger/LINE street grids
#
# Usage:		To be run as batch with CityInfo.csv as input			
#
# File types:	Edited street grid shapefiles
#				Tiger/LINE street grid shapefiles
#


from __future__ import print_function
from multiprocessing import Pool
import time
import arcpy
import os
import sys
import re
import pysal as ps
import pandas as pd
import numpy as np
arcpy.env.overwriteOutput = True

# Functions

# Function to reads in DBF files and return Pandas DF
def dbf2DF(dbfile, upper=True):
	db = ps.open(dbfile) #Pysal to open DBF
	d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
	#pandasDF = pd.DataFrame(db[:]) #Convert to Pandas DF
	pandasDF = pd.DataFrame(d) #Convert to Pandas DF
	if upper == True: #Make columns uppercase if wanted 
		pandasDF.columns = map(str.upper, db.header) 
	db.close() 
	return pandasDF

# Function to save Pandas DF as DBF file 
def save_dbf(df, shapefile_name):
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
		return [st, DIR, NAME, TYPE]

# Paths
dir_path = "S:/Users/Chris/"
stedit_path = "S:/Projects/1940Census/StreetGridsStdName/"
tiger2012_path = "S:/Projects/1940Census/County Shapefiles/"
sj_path = "S:/Projects/1940Census/DirAdd/"

# Get city list
city_info_csv = tiger2012_path + 'CityInfo.csv'
city_info_df = pd.read_csv(city_info_csv, dtype={'fips':str})

# Create city dictionary {CityState:CountyFIPS}
city_info_list = city_info_df.values.tolist()
city_fips_dict = {i[0].replace(' ','')+i[1]:i[3] for i in city_info_list}

# Function to fix blank street names
def fix_blank_names(stedit, contemp1, contemp2):
	# If student edited grid has no street name, fill it in 
	if stedit == "":
		if contemp1 == "":
			return contemp2
		else:
			return contemp1
	else:
		return stedit
			
# Function to add direction
# Note: If edited NAME+TYPE is same as contemp NAME+TYPE, check if edited DIR is same as contemp DIR
def add_dir(dir_e, dir_t1, dir_t2, st_e, st_t1, st_t2):
	if st_e == st_t1:
		if dir_e != "" and dir_t1 != "" and dir_e != dir_t1:
			return '', True
		if dir_e == "" and dir_t1 != "":
			return dir_t1, False
		else:
			return '', False
	if st_e == st_t2:
		if dir_e != "" and dir_t2 != "" and dir_e != dir_t2:
			return '', True
		if dir_e == "" and dir_t2 != "":
			return dir_t2, False
		else:
			return '', False
	else:
		return '', False

# Function to do the work
def fix_dir(city):

	# Load files
	citystate = city[0]
	fips = city[1]

	# Filenames
	stedit_shp_file = stedit_path + citystate + "_1940_stgrid_edit.shp"
	stedit_pol_shp_file = stedit_path + citystate + "_1940_stgrid_pol.shp"
	stedit_pol_diss_shp_file = stedit_path + citystate + "_1940_stgrid_pol_diss.shp"
	stedit_pol_diss_buff_shp_file = stedit_path + citystate + "_1940_stgrid_pol_diss_buff.shp"
	tiger2012_shp_file = tiger2012_path + citystate + "_2012_tigerline.shp"
	tiger2012_clip_shp_file = tiger2012_path + citystate + "_2012_tigerline_clip.shp"
	sj_file = sj_path + citystate + "_Spatial_Join.shp"
	sj2_file = sj_path + citystate + "_Spatial_Join2.shp"
	buff_file = sj_path + citystate + "_1940_60ft_BUFF.shp"
	diradd_file = sj_path + citystate + "_1940_stgrid_diradd.shp"
	gaps_file = stedit_path + citystate + "_gaps.shp"
	temp_file = stedit_path + citystate + "_temp.shp"

	# Create copy of edited 1940 street grid
	try:
		arcpy.DeleteFeatures_management(stedit_shp_file)
	except:
		pass
	try:
		if citystate == "StLouisMO":
			arcpy.CopyFeatures_management("S:\\Projects\\1940Census\\StLouis\\GIS_edited\\StLouisMO_1930_stgrid_edit.shp", 
			stedit_shp_file)
		else:
			arcpy.CopyFeatures_management("S:\\Projects\\1940Census\\StreetGrids\\" + citystate + "_1940_stgrid_edit.shp", 
			stedit_shp_file)
	except Exception as e:
		print("Error loading 1940 street grid for %s" % (citystate))
		return ['','','','','',''], {}

	# Create copy of TigerLINE 2012 street grid
	try:
		arcpy.DeleteFeatures_management(tiger2012_shp_file)
	except:
		pass
	arcpy.CopyFeatures_management("S:\\Projects\\1940Census\\County Shapefiles\\tl_2012_" + fips + "_edges.shp", 
		tiger2012_shp_file)

	# Clip TigerLINE 2012 file to match 1940 street grid (Lisa)
	arcpy.FeatureToPolygon_management(in_features=stedit_shp_file, 
		out_feature_class=stedit_pol_shp_file, 
		attributes="ATTRIBUTES")
	arcpy.Dissolve_management(in_features=stedit_pol_shp_file, 
		out_feature_class=stedit_pol_diss_shp_file, 
		dissolve_field="Id", 
		multi_part="MULTI_PART", 
		unsplit_lines="DISSOLVE_LINES")
	arcpy.Buffer_analysis(in_features=stedit_pol_diss_shp_file, 
		out_feature_class=stedit_pol_diss_buff_shp_file, 
		buffer_distance_or_field="1000 Feet", 
		line_side="FULL", 
		line_end_type="ROUND", 
		dissolve_option="NONE", 
		method="PLANAR")
	arcpy.Clip_analysis(in_features=tiger2012_shp_file, 
		clip_features=stedit_pol_diss_buff_shp_file, 
		out_feature_class=tiger2012_clip_shp_file)

	# Load attibute data for files
	df_stedit = dbf2DF(stedit_shp_file.replace('.shp','.dbf'),upper=False)
	df_tiger2012 = dbf2DF(tiger2012_clip_shp_file.replace('.shp','.dbf'),upper=False)

	# Determine number of DIR in TigerLINE 2012
	df_tiger2012['FULLSTD'], df_tiger2012['DIR'], df_tiger2012['NAME'], df_tiger2012['TYPE'] = zip(*df_tiger2012.apply(lambda x: standardize_street(x['FULLNAME']), axis=1))
	tiger2012_dir_counts_dict = df_tiger2012['DIR'].value_counts().to_dict()

	# Drop all extraneous variables
	df_stedit['FULLEDIT'] = df_stedit['FULLNAME']
	df_stedit['OrigStE'] = df_stedit['FULLNAME']
	keep_vars_stedit = ['FULLEDIT','LFROMADD','LTOADD','RFROMADD','RTOADD','OrigStE']
	df_stedit = df_stedit[keep_vars_stedit]
	
	df_tiger2012['FULL2012'] = df_tiger2012['FULLNAME']
	df_tiger2012['OrigStT'] = df_tiger2012['FULLNAME']
	keep_vars_tiger2012 = ['FULL2012','OrigStT']
	df_tiger2012 = df_tiger2012[keep_vars_tiger2012]

	# Write .dbf
	save_dbf(df_stedit, stedit_shp_file)
	save_dbf(df_tiger2012, tiger2012_clip_shp_file)

	# Create copies of original FID (text) variable
	arcpy.AddField_management(stedit_shp_file, "FIDCOPYE", "TEXT", 50, "", "","", "", "")
	arcpy.AddField_management(tiger2012_clip_shp_file, "FIDCOPYT", "TEXT", 50, "", "","", "", "")

	arcpy.CalculateField_management(in_table=stedit_shp_file, 
		field="FIDCOPYE", 
		expression="!FID!", 
		expression_type="PYTHON") 
	arcpy.CalculateField_management(in_table=tiger2012_clip_shp_file,
		field="FIDCOPYT", 
		expression="!FID!", 
		expression_type="PYTHON") 

	# Process: Spatial Join

	# Spatial join - ARE_IDENTICAL_TO
	arcpy.SpatialJoin_analysis(target_features=stedit_shp_file, 
		join_features=tiger2012_clip_shp_file, 
		out_feature_class=sj_file, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL", 
		field_mapping="""FULLEDIT "FULLEDIT" true true false 254 Text 0 0 ,First,#,%s,FULLEDIT,-1,-1;
		LFROMADD "LFROMADD" true true false 10 Long 0 10 ,First,#,%s,LFROMADD,-1,-1;
		LTOADD "LTOADD" true true false 10 Long 0 10 ,First,#,%s,LTOADD,-1,-1;
		RFROMADD "RFROMADD" true true false 10 Long 0 10 ,First,#,%s,RFROMADD,-1,-1;
		RTOADD "RTOADD" true true false 10 Long 0 10 ,First,#,%s,RTOADD,-1,-1;
		OrigStE "OrigStE" true true false 254 Text 0 0 ,First,#,%s,OrigStE,-1,-1;
		FIDCOPYE "FIDCOPYE" true true false 254 Text 0 0 ,First,#,%s,FIDCOPYE,-1,-1;
		FULL2012 "FULL2012" true true false 254 Text 0 0 ,First,#,%s,FULL2012,-1,-1;
		OrigStT "OrigStT" true true false 254 Text 0 0 ,First,#,%s,OrigStT,-1,-1;
		FIDCOPYT "FIDCOPYT" true true false 254 Text 0 0 ,First,#,%s,FIDCOPYT,-1,-1""" % (stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, stedit_shp_file, tiger2012_clip_shp_file, tiger2012_clip_shp_file, tiger2012_clip_shp_file), 
		match_option="ARE_IDENTICAL_TO")
	# Create Buffer
	arcpy.Buffer_analysis(in_features=sj_file, 
		out_feature_class=buff_file, 
		buffer_distance_or_field="60 Feet", 
		line_side="FULL", 
		line_end_type="ROUND", 
		dissolve_option="NONE", 
		method="PLANAR")
	# Spatial join - CONTAINS
	arcpy.SpatialJoin_analysis(target_features=buff_file, 
		join_features=tiger2012_clip_shp_file, 
		out_feature_class=sj2_file, 
		join_operation="JOIN_ONE_TO_ONE", 
		join_type="KEEP_ALL", 
		match_option="CONTAINS")

	# Load final street grid data and create vars for comparison
	df_sj2 = dbf2DF(sj2_file.replace('.shp','.dbf'),upper=False)

	df_sj2['FULLSTD_e'], df_sj2['DIR_e'], df_sj2['NAME_e'], df_sj2['TYPE_e'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULLEDIT']), axis=1))
	df_sj2['FULLSTD_t1'], df_sj2['DIR_t1'], df_sj2['NAME_t1'], df_sj2['TYPE_t1'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULL2012']), axis=1))
	df_sj2['FULLSTD_t2'], df_sj2['DIR_t2'], df_sj2['NAME_t2'], df_sj2['TYPE_t2'] = zip(*df_sj2.apply(lambda x: standardize_street(x['FULL2012_1']), axis=1))

	df_sj2['st_e'] = df_sj2['NAME_e'] + ' ' + df_sj2['TYPE_e']
	df_sj2['st_e'] = df_sj2['st_e'].str.rstrip()
	df_sj2['st_t1'] = df_sj2['NAME_t1'] + ' ' + df_sj2['TYPE_t1']
	df_sj2['st_t1'] = df_sj2['st_t1'].str.rstrip()
	df_sj2['st_t2'] = df_sj2['NAME_t2'] + ' ' + df_sj2['TYPE_t2']
	df_sj2['st_t2'] = df_sj2['st_t2'].str.rstrip()

	# Fix blank street names
 #	df_sj2['FULLSTD'] = df_sj2.apply(lambda x: fix_blank_names(x['FULLSTD_e'], x['FULLSTD_t1'], x['FULLSTD_t2']), axis=1)

	# Add DIR if called for
	df_sj2['DIR_fix'], df_sj2['DIR_mismatch'] = zip(*df_sj2.apply(lambda x: add_dir(x['DIR_e'], x['DIR_t1'], x['DIR_t2'], x['st_e'], x['st_t1'], x['st_t2']), axis=1))

	# Rereate FULLNAME based on fixed DIR
	def make_fullname(dir_e, dir_fix, st_e):
		if dir_e != '':
			return dir_e + ' ' + st_e
		if dir_e == '' and dir_fix != '':
			return dir_fix + ' ' + st_e
		if dir_e == '' and dir_fix == '':
			return st_e
	df_sj2['FULLNAME'] = df_sj2.apply(lambda x: make_fullname(x['DIR_e'],x['DIR_fix'],x['st_e']), axis=1)

	# Save df_sj2
	save_dbf(df_sj2, sj2_file)

	# Create DF to merge with 1940 edited street grid
	df_tomerge = df_sj2[['FIDCOPYE','DIR_e','DIR_fix','FULLNAME']]

	# Merge streets with fixed DIR and 1940 edited street grid
	df_stedit = dbf2DF(stedit_shp_file.replace('.shp','.dbf'),upper=False)
	df = df_stedit.merge(df_tomerge, how='left', on='FIDCOPYE')
	arcpy.CopyFeatures_management(stedit_shp_file, temp_file)	
	save_dbf(df, temp_file)

	# Fix gaps
	arcpy.SpatialJoin_analysis(target_features=temp_file,
		join_features=temp_file, 
		out_feature_class=gaps_file, 
		join_operation="JOIN_ONE_TO_MANY", 
		join_type="KEEP_ALL", 
		field_mapping="""FIDCOPYE "FIDCOPYE" true true false 100 Text 0 0 ,First,#,%s,FIDCOPYE,-1,-1;
		FULLNAME "FULLNAME" true true false 100 Text 0 0 ,First,#,%s,FULLNAME,-1,-1;
		FULLNAME_1 "FULLNAME_1" true true false 100 Text 0 0 ,First,#,%s,FULLNAME,-1,-1""" % (temp_file, temp_file, temp_file), 
		match_option="INTERSECT")

	def list_append_unique(LIST, item) :
		if(not item in LIST) :
			LIST.append(item)
		return LIST

	def make_nametype(st_list):
		NAME, TYPE = st_list
		nametype = NAME + ' ' + TYPE
		return nametype.rstrip()

	df_gaps = dbf2DF(gaps_file.replace('.shp','.dbf'),upper=False)
	# Make dictionary for FID to TARGET FID
	fid_dict = {target_fid:df_group['FULLNAME'].tolist() for target_fid, df_group in df_gaps.groupby('TARGET_FID')}
 #	for target_fid, df_group in df_diradd.groupby('TARGET_FID'):
 #		fid_dict[target_fid] = df_group['FULLNAME'].tolist()
	# run through FIDs from original Target file	
	def fill_gap(curFID, fullname):
		_, st_dir, st_name, st_type = standardize_street(fullname)
		# st=FULLNAME of segment identified by curFID #we can either retrieve this from original Target, or it is the record from TargetSJ where TARGET_FID == JOIN_FID == curFID
		nametype = make_nametype([st_name, st_type])
		#select records where TARGET_FID == curFID # this gives us all streets that intersected with segment identified by curFID
		intersect_list = fid_dict[int(curFID)]
		same_name_list = filter(lambda x: make_nametype(standardize_street(x)[2:])==nametype, intersect_list)
		dir_list = []
		for st in same_name_list :
			list_append_unique(dir_list, standardize_street(st)[1])
		if (len(dir_list)==1) and st_dir == '':
			return same_name_list[0]
		else :
			#multiple different directions, no change
			return fullname
	arcpy.CopyFeatures_management(temp_file, diradd_file)
	df_diradd = dbf2DF(diradd_file.replace('.shp','.dbf'),upper=False)	
	df_diradd['FULLNAMEda'] = df_diradd.apply(lambda x: fill_gap(x['FIDCOPYE'], x['FULLNAME']), axis=1)

	def note_gap_dir_fixes(st,dir_fix):
		_, st_dir, _, _ = standardize_street(st)
		if dir_fix == "" and st_dir != "":
			return st_dir
		else:
			return dir_fix

	num_missing_before = len(df_diradd[df_diradd['DIR_e']!=df_diradd['DIR_fix']])
	df_diradd['DIR_fix'] = df_diradd.apply(lambda x: note_gap_dir_fixes(x['FULLNAMEda'], x['DIR_fix']), axis=1)
	num_missing_after = len(df_diradd[df_diradd['DIR_e']!=df_diradd['DIR_fix']])
	num_gaps_filled = num_missing_before - num_missing_after

	# Cleanup shapefiles
	arcpy.Delete_management(stedit_pol_shp_file)
	arcpy.Delete_management(stedit_pol_diss_shp_file)
	arcpy.Delete_management(stedit_pol_diss_buff_shp_file)
	arcpy.Delete_management(tiger2012_shp_file)
	arcpy.Delete_management(buff_file)
	arcpy.Delete_management(sj_file)
	arcpy.Delete_management(sj2_file)
	arcpy.Delete_management(gaps_file)
	arcpy.Delete_management(temp_file)

	# Count changes
	stgrid_dir_counts_dict = df_sj2['DIR_e'].value_counts().to_dict()
	fixed_dir_counts_dict = df_diradd['DIR_fix'].value_counts().to_dict()

	num_stseg = sum(stgrid_dir_counts_dict.values())
	num_dirs_stedit = num_stseg - stgrid_dir_counts_dict['']
	num_dirs_added = stgrid_dir_counts_dict[''] - fixed_dir_counts_dict[''] 

	num_tiger = sum(tiger2012_dir_counts_dict.values()) 
	num_dirs_tiger = num_tiger - tiger2012_dir_counts_dict['']

	info_dict = {'tiger2012':tiger2012_dir_counts_dict,
		'stedit':stgrid_dir_counts_dict,
		'diradd':fixed_dir_counts_dict}

	info = [citystate, num_stseg, num_dirs_stedit, num_dirs_added, num_tiger, num_dirs_tiger]

	print("Finished %s, %s DIR mismatches" % (citystate, str(df_sj2['DIR_mismatch'].sum())))

	return info, info_dict 


# This iterates sequentially as opposed to parallel processing
temp_dict = {}
temp = []
start_total = time.time()
for i in city_fips_dict.items():
	info, info_dict = fix_dir(i)
	temp.append(info)
	temp_dict[i[0]] = info_dict
temp = [i for i in temp if i != ['', '', '', '', '', '']]
end_total = time.time()

total_time = round(float(end_total-start_total)/60,1)
print("Total processing time: %s\n" % (total_time))

'''
pool = Pool(processes=4, maxtasksperchild=1)
temp = pool.map(fix_dir, city_fips_dict.items())
pool.close()
'''
# pd.DataFrame.from_dict(info_dict)

# Build dashboard for decade and save
city_state = ['City']
tiger_names = ['num_tiger','num_dirs_tiger']
stedit_names = ['num_stedit','num_dirs_stedit','num_dirs_added']

sp = ['']
names = city_state + stedit_names + tiger_names 
df = pd.DataFrame(temp,columns=names)

dfnum = df.ix[:,0:5].sort_values(by='num_dirs_stedit').reset_index()

dashboard = pd.concat([dfnum],axis=1)
del dashboard['index']

csv_file = sj_path + '/DirAddSummary.csv' 
dashboard.to_csv(csv_file, index=False)
