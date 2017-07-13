##This script generates a 1900 extract for the segregation indices analysis
##Based on earlier scripts but last updated 10 May 2017; cosmetic updates 13 July 2017

##INPUT FILES ARE THE _forsis.txt FILES IN LATESTCITIES/1900/SIS
##OUTPUT FILE IS citiesnoannexnofalsematch1900.txt

library(data.table)
library(dplyr)
library(dtplyr)

setwd("/home/s4-data/LatestCities/1900/SIS") ##input files

list.of.files <- list.files(".",pattern="*_forsis.txt") ##use pattern to get a list of input files 
list.of.files <- list.of.files[substr(file.info(list.of.files)$mtime,1,10)=="2017-03-08" | substr(file.info(list.of.files)$mtime,1,10)=="2017-03-09"] ##Note that this needs to be changed to reflect last time raw files were run
list.of.cities <- lapply(list.of.files,fread,fill=TRUE) ##read in all the files to memory
all.cities <- rbindlist(list.of.cities) ##append them into a single df/dt
all.cities <- all.cities[!duplicated(all.cities),] remove duplicates
all.cities$citystate <- paste0(all.cities$self_residence_place_city, " ", all.cities$self_residence_place_state) make a combined city-state variable in std format
write.csv(unique(all.cities$citystate),"uniquecitystatepairs.csv") write out the list of city-state pairs

##Manually inspect that CSV output to determine which cities shouldn't be there, make a CSV of those pairs, then read it in...
false.to.rm <- fread("falsepositives.csv") ##Note that if you have messed up the manual edit format this should catch it
false.to.rm$citystate <- paste0(false.to.rm$city, " ", false.to.rm$state)
updated.cities <- all.cities[all.cities$citystate %in% false.to.rm$citystate == FALSE, ] ##eliminate false matches
fwrite(updated.cities,"citiesfalsematchesremovedv2.txt",sep="|",eol="\r\n") ##write that back out

updated.cities <- fread("citiesfalsematchesremovedv2.txt") ##read in the file you just wrote out

##This next block of code gets rid of a lot of extraneous strings and false matches
updated.cities$city_edit <- gsub(" Ward ","",ignore.case=TRUE, gsub("[0-9]", "", updated.cities$self_residence_place_city))
updated.cities$city_edit <- gsub(" Precinct ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" Assembly District ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" Wards ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" and ","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit <- gsub(" city","", gsub("[0-9]", "", updated.cities$city_edit))
updated.cities$city_edit[grepl("Richmond",updated.cities$city_edit,ignore.case=TRUE)] <- "Richmond"
updated.cities$city_edit[grepl("brooklyn",updated.cities$city_edit)] <- "Brooklyn"
updated.cities$city_edit[grepl("Wilkes Barre",updated.cities$city_edit)] <- "Wilkes-Barre"
updated.cities$city_edit[grepl("Berkely",updated.cities$city_edit)] <- "Berkeley"
updated.cities$city_edit[grepl("District",updated.cities$state)] <- "Washington"
updated.cities$city_edit[grepl("Center",updated.cities$city_edit)] <- "Indianapolis"
updated.cities$city_edit[grepl("Pigeon",updated.cities$city_edit)] <- "Evansville"
updated.cities$city_edit[grepl("Harrison",updated.cities$city_edit)] <- "Terre Haute"
updated.cities$city_edit[grepl("Wayne",updated.cities$city_edit)] <- "Fort Wayne"
updated.cities$city_edit[grepl("Julien",updated.cities$city_edit)] <- "Dubuque"
updated.cities$city_edit[grepl("Sioux",updated.cities$city_edit)] <- "Sioux City"
updated.cities$city_edit[grepl("Richmond",updated.cities$city_edit)==TRUE & grepl("York",updated.cities$state)==TRUE] <- "Staten Island"
updated.cities$city_edit[grepl("Vernon",updated.cities$city_edit)] <- "Mount Vernon"
updated.cities$city_edit[grepl("San Diego Barracks",updated.cities$city_edit)] <- "San Diego"
updated.cities$city_edit[grepl("Washington Barracks",updated.cities$city_edit)] <- "Washington"
updated.cities$city_edit[grepl("Augusta Arsenal",updated.cities$city_edit)] <- "Augusta"
updated.cities$city_edit[grepl("Louisville",updated.cities$city_edit)] <- "Louisville"
updated.cities$city_edit[grepl("Chelsea",updated.cities$city_edit)] <- "Chelsea"
updated.cities$city_edit[grepl("Springfield Armory",updated.cities$city_edit)] <- "Springfield"
updated.cities$city_edit[grepl("St Louis",updated.cities$city_edit)] <- "St Louis"
updated.cities$city_edit[grepl("Columbus Barracks",updated.cities$city_edit)] <- "Columbus"
updated.cities$city_edit[grepl("Norman",updated.cities$city_edit)] <- "Norman"
updated.cities$city_edit[grepl("York County Almshouse",updated.cities$city_edit)] <- "York"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit)] <- "Providence"
updated.cities$city_edit[grepl("Providence Rhode Island Hospital",updated.cities$city_edit)] <- "Providence"
updated.cities$city_edit[grepl("Austin State",updated.cities$city_edit)==TRUE | grepl("Austin Texas",updated.cities$city_edit)==TRUE] <- "Austin"
updated.cities$city_edit[grepl("Fort Worth",updated.cities$city_edit)] <- "Fort Worth"
updated.cities$city_edit[grepl("San Antonio",updated.cities$city_edit)] <- "San Antonio"





