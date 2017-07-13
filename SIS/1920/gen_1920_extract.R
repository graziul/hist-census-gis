##This code will organize information on race, birthplace, and parents' birthplace for 
##all cities in 1920 (as well as other vars of interest), generating an extract file for index 
##calculation for the SIS/segregation indices project. 

##Nate Frey, last updated c. April 2017, cosmetic changes 13 July 2017
##Based on code for 1910/1900

###Begin code

##Clear out memory 
rm(list=ls())
gc()
library(data.table)
library(dplyr)
library(dtplyr)
setwd("/home/s4-data/LatestCities/1920/raw/SIS")

####Begin generalized code 

##Read in the list of city-state pairs

allcities <- fread("sis_cities_rev.csv",fill=TRUE) ####Use this for main list of cities


##Initialize the big loop over all the states that have cities on the list
for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  
  filename <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"1920.txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  current.state$stdcity <- gsub("\\.","",current.state$stdcity)
  setkey(current.state,ID) ##set a key for data.table to make other data.table operations work properly
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
  state.filename.towrite <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"_raw_forsis.txt") ##Name the output file for all cities in state
  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
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

##Specific 1920 NYC code (see documentation -- for various reasons NYC does not work right in 1920 if you don't do this)
nyc.1920 <- fread("NYC1920.txt")
nyc.1920$stdcity[nyc.1920$stcounty==360050] <- "BRONX"
nyc.1920$stdcity[nyc.1920$stcounty==360470] <- "BROOKLYN"
nyc.1920$stdcity[nyc.1920$stcounty==360610] <- "MANHATTAN"
nyc.1920$stdcity[nyc.1920$stcounty==360810] <- "QUEENS"
nyc.1920$stdcity[nyc.1920$stcounty==360850] <- "STATEN ISLAND"

allcities <- as.data.frame(cbind(c("BRONX","BROOKLYN","MANHATTAN","QUEENS","STATEN ISLAND"),c(rep("NYC",5))))
names(allcities) <- c("city","state")

for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  
  filename <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"1920.txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  current.state$stdcity[current.state$stcounty==360050] <- "BRONX"
  current.state$stdcity[current.state$stcounty==360470] <- "BROOKLYN"
  current.state$stdcity[current.state$stcounty==360610] <- "MANHATTAN"
  current.state$stdcity[current.state$stcounty==360810] <- "QUEENS"
  current.state$stdcity[current.state$stcounty==360850] <- "STATEN ISLAND"
  current.state$stdcity <- gsub("\\.","",current.state$stdcity)
  setkey(current.state,ID) ##set a key for data.table to make other data.table operations work properly
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
  state.filename.towrite <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"_raw_forsis.txt") ##Name the output file for all cities in state
  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1920/raw/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
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
gc()


setwd("/home/s4-data/LatestCities/1920/raw/SIS/")

list.of.files <- list.files(".",pattern="*_forsis.txt") ##list files consisting of output of previous step
list.of.files <- list.of.files[substr(file.info(list.of.files)$mtime,1,10)=="2017-03-15"] ##Note that this needs to be changed to reflect last time raw files were run
list.of.cities <- lapply(list.of.files,fread,fill=TRUE) ##read in files
all.cities <- rbindlist(list.of.cities) ##append them into a single df/dt
all.cities <- all.cities[!duplicated(all.cities),] ##remove any duplicates (not that there should be any)
all.cities$citystate <- paste0(all.cities$stdcity, " ", all.cities$statefip) ##create a standardized city-state variable
write.csv(unique(all.cities$citystate),"uniquecitystatepairs.csv") ##write out unique city-state pairs for manual inspection

##Manually inspect that CSV output to determine which cities shouldn't be there, make a CSV of those pairs, then...
false.to.rm <- fread("falsepositives.csv") ##Note that if you have messed up the manual edit format this should catch it
false.to.rm$citystate <- paste0(false.to.rm$city, " ", false.to.rm$state)
updated.cities <- all.cities[all.cities$citystate %in% false.to.rm$citystate == FALSE, ] ##get rid of false matches (if any)
fwrite(updated.cities,"citiesfalsematchesremoved1920.txt",sep="|",eol="\r\n") ##write out with false matches removed

updated.cities <- fread("citiesfalsematchesremoved1920.txt") ##read back in what you just wrote out


