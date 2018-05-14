##This code will pull identifying information, race, birthplace, and parents' birthplace for 
##all cities in 1900. It takes a list of city-state pairs, combines it with raw state-by-state
##1900 census data files (PSV), and outputs PSVs for the cities of interest state-by-state.

##Nate Frey, last updated 7 March 2017 (cosmetic fixes July 2017)

###NOTE: THIS CODE ASSUMES YOU HAVE ALREADY RUN .DO FILES 1_ and 2_ in /home/s4-data/HCDMicro

###Begin code

##Clear out memory 
#rm(list=ls())
gc()
library(data.table)

####Begin generalized code 

##Read in the list of city-state pairs
 allcities <- fread("/home/s4-data/LatestCities/SIS/sis_cities_rev.csv")

##Initialize the big loop over all the states that have cities on the list
for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  
  filename <- paste0("/home/s4-data/HCDMicro/1900_",unique(allcities$state)[i],"_toR.txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  setkey(current.state,pid) ##set a key for data.table to make other data.table operations work properly
##subsetting procedure (deprecated, now done at an earlier step)
#  current.state <- current.state[,c("pid","self_residence_place_county","self_residence_place_city","indexed_enumeration_district","self_empty_info_race",
#                                    "self_empty_info_relationtohead", "self_birth_place_empty","father_birth_place_empty","mother_birth_place_empty",
#                                    "general_institution_fs","self_residence_place_state",
#                                    "general_page_number","general_page_letter","general_order_on_page"), with=FALSE] ##Drop some variables to save memory
##
  cities.subset <- allcities[allcities$state==unique(allcities$state)[i],] ##Cities in the state we're working with
  current.cities <- cities.subset[[1]] ##Just a vector of the city names
  rm(cities.subset)
  for (j in 1:length(current.cities)) ##Initialize loop over the cities in this state
    {
  if (j == 1) {
    state.subset <- current.state[grep(current.cities[j],current.state$self_residence_place_city),] ##create the data frame with values for one city, using grep for matches with extra words/characters   
  } 
    if (j > 1) {
    state.subset.temp <- current.state[grep(current.cities[j],current.state$self_residence_place_city),] ##Create values for another city
    state.subset <- rbind(state.subset,state.subset.temp) ##Then combine with values from the previous city
  }
    }
  state.filename.towrite <- paste0("/home/s4-data/LatestCities/1900/SIS/",unique(allcities$state)[i],"_raw_forsis.txt") ##Name the output file for all cities in state
  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1900/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
  state.subset.nodup <- state.subset[duplicated(state.subset)==FALSE,] ##Create a dataframe of non-duplicates
  if(length(state.subset$pid) == length(state.subset.nodup$pid)) { 
  print(paste0("no dups found in ",unique(allcities$state)[i])) ##If no duplicates found, print that to terminal
    fwrite(state.subset,state.filename.towrite,sep="|",quote=TRUE) ##then write out the file
  } else {
    fwrite(state.subset.nodup,state.filename.towrite.nodup,sep="|",quote=TRUE) ##If duplicates found, use the file name indicating that
  }
  rm(current.state,state.subset.temp,current.cities) 
  gc()  ##Some cleanup
  
  print(paste0("made it to ",unique(allcities$state)[i], " which is number ", i)) ##Print progress to terminal
  }

rm(list=ls()) #Remove files from memory