updated.cities.annexations <- updated.cities[(updated.cities$city_edit == "South Bend" | updated.cities$city_edit=="East St Louis" |
					      updated.cities$city_edit == "East Orange") | 
					     (grepl("North",updated.cities$city_edit) == FALSE & grepl("East",updated.cities$city_edit)==FALSE &
                                 	      grepl("South",updated.cities$city_edit) == FALSE & grepl("West",updated.cities$city_edit)==FALSE &
					      grepl("Chapel",updated.cities$city_edit) == FALSE & grepl("York Haven",updated.cities$city_edit)==FALSE &
					      grepl("Central Covington",updated.cities$city_edit) == FALSE & grepl("Lynnfield",updated.cities$city_edit)==FALSE &
					      grepl("Galveston Island",updated.cities$city_edit) == FALSE & 
					      grepl("Heights",updated.cities$city_edit) == FALSE & grepl("Port ",updated.cities$city_edit)==FALSE),]
				 

full1900 <- updated.cities.annexations
rm(updated.cities.annexations)

full1900$citystate <- paste0(full1900$city_edit,", ",full1900$self_residence_place_state)
full1900$self_residence_place_state[full1900$city_edit=="Oshkosh"] <- "Wisconsin"
full1900$self_residence_place_state[full1900$city_edit=="Spokane"] <- "Washington"
full1900$self_residence_place_state[full1900$city_edit=="Providence"] <- "Rhode Island"
full1900$self_residence_place_state[full1900$city_edit=="Pawtucket"] <- "Rhode Island"
full1900$self_residence_place_state[full1900$city_edit=="Scranton"] <- "Pennsylvania"
full1900$self_residence_place_state[substr(full1900$city_edit,1,10)=="Pittsburgh"] <- "Pennsylvania"
full1900$city_edit[substr(full1900$city_edit,1,10)=="Pittsburgh"] <- "Pittsburgh"

full1900$self_residence_place_state[substr(full1900$city_edit,1,12)=="Philadelphia"] <- "Pennsylvania"
full1900$city_edit[substr(full1900$city_edit,1,12)=="Philadelphia"] <- "Philadelphia"

full1900$self_residence_place_state[full1900$city_edit=="Chester"] <- "Pennsylvania"
full1900$self_residence_place_state[full1900$city_edit=="Allegheny"] <- "Pennsylvania"
full1900$self_residence_place_state[substr(full1900$city_edit,1,8)=="Brooklyn"] <- "New York"
full1900$city_edit[substr(full1900$city_edit,1,8)=="Brooklyn"] <- "Brooklyn"

full1900$self_residence_place_state[substr(full1900$city_edit,1,9)=="Manhattan"] <- "New York"
full1900$city_edit[substr(full1900$city_edit,1,9)=="Manhattan"] <- "Manhattan"