##This step theoretically shouldn't really be necessary for IPUMS-standardized files, but it is run to be safe
##It gets rid ofa  lot of known typos and false matches from 1900 and 1910
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
#updated.cities$city_edit[grepl("St Louis",updated.cities$city_edit,ignore.case=TRUE)] <- "St Louis"
updated.cities$city_edit[grepl("Columbus Barracks",updated.cities$city_edit,ignore.case=TRUE)] <- "Columbus"
updated.cities$city_edit[grepl("Norman",updated.cities$city_edit,ignore.case=TRUE)] <- "Norman"
updated.cities$city_edit[grepl("York County Almshouse",updated.cities$city_edit,ignore.case=TRUE)] <- "York"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit,ignore.case=TRUE)] <- "Providence"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit,ignore.case=TRUE)] <- "Providence"
updated.cities$city_edit[grepl("Austin State",updated.cities$city_edit,ignore.case=TRUE)==TRUE | grepl("Austin Texas",updated.cities$city_edit,ignore.case=TRUE)==TRUE] <- "Austin"
updated.cities$city_edit[grepl("Fort Worth",updated.cities$city_edit,ignore.case=TRUE)] <- "Fort Worth"
updated.cities$city_edit[grepl("San Antonio",updated.cities$city_edit,ignore.case=TRUE)] <- "San Antonio"
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
					      grepl("Galveston Island",updated.cities$city_edit,ignore.case=TRUE) == FALSE & 
					      grepl("Heights",updated.cities$city_edit,ignore.case=TRUE) == FALSE & grepl("Port ",updated.cities$city_edit,ignore.case=TRUE)==FALSE),]
				 
##End cleanup code

full1920 <- updated.cities.annexations ##rename (this allows bridging two sets of code that were integrated into this file)
rm(updated.cities.annexations)

##Start generating race-ethnicity variables

full1920$sisrace <- 0  ##Initialize an empty sisrace variable
full1920$sisrace[full1920$race=="White"] <- 1
full1920$sisrace[full1920$race=="Caucasian Hawaiian (1920)"] <- 1
##full1920$sisrace[full1920$race=="Spanish write_in"] <- 1



full1920$sisrace[full1920$race=="Black/Negro"] <- 2
full1920$sisrace[full1920$race=="Mulatto"] <- 2


full1920$sisrace[full1920$race==""] <- NA ##Blanks are NAs

full1920$sisrace[full1920$sisrace == 0] <- 3

full1920$white <- 0
full1920$white[full1920$sisrace==1] <- 1
full1920$black <- 0
full1920$black[full1920$sisrace==2] <- 1

##Capitalize birthplaces for easier string matching
full1920$bpl <- toupper(full1920$bpl)
full1920$mbpl <- toupper(full1920$mbpl)
full1920$fbpl <- toupper(full1920$fbpl)

full1920$bpl[substr(full1920$bpl,1,10)=="OTHER USSR"] <- "RUSSIA" ##this string is very garbled in some years
full1920$bpl[substr(full1920$bpl,1,4)=="USSR"] <- "RUSSIA" 
states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ##list of states for finding third-gen whites


##Dummy for the native-born to native-born parents
full1920$wnbnp <- 0 ##white native born to native parents
full1920$wnbnp[full1920$nativity=="Both parents native-born" & full1920$sisrace==1] <- 1 ##were you and both of your parents born in the US?

##Dummy for born in Germany
full1920$german <- 0
full1920$german[full1920$bpl == "GERMANY" | full1920$bpl == "BAVARIA" | full1920$bpl == "SAXONY"
		| full1920$bpl == "BADEN" | full1920$bpl == "HANOVER" | full1920$bpl == "EAST GERMANY, N.E.C."
		| full1920$bpl == "PRUSSIA, N.E.C." | full1920$bpl == "WEST PRUSSIA" ] <- 1
