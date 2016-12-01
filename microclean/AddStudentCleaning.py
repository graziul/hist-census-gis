
#
# Name:			AddStudentCleaning.py
#
# Purpose:		Integrate student cleaning into autocleaning results 
#
# Usage:		python AddStudentCleaning.py [city-state] [student file name] [autoclean version] [year]
#					
#				ex: 
#	 
#				python AddStudentCleaning.py AlbanyNY AlbanyNY_ForStudentsV1_ashley.dta 1 1930
#
# Note:			Student file MUST BE ON RHEA SERVER in the "studentcleaned" directory
#
#				ex:	"/LatestCities/1930/studentcleaned"

import os, sys, subprocess
import unicodecsv as csv
import pandas as pd
import numpy as np

csv.field_size_limit(sys.maxsize)

file_path = '/home/s4-data/LatestCities' 

city_info_file = file_path + '/CityInfo.csv' 
city_info_df = pd.read_csv(city_info_file)
city_info_list = city_info_df.values.tolist()


city = sys.argv[1]
student_file = sys.argv[2]
version = sys.argv[3]
year = sys.argv[4]

'''
city = "AlbanyNY"
student_file = "AlbanyNY_ForStudentsV1_ashley.dta"
version = 1
year = 1930
'''

studentcleaned_file_name = file_path + '/%s/studentcleaned/%s' % (str(year),student_file)
autocleaned_file_name = file_path + '/%s/autocleaned/V%s/%s_AutoCleanedV%s.csv' % (str(year),str(version),city,str(version))

sc = pd.read_stata(studentcleaned_file_name)
ac = pd.read_csv(autocleaned_file_name,low_memory=False)

if int(version) == 1:
	sc_formerge = sc.drop(sc.columns[[0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,17]], axis=1)
	mc = ac.merge(sc_formerge,on=['image_id','line_num'],indicator=True)

if len(mc) != sum(mc['_merge'] == 'both'):
	print('Merge error')
del mc['_merge']

def find_best_street(overall_match,st_edit,checked_st,clean_priority):
	if overall_match != '':
		return overall_match
	if (checked_st != 'c, ambiguous') & (~np.isnan(clean_priority) != ''):
		return st_edit
	else:
		return ''

mc['autostud_street'] = mc['overall_match']
mc.loc[(mc['checked_st'] != 'c, ambiguous') & (mc['checked_st'] != '') & (~np.isnan(mc['clean_priority'])),'autostud_street'] = mc['st_edit']

mc = mc.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('', '.')

autostud_file_name = file_path + '/%s/%s' % (str(year),city + '_StudAuto.csv')
mc.to_csv(autostud_file_name)

autostud_file_stata = file_path + '/%s/%s' % (str(year),city + '_StudAuto.dta')

## Set do-file information
dofile = file_path + "/ConvertCsvToDta.do"
cmd = ["stata","-b","do", dofile, autostud_file_name, autostud_file_stata,"&"]
## Run do-file
subprocess.call(cmd) 

os.remove(autostud_file_name)