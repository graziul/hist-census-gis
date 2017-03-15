import os
import subprocess
import arcpy

image_path = sys.argv[1] + "\\GIS_edited\\1930 ED Maps\\"
matlab_path = "C:\\Program Files\\MATLAB\\R2016b\\bin\\matlab.exe"
script_path = sys.argv[2] + "\\blocknum\\Matlab\\" 

#Convert georeferenced .jpg to GeoTIFF
print("Converting images\n")
georeferenced_images = [fn for fn in os.listdir(image_path) if fn.endswith(".jgwx")]
for fn in georeferenced_images:
	#Remove old files before conversion (or multiple copies get created)
	fn_tif = image_path+fn.replace(".jgwx",".tif")
	if os.path.isfile(fn_tif):
		os.remove(fn_tif)
		os.remove(fn_tif+".aux.xml")
		os.remove(fn_tif+".xml")
		os.remove(fn_tif+".ovr")
		os.remove(fn_tif.replace(".tif",".tfw"))
	arcpy.RasterToOtherFormat_conversion(image_path+fn.replace(".jgwx",".jpg"),image_path,"TIFF")

#Save list of GeoTIFF files
filenames = [image_path+fn.replace(".jgwx",".jpg") for fn in georeferenced_images]
list_of_images = open(image_path+'georeferenced_images.txt','w')
list_of_images.write("\n".join(filenames))
list_of_images.close()

#Invoke Matlab script
print("Images sent to Matlab\n")
command_to_add_path = "addpath('C:/Users/cgraziul/hist-census-gis/blocknum/Matlab/')"
try:
	t = subprocess.call([matlab_path,"/minimize","/nosplash","/nodesktop","/r","%s; OCRblocknums %s" % (command_to_add_path,"'"+image_path+"'")])
	if t != 0:
		cprint("Error sending images to Matlab for "+city_name, 'red', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error sending images to Matlab for "+city_name, 'red', file=AnsiToWin32(sys.stdout))