full1920$german2gens <- 0
full1920$german2gens[full1920$bpl == "GERMANY" | full1920$bpl == "BAVARIA" | full1920$bpl == "SAXONY"
		| full1920$bpl == "BADEN" | full1920$bpl == "HANOVER" | full1920$bpl == "EAST GERMANY, N.E.C."
		| full1920$bpl == "PRUSSIA, N.E.C." | full1920$bpl == "WEST PRUSSIA" 
		| full1920$fbpl == "GERMANY" | full1920$fbpl == "BAVARIA" | full1920$fbpl == "SAXONY"
		| full1920$fbpl == "BADEN" | full1920$fbpl == "HANOVER" | full1920$fbpl == "EAST GERMANY, N.E.C."
		| full1920$fbpl == "PRUSSIA, N.E.C." | full1920$fbpl == "WEST PRUSSIA" 
		| full1920$mbpl == "GERMANY" | full1920$mbpl == "BAVARIA" | full1920$mbpl == "SAXONY"
		| full1920$mbpl == "BADEN" | full1920$mbpl == "HANOVER" | full1920$mbpl == "EAST GERMANY, N.E.C."
		| full1920$mbpl == "PRUSSIA, N.E.C." | full1920$mbpl == "WEST PRUSSIA" ] <- 1

full1920$german2gens[full1920$mbpl != "GERMANY" & full1920$mbpl != "BAVARIA" & full1920$mbpl != "SAXONY"
		& full1920$mbpl != "BADEN" & full1920$mbpl != "HANOVER" & full1920$mbpl != "EAST GERMANY, N.E.C."
		& full1920$mbpl != "PRUSSIA, N.E.C." & full1920$mbpl != "WEST PRUSSIA" &
		full1920$bpl != "GERMANY" & full1920$bpl != "BAVARIA" & full1920$bpl != "SAXONY"
		& full1920$bpl != "BADEN" & full1920$bpl != "HANOVER" & full1920$bpl != "EAST GERMANY, N.E.C."
		& full1920$bpl != "PRUSSIA, N.E.C." & full1920$bpl != "WEST PRUSSIA" & !(full1920$mbpl %in% states$State)
		& (full1920$fbpl == "GERMANY" | full1920$fbpl == "BAVARIA" | full1920$fbpl == "SAXONY"
		| full1920$fbpl == "BADEN" | full1920$fbpl == "HANOVER" | full1920$fbpl == "EAST GERMANY, N.E.C."
		| full1920$fbpl == "PRUSSIA, N.E.C." | full1920$fbpl == "WEST PRUSSIA")] <- 0

##Dummy for born in Britain
full1920$british <- 0
full1920$british[full1920$bpl == "ENGLAND" | full1920$bpl == "SCOTLAND" | full1920$bpl=="WALES"] <- 1

full1920$british2gens <- 0
full1920$british2gens[full1920$bpl == "ENGLAND" | full1920$bpl == "SCOTLAND" | full1920$bpl=="WALES"
		      | full1920$fbpl == "ENGLAND" | full1920$fbpl == "SCOTLAND" | full1920$fbpl=="WALES"
		      | full1920$mbpl == "ENGLAND" | full1920$mbpl == "SCOTLAND" | full1920$mbpl=="WALES"] <- 1
full1920$british2gens[full1920$mbpl!="ENGLAND" & full1920$mbpl!="SCOTLAND" & full1920$mbpl!="WALES" 
			& !(full1920$mbpl %in% states$State) & full1920$bpl != "ENGLAND" & full1920$bpl!="SCOTLAND" & 
			full1920$bpl!="WALES" & (full1920$fbpl=="IRELAND" | full1920$fbpl=="SCOTLAND" | full1920$fbpl=="WALES")] <- 0

##Dummy for born in Ireland
full1920$irish <- 0
full1920$irish[full1920$bpl == "IRELAND"] <- 1

full1920$irish2gens <- 0
full1920$irish2gens[full1920$bpl == "IRELAND" | full1920$fbpl == "IRELAND" | full1920$mbpl == "IRELAND"] <- 1
full1920$irish2gens[full1920$mbpl!="IRELAND" & full1920$bpl!="IRELAND" & !(full1920$mbpl %in% states$State) & full1920$fbpl=="IRELAND"] <- 0


##Dummy for born in Italy
full1920$italian <- 0
full1920$italian[full1920$bpl == "ITALY"] <- 1

full1920$ital2gens <- 0
full1920$ital2gens[(full1920$mbpl =="ITALY" | full1920$fbpl=="ITALY" | full1920$bpl=="ITALY")] <- 1
full1920$ital2gens[full1920$mbpl!="ITALY" & full1920$bpl!="ITALY" & !(full1920$mbpl %in% states$State) & full1920$fbpl=="ITALY"] <- 0



