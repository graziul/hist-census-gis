#
# Name: IOutils.py
#
# Content: Functions involving various IO operations
#

import pandas as pd
import geopandas as gpd
import csv
import xlrd
import os

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

	# Convert objects to categories to save memory
	for col in df.columns:
		# Downcast int 
		if df[col].dtype == 'int':
			df.loc[:,col] = df[col].apply(pd.to_numeric,downcast='signed')
		# Downcast float 
		if df[col].dtype == 'float':
			df.loc[:,col] = df[col].apply(pd.to_numeric,downcast='float')
	
	return df

# Function to reads in DBF files and return Pandas DF
def load_shp(filename, ranges=None):
	
	# Remove None function
	def remove_none(df, ranges):
		if ranges == None:
			return df
		else:
			mask = df.applymap(lambda x: x is None)
			cols = df.columns[(mask).any()]
			for col in df[cols]:
				if df[col].dtype == 'O':
					df.loc[mask[col], col] = ''
					if col in ranges:
						df[col] = df[col].apply(lambda x: '' if '-' in x else x).str.replace(r'[aA-zZ]+','').replace('','0').astype(int)
			return df

	filename = filename.replace('.dbf','.shp')
	if ranges is not None:
		temp_df = remove_none(gpd.read_file(filename), ranges)
	else:
		temp_df = gpd.read_file(filename)

	return temp_df

# Function to save Pandas DF as DBF file 
def save_shp(df, shapefile_name):
	df.to_file(filename=shapefile_name, encoding='utf-8', driver='ESRI Shapefile')

# Function to convert Excel to .csv
def csv_from_excel(excel_file, csv_name):
	workbook = xlrd.open_workbook(excel_file)
	all_worksheets = workbook.sheet_names()
	for i,worksheet_name in enumerate(all_worksheets[0:2]) : #Use only first two worksheets
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

def rename_raw(decade, file_path='/home/s4-data/LatestCities', city_extract_csv='CityExtractionList.csv'):
	df = pd.read_csv(file_path + '/' + city_extract_csv)
	df_extract = df[df['Status']>0]
	temp_dict = df_extract[['Code','City']].set_index('Code').to_dict('dict')['City']
	city_extract_dict = {str(k):v.replace(' ','').replace(',','') for k,v in temp_dict.items()}
	for code, city in city_extract_dict.items():
		old_file = '%s/%s/%sdta.dta' % (file_path, str(decade), code)
		new_file = '%s/%s/%s.dta' % (file_path, str(decade), city)
		os.rename(old_file, new_file)

#
# DEPRECATED 
#

'''
#Function to reads in DBF files and return Pandas DF
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
def save_dbf(df, shapefile_name):
	dir_temp = '/'.join(shapefile_name.split('/')[:-1])
	file_temp = shapefile_name.split('/')[-1]
	csv_file = dir_temp + "/temp_for_dbf.csv"
	df.to_csv(csv_file,index=False)
	try:
		os.remove(dir_temp + "/schema.ini")
	except:
		pass
	arcpy.TableToTable_conversion(in_rows=csv_file, out_path=dir_temp, out_name="temp_for_shp.dbf")
	os.remove(shapefile_name.replace('.shp','.dbf'))
	os.remove(csv_file)
	os.rename(dir_temp+"/temp_for_shp.dbf",shapefile_name.replace('.shp','.dbf'))
	os.remove(dir_temp+"/temp_for_shp.dbf.xml")
	os.remove(dir_temp+"/temp_for_shp.cpg")
'''