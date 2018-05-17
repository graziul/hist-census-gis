##This script uses the output of DataPrep1910.R to generate a full 1910 extract for all cities for the segregation
##indices project. 
##Frey, Last updated 30 May 2017; cosmetic updates 13 July 2017

library(data.table)
library(dplyr)
library(dtplyr)

setwd("/home/s4-data/LatestCities/1910/SIS") 
list.of.files <- list.files(".",pattern="*_forsis.txt") ##get list of files to read in from previous step
list.of.files <- list.of.files[substr(file.info(list.of.files)$mtime,1,10)=="2017-04-12"] ##Note that this needs to be changed to reflect last time raw files were run
list.of.cities <- lapply(list.of.files,fread,fill=TRUE) ##read all state-files in at once
all.cities <- rbindlist(list.of.cities) ##append them to one another
all.cities <- all.cities[!duplicated(all.cities),] ##remove duplicates
all.cities$citystate <- paste0(all.cities$ResidenceCity, " ", all.cities$state) ##create a standard format city-state variable
write.csv(unique(all.cities$citystate),"uniquecitystatepairs.csv") ##write out the list of city-state pairs to manually inspect

##Read back in your manual fixes, if any
false.to.rm <- fread("falsepositives.csv") ##Note that if you have screwed up the manual edit format this should catch it
false.to.rm$citystate <- paste0(false.to.rm$city, " ", false.to.rm$state)

##Lot of name cleanup
updated.cities <- all.cities[all.cities$citystate %in% false.to.rm$citystate == FALSE, ]
updated.cities$city_edit <- gsub(" Ward ","",ignore.case=TRUE, gsub("[0-9]", "", updated.cities$ResidenceCity))
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

						  
full1910 <- updated.cities.annexations
rm(updated.cities.annexations)
full1910$citystate <- paste0(full1910$city_edit,", ",full1910$state)




full1910$citystate[full1910$citystate=="Brooklyn, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Bronx, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Queens, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Richmond, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Staten Island, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Manhattan, New York"] <- "New York, New York"
full1910$citystate[full1910$citystate=="Winston, North Carolina"] <- "Winston-Salem, North Carolina"
full1910$citystate[full1910$citystate=="Salem, North Carolina"] <- "Winston-Salem, North Carolina"



full1910 <- full1910[!duplicated(full1910),]

full1910$citystate <- toupper(full1910$citystate)

full1910 <- full1910[full1910$citystate!="ARKANSAS CITY, KANSAS" & full1910$citystate!="BRONXVILLE, NEW YORK" &
                                full1910$citystate!="CHESTER HILL, PENNSYLVANIA" & full1910$citystate!="COHOES, NEW YORK" &  
                                full1910$citystate!="LOCKPORT, NEW YORK" & full1910$citystate!="KINGSTON, NEW YORK" &
                                full1910$citystate!="MANCHESTER, PENNSYLVANIA" & full1910$citystate!="MIAMI BEACH, FL" & 
                                full1910$citystate!="NEW BRIGHTON, NEW YORK" & full1910$citystate!="NEWBURGH, NEW YORK" & 
                                full1910$citystate!="OGDENSBURG, NEW YORK" & full1910$citystate!="OSWEGO, NEW YORK" & 
                                full1910$citystate!="ROME, NEW YORK" & full1910$citystate!="SALEMBURG, NORTH CAROLINA" & 
                                full1910$citystate!="ST PAUL PARK, MINNESOTA" & full1910$citystate!="VERNON, NEW YORK" & 
                                full1910$citystate!="WATERTOWN, NEW YORK" & full1910$citystate!="WEST CHESTER, PENNSYLVANIA" & 
                                full1910$citystate!="WEST CHICAGO, ILLINOIS" & full1910$citystate!="WEST MILWAUKEE, WISCONSIN" & 
                                full1910$citystate!="WEST MINNEAPOLIS, MINNESOTA" & full1910$citystate!="WEST PATERSON, NEW JERSEY" & 
                                full1910$citystate!="WEST READING, PENNSYLVANIA" & full1910$citystate!="WEST ST PAUL, MINNESOTA" & 
                                full1910$citystate!="WEST TAMPA, FLORIDA" & full1910$citystate!="WEST YORK, PENNSYLVANIA" & 
                                full1910$citystate!="YORK SPRINGS, PENNSYLVANIA" & full1910$citystate!="YORKANA, PENNSYLVANIA" & 
                                full1910$citystate!="INDIANAPOLIS, IOWA" & full1910$citystate!="LONG ISLAND CITY, NEW YORK" &
                                full1910$citystate!="LOS ANGELES, LOS ANGELES" & full1910$citystate!="OKLAHOMA, OKLAHOMA" &
                                full1910$citystate!="WEST LINCOLN, NEBRASKA" & full1910$citystate!="ROCHESTER, PENNSYLVANIA" &
                                full1910$citystate!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1910$citystate!="MISSING, MISSING" & full1910$citystate!="NORMAN, OKLAHOMA" &
                                full1910$citystate!="NEW YORK MILLS, NEW YORK" &
                                full1910$citystate!="CHICAGO RIDGE, ILLINOIS" & full1910$citystate!="PORTLAND, PORTLAND,"
								& full1910$citystate!="PORTLAND, ",]

