###Generate 1930 extract file starting with the output of create_1930.R for SIS/seg indices project
##Last updated by Frey in May 2017, cosmetic fixes mid-July 2017

##Clear out memory 
 rm(list=ls())
 gc()
 library(data.table)
 library(dplyr)
 library(dtplyr)
setwd("/home/s4-data/LatestCities/1930/raw/SIS")


####Begin generalized code 

##Read in the list of city-state pairs
allcities <- fread("sis_cities_rev.csv",fill=TRUE) ####Use this for main list of cities



##Initialize the big loop over all the states that have cities on the list
for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  
  filename <- paste0("/home/s4-data/LatestCities/1930/raw/SIS/",unique(allcities$state)[i],"1930.txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  setkey(current.state,histid) ##set a key for data.table to make other data.table operations work properly
  cities.subset <- allcities[allcities$state==unique(allcities$state)[i],] ##Cities in the state we're working with
  current.cities <- toupper(cities.subset[[1]]) ##Just a vector of the city names
  rm(cities.subset)
  for (j in 1:length(current.cities)) ##Initialize loop over the cities in this state
    {
  if (j == 1) {
    state.subset <- current.state[grep(current.cities[j],current.state$stdcity),] ##create the data frame with values for one city, using grep for matches with extra words/characters   
  } 
    if (j > 1) {
    state.subset.temp <- current.state[grep(current.cities[j],current.state$stdcity),] ##Create values for another city
    state.subset <- rbind(state.subset,state.subset.temp) ##Then combine with values from the previous city
  }
    }
  state.filename.towrite <- paste0("/home/s4-data/LatestCities/1930/raw/SIS/",unique(allcities$state)[i],"_raw_forsis.txt") ##Name the output file for all cities in state
  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1930/raw/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
  state.subset$pid <- paste0(state.subset$serial,state.subset$pernum)
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

rm(list=ls())

##NYC as special case

allcities <- fread("addnyc.csv", fill=TRUE) ##this is just a hack to get the city name for New York into the list
for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  
  filename <- paste0("/home/s4-data/LatestCities/1930/raw/SIS/",unique(allcities$state)[i],"1930.txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  setkey(current.state,histid) ##set a key for data.table to make other data.table operations work properly
  cities.subset <- allcities[allcities$state==unique(allcities$state)[i],] ##Cities in the state we're working with
  current.cities <- toupper(cities.subset[[1]]) ##Just a vector of the city names
  rm(cities.subset)
  for (j in 1:length(current.cities)) ##Initialize loop over the cities in this state
    {
  if (j == 1) {
    state.subset <- current.state[grep(current.cities[j],current.state$stdcity),] ##create the data frame with values for one city, using grep for matches with extra words/characters   
  } 
    if (j > 1) {
    state.subset.temp <- current.state[grep(current.cities[j],current.state$stdcity),] ##Create values for another city
    state.subset <- rbind(state.subset,state.subset.temp) ##Then combine with values from the previous city
  }
    }}

##Note that your named output here is just the no-dup version of the new york file, so beware of confusion if input files change

  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1930/raw/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
  state.subset$pid <- paste0(state.subset$serial,state.subset$pernum)
  state.subset.nodup <- state.subset[duplicated(state.subset)==FALSE,] ##Create a dataframe of non-duplicates
  fwrite(state.subset.nodup,state.filename.towrite.nodup,sep="|",quote=TRUE) ##If duplicates found, use the file name indicating that
  rm(current.state,state.subset.temp,current.cities) 
  gc()  ##Some cleanup

rm(list=ls())

list.of.files <- list.files(".",pattern="*_forsis.txt")
list.of.files <- list.of.files[substr(file.info(list.of.files)$mtime,1,10)=="2017-05-11" ] ##Note that this needs to be changed to reflect last time raw files were run
list.of.cities <- lapply(list.of.files,fread,fill=TRUE)
all.cities <- rbindlist(list.of.cities)
all.cities <- all.cities[!duplicated(all.cities),]
all.cities$citystate <- paste0(all.cities$stdcity, ", ", all.cities$statefip)
write.csv(unique(all.cities$citystate),"uniquecitystatepairs.csv")

##Manually inspect that CSV output to determine which cities shouldn't be there, make a CSV of those pairs, then...
false.to.rm <- fread("falsepositives.csv") ##Note that if you have screwed up the manual edit format this should catch it
false.to.rm$citystate <- paste0(false.to.rm$city, ", ", false.to.rm$state)
updated.cities <- all.cities[all.cities$citystate %in% false.to.rm$citystate == FALSE, ]
fwrite(updated.cities,"citiesfalsematchesremoved1930.txt",sep="|",eol="\r\n")

updated.cities <- fread("citiesfalsematchesremoved1930.txt")

updated.cities$city_edit <- gsub(" Ward ","",ignore.case=TRUE, gsub("[0-9]", "", updated.cities$stdcity))
updated.cities$city_edit <- gsub(" Precinct ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" Assembly District ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" Wards ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" and ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" city","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit[grepl("Richmond",updated.cities$city_edit,ignore.case=TRUE)] <- "Richmond"
updated.cities$city_edit[grepl("brooklyn",updated.cities$city_edit,ignore.case=TRUE)] <- "Brooklyn"
updated.cities$city_edit[grepl("Wilkes Barre",updated.cities$city_edit,ignore.case=TRUE)] <- "Wilkes-Barre"
updated.cities$city_edit[grepl("Berkely",updated.cities$city_edit,ignore.case=TRUE)] <- "Berkeley"
updated.cities$city_edit[grepl("District",updated.cities$state,ignore.case=TRUE)] <- "Washington"
updated.cities$city_edit[grepl("Center",updated.cities$city_edit,ignore.case=TRUE)] <- "Indianapolis"
updated.cities$city_edit[grepl("Pigeon",updated.cities$city_edit,ignore.case=TRUE)] <- "Evansville"
updated.cities$city_edit[grepl("Harrison",updated.cities$city_edit,ignore.case=TRUE)] <- "Terre Haute"
updated.cities$city_edit[grepl("Wayne",updated.cities$city_edit,ignore.case=TRUE)] <- "Fort Wayne"
updated.cities$city_edit[grepl("Julien",updated.cities$city_edit,ignore.case=TRUE)] <- "Dubuque"
updated.cities$city_edit[grepl("Sioux",updated.cities$city_edit,ignore.case=TRUE)] <- "Sioux City"
updated.cities$city_edit[grepl("Richmond",updated.cities$city_edit,ignore.case=TRUE)==TRUE & grepl("York",updated.cities$state,ignore.case=TRUE)==TRUE] <- "Staten Island"
updated.cities$city_edit[grepl("Vernon",updated.cities$city_edit)] <- "Mount Vernon"
updated.cities$city_edit[grepl("San Diego Barracks",updated.cities$city_edit,ignore.case=TRUE)] <- "San Diego"
updated.cities$city_edit[grepl("Washington Barracks",updated.cities$city_edit,ignore.case=TRUE)] <- "Washington"
updated.cities$city_edit[grepl("Augusta Arsenal",updated.cities$city_edit,ignore.case=TRUE)] <- "Augusta"
updated.cities$city_edit[grepl("Louisville",updated.cities$city_edit,ignore.case=TRUE)] <- "Louisville"
updated.cities$city_edit[grepl("Chelsea",updated.cities$city_edit,ignore.case=TRUE)] <- "Chelsea"
updated.cities$city_edit[grepl("Springfield Armory",updated.cities$city_edit,ignore.case=TRUE)] <- "Springfield"
updated.cities$city_edit[grepl("St Louis",updated.cities$city_edit,ignore.case=TRUE)] <- "St Louis"
updated.cities$city_edit[grepl("Columbus Barracks",updated.cities$city_edit,ignore.case=TRUE)] <- "Columbus"
updated.cities$city_edit[grepl("Norman",updated.cities$city_edit,ignore.case=TRUE)] <- "Norman"
updated.cities$city_edit[grepl("York County Almshouse",updated.cities$city_edit,ignore.case=TRUE)] <- "York"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit,ignore.case=TRUE)] <- "Providence"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit,ignore.case=TRUE)] <- "Providence"
updated.cities$city_edit[grepl("Austin State",updated.cities$city_edit,ignore.case=TRUE)==TRUE | grepl("Austin Texas",updated.cities$city_edit,ignore.case=TRUE)==TRUE] <- "Austin"
updated.cities$city_edit[grepl("Fort Worth",updated.cities$city_edit,ignore.case=TRUE)] <- "Fort Worth"
updated.cities$city_edit[grepl("San Antonio",updated.cities$city_edit,ignore.case=TRUE)] <- "San Antonio"
updated.cities$city_edit[grepl("St\\. Louis",updated.cities$city_edit,ignore.case=TRUE)] <- "Saint Louis"
updated.cities$city_edit[grepl("St\\. Joseph",updated.cities$city_edit,ignore.case=TRUE)] <- "Saint Joseph"
updated.cities$city_edit[grepl("St\\. Paul",updated.cities$city_edit,ignore.case=TRUE)] <- "Saint Paul"
updated.cities <- updated.cities[grepl("NEW PHILADELPHIA",updated.cities$city_edit,ignore.case=TRUE)==FALSE] 
updated.cities <- updated.cities[grepl("CHICAGO RIDGE",updated.cities$city_edit,ignore.case=TRUE)==FALSE] 
updated.cities <- updated.cities[grepl("COLUMBUS GROVE",updated.cities$city_edit,ignore.case=TRUE)==FALSE] 


