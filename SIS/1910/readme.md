# 1910 #

•	Directory 1: /home/s4-data/LatestCities/1910/SIS

•	Input Files: /home/s4-data/LatestCities/1910/raw/     Census1910_STATE.txt

    o	Again, as in 1900, I don’t know the provenance of these files. I have a suspicion that there might be something else “rawer” floating around, but these are what I was told to use when I started this project. Variable names don’t look “raw”.

•	Script 1: DataPrep1910.R

    o	Reads in the files listed in Input Files, subsets key variables, makes some data corrections, outputs state-level files containing the cities of interest as pipe-delimited text files. (Watch out for unwanted spaces in this step, which can break subsequent steps. Manually fix file names if spaces occur, e.g. “North Dakota” -> “NorthDakota”.)

•	Directory 2: /home/s4-data/LatestCities/SIS

•	Script 2: gen_1910_extract.R

    o	Reads in text files generated by Script 1. Does variable generation for index generation, cleans up some false positives, fixes some formatting problems. Outputs pipe delimited “revised_1910_extract.txt.” Note, as with 1900, that there is a line in this that needs to be manually changed to reflect the date that the inputs were generated. This is actually a safeguard against bad files getting into the workflow, although it is annoying. 
 