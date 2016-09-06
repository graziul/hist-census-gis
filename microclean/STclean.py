#
#	Name: 		STclean.py
#	Authors: 	Chris Graziul
#
#	Input:		file_name - File name of city file, saved in Stata 13 (or below) format
#	Output:		<file_name>_autocleaned.csv - City file with addresses cleaned 
#
#	Purpose:	This is the master script for automatically cleaning addresses before
#				manually cleaning the file using Ancestry images. Large functions will
#				eventually become separate scripts that will be further refined and
#				called from this script.
#

from __future__ import print_function
import urllib
import re
import os
import sys
import time
import math
import pickle
import numpy as np
import pandas as pd
import fuzzyset
from termcolor import colored, cprint
from colorama import AnsiToWin32, init
from microclean.STstandardize import *

file_path = '/home/s4-data/LatestCities' 

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

def load_city(city,state,year):

    start = time.time()

    try:
        file_name = city + state
        df = pd.read_stata(file_path + '/%s/%s.dta' % (str(year),file_name), convert_categoricals=False)
    except:
        print('Error loading %s raw data' % (city))
        return [year, city, state, 0, 
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0, 0,
    0, 0, 0, 0, 0] 

    if len(df) == 0:
        print('Error loading %s raw data' % (city))
        return [year, city, state, 0, 
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0, 0,
    0, 0, 0, 0, 0]   

    end = time.time()

    num_records = len(df)

    load_time = round(float(end-start)/60,1)
    cprint('Loading data for %s took %s' % (city,load_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

    #Save a pristine copy for debugging
    #df_save = df

    #The original variable names change from census to census

    if year == 1940:
        df['street_raw'] = df['street']
    if year == 1930:
        df['street_raw'] = df['self_residence_place_streetaddre']
    if year == 1920:
        df['street_raw'] = df['indexed_street']
    if year == 1910:
        df['street_raw'] = df['Street']

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

    if year == 1940:
        df['hn'] = df['housenum']
    if year == 1930:
        df['hn'] = df['general_house_number_in_cities_o']
    if year == 1920:
        df['hn'] = df['general_housenumber']
    if year == 1910:
        df['hn'] = df['HouseNumber']    

    return df, load_time

def load_steve_morse(df,city,state,year):

    #NOTE: This dictionary must be built independently of this script
    sm_st_ed_dict_file = pickle.load(open(file_path + '/sm_st_ed_dict.pickle','rb'))
    sm_st_ed_dict = sm_st_ed_dict_file[year][(city,'%s' % (state.lower()))]

    #Capture all Steve Morse streets in one list
    sm_all_streets = sm_st_ed_dict.keys()

    #For bookkeeping when validating matches using ED 
    microdata_all_streets = np.unique(df['street_precleaned'])
    for st in microdata_all_streets:
        if st not in sm_all_streets:
            sm_st_ed_dict[st] = None

    #
    # Build a Steve Morse (sm) ED-to-Street (ed_st) dictionary (dict)
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

    return sm_all_streets, sm_st_ed_dict, sm_ed_st_dict

def preclean_street(df,city):

    start = time.time()
    #Create dictionary for (and run precleaning on) unique street names
    grouped = df.groupby(['street_raw'])
    cleaning_dict = {}
    for name,_ in grouped:
        cleaning_dict[name] = standardize_street(name)
    #Use dictionary create st (cleaned street), DIR (direction), NAME (street name), and TYPE (street type)
    df['street_precleaned'] = df['street_raw'].apply(lambda s: cleaning_dict[s][0])
    df['DIR'] = df['street_raw'].apply(lambda s: cleaning_dict[s][1])
    df['NAME'] = df['street_raw'].apply(lambda s: cleaning_dict[s][2])
    df['TYPE'] = df['street_raw'].apply(lambda s: cleaning_dict[s][3])
    end = time.time()
    preclean_time = round(float(end-start)/60,1)

    cprint('Precleaning street names for %s took %s\n' % (city,preclean_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

    return df, preclean_time

def find_exact_matches(df,city,sm_all_streets,sm_st_ed_dict):

    num_records = len(df)

    cprint("Exact matching algorithm \n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

    start = time.time()

    #
    # Check for exact matches between Steve Morse ST and microdata ST
    #

    df['sm_st_exact_match_bool'] = df['street_precleaned'].apply(lambda s: s in sm_all_streets)
    sm_st_exact_matches = np.sum(df['sm_st_exact_match_bool'])
    if num_records == 0:
        num_records += 1
    cprint("Exact matches before ED validation: "+str(sm_st_exact_matches)+" of "+str(num_records)+" cases ("+str(round(100*float(sm_st_exact_matches)/float(num_records),1))+"%)",file=AnsiToWin32(sys.stdout))

    #
    # Validate exact matches by comparing Steve Morse ED to microdata ED
    #

    #Helper function for checking that microdata ED is in Steve Morse list of EDs for street name
    def check_ed_match(microdata_ed,microdata_st):
        if (microdata_st is None) or (sm_st_ed_dict[microdata_st] is None):
            return False
        else:
            if microdata_ed in sm_st_ed_dict[microdata_st]:
                return True
            else:
                return False

    df['sm_ed_match_bool'] = df.apply(lambda s: check_ed_match(s['ed'],s['street_precleaned']), axis=1)

    #Validation of exact match fails if microdata ED and Steve Morse ED do not match
    failed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_ed_match_bool==False)]
    num_failed_validation = len(failed_validation)
    #Validation of exact match succeeds if microdata ED and Steve Morse ED are the same
    passed_validation = df[(df.sm_st_exact_match_bool==True) & (df.sm_ed_match_bool==True)]
    num_passed_validation = len(passed_validation)

    #Keep track of unique street-ED pairs that have failed versus passed validation
    num_pairs_failed_validation = len(failed_validation.groupby(['ed','street_precleaned']).count())
    num_pairs_passed_validation = len(passed_validation.groupby(['ed','street_precleaned']).count())
    num_pairs = num_pairs_failed_validation + num_pairs_passed_validation
    end = time.time()
    exact_matching_time = round(float(end-start)/60,1)

    if sm_st_exact_matches == 0:
        sm_st_exact_matches += 1
    cprint("Failed ED validation: "+str(num_failed_validation)+" of "+str(sm_st_exact_matches)+" cases with exact name matches ("+str(round(100*float(len(failed_validation))/float(sm_st_exact_matches),1))+"%)",'red',file=AnsiToWin32(sys.stdout))
    cprint("Exact matches after ED validation: "+str(num_passed_validation)+" of "+str(num_records)+" cases ("+str(round(100*float(num_passed_validation)/float(num_records),1))+"%)",file=AnsiToWin32(sys.stdout))
    if num_pairs == 0:
        num_pairs += 1
    cprint("Cases failing ED validation represent "+str(num_pairs_failed_validation)+" of "+str(num_pairs)+" total Street-ED pairs ("+str(round(100*float(num_pairs_failed_validation)/float(num_pairs),1))+"%)\n",'yellow',file=AnsiToWin32(sys.stdout))
    cprint("Exact matching and ED validation for %s took %s\n" % (city,exact_matching_time), 'cyan', attrs=['dark'], file=AnsiToWin32(sys.stdout))

    prop_passed_validation = float(num_passed_validation)/float(num_records)
    prop_failed_validation = float(num_failed_validation)/float(num_records)
    prop_pairs_failed_validation = float(num_pairs_failed_validation)/float(num_pairs)

    exact_info = [num_records, num_passed_validation, prop_passed_validation, num_failed_validation, prop_failed_validation, num_pairs_failed_validation, num_pairs, prop_pairs_failed_validation]

    return df, exact_info

def find_fuzzy_matches(df,city,sm_all_streets,sm_ed_st_dict):

    num_records = len(df)

    cprint("Fuzzy matching algorithm \n",attrs=['underline'],file=AnsiToWin32(sys.stdout))

    start = time.time()

    #
    # Find the best matching Steve Morse street name
    #

    #Create a set of all streets for fuzzy matching (create once, call on)
    sm_all_streets_fuzzyset = fuzzyset.FuzzySet(sm_all_streets)

    #Keep track of problem EDs
    problem_EDs = []

    def sm_fuzzy_match(street,ed):
        
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
        if (best_match_ed[1] == best_match_all[1]) & (best_match_ed[0] > 0.5):
            return [best_match_ed[1],best_match_ed[0],True]
        else:
            return ['','',False]

    #Create dictionary based on Street-ED pairs for faster lookup using helper function
    df_no_validated_exact_match = df[(df.sm_st_exact_match_bool==False) | (df.sm_ed_match_bool==False)]
    df_grouped = df_no_validated_exact_match.groupby(['street_precleaned','ed'])
    sm_fuzzy_match_dict = {}
    for st_ed,_ in df_grouped:
    	sm_fuzzy_match_dict[st_ed] = sm_fuzzy_match(st_ed[0],st_ed[1])

    #Helper function (necessary since dictionary built only for cases without validated exact matches)
    def get_fuzzy_match(ed,street):
        try:
            return sm_fuzzy_match_dict[street,ed]
        except:
            return ['','',False]
       
    #Get fuzzy matches and replace missing data with null values
    df['sm_st_fuzzy_match'] = df.apply(lambda s: get_fuzzy_match(s['ed'],s['street_precleaned'])[0], axis=1)
    df['sm_st_fuzzy_match_score'] = df.apply(lambda s: get_fuzzy_match(s['ed'],s['street_precleaned'])[1], axis=1)
    df['sm_st_fuzzy_match_bool'] = df.apply(lambda s: get_fuzzy_match(s['ed'],s['street_precleaned'])[2], axis=1)
    sm_st_fuzzy_matches = np.sum(df['sm_st_fuzzy_match_bool'])

    end = time.time()
    fuzzy_matching_time = round(float(end-start)/60,1)

    #Compute number of cases without validated exact match
    num_current_residual_cases = num_records - num_passed_validation

    cprint("Fuzzy matches (using microdata ED): "+str(sm_st_fuzzy_matches)+" of "+str(num_current_residual_cases)+" unmatched cases ("+str(round(100*float(sm_st_fuzzy_matches)/float(num_current_residual_cases),1))+"%)\n",file=AnsiToWin32(sys.stdout))
    cprint("Fuzzy matching for %s took %s\n" % (city,fuzzy_matching_time),'cyan',attrs=['dark'],file=AnsiToWin32(sys.stdout))

    fuzzy_info = [sm_st_fuzzy_matches,prop_sm_fuzzy_matches]

    return df, fuzzy_info, problem_EDs

