# Index Calculation (Italians) #

*	NOTE: This part is a little more complicated than the data pulls. A little backstory… originally this task 
was designed such that I (Nate) did all of the work of calculating everyone’s indices. There is one workflow, 
reflected in the now-mostly-antiquated /SIS/analysis_files/scripts directory, which operates this on this 
assumption. This was re-thought in Spring 2017, with my focus now being on outputting files for everyone that 
could function as inputs for index calculation and then I only was responsible for the indices for the 
late-arriving groups. The workflow described here is the latter, which only calculates the indices for Italians. 
That work is generalizable to other groups, but it’s up to someone else to do so. One could also go back to the 
old workflow and mine that for scripting ideas if one wished.

*	Directory: /home/s4-data/LatestCities/SIS/ital

*	Script 1: gen_all_indices_italiansgen2.R

    *	This script does a lot of things. Basically, it reads in a single year’s file (the output of one of 
    the preceding scripts described in this file), calculates the SIS, dissimilarity, and four isolation/exposure 
    indices relative to third-generation whites for each city, saves the results, and moves on to the next year. 
    Then, it mashes that all together into a “wide” file and ultimately into a “long” file that can be used to 
    make plots in ggplot2. 

*	Script 2: remove_small_pops_and_plot.R

    *	This script is used to apply the criteria we established as a group for which cities get included in the 
    analysis (currently the city must have 30,000 individuals and there must be at least 100 focal group-headed 
    households). It writes out both wide and long files containing these cities and then makes the huge facet 
    plot as a .png file using ggplot2 in R.