updated.cities$city_edit <- toupper(updated.cities$city_edit)




updated.cities.annexations <- updated.cities[(updated.cities$city_edit == "SOUTH BEND" | updated.cities$city_edit=="EAST ST LOUIS" |
					      updated.cities$city_edit == "EAST ORANGE") | 
					     (grepl("North",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("East",updated.cities$city_edit,ignore.case=TRUE)==FALSE &
                                 	      grepl("South",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("West",updated.cities$city_edit,ignore.case=TRUE)==FALSE &
					      grepl("Chapel",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("York Haven",updated.cities$city_edit,ignore.case=TRUE)==FALSE &
					      grepl("Central Covington",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("Lynnfield",updated.cities$city_edit,ignore.case=TRUE)==FALSE &
					      grepl("Galveston Island",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("Springs",updated.cities$city_edit,ignore.case=TRUE)==FALSE & 
					      grepl("Heights",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("Yorkana",updated.cities$city_edit,ignore.case=TRUE)==FALSE 
					      & grepl("Arkansas City",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("Port ",updated.cities$city_edit,ignore.case=TRUE)==FALSE),]
				 

updated.cities.annexations$citystate <- paste0(updated.cities.annexations$city_edit, ", ", updated.cities.annexations$statefip)

full1930 <- updated.cities.annexations ##run this line instead of the rm() statement to skip reloading the data

full1930 <- fread("citiesnoannexnofalsematch1930.txt")

###############
##I AM PRETTY SURE THIS ISN'T TRUE ANYMORE BUT AM LEAVING THE COMMENTED CODE HERE JUST IN CASE##
##Note that NYC is a special case and this code needs to be re-run on that file.
# full1930 <- fread("NewYork_raw_nd_forsis.txt") ##AGAIN NOTE THE FILE NAME HERE
###############

full1930$sisrace <- 0  ##Initialize an empty sisrace variable
full1930$sisrace[full1930$race=="White"] <- 1
#full1930$sisrace[full1930$race=="Spanish write_in"] <- 1 #check
full1930$sisrace[full1930$race=="Caucasian Hawaiian (1920)"] <- 1 #check
full1930$sisrace[full1930$race=="Portuguese"] <- 1 #check




full1930$sisrace[full1930$race=="Black/Negro"] <- 2
full1930$sisrace[full1930$race=="Mulatto"] <- 2

##Note that I am keeping "Brown/Dark/Yellow" type categories as "other"

full1930$sisrace[full1930$race==""] <- NA ##Blanks are NAs

full1930$sisrace[full1930$sisrace == 0] <- 3

fwrite(full1930,"toSIS1930racebplclean.txt",sep="|",eol="\r\n")

rm(list=ls())
gc()

full1930 <- fread("toSIS1930racebplclean.txt",integer64="character")
full1930 <- full1930[!duplicated(full1930),]


full1930$citystate[full1930$citystate=="BROOKLYN, New York"] <- "NEW YORK CITY, New York"
full1930$citystate[full1930$citystate=="BRONX, New York"] <- "NEW YORK CITY, New York"
full1930$citystate[full1930$citystate=="QUEENS, New York"] <- "NEW YORK CITY, New York"
full1930$citystate[full1930$citystate=="RICHMOND, New York"] <- "NEW YORK CITY, New York"
full1930$citystate[full1930$citystate=="STATEN ISLAND, New York"] <- "NEW YORK CITY, New York"
full1930$citystate[full1930$citystate=="MANHATTAN, New York"] <- "NEW YORK CITY, New York"


full1930$black <- 0
full1930$black[full1930$sisrace==2] <- 1
full1930$white <- 0
full1930$white[full1930$sisrace==1] <- 1

full1930$bpl <- toupper(full1930$bpl)
full1930$mbpl <- toupper(full1930$mbpl)
full1930$fbpl <- toupper(full1930$fbpl)

full1930$bpl[substr(full1930$bpl,1,10)=="OTHER USSR"] <- "RUSSIA" ##this string has gotten very garbled
full1930$bpl[substr(full1930$bpl,1,4)=="USSR"] <- "RUSSIA" 
states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ##list of states


##Dummy for the native-born to native-born parents
full1930$wnbnp <- 0 ##white native born to native parents
full1930$wnbnp[full1930$nativity=="Both parents native-born" & full1930$sisrace==1] <- 1 ##were you and both of your parents born in the US?

##Dummy for born in Germany
full1930$german <- 0
full1930$german[full1930$bpl == "GERMANY" | full1930$bpl == "BAVARIA" | full1930$bpl == "SAXONY"
		| full1930$bpl == "BADEN" | full1930$bpl == "HANOVER" | full1930$bpl == "EAST GERMANY, N.E.C."
		| full1930$bpl == "PRUSSIA, N.E.C." | full1930$bpl == "WEST PRUSSIA" ] <- 1

full1930$german2gens <- 0
full1930$german2gens[full1930$bpl == "GERMANY" | full1930$bpl == "BAVARIA" | full1930$bpl == "SAXONY"
		| full1930$bpl == "BADEN" | full1930$bpl == "HANOVER" | full1930$bpl == "EAST GERMANY, N.E.C."
		| full1930$bpl == "PRUSSIA, N.E.C." | full1930$bpl == "WEST PRUSSIA" 
		| full1930$fbpl == "GERMANY" | full1930$fbpl == "BAVARIA" | full1930$fbpl == "SAXONY"
		| full1930$fbpl == "BADEN" | full1930$fbpl == "HANOVER" | full1930$fbpl == "EAST GERMANY, N.E.C."
		| full1930$fbpl == "PRUSSIA, N.E.C." | full1930$fbpl == "WEST PRUSSIA" 
		| full1930$mbpl == "GERMANY" | full1930$mbpl == "BAVARIA" | full1930$mbpl == "SAXONY"
		| full1930$mbpl == "BADEN" | full1930$mbpl == "HANOVER" | full1930$mbpl == "EAST GERMANY, N.E.C."
		| full1930$mbpl == "PRUSSIA, N.E.C." | full1930$mbpl == "WEST PRUSSIA" ] <- 1

full1930$german2gens[full1930$mbpl != "GERMANY" & full1930$mbpl != "BAVARIA" & full1930$mbpl != "SAXONY"
		& full1930$mbpl != "BADEN" & full1930$mbpl != "HANOVER" & full1930$mbpl != "EAST GERMANY, N.E.C."
		& full1930$mbpl != "PRUSSIA, N.E.C." & full1930$mbpl != "WEST PRUSSIA" &
		full1930$bpl != "GERMANY" & full1930$bpl != "BAVARIA" & full1930$bpl != "SAXONY"
		& full1930$bpl != "BADEN" & full1930$bpl != "HANOVER" & full1930$bpl != "EAST GERMANY, N.E.C."
		& full1930$bpl != "PRUSSIA, N.E.C." & full1930$bpl != "WEST PRUSSIA" & !(full1930$mbpl %in% states$State)
		& (full1930$fbpl == "GERMANY" | full1930$fbpl == "BAVARIA" | full1930$fbpl == "SAXONY"
		| full1930$fbpl == "BADEN" | full1930$fbpl == "HANOVER" | full1930$fbpl == "EAST GERMANY, N.E.C."
		| full1930$fbpl == "PRUSSIA, N.E.C." | full1930$fbpl == "WEST PRUSSIA")] <- 0




##Dummy for born in Britain
full1930$british <- 0
full1930$british[full1930$bpl == "ENGLAND" | full1930$bpl == "SCOTLAND" | full1930$bpl=="WALES"] <- 1

full1930$british <- 0
full1930$british[full1930$bpl == "ENGLAND" | full1930$bpl == "SCOTLAND" | full1930$bpl=="WALES"] <- 1

full1930$british2gens <- 0
full1930$british2gens[full1930$bpl == "ENGLAND" | full1930$bpl == "SCOTLAND" | full1930$bpl=="WALES"
		      | full1930$fbpl == "ENGLAND" | full1930$fbpl == "SCOTLAND" | full1930$fbpl=="WALES"
		      | full1930$mbpl == "ENGLAND" | full1930$mbpl == "SCOTLAND" | full1930$mbpl=="WALES"] <- 1
full1930$british2gens[full1930$mbpl!="ENGLAND" & full1930$mbpl!="SCOTLAND" & full1930$mbpl!="WALES" 
			& !(full1930$mbpl %in% states$State) & full1930$bpl != "ENGLAND" & full1930$bpl!="SCOTLAND" & 
			full1930$bpl!="WALES" & (full1930$fbpl=="IRELAND" | full1930$fbpl=="SCOTLAND" | full1930$fbpl=="WALES")] <- 0





##Dummy for born in Ireland
full1930$irish <- 0
full1930$irish[full1930$bpl == "IRELAND"] <- 1


full1930$irish2gens <- 0
full1930$irish2gens[full1930$bpl == "IRELAND" | full1930$fbpl == "IRELAND" | full1930$mbpl == "IRELAND"] <- 1
full1930$irish2gens[full1930$mbpl!="IRELAND" & full1930$bpl!="IRELAND" & !(full1930$mbpl %in% states$State) & full1930$fbpl=="IRELAND"] <- 0


##Dummy for born in Italy
full1930$italian <- 0
full1930$italian[full1930$bpl == "ITALY"] <- 1

full1930$italian <- 0
full1930$italian[full1930$bpl == "ITALY"] <- 1
full1930$ital2gens <- 0
full1930$ital2gens[(full1930$mbpl =="ITALY" | full1930$fbpl=="ITALY" | full1930$bpl=="ITALY")] <- 1
full1930$ital2gens[full1930$mbpl!="ITALY" & full1930$bpl!="ITALY" & !(full1930$mbpl %in% states$State) & full1930$fbpl=="ITALY"] <- 0



#####Below is code to generate dummies for groups we considered analyzing but currently are not
# #Dummy for born in Canada
# full1930$canadian <- 0
# full1930$canadian[full1930$bpl == "CANADA" | full1930$bpl == "NOVA SCOTIA" | full1930$bpl=="NEW BRUNSWICK" |
		   # full1930$bpl == "NEWFOUNDLAND" | full1930$bpl=="PRINCE EDWARD ISLAND" | 
		   # full1930$bpl == "FRENCH CANADA" | full1930$bpl=="ONTARIO" | full1930$bpl == "BRITISH COLUMBIA" | 
		   # full1930$bpl=="QUEBEC" | full1930$bpl == "CAPE BRETON" | full1930$bpl=="MANITOBA"] <- 1

# #Dummy for born in Russia
# full1930$russian <- 0
# full1930$russian[full1930$bpl == "RUSSIA"] <- 1


# #Dummy for born in Austria
# full1930$austrian <- 0
# full1930$austrian[full1930$bpl == "AUSTRIA" | full1930$bp_final == "AUSTRIA-VIENNA"  
		  # | full1930$bp_final == "AUSTRIA-HUNGARY" | full1930$bp_final == "AUSTRIA-TYROL"
		  # | full1930$bp_final == "AUSTRIA-GRAZ" | full1930$bp_final == "AUSTRIA-SALZBURG"
		  # | full1930$bp_final == "AUSTRIA-KAERNTEN"] <- 1

# #Dummy for born in Sweden
# full1930$swedish <- 0
# full1930$swedish[full1930$bpl == "SWEDEN"] <- 1

# #Dummy for born in Norway
# full1930$norwegian <- 0
# full1930$norwegian[full1930$bpl == "NORWAY"] <- 1

# #Dummy for born in Hungary
# full1930$hungarian <- 0
# full1930$hungarian[full1930$bpl == "HUNGARY"] <- 1

# #Dummy for born in Poland
# full1930$polish <- 0
# full1930$polish[full1930$bpl == "RUSSIAN POLAND" | full1930$bpl == "POLAND" | 
		# full1930$bpl == "GERMAN POLAND" | full1930$bpl == "AUSTRIAN POLAND" | full1930$bpl == "SLOVONIA"] <- 1

# #Dummy for born in France
# full1930$french <- 0
# full1930$french[full1930$bpl == "FRANCE" | full1930$bpl == "ALSACE"] <- 1

# #Dummy for born in Czechoslovakia/Bohemia
# full1930$czech <- 0
# full1930$czech[full1930$bpl == "BOHEMIA" | full1930$bpl == "CZECHOSLOVAKIA" | full1930$bpl == "BOHEMIA-MORAVIA"
		# | full1930$bpl == "CZECH REPUBLIC"] <- 1

# #Dummy for born in Denmark
# full1930$danish <- 0
# full1930$danish[full1930$bpl == "DENMARK"] <- 1

# #Dummy for born in Mexico
# full1930$mexican <- 0
# full1930$mexican[full1930$bpl == "MEXICO"] <- 1

###END RACE/ETHNICITY CODE

##SOME MORE CLEANUP, POTENTIALLY NOT NECESSARY BUT BETTER SAFE THAN SORRY

full1930$citystate <- toupper(full1930$citystate)

full1930 <- full1930[full1930$citystate!="ARKANSAS CITY, KANSAS" & full1930$citystate!="BRONXVILLE, NEW YORK" &
                                full1930$citystate!="CHESTER HILL, PENNSYLVANIA" & full1930$citystate!="COHOES, NEW YORK" &  
                                full1930$citystate!="LOCKPORT, NEW YORK" & full1930$citystate!="KINGSTON, NEW YORK" &
                                full1930$citystate!="MANCHESTER, PENNSYLVANIA" & full1930$citystate!="MIAMI BEACH, FLORIDA" & 
                                full1930$citystate!="NEW BRIGHTON, NEW YORK" & full1930$citystate!="NEWBURGH, NEW YORK" & 
                                full1930$citystate!="OGDENSBURG, NEW YORK" & full1930$citystate!="OSWEGO, NEW YORK" & 
                                full1930$citystate!="ROME, NEW YORK" & full1930$citystate!="SALEMBURG, NORTH CAROLINA" & 
                                full1930$citystate!="ST PAUL PARK, MINNESOTA" & full1930$citystate!="VERNON, NEW YORK" & 
                                full1930$citystate!="WATERTOWN, NEW YORK" & full1930$citystate!="WEST CHESTER, PENNSYLVANIA" & 
                                full1930$citystate!="WEST CHICAGO, ILLINOIS" & full1930$citystate!="WEST MILWAUKEE, WISCONSIN" & 
                                full1930$citystate!="WEST MINNEAPOLIS, MINNESOTA" & full1930$citystate!="WEST PATERSON, NEW JERSEY" & 
                                full1930$citystate!="WEST READING, PENNSYLVANIA" & full1930$citystate!="WEST ST PAUL, MINNESOTA" & 
                                full1930$citystate!="WEST TAMPA, FLORIDA" & full1930$citystate!="WEST YORK, PENNSYLVANIA" & 
                                full1930$citystate!="YORK SPRINGS, PENNSYLVANIA" & full1930$citystate!="YORKANA, PENNSYLVANIA" & 
                                full1930$citystate!="INDIANAPOLIS, IOWA" & full1930$citystate!="LONG ISLAND CITY, NEW YORK" &
                                full1930$citystate!="LOS ANGELES, LOS ANGELES" & full1930$citystate!="OKLAHOMA, OKLAHOMA" &
                                full1930$citystate!="WEST LINCOLN, NEBRASKA" & full1930$citystate!="ROCHESTER, PENNSYLVANIA" &
                                full1930$citystate!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1930$citystate!="MISSING, MISSING" & full1930$citystate!="NORMAN, OKLAHOMA" &
                                full1930$citystate!="NEW YORK MILLS, NEW YORK" &
                                full1930$citystate!="CHICAGO RIDGE, ILLINOIS" & full1930$citystate!="PORTLAND, PORTLAND,"
								& full1930$citystate!="PORTLAND, ",]

 
full1930$citystate[full1930$citystate=="EAST ST. LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1930$citystate[full1930$citystate=="NEW YORK CITY, NEW YORK"] <- "NEW YORK, NEW YORK" 
full1930$citystate[full1930$citystate=="LACROSSE, WISCONSIN"] <- "LA CROSSE, WISCONSIN" 
full1930$citystate[full1930$citystate=="OAK PARK VILLAGE, ILLINOIS"] <- "OAK PARK, ILLINOIS" 
full1930$citystate[full1930$citystate=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, ARIZONA" 
full1930$citystate[full1930$citystate=="RICHMOND, NEW YORK"] <- "STATEN ISLAND, NEW YORK" 
full1930$citystate[full1930$citystate=="SCHENECTEDY, NEW YORK"] <- "SCHENECTADY, NEW YORK" 
full1930$citystate[full1930$citystate=="ST LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1930$citystate[full1930$citystate=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DISTRICT OF COLUMBIA"
full1930$citystate[full1930$citystate=="ST LOUIS, MISSOURI"] <- "SAINT LOUIS, MISSOURI"
full1930$citystate[full1930$citystate=="SAINT LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS"
full1930$citystate[full1930$citystate=="ST JOSEPH, MISSOURI"] <- "SAINT JOSEPH, MISSOURI"
full1930$citystate[full1930$citystate=="ST PAUL, MINNESOTA"] <- "SAINT PAUL, MINNESOTA"
full1930$citystate[full1930$citystate=="ALLEGHENY, PENNSYLVANIA"] <- "PITTSBURGH, PENNSYLVANIA"

full1930$citystate[full1930$citystate=="BROOKLYN, NEW YORK" | full1930$citystate=="BRONX, NEW YORK" | full1930$citystate=="QUEENS, NEW YORK" | 
					full1930$citystate=="MANHATTAN, NEW YORK" | full1930$citystate=="STATEN ISLAND, NEW YORK"] <- "NEW YORK, NEW YORK" 


full1930 <- rename(full1930,hn=us1930d_0061) ##rename house number variable
	
fwrite(full1930,"/home/s4-data/LatestCities/SIS/revised_1930_extract.txt",sep="|",eol="\r\n") ##write out pipe delimited
	
		