##As in other years, there's a bunch of code here for groups we're not currently analyzing but considered at one point
##If you uncomment it, it should work, although it would have to be adapted to include a second generation

# ##Dummy for born in Canada
# full1920$canadian <- 0
# full1920$canadian[full1920$bpl == "CANADA" | full1920$bpl == "NOVA SCOTIA" | full1920$bpl=="NEW BRUNSWICK" |
		   # full1920$bpl == "NEWFOUNDLAND" | full1920$bpl=="PRINCE EDWARD ISLAND" | 
		   # full1920$bpl == "FRENCH CANADA" | full1920$bpl=="ONTARIO" | full1920$bpl == "BRITISH COLUMBIA" | 
		   # full1920$bpl=="QUEBEC" | full1920$bpl == "CAPE BRETON" | full1920$bpl=="MANITOBA"] <- 1

# ##Dummy for born in Russia
# full1920$russian <- 0
# full1920$russian[full1920$bpl == "RUSSIA"] <- 1


# ##Dummy for born in Austria
# full1920$austrian <- 0
# full1920$austrian[full1920$bpl == "AUSTRIA" | full1920$bp_final == "AUSTRIA-VIENNA"  
		  # | full1920$bp_final == "AUSTRIA-HUNGARY" | full1920$bp_final == "AUSTRIA-TYROL"
		  # | full1920$bp_final == "AUSTRIA-GRAZ" | full1920$bp_final == "AUSTRIA-SALZBURG"
		  # | full1920$bp_final == "AUSTRIA-KAERNTEN"] <- 1

# ##Dummy for born in Sweden
# full1920$swedish <- 0
# full1920$swedish[full1920$bpl == "SWEDEN"] <- 1

# ##Dummy for born in Norway
# full1920$norwegian <- 0
# full1920$norwegian[full1920$bpl == "NORWAY"] <- 1

# ##Dummy for born in Hungary
# full1920$hungarian <- 0
# full1920$hungarian[full1920$bpl == "HUNGARY"] <- 1

# ##Dummy for born in Poland
# full1920$polish <- 0
# full1920$polish[full1920$bpl == "RUSSIAN POLAND" | full1920$bpl == "POLAND" | 
		# full1920$bpl == "GERMAN POLAND" | full1920$bpl == "AUSTRIAN POLAND" | full1920$bpl == "SLOVONIA"] <- 1

# ##Dummy for born in France
# full1920$french <- 0
# full1920$french[full1920$bpl == "FRANCE" | full1920$bpl == "ALSACE"] <- 1

# ##Dummy for born in Czechoslovakia/Bohemia
# full1920$czech <- 0
# full1920$czech[full1920$bpl == "BOHEMIA" | full1920$bpl == "CZECHOSLOVAKIA" | full1920$bpl == "BOHEMIA-MORAVIA"
		# | full1920$bpl == "CZECH REPUBLIC"] <- 1

# ##Dummy for born in Denmark
# full1920$danish <- 0
# full1920$danish[full1920$bpl == "DENMARK"] <- 1

# ##Dummy for born in Mexico
# full1920$mexican <- 0
# full1920$mexican[full1920$bpl == "MEXICO"] <- 1


##Some additional cleanup code, maybe not necessary, but better safe than sorry?

full1920$citystate <- toupper(full1920$citystate)

