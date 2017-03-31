import os, sys
import pandas as pd
import paramiko
import win32api, win32con
from shutil import copyfile

#Read in raw file (saved from Google docs)
path = "S:\\Users\\Chris\\"
stgrid_csv = path + 'Street Grid Progress (1940).csv'
df = pd.read_csv(stgrid_csv)

#Create dataframe with relevant information
df1 = df.iloc[:,[7,11,12]]
df1.columns = ['citystate','map_path','map_name']
df1 = df1.dropna(axis=0,how='any').reset_index()
df1['map_path'] = df1['map_path'].apply(lambda x: x.replace("Z:\\S4\\","S:\\"))+"\\"
del df1['index']
df1['city'],df1['state'] = df1['citystate'].str.split(',', 1).str
df1['state'] = df1['state'].str.replace(' ','')
del df1['citystate']
#Save relevant information for Clean.py (i.e. the microdata cleaning algorithm)
df2 = df1[['city','state']]
df2.to_csv(path+'CityInfo_with_map.csv',index=False)


dir_path = "S:\\Projects\\1940Census\\StreetGrids\\"
def copy_rename_map_files(map_path, map_name, city, state):
	map_files = [map_path+x for x in os.listdir(map_path) if x.split('.')[0]==map_name]
	for f in map_files:
		win32api.SetFileAttributes(f,win32con.FILE_ATTRIBUTE_READONLY)
		new_file_name = city.replace(' ','')+state+"_1940_stgrid_edit"
		copyfile(f, dir_path+f.split("\\")[-1].replace(map_name,new_file_name))
	return None

t = df1.apply(lambda x: copy_rename_map_files(x['map_path'],x['map_name'],x['city'],x['state']),axis=1)
print("%s maps found" % (str(len(t))))

username = "cgraziul"
password = "Tb82k#9v!G"
#username = sys.argv[1]
#password = sys.argv[2]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys
#ssh.load_host_keys('C:\\Users\\cgraziul')
ssh.connect('rhea.pstc.brown.edu',username=username,password=password)
sftp = ssh.open_sftp()
for city, state in df2.values.tolist():
	new_file_name = city.replace(' ','')+state+"_1940_stgrid_edit"
	map_files = [x for x in os.listdir(dir_path) if x.split('.')[0]==new_file_name]
	target_path = '/home/s4-data/LatestCities/1940/stgrid/%s%s/' % (city.replace(' ',''),state)
	#Try to find directory, create it if it doesn't exist
	try:
		sftp.listdir(target_path)
	except IOError:
		sftp.mkdir(target_path)
	for item in map_files:
		file_name = '%s/%s' % (target_path, item)
		#Try to remove old file if it exist
		try: 
			sftp.remove(file_name)
		except IOError:
			pass
		sftp.put(os.path.join(dir_path, item), file_name)
city_list_file_name = '/home/s4-data/LatestCities/CityInfo_with_map.csv'
try:
	sftp.remove(city_list_file_name)
except IOError:
	pass
sftp.put(path+'CityInfo_with_map.csv',city_list_file_name)
sftp.close()
ssh.close()
