# 1940 #
*	Raw-est current file is us1940b_usa_7_11_16.zip, in /home/s4-data/LatestCities/1940/raw, which gets unzipped into:
*	Directory 1: /home/s4-data/LatestCities/1940/raw/SIS
*	Script 1: Get1940citiesSIS.sas
    *	NOTE: 1940 was the first year I came across where a mixture of R and Stata didn’t get the job done. The 
    raw file is massive (> 500 GB I believe) and the memory handling in those programs just doesn’t get the job 
    done, even on CS1. As such, this has to be done in SAS, which has much better memory management. As I alluded 
    to in the 1880 comments, this is arguably a much better way of initially pulling the city-level data, but it 
    didn’t seem like a good use of time to redo 1920 and 1930 this way once I learned that, and 1900 and 1910 
    can’t be done this way until we have cleaner files from IPUMS.
    *	This script does something somewhat different than the 1900-1930 data pull scripts; it pulls things out 
    city-by-city and generates a file for each city, rather than making a “big file” first and pulling the 
    cities from that.
    *	The only trick to running this script is that you have to feed it only a handful of cities at a time or it 
    doesn’t run. See the section with the macro toward the bottom of the script. Basically you have to plug a 
    subset of city IDs into that %m1 bit and then rerun it each time. Once you’ve made the sas7bdat files the first 
    time this is pretty quick.
    *	The output of this script is a set of pipe delimited files.
*	Script 2: gen1940fullnew.R
    *	This takes all of the output from Script 1 and turns it into a single file with all of the variables we want. 
    It also fixes some workarounds that had to be undertaken to get cities for which IPUMS doesn’t have codes in the 
    data. Output is “full1940us_update2.txt”.  
*	Directory 2: /home/s4-data/LatestCities/SIS
*	Script 3: gen_1940_extract.R
    *	Reads in the output of Script 2. Renames and recodes various variables for segregation index calculations. 
    Does some cleanup. Outputs “revised_1940_extract.txt”, a pipe-delimited text file. 
