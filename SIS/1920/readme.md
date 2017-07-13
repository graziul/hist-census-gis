# 1920 #

•	Rawest raw file is in /home/s4-data/1940new/Newest1920_1930Data

•	Historically speaking that gets unzipped into:

•	Directory 1: /home/s4-data/LatestCities/1920/raw/SIS

•	Script 1: us1920c_usa_v2.do

    o	This is a slightly modified version of the script that IPUMS provides with the 
    raw 1920 data – main modifications are to “find” some variables they don’t actually 
    define in the original script, and to output a pipe-delimited version of the full file

•	Script 2: 1. Create_1920.R

    o	Reads in the output of Script 1, subsets a bunch of variables, outputs state-level 
    files, also breaks NYC out as a special case, which it is in 1920

•	Directory 2: /home/s4-data/LatestCities/SIS

•	Script 4: gen_1920_extract.R

    o	Reads in output of Script 2 and subsets cities we are interested in. Some cleanup of names. 
    Recoding and calculation of variables for the calculation of indices. Adds NYC back to main file. 
    Final output is pipe-delimited revised_1920_extract.txt. Again note that there is a manual step 
    here of entering an appropriate date for file creation (second list.of.files command).
