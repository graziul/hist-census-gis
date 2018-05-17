import os
import subprocess
import arcpy
import comtypes
import psutil
import time

image_path = sys.argv[1] + "\\GIS_edited\\1930 ED Maps\\"
matlab_path = "C:\\Program Files\\MATLAB\\R2016b\\bin\\matlab.exe"
script_path = sys.argv[2] + "\\blocknum\\Matlab\\" 
arcpy.env.scratchWorkspace = image_path
arcpy.env.overwriteOutput=True

#Code to create MXD from scratch (need to add .jpg to .mxd then ExportToTIFF to get ref info)
def CreateMXD(path):
    GetModule('esriCarto.olb')
    import comtypes.gen.esriCarto as esriCarto
    pMapDocument = CreateObject(esriCarto.MapDocument, esriCarto.IMapDocument)
    pMapDocument.New(path)
#    pMapDocument.Save() #probably not required...

def GetLibPath():
    """ Get the ArcObjects library path

        It would be nice to just load the module directly instead of needing the path,
        they are registered after all... But I just don't know enough about COM to do this

    """
    compath=os.path.join(arcpy.GetInstallInfo()['InstallDir'],'com')
    return compath

def GetModule(sModuleName):
    """ Generate (if not already done) wrappers for COM modules
    """
    from comtypes.client import GetModule
    sLibPath = GetLibPath()
    GetModule(os.path.join(sLibPath,sModuleName))

def CreateObject(COMClass, COMInterface):
    """ Creates a new comtypes POINTER object where
        COMClass is the class to be instantiated,
        COMInterface is the interface to be assigned
    """
    ptr = comtypes.client.CreateObject(COMClass, interface=COMInterface)
    return ptr

#Convert georeferenced .jpg to GeoTIFF
print("Converting images\n")
georeferenced_images = [fn for fn in os.listdir(image_path) if fn.endswith(".jgwx")]
temp_mxd = 'temp.mxd'
CreateMXD(temp_mxd)
for fn in georeferenced_images:
	#Remove old files before conversion (or multiple copies get created)
	fn_tif = image_path+fn.replace(".jgwx",".tif")
	if os.path.isfile(fn_tif):
		os.remove(fn_tif)
		os.remove(fn_tif.replace(".tif",".tfw"))
	rasterFile = image_path+fn.replace(".jgwx",".jpg")
	mxd = arcpy.mapping.MapDocument(temp_mxd)
	df = arcpy.mapping.ListDataFrames(mxd)[0]
	result = arcpy.MakeRasterLayer_management(rasterFile, 'rasterLayer')
	layer = result.getOutput(0)
	arcpy.mapping.AddLayer(df, layer, 'AUTO_ARRANGE')
	size_x = arcpy.GetRasterProperties_management(rasterFile, "ROWCOUNT").getOutput(0)
	size_y = arcpy.GetRasterProperties_management(rasterFile, "COLUMNCOUNT").getOutput(0)
	arcpy.mapping.ExportToTIFF(mxd, image_path+fn.replace(".jgwx",".tif"),df,
		df_export_width=int(size_x),df_export_height=int(size_y),
		color_mode="8-BIT_GRAYSCALE",world_file=True,tiff_compression="NONE",geoTIFF_tags=True)
	del mxd
arcpy.Delete_management(arcpy.env.scratchGDB) 

#Save list of GeoTIFF files
filenames = [image_path+fn.replace(".jgwx",".tif") for fn in georeferenced_images]
list_of_images = open(image_path+'georeferenced_images.txt','w')
list_of_images.write("\n".join(filenames))
list_of_images.close()

#Invoke Matlab script
print("Images sent to Matlab\n")
command_to_add_path = "addpath('C:/Users/cgraziul/hist-census-gis/blocknum/Matlab/')"
try:
	t = subprocess.call([matlab_path,"/minimize","/nosplash","/nodesktop","/r","%s; OCRblocknums %s" % (command_to_add_path,"'"+image_path+"'")])
	for fn in filenames:
		while not os.path.exists(fn):
	   		time.sleep(1)
	if t != 0:
		cprint("Error sending images to Matlab for "+city_name, 'red', file=AnsiToWin32(sys.stdout))
except subprocess.CalledProcessError:
	cprint("Error sending images to Matlab for "+city_name, 'red', file=AnsiToWin32(sys.stdout))

#Clean up
#os.remove(image_path+'georeferenced_images.txt')