full1910 <- full1910[full1910$citystate!="ALLEGHENY, PENNSYLVANIA",]
 
full1910$citystate[full1910$citystate=="EAST ST. LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1910$citystate[full1910$citystate=="NEW YORK CITY, NEW YORK"] <- "NEW YORK, NEW YORK" 
full1910$citystate[full1910$citystate=="LACROSSE, WISCONSIN"] <- "LA CROSSE, WISCONSIN" 
full1910$citystate[full1910$citystate=="OAK PARK VILLAGE, ILLINOIS"] <- "OAK PARK, ILLINOIS" 
full1910$citystate[full1910$citystate=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, ARIZONA" 
full1910$citystate[full1910$citystate=="RICHMOND, NEW YORK"] <- "STATEN ISLAND, NEW YORK" 
full1910$citystate[full1910$citystate=="SCHENECTEDY, NEW YORK"] <- "SCHENECTADY, NEW YORK" 
full1910$citystate[full1910$citystate=="ST LOUIS, ILLINOIS"] <- "EAST ST LOUIS, ILLINOIS" 
full1910$citystate[full1910$citystate=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DISTRICT OF COLUMBIA"
full1910$citystate[full1910$citystate=="ST LOUIS, MISSOURI"] <- "SAINT LOUIS, MISSOURI"
full1910$citystate[full1910$citystate=="ST JOSEPH, MISSOURI"] <- "SAINT JOSEPH, MISSOURI"
full1910$citystate[full1910$citystate=="ST PAUL, MINNESOTA"] <- "SAINT PAUL, MINNESOTA"
full1910$citystate[full1910$citystate=="ALLEGHENY, PENNSYLVANIA"] <- "PITTSBURGH, PENNSYLVANIA"

full1910$citystate[full1910$citystate=="BROOKLYN, NEW YORK" | full1910$citystate=="BRONX, NEW YORK" | full1910$citystate=="QUEENS, NEW YORK" | 
					full1910$citystate=="MANHATTAN, NEW YORK" | full1910$citystate=="STATEN ISLAND, NEW YORK"] <- "NEW YORK, NEW YORK" 

###END NAME CLEANUP

##BEGIN RACE/ETHNICITY VARIABLE GENERATION
					
full1910$sisrace <- 0  ##Initialize an empty sisrace variable
full1910$sisrace[full1910$Race=="White"] <- 1
full1910$sisrace[full1910$Race=="French"] <- 1 
full1910$sisrace[full1910$Race=="German"] <- 1 
full1910$sisrace[full1910$Race=="Greek"] <- 1 
full1910$sisrace[full1910$Race=="Arabic"] <- 1 
full1910$sisrace[full1910$Race=="Aust"] <- 1
full1910$sisrace[full1910$Race=="Caucasian"] <- 1
full1910$sisrace[full1910$Race=="Finnish"] <- 1
full1910$sisrace[full1910$Race=="Italian"] <- 1
full1910$sisrace[full1910$Race=="Jewish"] <- 1
full1910$sisrace[full1910$Race=="Polish"] <- 1
full1910$sisrace[full1910$Race=="Portuguese"] <- 1
full1910$sisrace[full1910$Race=="Potg"] <- 1
full1910$sisrace[full1910$Race=="Russian"] <- 1
full1910$sisrace[full1910$Race=="Spanish"] <- 1
full1910$sisrace[full1910$Race=="Swies"] <- 1
full1910$sisrace[full1910$Race=="Syri"] <- 1
full1910$sisrace[full1910$Race=="Syrian"] <- 1
full1910$sisrace[full1910$Race=="Turk"] <- 1
full1910$sisrace[full1910$Race=="Turkish"] <- 1
full1910$sisrace[full1910$Race=="Puerto Rican"] <- 1
full1910$sisrace[full1910$Race=="Uk"] <- 1
full1910$sisrace[full1910$Race=="White;Mexican"] <- 1

full1910$sisrace[full1910$Race=="Black"] <- 2
full1910$sisrace[full1910$Race=="Colored"] <- 2
full1910$sisrace[full1910$Race=="Negro"] <- 2
full1910$sisrace[full1910$Race=="Black/Colored"] <- 2
full1910$sisrace[full1910$Race=="Bl"] <- 2
full1910$sisrace[full1910$Race=="B??"] <- 2
full1910$sisrace[full1910$Race=="Brown"] <- 2
full1910$sisrace[full1910$Race=="Creole"] <- 2
full1910$sisrace[full1910$Race=="Dark"] <- 2
full1910$sisrace[full1910$Race=="Octoroon"] <- 2
full1910$sisrace[full1910$Race=="Quadroon"] <- 2
full1910$sisrace[full1910$Race=="Mulatto"] <- 2




##Note that I am keeping "Brown/Dark/Yellow" type categories as "other"

full1910$sisrace[full1910$Race==""] <- NA ##Blanks are NAs

full1910$sisrace[full1910$sisrace == 0] <- 3

full1910$white <- 0
full1910$white[full1910$sisrace==1] <- 1
full1910$black <- 0
full1910$black[full1910$sisrace==2] <- 1

##This bit of code corrects unstandardized birthplaces to standardized ones based on work by prior postdocs & IPUMS
name.correcter <- fread("/home/s4-data/LatestCities/SIS/Corrected_1940_Birthplaces.csv") ##Read in name corrections file

bpl.correcter <- rename(name.correcter,BirthPlace=bp_original) ##rename some variables for merges
fbpl.correcter <- rename(name.correcter,FatherBirthPlace=bp_original)
fbpl.correcter <- rename(fbpl.correcter,fbp_final=bp_final)
mbpl.correcter <- rename(name.correcter,MotherBirthPlace=bp_original)
mbpl.correcter <- rename(mbpl.correcter,mbp_final=bp_final)

full1910.bpl <- merge(full1910,bpl.correcter,by="BirthPlace",all.x=TRUE) ##merge three times to get corrected names
full1910.mbpl <- merge(full1910.bpl,mbpl.correcter,by="MotherBirthPlace",all.x=TRUE)
full1910.allbpl <- merge(full1910.mbpl,fbpl.correcter,by="FatherBirthPlace",all.x=TRUE)


states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ##list of states for third-gen identification

##Dummy for the native-born to native-born parents
full1910.allbpl$wnbnp <- 0 ##native born to native parents
full1910.allbpl$wnbnp[full1910.allbpl$bp_final %in% states$State & full1910.allbpl$fbp_final %in% states$State & 
		full1910.allbpl$mbp_final %in% states$State & full1910.allbpl$sisrace==1] <- 1 ##were you and both of your parents born in the US?

##Dummy for born in Germany
full1910.allbpl$german <- 0
full1910.allbpl$german[full1910.allbpl$bp_final == "GERMANY" | full1910.allbpl$bp_final == "BAVARIA" | full1910.allbpl$bp_final == "SAXONY"
		| full1910.allbpl$bp_final == "BADEN" | full1910.allbpl$bp_final == "HANOVER"] <- 1

full1910.allbpl$german2gens <- 0
full1910.allbpl$german2gens[full1910.allbpl$bp_final == "GERMANY" | full1910.allbpl$bp_final == "BAVARIA" | full1910.allbpl$bp_final == "SAXONY"
			| full1910.allbpl$bp_final == "BADEN" | full1910.allbpl$bp_final == "HANOVER"
			| full1910.allbpl$fbp_final == "GERMANY" | full1910.allbpl$fbp_final == "BAVARIA" | full1910.allbpl$fbp_final == "SAXONY"
			| full1910.allbpl$fbp_final == "BADEN" | full1910.allbpl$fbp_final == "HANOVER"
			| full1910.allbpl$mbp_final == "GERMANY" | full1910.allbpl$mbp_final == "BAVARIA" | full1910.allbpl$mbp_final == "SAXONY"
			| full1910.allbpl$mbp_final == "BADEN" | full1910.allbpl$mbp_final == "HANOVER"] <- 1

full1910.allbpl$german2gens[full1910.allbpl$mbp_final != "GERMANY" & full1910.allbpl$mbp_final != "BAVARIA" & full1910.allbpl$mbp_final != "SAXONY"
		& full1910.allbpl$mbp_final != "BADEN" & full1910.allbpl$mbp_final != "HANOVER" & full1910.allbpl$mbp_final != "EAST GERMANY, N.E.C."
		& full1910.allbpl$mbp_final != "PRUSSIA, N.E.C." & full1910.allbpl$mbp_final != "WEST PRUSSIA" &
		full1910.allbpl$bp_final != "GERMANY" & full1910.allbpl$bp_final != "BAVARIA" & full1910.allbpl$bp_final != "SAXONY"
		& full1910.allbpl$bp_final != "BADEN" & full1910.allbpl$bp_final != "HANOVER" & full1910.allbpl$bp_final != "EAST GERMANY, N.E.C."
		& full1910.allbpl$bp_final != "PRUSSIA, N.E.C." & full1910.allbpl$bp_final != "WEST PRUSSIA" & !(full1910.allbpl$mbp_final %in% states$State)
		& (full1910.allbpl$fbp_final == "GERMANY" | full1910.allbpl$fbp_final == "BAVARIA" | full1910.allbpl$fbp_final == "SAXONY"
		| full1910.allbpl$fbp_final == "BADEN" | full1910.allbpl$fbp_final == "HANOVER" | full1910.allbpl$fbp_final == "EAST GERMANY, N.E.C."
		| full1910.allbpl$fbp_final == "PRUSSIA, N.E.C." | full1910.allbpl$fbp_final == "WEST PRUSSIA")] <- 0

##Dummy for born in Britain
full1910.allbpl$british <- 0
full1910.allbpl$british[full1910.allbpl$bp_final == "ENGLAND" | full1910.allbpl$bp_final == "SCOTLAND" | full1910.allbpl$bp_final=="WALES"] <- 1

full1910.allbpl$british2gens <- 0
full1910.allbpl$british2gens[full1910.allbpl$bp_final == "ENGLAND" | full1910.allbpl$bp_final == "SCOTLAND" | full1910.allbpl$bp_final=="WALES"
			| full1910.allbpl$fbp_final == "ENGLAND" | full1910.allbpl$fbp_final == "SCOTLAND" | full1910.allbpl$fbp_final=="WALES"
			| full1910.allbpl$mbp_final == "ENGLAND" | full1910.allbpl$mbp_final == "SCOTLAND" | full1910.allbpl$mbp_final=="WALES"] <- 1
full1910.allbpl$british2gens[full1910.allbpl$mbp_final!="ENGLAND" & full1910.allbpl$mbp_final!="SCOTLAND" & full1910.allbpl$mbp_final!="WALES" 
			& !(full1910.allbpl$mbp_final %in% states$State) & full1910.allbpl$bp_final != "ENGLAND" & full1910.allbpl$bp_final!="SCOTLAND" & 
			full1910.allbpl$bp_final!="WALES" & (full1910.allbpl$fbp_final=="IRELAND" | full1910.allbpl$fbp_final=="SCOTLAND" | full1910.allbpl$fbp_final=="WALES")] <- 0


##Dummy for born in Ireland
full1910.allbpl$irish <- 0
full1910.allbpl$irish[full1910.allbpl$bp_final == "IRELAND"] <- 1

full1910.allbpl$irish2gens <- 0
full1910.allbpl$irish2gens[full1910.allbpl$bp_final == "IRELAND" | full1910.allbpl$fbp_final == "IRELAND" | full1910.allbpl$mbp_final == "IRELAND"] <- 1
full1910.allbpl$irish2gens[full1910.allbpl$mbp_final!="IRELAND" & full1910.allbpl$bp_final!="IRELAND" & !(full1910.allbpl$mbp_final %in% states$State) & full1910.allbpl$fbp_final=="IRELAND"] <- 0



##Dummy for born in Italy
full1910.allbpl$italian <- 0
full1910.allbpl$italian[full1910.allbpl$bp_final == "ITALY"] <- 1

full1910.allbpl$ital2gens <- 0
full1910.allbpl$ital2gens[full1910.allbpl$bp_final == "ITALY" | full1910.allbpl$fbp_final == "ITALY" | full1910.allbpl$mbp_final == "ITALY"] <- 1
full1910.allbpl$ital2gens[full1910.allbpl$mbp_final!="ITALY" & full1910.allbpl$bp_final!="ITALY" & !(full1910.allbpl$mbp_final %in% states$State) & full1910.allbpl$fbp_final=="ITALY"] <- 0


##These ethnicities are commented out because we considered them but are no longer actively analyzing them. Code should still work.

# ##Dummy for born in Canada
# full1910.allbpl$canadian <- 0
# full1910.allbpl$canadian[full1910.allbpl$bp_final == "CANADA" | full1910.allbpl$bp_final == "NOVA SCOTIA" | full1910.allbpl$bp_final=="NEW BRUNSWICK" |
		   # full1910.allbpl$bp_final == "NEWFOUNDLAND" | full1910.allbpl$bp_final=="PRINCE EDWARD ISLAND" | 
		   # full1910.allbpl$bp_final == "FRENCH CANADA" | full1910.allbpl$bp_final=="ONTARIO" | full1910.allbpl$bp_final == "BRITISH COLUMBIA" | 
		   # full1910.allbpl$bp_final=="QUEBEC" | full1910.allbpl$bp_final == "CAPE BRETON" | full1910.allbpl$bp_final=="MANITOBA"] <- 1

# ##Dummy for born in Russia
# full1910.allbpl$russian <- 0
# full1910.allbpl$russian[full1910.allbpl$bp_final == "RUSSIA"] <- 1


# ##Dummy for born in Austria
# full1910.allbpl$austrian <- 0
# full1910.allbpl$austrian[full1910.allbpl$bp_final == "AUSTRIA" | full1910.allbpl$bp_final == "AUSTRIA-VIENNA"] <- 1

# ##Dummy for born in Sweden
# full1910.allbpl$swedish <- 0
# full1910.allbpl$swedish[full1910.allbpl$bp_final == "SWEDEN"] <- 1

# ##Dummy for born in Norway
# full1910.allbpl$norwegian <- 0
# full1910.allbpl$norwegian[full1910.allbpl$bp_final == "NORWAY"] <- 1

# ##Dummy for born in Hungary
# full1910.allbpl$hungarian <- 0
# full1910.allbpl$hungarian[full1910.allbpl$bp_final == "HUNGARY"] <- 1

# ##Dummy for born in Poland
# full1910.allbpl$polish <- 0
# full1910.allbpl$polish[full1910.allbpl$bp_final == "RUSSIAN POLAND" | full1910.allbpl$bp_final == "POLAND" | full1910.allbpl$bp_final == "PRUSSIAN POLAND" |
		# full1910.allbpl$bp_final == "GERMAN POLAND" | full1910.allbpl$bp_final == "AUSTRIAN POLAND" | full1910.allbpl$bp_final == "SLOVONIA"] <- 1

# ##Dummy for born in France
# full1910.allbpl$french <- 0
# full1910.allbpl$french[full1910.allbpl$bp_final == "FRANCE" | full1910.allbpl$bp_final == "ALSACE"] <- 1

# ##Dummy for born in Czechoslovakia/Bohemia
# full1910.allbpl$czech <- 0
# full1910.allbpl$czech[full1910.allbpl$bp_final == "BOHEMIA" | full1910.allbpl$bp_final == "CZECHOSLOVAKIA" | full1910.allbpl$bp_final == "BOHEMIA-MORAVIA"] <- 1

# ##Dummy for born in Denmark
# full1910.allbpl$danish <- 0
# full1910.allbpl$danish[full1910.allbpl$bp_final == "DENMARK"] <- 1

# ##Dummy for born in Mexico
# full1910.allbpl$mexican <- 0
# full1910.allbpl$mexican[full1910.allbpl$bp_final == "MEXICO"] <- 1

				

fwrite(full1910.allbpl,"/home/s4-data/LatestCities/SIS/revised_1910_extract.txt",sep="|",eol="\r\n") ##Write out pipe-delimited extract

