import pandas as pd
import re
import csv
import os
import numpy as np

#Given a string found in the block microdata field, return a list of the unique block IDs that should make up
#the string. Assumes that block IDs are numerical (with perhaps one alphabetical character as a suffix)
def parse_block_string(s) :
        s = s.strip(' .')
        # Deal with cases that are exceptions to the normal delimiters first        
        exception_list = []
        exception_patt = '^[0-9]+[\.\- ]*[A-Za-z]( |$)'
        exception_str = re.search(exception_patt,s)
        while exception_str : # find strings like: '102 - S' or 100-A
                exception_str = exception_str.group(0)
                exception_list.append(re.sub(' |-|\.','',exception_str))
                s = re.sub(re.escape(exception_str),'',s)
                exception_str = re.search(exception_patt,s)
        # ignore direction in strings like 'W 3719 and S 3532' or 'E 3176-3174' (only seem to be in DC)

        #TODO: Deal with '1 1/2'
        
        s = re.sub(' ?[Ss][Ee]+ [Aa]?[Ll]?[Ss]?[Oo]?.*','',s) #remove 'see (also)' and anything following
        s = re.sub(' ?[Aa][Ll][Ss][Oo] [Ss][Ee]+.*','',s) #remove 'also see' and anything following
        s = re.sub(' ?[Cc][Oo][Nn]\'?[TtDd].*','',s) #remove 'cont' and anything following
        s = re.sub(' ?[Ss]?[Ee]* ?[Pp][Aa][Gg][Ee].*','',s) #remove '(see )page' and anything following
        s = re.sub(' ?[Gg][Ee][Oo][Gg].*','',s) #remove 'geog' and anything following
        s = re.sub(' ?[Ss][Hh][Ee]+[Tt].*','',s) #remove 'sheet' and anything following
        s = re.sub(' ?[Ll][Ii][Nn][Ee].*','',s) #remove 'line' and anything following
        s = re.sub('^([Pp][Aa][Rr][Tt])? ?([Oo][Ff])? ?([Bb][Ll][A-Za-z]+)? ?','',s) #remove '(part) (of) (bl.)' at beginning
        s = re.sub('[ \-\.][^0-9]+$','',s) #remove any length string of non-numeric characters at end of s following ( ,-,.)
        s = re.sub('[^0-9 ]{5,}.*','',s) #remove a string of at least 5 non-numeric or space characters and anything following

        
        delimiters = ['[Aa][Nn][Dd]','[Oo][Rr]','[Tt][Oo]','-',' ',',']
        delim_str = '|'.join(delimiters)
        string_list = re.split(delim_str,s)
        string_list = filter(lambda x: re.search('[0-9]+',x),string_list)
        string_list.extend(exception_list)

        return list(np.unique(string_list))

def fix_block(city_info) :
        city, state_abbr, year = city_info
        os.chdir(file_path+'/'+year+'/autocleaned/V7')
        csv_file = city+state_abbr+"_AutoCleanedV7.csv"
        #TODO
        

def fix_block_all_cities(year) :

        file_path='/home/s4-data/LatestCities'
        city_info_file = file_path + '/CityExtractionList.csv' 
        city_info_df = pd.read_csv(city_info_file)
        city_info_df = city_info_df[city_info_df['Status']>0]
        city_info_df.loc[:,'city_name'], city_info_df.loc[:,'state_abbr'] = zip(*city_info_df['City'].str.split(','))
        city_info_df = city_info_df[['city_name','state_abbr']]
        city_info_df['city_name'] = city_info_df['city_name'].str.replace('Saint','St').str.replace(' ','') #have to keep "St. ____"
        city_info_df['state_abbr'] = city_info_df['state_abbr'].str.replace(' ','')
        city_state_iterator = zip(city_info_df['city_name'],city_info_df['state_abbr'])

        for city, state_abbr in city_state_iterator :
                city_info = [city,state_abbr,year]
                csv_file = city+state_abbr+"_AutoCleanedV7.csv"
                if os.path.isfile(csv_file) :
                        fix_block([city,state_abbr,year])