full1900$self_residence_place_state[full1900$city_edit=="Newark"] <- "New Jersey"
full1900$self_residence_place_state[full1900$city_edit=="Jersey City"] <- "New Jersey"
full1900$self_residence_place_state[full1900$city_edit=="Bayonne"] <- "New Jersey"
full1900$self_residence_place_state[full1900$city_edit=="Minneapolis"] <- "Minnesota"
full1900$self_residence_place_state[substr(full1900$city_edit,1,10)=="Somerville"] <- "Massachusetts"
full1900$city_edit[substr(full1900$city_edit,1,10)=="Somerville"] <- "Somerville"

full1900$self_residence_place_state[full1900$city_edit=="Holyoke"] <- "Massachusetts"
full1900$self_residence_place_state[full1900$city_edit=="Haverhill"] <- "Massachusetts"
full1900$self_residence_place_state[substr(full1900$city_edit,1,6)=="Boston"] <- "Massachusetts"
full1900$city_edit[substr(full1900$city_edit,1,6)=="Boston"] <- "Boston"

full1900$self_residence_place_state[full1900$city_edit=="Baltimore"] <- "Maryland"
full1900$self_residence_place_state[full1900$city_edit=="Louisville"] <- "Kentucky"
full1900$self_residence_place_state[full1900$city_edit=="Wichita"] <- "Kansas"
full1900$self_residence_place_state[full1900$city_edit=="Indianapolis"] <- "Indiana"
full1900$self_residence_place_state[full1900$city_edit=="Fort Wayne"] <- "Indiana"
full1900$self_residence_place_state[full1900$city_edit=="Peoria"] <- "Illinois"
full1900$self_residence_place_state[substr(full1900$city_edit,1,7)=="Chicago"] <- "Illinois"
full1900$city_edit[substr(full1900$city_edit,1,7)=="Chicago"] <- "Chicago"

full1900$self_residence_place_state[substr(full1900$city_edit,1,10)=="Washington"] <- "District of Columbia"
full1900$city_edit[substr(full1900$city_edit,1,10)=="Washington"] <- "Washington"

full1900$self_residence_place_state[full1900$city_edit=="Mobile"] <- "Alabama"
full1900$city_edit[full1900$city_edit=="St Louis" & full1900$self_residence_place_state=="Illinois"] <- "East St Louis"


full1900$citystate <- paste0(full1900$city_edit,", ",full1900$self_residence_place_state)

##full1900$citystate[full1900$citystate=="Washington, District of Columbia"] <- "Washington, DC" ##this might be causing problems downstream


full1900 <- full1900[!duplicated(full1900),]

full1900$citystate <- toupper(full1900$citystate) ##citystate var to uppercase for matching

full1900 <- full1900[full1900$citystate!="ARKANSAS CITY, KANSAS" & full1900$citystate!="BRONXVILLE, NEW YORK" &
                                full1900$citystate!="CHESTER HILL, PENNSYLVANIA" & full1900$citystate!="COHOES, NEW YORK" &  
                                full1900$citystate!="LOCKPORT, NEW YORK" & full1900$citystate!="KINGSTON, NEW YORK" &
                                full1900$citystate!="MANCHESTER, PENNSYLVANIA" & full1900$citystate!="MIAMI BEACH, FL" & 
                                full1900$citystate!="NEW BRIGHTON, NEW YORK" & full1900$citystate!="NEWBURGH, NEW YORK" & 
                                full1900$citystate!="OGDENSBURG, NEW YORK" & full1900$citystate!="OSWEGO, NEW YORK" & 
                                full1900$citystate!="ROME, NEW YORK" & full1900$citystate!="SALEMBURG, NORTH CAROLINA" & 
                                full1900$citystate!="ST PAUL PARK, MINNESOTA" & full1900$citystate!="VERNON, NEW YORK" & 
                                full1900$citystate!="WATERTOWN, NEW YORK" & full1900$citystate!="WEST CHESTER, PENNSYLVANIA" & 
                                full1900$citystate!="WEST CHICAGO, ILLINOIS" & full1900$citystate!="WEST MILWAUKEE, WISCONSIN" & 
                                full1900$citystate!="WEST MINNEAPOLIS, MINNESOTA" & full1900$citystate!="WEST PATERSON, NEW JERSEY" & 
                                full1900$citystate!="WEST READING, PENNSYLVANIA" & full1900$citystate!="WEST ST PAUL, MINNESOTA" & 
                                full1900$citystate!="WEST TAMPA, FLORIDA" & full1900$citystate!="WEST YORK, PENNSYLVANIA" & 
                                full1900$citystate!="YORK SPRINGS, PENNSYLVANIA" & full1900$citystate!="YORKANA, PENNSYLVANIA" & 
                                full1900$citystate!="INDIANAPOLIS, IOWA" & full1900$citystate!="LONG ISLAND CITY, NEW YORK" &
                                full1900$citystate!="LOS ANGELES, LOS ANGELES" & full1900$citystate!="OKLAHOMA, OKLAHOMA" &
                                full1900$citystate!="WEST LINCOLN, NEBRASKA" & full1900$citystate!="ROCHESTER, PENNSYLVANIA" &
                                full1900$citystate!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1900$citystate!="MISSING, MISSING" & full1900$citystate!="NORMAN, OKLAHOMA" &
                                full1900$citystate!="NEW YORK MILLS, NEW YORK" &
                                full1900$citystate!="CHICAGO RIDGE, ILLINOIS" & full1900$citystate!="PORTLAND, PORTLAND,"
								& full1900$citystate!="PORTLAND, ",]
