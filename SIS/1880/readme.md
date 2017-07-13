# 1880 #

•	Directory: /home/s4-data/LatestCities/1880/SIS

•	Input Files: Contents of “1880raw_2016.zip” (newest 1880 files from 2016)

•	Script 1: Get1880_frey.sas

    o	Extracts cities of interest to us from the full 1880 files
  
    o	Note that the %savecities part of the macro sometimes breaks and if that 
    happens you need to run less cities at once.

•	Script 2: make1880fullfile.do

    o	Mashes all of the city .dta files together and outputs a pipe-delimited full1880.txt 
    file.

•	Switch directories: /home/s4-data/LatestCities/SIS

•	Script 3: gen_1880_extract.R

    o	Takes full1880.txt and generates all of the variables that are calculated from the raw data 
    and does some other formatting/cleanup
  
    o	Output is revised_1880_extract.txt, a pipe-delimited file. This is the working file for this 
    year for all of the index calculations
 
