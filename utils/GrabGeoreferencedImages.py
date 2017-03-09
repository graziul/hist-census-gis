import os
import glob
from shutil import copyfile

path = r"S:\Projects\1940Census"
cities = ["SanAntonio",
"Youngstown",
"Columbus",
"Buffalo",
"Worcester",
"Miami",
"StPaul",
"Springfield",
"KansasMO",
"Dallas",
"Denver",
"LosAngeles",
"Omaha",
"NewYork",
"Yonkers",
"Portland",
"Newark",
"Hartford",
"Minneapolis",
"Pittsburgh",
"Chicago",
"FortWorth",
"Oakland",
"Seattle",
"Memphis",
"DesMoines",
"Flint",
"Kansas",
"Paterson",
"Richmond",
"Baltimore",
"WashingtonDC",
"Indianapolis",
"Philadelphia",
"Detroit",
"Providence",
"Dayton",
"Oklahoma",
"Tulsa",
"Spokane",
"Albany",
"Nashville",
"Houston",
"SanDiego",
"SaltLake",
"Akron",
"Cleveland",
"SanFrancisco",
"Milwaukee",
"Cincinnati",
"Syracuse",
"Rochester",
"Bridgeport",
"NewOrleans",
"Toledo",
"StLouis",
"LongBeachCity",
"Atlanta",
"Jacksonville",
"Trenton",
"Birmingham",
"Louisville",
"JerseyCity"]
cities = [city for city in cities if city not in ['Omaha','SanAntonio']]

file_paths = [path+"\\"+city for city in cities]

georefed = [os.path.join(dirpath, f)
	for file_path in file_paths
    for dirpath, dirnames, files in os.walk(file_path)
    for f in files if f.endswith('.jgwx') and f.startswith('record-image')]

omaha = [os.path.join(r"S:\Projects\RA\Omaha\GIS\1930 ED Maps", f)
    for dirpath, dirnames, files in os.walk(r"S:\Projects\RA\Omaha")
    for f in files if f.endswith('.jgwx') and f.startswith('record-image')]

sanantonio = [os.path.join(r"S:\Projects\1940Census\Block Creation\San Antonio", f)
    for dirpath, dirnames, files in os.walk(r"S:\Projects\1940Census\Block Creation\San Antonio")
    for f in files if f.endswith('.jgwx')]

georefed = georefed + omaha + sanantonio

georefed_images = [i.replace("jgwx","jpg") for i in georefed]

for image in georefed_images:
	image_file = image.split("\\")[-1]
	copyfile(image,"S:\\Users\\Chris\\1930\\images\\"+image_file)