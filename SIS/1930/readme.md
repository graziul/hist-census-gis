# 1930 #

•	Rawest raw file is in /home/s4-data/1940new/Newest1920_1930Data

•	Historically speaking, that gets unzipped into: 

•	Directory 1: /home/s4-data/LatestCities/1930/raw/SIS

•	Script 1a and 1b: us1930d_usa_v2.do and us1930d_usa_v2pt2.do

    o	These are a modified version of the script provided by IPUMS with the raw data file. Generally I have had to run them in two parts because trying to run the whole thing at once leads to errors, likely due to data size. The first part builds a household file and a person file separately. The second part merges them, drops a lot of variables, and outputs a pipe-delimited text file “full1930us.txt.”
    
•	Script 2: create_1930.R

    o	Takes the output of Script 1b and breaks it out into state-level files that drop some unnecessary columns.

•	Directory 2: /home/s4-data/LatestCities/SIS

•	Script 3: gen_1930_extract.R

    o	Reads in output of Script 2 and subsets cities we are interested in. Some cleanup of names. Recoding and calculation of variables for the calculation of indices. Final output is pipe-delimited revised_1930_extract.txt