full1920 <- full1920[full1920$citystate!="ARKANSAS CITY, KANSAS" & full1920$citystate!="BRONXVILLE, NEW YORK" &
                                full1920$citystate!="CHESTER HILL, PENNSYLVANIA" & full1920$citystate!="COHOES, NEW YORK" &  
                                full1920$citystate!="LOCKPORT, NEW YORK" & full1920$citystate!="KINGSTON, NEW YORK" &
                                full1920$citystate!="MANCHESTER, PENNSYLVANIA" & full1920$citystate!="MIAMI BEACH, FL" & 
                                full1920$citystate!="NEW BRIGHTON, NEW YORK" & full1920$citystate!="NEWBURGH, NEW YORK" & 
                                full1920$citystate!="OGDENSBURG, NEW YORK" & full1920$citystate!="OSWEGO, NEW YORK" & 
                                full1920$citystate!="ROME, NEW YORK" & full1920$citystate!="SALEMBURG, NORTH CAROLINA" & 
                                full1920$citystate!="ST PAUL PARK, MINNESOTA" & full1920$citystate!="VERNON, NEW YORK" & 
                                full1920$citystate!="WATERTOWN, NEW YORK" & full1920$citystate!="WEST CHESTER, PENNSYLVANIA" & 
                                full1920$citystate!="WEST CHICAGO, ILLINOIS" & full1920$citystate!="WEST MILWAUKEE, WISCONSIN" & 
                                full1920$citystate!="WEST MINNEAPOLIS, MINNESOTA" & full1920$citystate!="WEST PATERSON, NEW JERSEY" & 
                                full1920$citystate!="WEST READING, PENNSYLVANIA" & full1920$citystate!="WEST ST PAUL, MINNESOTA" & 
                                full1920$citystate!="WEST TAMPA, FLORIDA" & full1920$citystate!="WEST YORK, PENNSYLVANIA" & 
                                full1920$citystate!="YORK SPRINGS, PENNSYLVANIA" & full1920$citystate!="YORKANA, PENNSYLVANIA" & 
                                full1920$citystate!="INDIANAPOLIS, IOWA" & full1920$citystate!="LONG ISLAND CITY, NEW YORK" &
                                full1920$citystate!="LOS ANGELES, LOS ANGELES" & full1920$citystate!="OKLAHOMA, OKLAHOMA" &
                                full1920$citystate!="WEST LINCOLN, NEBRASKA" & full1920$citystate!="ROCHESTER, PENNSYLVANIA" &
                                full1920$citystate!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1920$citystate!="MISSING, MISSING" & full1920$citystate!="NORMAN, OKLAHOMA" &
                                full1920$citystate!="NEW YORK MILLS, NEW YORK" &
                                full1920$citystate!="CHICAGO RIDGE, ILLINOIS" & full1920$citystate!="PORTLAND, PORTLAND,"
								& full1920$citystate!="PORTLAND, ",]

full1920 <- full1920[full1920$citystate!="ALLEGHENY, PENNSYLVANIA",]
 
full1920$citystate[full1920$citystate=="EAST ST. LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1920$citystate[full1920$citystate=="NEW YORK CITY, NEW YORK"] <- "NEW YORK, NEW YORK" 
full1920$citystate[full1920$citystate=="LACROSSE, WISCONSIN"] <- "LA CROSSE, WISCONSIN" 
full1920$citystate[full1920$citystate=="OAK PARK VILLAGE, ILLINOIS"] <- "OAK PARK, ILLINOIS" 
full1920$citystate[full1920$citystate=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, ARIZONA" 
full1920$citystate[full1920$citystate=="RICHMOND, NEW YORK"] <- "STATEN ISLAND, NEW YORK" 
full1920$citystate[full1920$citystate=="SCHENECTEDY, NEW YORK"] <- "SCHENECTADY, NEW YORK" 
full1920$citystate[full1920$citystate=="ST LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1920$citystate[full1920$citystate=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DISTRICT OF COLUMBIA"
full1920$citystate[full1920$citystate=="ST LOUIS, MISSOURI"] <- "SAINT LOUIS, MISSOURI"
full1920$citystate[full1920$citystate=="ST JOSEPH, MISSOURI"] <- "SAINT JOSEPH, MISSOURI"
full1920$citystate[full1920$citystate=="ST PAUL, MINNESOTA"] <- "SAINT PAUL, MINNESOTA"
full1920$citystate[full1920$citystate=="ALLEGHENY, PENNSYLVANIA"] <- "PITTSBURGH, PENNSYLVANIA"

full1920$citystate[full1920$citystate=="BROOKLYN, NEW YORK" | full1920$citystate=="BRONX, NEW YORK" | full1920$citystate=="QUEENS, NEW YORK" | 
					full1920$citystate=="MANHATTAN, NEW YORK" | full1920$citystate=="STATEN ISLAND, NEW YORK"] <- "NEW YORK, NEW YORK" 


fwrite(full1920,"/home/s4-data/LatestCities/SIS/revised_1920_extract.txt",sep="|",eol="\r\n") ##write out a data extract
	
		
		