full1900$citystate[full1900$citystate=="EAST ST. LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1900$citystate[full1900$citystate=="NEW YORK CITY, NEW YORK"] <- "NEW YORK, NEW YORK" 
full1900$citystate[full1900$citystate=="LACROSSE, WISCONSIN"] <- "LA CROSSE, WISCONSIN" 
full1900$citystate[full1900$citystate=="OAK PARK VILLAGE, ILLINOIS"] <- "OAK PARK, ILLINOIS" 
full1900$citystate[full1900$citystate=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, ARIZONA" 
full1900$citystate[full1900$citystate=="RICHMOND, NEW YORK"] <- "STATEN ISLAND, NEW YORK" 
full1900$citystate[full1900$citystate=="SCHENECTEDY, NEW YORK"] <- "SCHENECTADY, NEW YORK" 
full1900$citystate[full1900$citystate=="ST LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1900$citystate[full1900$citystate=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DISTRICT OF COLUMBIA"
full1900$citystate[full1900$citystate=="ST LOUIS, MISSOURI"] <- "SAINT LOUIS, MISSOURI"
full1900$citystate[full1900$citystate=="ST JOSEPH, MISSOURI"] <- "SAINT JOSEPH, MISSOURI"
full1900$citystate[full1900$citystate=="ST PAUL, MINNESOTA"] <- "SAINT PAUL, MINNESOTA"
full1900$citystate[full1900$citystate=="ALLEGHENY, PENNSYLVANIA"] <- "PITTSBURGH, PENNSYLVANIA"

full1900$citystate[full1900$citystate=="BROOKLYN, NEW YORK" | full1900$citystate=="BRONX, NEW YORK" | full1900$citystate=="QUEENS, NEW YORK" | 
					full1900$citystate=="MANHATTAN, NEW YORK" | full1900$citystate=="STATEN ISLAND, NEW YORK"] <- "NEW YORK, NEW YORK" 

full1900$citystate[full1900$citystate=="WINSTON, NORTH CAROLINA"] <- "WINSTON-SALEM, NORTH CAROLINA"
full1900$citystate[full1900$citystate=="SALEM, NORTH CAROLINA"] <- "WINSTON-SALEM, NORTH CAROLINA"

###END CITYSTATE CLEANUP CODE


##Next section generates dummy variables for segregation analyses

full1900$sisrace <- 0  ##Initialize an empty race variable
full1900$sisrace[full1900$self_empty_info_race=="White"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Arabic"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Greek"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Italian"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="American"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Syrian"] <- 1
##full1900$sisrace[full1900$self_empty_info_race=="Spanish"] <- 1 ##Note that this is commented out bc we don't code them as "white"
full1900$sisrace[full1900$self_empty_info_race=="Caucasian"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="German"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="French"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Russian"] <- 1
##full1900$sisrace[full1900$self_empty_info_race=="Latino"] <- 1 ##Same as prev comment
full1900$sisrace[full1900$self_empty_info_race=="Hebrew"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Polish"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Jewish"] <- 1
full1900$sisrace[full1900$self_empty_info_race=="Scottish"] <- 1



full1900$sisrace[full1900$self_empty_info_race=="Black"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Colored"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Negro"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Black/Colored"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Brown"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Mulatto"] <- 2
full1900$sisrace[full1900$self_empty_info_race=="Quadroon"] <- 2





full1900$sisrace[full1900$self_empty_info_race==""] <- NA ##Set blanks to NAs 

full1900$sisrace[full1900$sisrace == 0] <- 3


##This bit of code relies on something developed by previous postdocs to update the birthplaces
##to "standardized" place names based on prior work at IPUMS
name.correcter <- fread("/home/s4-data/LatestCities/SIS/Corrected_1940_Birthplaces.csv") ##read in file from prev postdocs
bpl.correcter <- rename(name.correcter,self_birth_place_empty=bp_original) ##rename some variables for merging
fbpl.correcter <- rename(name.correcter,father_birth_place_empty=bp_original)
fbpl.correcter <- rename(fbpl.correcter,fbp_final=bp_final)
mbpl.correcter <- rename(name.correcter,mother_birth_place_empty=bp_original)
mbpl.correcter <- rename(mbpl.correcter,mbp_final=bp_final)

full1900.bpl <- merge(full1900,bpl.correcter,by="self_birth_place_empty",all.x=TRUE) ##merge on each of bpl/mbpl/fbpl
full1900.mbpl <- merge(full1900.bpl,mbpl.correcter,by="mother_birth_place_empty",all.x=TRUE)
full1900.allbpl <- merge(full1900.mbpl,fbpl.correcter,by="father_birth_place_empty",all.x=TRUE)

	
states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ##list of states for determining 3rd-gen status

##More race/ethnicity dummies

full1900.allbpl$white <- 0
full1900.allbpl$white[full1900.allbpl$sisrace==1] <- 1

full1900.allbpl$black <- 0
full1900.allbpl$black[full1900.allbpl$sisrace==2] <- 1

full1900.allbpl$wnbnp <- 0 ##native born to native parents
full1900.allbpl$wnbnp[full1900.allbpl$bp_final %in% states$State & full1900.allbpl$fbp_final %in% states$State & 
		full1900.allbpl$mbp_final %in% states$State & full1900.allbpl$sisrace==1] <- 1 ##were you and both of your parents born in the US?

##Dummy for born in Germany
full1900.allbpl$german <- 0
full1900.allbpl$german[full1900.allbpl$bp_final == "GERMANY" | full1900.allbpl$bp_final == "BAVARIA" | full1900.allbpl$bp_final == "SAXONY"
		| full1900.allbpl$bp_final == "BADEN" | full1900.allbpl$bp_final == "HANOVER"] <- 1

full1900.allbpl$german2gens <- 0
full1900.allbpl$german2gens[full1900.allbpl$bp_final == "GERMANY" | full1900.allbpl$bp_final == "BAVARIA" | full1900.allbpl$bp_final == "SAXONY"
			| full1900.allbpl$bp_final == "BADEN" | full1900.allbpl$bp_final == "HANOVER"
			| full1900.allbpl$fbp_final == "GERMANY" | full1900.allbpl$fbp_final == "BAVARIA" | full1900.allbpl$fbp_final == "SAXONY"
			| full1900.allbpl$fbp_final == "BADEN" | full1900.allbpl$fbp_final == "HANOVER"
			| full1900.allbpl$mbp_final == "GERMANY" | full1900.allbpl$mbp_final == "BAVARIA" | full1900.allbpl$mbp_final == "SAXONY"
			| full1900.allbpl$mbp_final == "BADEN" | full1900.allbpl$mbp_final == "HANOVER"] <- 1

full1900.allbpl$german2gens[full1900.allbpl$mbp_final != "GERMANY" & full1900.allbpl$mbp_final != "BAVARIA" & full1900.allbpl$mbp_final != "SAXONY"
		& full1900.allbpl$mbp_final != "BADEN" & full1900.allbpl$mbp_final != "HANOVER" & full1900.allbpl$mbp_final != "EAST GERMANY, N.E.C."
		& full1900.allbpl$mbp_final != "PRUSSIA, N.E.C." & full1900.allbpl$mbp_final != "WEST PRUSSIA" &
		full1900.allbpl$bp_final != "GERMANY" & full1900.allbpl$bp_final != "BAVARIA" & full1900.allbpl$bp_final != "SAXONY"
		& full1900.allbpl$bp_final != "BADEN" & full1900.allbpl$bp_final != "HANOVER" & full1900.allbpl$bp_final != "EAST GERMANY, N.E.C."
		& full1900.allbpl$bp_final != "PRUSSIA, N.E.C." & full1900.allbpl$bp_final != "WEST PRUSSIA" & !(full1900.allbpl$mbp_final %in% states$State)
		& (full1900.allbpl$fbp_final == "GERMANY" | full1900.allbpl$fbp_final == "BAVARIA" | full1900.allbpl$fbp_final == "SAXONY"
		| full1900.allbpl$fbp_final == "BADEN" | full1900.allbpl$fbp_final == "HANOVER" | full1900.allbpl$fbp_final == "EAST GERMANY, N.E.C."
		| full1900.allbpl$fbp_final == "PRUSSIA, N.E.C." | full1900.allbpl$fbp_final == "WEST PRUSSIA")] <- 0


##Dummy for born in Britain
full1900.allbpl$british <- 0
full1900.allbpl$british[full1900.allbpl$bp_final == "ENGLAND" | full1900.allbpl$bp_final == "SCOTLAND" | full1900.allbpl$bp_final=="WALES"] <- 1

full1900.allbpl$british2gens <- 0
full1900.allbpl$british2gens[full1900.allbpl$bp_final == "ENGLAND" | full1900.allbpl$bp_final == "SCOTLAND" | full1900.allbpl$bp_final=="WALES"
			| full1900.allbpl$fbp_final == "ENGLAND" | full1900.allbpl$fbp_final == "SCOTLAND" | full1900.allbpl$fbp_final=="WALES"
			| full1900.allbpl$mbp_final == "ENGLAND" | full1900.allbpl$mbp_final == "SCOTLAND" | full1900.allbpl$mbp_final=="WALES"] <- 1
full1900.allbpl$british2gens[full1900.allbpl$mbp_final!="ENGLAND" & full1900.allbpl$mbp_final!="SCOTLAND" & full1900.allbpl$mbp_final!="WALES" 
			& !(full1900.allbpl$mbp_final %in% states$State) & full1900.allbpl$bp_final != "ENGLAND" & full1900.allbpl$bp_final!="SCOTLAND" & 
			full1900.allbpl$bp_final!="WALES" & (full1900.allbpl$fbp_final=="IRELAND" | full1900.allbpl$fbp_final=="SCOTLAND" | full1900.allbpl$fbp_final=="WALES")] <- 0




##Dummy for born in Ireland
full1900.allbpl$irish <- 0
full1900.allbpl$irish[full1900.allbpl$bp_final == "IRELAND"] <- 1

full1900.allbpl$irish2gens <- 0
full1900.allbpl$irish2gens[full1900.allbpl$bp_final == "IRELAND" | full1900.allbpl$fbp_final == "IRELAND" | full1900.allbpl$mbp_final == "IRELAND"] <- 1
full1900.allbpl$irish2gens[full1900.allbpl$mbp_final!="IRELAND" & full1900.allbpl$bp_final!="IRELAND" & !(full1900.allbpl$mbp_final %in% states$State) & full1900.allbpl$fbp_final=="IRELAND"] <- 0



##Dummy for born in Italy
full1900.allbpl$italian <- 0
full1900.allbpl$italian[full1900.allbpl$bp_final == "ITALY"] <- 1

full1900.allbpl$ital2gens <- 0
full1900.allbpl$ital2gens[full1900.allbpl$bp_final == "ITALY" | full1900.allbpl$fbp_final == "ITALY" | full1900.allbpl$mbp_final == "ITALY"] <- 1
full1900.allbpl$ital2gens[full1900.allbpl$mbp_final!="ITALY" & full1900.allbpl$bp_final!="ITALY" & !(full1900.allbpl$mbp_final %in% states$State) & full1900.allbpl$fbp_final=="ITALY"] <- 0

##Commented-out origins are not currently part of the analysis but this code should work to bring them back in if desired
# ##Dummy for born in Canada
# full1900.allbpl$canadian <- 0
# full1900.allbpl$canadian[full1900.allbpl$bp_final == "CANADA" | full1900.allbpl$bp_final == "NOVA SCOTIA" | full1900.allbpl$bp_final=="NEW BRUNSWICK" |
		   # full1900.allbpl$bp_final == "NEWFOUNDLAND" | full1900.allbpl$bp_final=="PRINCE EDWARD ISLAND" | 
		   # full1900.allbpl$bp_final == "FRENCH CANADA" | full1900.allbpl$bp_final=="ONTARIO" | full1900.allbpl$bp_final == "BRITISH COLUMBIA" | 
		   # full1900.allbpl$bp_final=="QUEBEC" | full1900.allbpl$bp_final == "CAPE BRETON" | full1900.allbpl$bp_final=="MANITOBA"] <- 1

# ##Dummy for born in Russia
# full1900.allbpl$russian <- 0
# full1900.allbpl$russian[full1900.allbpl$bp_final == "RUSSIA"] <- 1


# ##Dummy for born in Austria
# full1900.allbpl$austrian <- 0
# full1900.allbpl$austrian[full1900.allbpl$bp_final == "AUSTRIA" | full1900.allbpl$bp_final == "AUSTRIA-VIENNA"] <- 1

# ##Dummy for born in Sweden
# full1900.allbpl$swedish <- 0
# full1900.allbpl$swedish[full1900.allbpl$bp_final == "SWEDEN"] <- 1

# ##Dummy for born in Norway
# full1900.allbpl$norwegian <- 0
# full1900.allbpl$norwegian[full1900.allbpl$bp_final == "NORWAY"] <- 1

# ##Dummy for born in Hungary
# full1900.allbpl$hungarian <- 0
# full1900.allbpl$hungarian[full1900.allbpl$bp_final == "HUNGARY"] <- 1

# ##Dummy for born in Poland
# full1900.allbpl$polish <- 0
# full1900.allbpl$polish[full1900.allbpl$bp_final == "RUSSIAN POLAND" | full1900.allbpl$bp_final == "POLAND" | 
		# full1900.allbpl$bp_final == "GERMAN POLAND" | full1900.allbpl$bp_final == "AUSTRIAN POLAND" | full1900.allbpl$bp_final == "SLOVONIA"] <- 1

# #full1880$bpl == "RUSSIAN POLAND" | full1880$bpl == "POLAND" | full1880$bpl == "PRUSSIAN POLAND" |
# #		full1880$bpl == "GERMAN POLAND" | full1880$bpl == "AUSTRIAN POLAND" | full1880$bpl == "SLOVONIA"

# ##Dummy for born in France
# full1900.allbpl$french <- 0
# full1900.allbpl$french[full1900.allbpl$bp_final == "FRANCE" | full1900.allbpl$bp_final == "ALSACE"] <- 1

# ##Dummy for born in Czechoslovakia/Bohemia
# full1900.allbpl$czech <- 0
# full1900.allbpl$czech[full1900.allbpl$bp_final == "BOHEMIA" | full1900.allbpl$bp_final == "CZECHOSLOVAKIA" | full1900.allbpl$bp_final == "BOHEMIA-MORAVIA"] <- 1

# ##Dummy for born in Denmark
# full1900.allbpl$danish <- 0
# full1900.allbpl$danish[full1900.allbpl$bp_final == "DENMARK"] <- 1

# ##Dummy for born in Mexico
# full1900.allbpl$mexican <- 0
# full1900.allbpl$mexican[full1900.allbpl$bp_final == "MEXICO"] <- 1
	

fwrite(full1900.allbpl,"/home/s4-data/LatestCities/SIS/revised_1900_extract.txt",sep="|",eol="\r\n") ##write out an extract file

