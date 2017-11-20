from operator import itemgetter
from itertools import groupby
import pandas as pd
import pysal as ps
import pickle

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


seq_dict = pickle.load(open('C:/Users/cgraziul/Documents/StLouis_consec.p','rb'))
df = dbf2DF("S:/Projects/1940Census/StLouis/GIS_edited/StLouisMO_1930_stgrid_edit_Uns2.dbf")

df_grouped = df.groupby['FULLNAME']
for name, group in df_grouped:
	#Do stuff

#Single element of for loop
name = 'Wyoming St'
group = df[df['FULLNAME']==name]
grid_id_list = seq_dict[name]
grid_id_dict = {grid_id_list[i]:i for i in range(len(grid_id_list))}
df_dict = pd.DataFrame(grid_id_dict.items(),columns=['grid_id','order'])
group = group.merge(df_dict, on='grid_id')
group = group.sort_values(['order'])

#Recursive function for filling in blanks on each side of street independently

#Do each side separately
#Create list of blank sequences
list_order = list(group['order'].values)
hn_ranges = ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD']
#Get blanks
blanks_dict = {hn:list(group.loc[group[hn]=='','order'].values) for hn in hn_ranges}
#Fix blanks

hn_ranges = ['MIN_LFROMA','MAX_LTOADD','MIN_RFROMA','MAX_RTOADD']

def fix_blanks(group, hn_ranges, blanks_dict):

	def get_ids(side):
		ranges = []
		data = blanks_dict[side]
		for k, g in groupby(enumerate(data), lambda (i,x): i-x):
			ranges.append(map(itemgetter(1), g))
		return ranges

	def get_value(id_val, var):
		try:
			return int(group.loc[group['order']==id_val,var].values[0])
		except:
			return None

	min_l, max_l, min_r, max_r = hn_ranges

	ranges_min_l = get_ids(min_l)
	ranges_max_l = get_ids(max_l)

	ranges_min_r = get_ids(min_r)
	ranges_max_r = get_ids(max_r)

	# Do something only if blanks are the same for left and right min/max:
	ranges_min = ranges_min_l
	ranges_max = ranges_max_l

	if ranges_min == ranges_max:
		for seq in ranges:
			# Select a sequence
			seq = ranges[0]
			# Get the start and end of the sequence
			max_id = max(seq)
			min_id = min(seq)
			# Get starting and ending house numbers based on available data	
			start = get_value(min_id-1, max_side)
			end = get_value(max_id+1, min_side)
			# If no house number before or after sequence, do nothing
			if start is None or end is None:
				group = group
			# Otherwise, break up by range number of segments and assign values
			else:
				num_segs = len(seq)
				if num_segs == 1:
					group.loc[group['order']==seq[0],min_l] = start+2
					group.loc[group['order']==seq[0],max_l] = end-2
				else:



seq = blanks_dict.values()[0]
group.loc[group['order']==seq,side[0]], group.loc[side[1]] 

#Create list of trios based on order 
def make_trios(id_list):
	trio_list = []
	for i in id_list:
		try:
			trio_list.append([id_list[i], id_list[i+1], id_list[i+2]])
		except:
			pass
	return trio_list
trios = make_trios(list(group['order'].values))




def check_trio(trio_ids, df_group):
	t1 = df_group[df_group['order']==trio_ids[0]]
	t2 = df_group[df_group['order']==trio_ids[1]] 
	t3 = df_group[df_group['order']==trio_ids[2]]

	blank_range = []
	for hn in hn_ranges:
		if t2[hn] == ' ':
			blank_range.append(hn) 

	return blank_range


for t in trios:


lf = group['LFROMADD'].tolist()
lt = group['LTOADD'].tolist()

rf = group['RFROMADD'].tolist()
rt = group['RTOADD'].tolist()


lf_d = {i:lf[i] for i in range(len(lf))}
def count_dist(a,b):
	try:
		a = int(a)
		b = int(b)
		return b-a
	except:
		return 0

lf_dist = sum([count_dist(lf_d[i],lf_d[i+1]) for i in range(len(lf_d)-1)])/len(lf_d)



zip(lf,rf)
zip(lt,rt)
