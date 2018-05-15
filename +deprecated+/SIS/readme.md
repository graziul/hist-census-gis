Processing Data for SIS

Nate Frey, July 2017

SUMMARY

This document is a comprehensive guide to how the data processing steps have worked for the 1880-1940 SIS x Ethnicity Project to date. Using it, the documentation in the scripts I have run, and readme files in the relevant subdirectories, it should be possible to repeat every step of the process. 

KEY POINTS

•	Almost all of the key files are on the PSTC servers (rhea/cs1). Generally I have done all of my work on CS1 because the very largest tasks (1930-1940 raw file processing) run poorly-to-not-at-all on Rhea.  That said, in terms of files, the two servers are mirrors of one another and most tasks can be run on either. You may, however, find that you can only install certain R packages on one server at a time, and then you will have to commit to one to run many scripts.

•	The process, particularly the first few steps, isn’t standardized across years. I started with 1900 and 1910 and there is some inefficient coding in there that wouldn’t work with the later years and larger files. I would say that if you were going to standardize the process across years (which may not actually be necessary!), use the 1940 process for everything where we have standardized files from Minnesota.

•	The current best extracts of all variables we need for all cities in the SIS project are in /home/s4-data/LatestCities/SIS. They are titled “revised_YYYY_extract.txt” and are pipe-delimited (“|”) text files. 

•	Several key R packages are needed for almost everything: data.table, dplyr, dtplyr, ggplot2. There might be others, see relevant scripts. Paul might have to put some of these on the server for you, specifically the ones that have dependencies outside of R.

•	The "etc" folder contains the neighbor index code and the Hispanics code.

KNOWN PROBLEMS – GENERAL 

•	Some variables are simply missing. Some are missing entirely in certain years; others are missing in certain cities in certain years. Notably this includes: enumeration districts in certain New York cities in 1900; serial/pid for certain cities in NY and IL in 1900 and/or 1910; house numbers in 1920 (although we suspect those are in the file and just aren’t delineated properly). In general our answer to all of these things has been to say we will wait for revised versions of the files from MPC that theoretically will be cleaner and work from there.

•	We know for sure that there are issues with the way some birthplaces are coded in 1900, and maybe 1910. This caused us to give up on defining Russians and Poles in these years. In 1900 there is no mother tongue variable, and in 1910 a large proportion of foreign-born Poles and Russians give their mother tongue as English, which renders the whole variable suspect. Again, we may want to wait for new data from MPC before giving up on this, but that’s the current status quo.
