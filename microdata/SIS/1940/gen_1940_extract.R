##Generates the 1940 extract for the SIS/segregation index project
##Last updated by Frey in May 2017; cosmetic updates 13 July 2017


library(data.table) 
library(dplyr)
library(dtplyr)
#unique(full1930$race) ##what are possible values of race variable
setwd("/home/s4-data/LatestCities/SIS/analysis_files/")
full1940 <- fread("/home/s4-data/LatestCities/1940/raw/SIS/full1940us_update2.txt") ##read in big full-year file

full1940$sisrace <- 0  ##Initialize an empty sisrace variable
full1940$sisrace[full1940$race=="White"] <- 1
full1940$sisrace[full1940$race=="Black/Negro"] <- 2
full1940$sisrace[full1940$race=="Mulatto"] <- 2

full1940$sisrace[full1940$race==""] <- NA ##Blanks are NAs

full1940$sisrace[full1940$sisrace == 0] <- 3

full1940$city <- toupper(full1940$city)

full1940$city[full1940$statefip=="Illinois" & full1940$county==1670] <- "SPRINGFIELD, IL"
full1940 <- full1940[!full1940$city=="Missing",]
full1940 <- full1940[!duplicated(full1940),]
#full1940 <- rename(full1940,enumdist=us1940b_0084)

##Start race/ethnicity dummies -- note that we don't know parents' birthplaces in 1940

full1940$black <- 0
full1940$black[full1940$sisrace==2] <- 1
full1940$white <- 0
full1940$white[full1940$sisrace==1] <- 1
#full1940 <- rename(full1940,enumdist=us1940b_0084)

full1940$bpl <- toupper(full1940$bpl)

full1940$bpl[substr(full1940$bpl,1,10)=="OTHER USSR"] <- "RUSSIA" ##this string has gotten very garbled
full1940$bpl[substr(full1940$bpl,1,4)=="USSR"] <- "RUSSIA" 
states <- fread("stateabbrev_eth.csv") ##list of states


##Dummy for the native-born to native-born parents
full1940$wnb <- 0 ##white native born to native parents
full1940$wnb[full1940$bpl %in% states$State & full1940$sisrace==1] <- 1 ##were you born in the US?
##Dummy for born in Germany
full1940$german <- 0
full1940$german[full1940$bpl == "GERMANY" | full1940$bpl == "BAVARIA" | full1940$bpl == "SAXONY"
		| full1940$bpl == "BADEN" | full1940$bpl == "HANOVER" | full1940$bpl == "EAST GERMANY, N.E.C."
		| full1940$bpl == "PRUSSIA, N.E.C." | full1940$bpl == "WEST PRUSSIA" ] <- 1

##Dummy for born in Britain
full1940$british <- 0
full1940$british[full1940$bpl == "ENGLAND" | full1940$bpl == "SCOTLAND" | full1940$bpl=="WALES"] <- 1

##Dummy for born in Ireland
full1940$irish <- 0
full1940$irish[full1940$bpl == "IRELAND"] <- 1

##Dummy for born in Italy
full1940$italian <- 0
full1940$italian[full1940$bpl == "ITALY"] <- 1

##We still have a procedure for ethnicities we are not presently considering from an earlier version of the analysis

# ##Dummy for born in Austria
# full1940$austrian <- 0
# full1940$austrian[full1940$bpl == "AUSTRIA" | full1940$bp_final == "AUSTRIA-VIENNA"  
		  # | full1940$bp_final == "AUSTRIA-HUNGARY" | full1940$bp_final == "AUSTRIA-TYROL"
		  # | full1940$bp_final == "AUSTRIA-GRAZ" | full1940$bp_final == "AUSTRIA-SALZBURG"
		  # | full1940$bp_final == "AUSTRIA-KAERNTEN"] <- 1


# ##Dummy for born in Canada
# full1940$canadian <- 0
# full1940$canadian[full1940$bpl == "CANADA" | full1940$bpl == "NOVA SCOTIA" | full1940$bpl=="NEW BRUNSWICK" |
		   # full1940$bpl == "NEWFOUNDLAND" | full1940$bpl=="PRINCE EDWARD ISLAND" | 
		   # full1940$bpl == "FRENCH CANADA" | full1940$bpl=="ONTARIO" | full1940$bpl == "BRITISH COLUMBIA" | 
		   # full1940$bpl=="QUEBEC" | full1940$bpl == "CAPE BRETON" | full1940$bpl=="MANITOBA"] <- 1

# ##Dummy for born in Russia
# full1940$russian <- 0
# full1940$russian[full1940$bpl == "RUSSIA"] <- 1


# ##Dummy for born in Sweden
# full1940$swedish <- 0
# full1940$swedish[full1940$bpl == "SWEDEN"] <- 1

# ##Dummy for born in Norway
# full1940$norwegian <- 0
# full1940$norwegian[full1940$bpl == "NORWAY"] <- 1

# ##Dummy for born in Hungary
# full1940$hungarian <- 0
# full1940$hungarian[full1940$bpl == "HUNGARY"] <- 1

# ##Dummy for born in Poland
# full1940$polish <- 0
# full1940$polish[full1940$bpl == "RUSSIAN POLAND" | full1940$bpl == "POLAND" | 
		# full1940$bpl == "GERMAN POLAND" | full1940$bpl == "AUSTRIAN POLAND" | full1940$bpl == "SLOVONIA"] <- 1

# ##Dummy for born in France
# full1940$french <- 0
# full1940$french[full1940$bpl == "FRANCE" | full1940$bpl == "ALSACE"] <- 1

# ##Dummy for born in Czechoslovakia/Bohemia
# full1940$czech <- 0
# full1940$czech[full1940$bpl == "BOHEMIA" | full1940$bpl == "CZECHOSLOVAKIA" | full1940$bpl == "BOHEMIA-MORAVIA"
		# | full1940$bpl == "CZECH REPUBLIC"] <- 1

# ##Dummy for born in Denmark
# full1940$danish <- 0
# full1940$danish[full1940$bpl == "DENMARK"] <- 1

# ##Dummy for born in Mexico
# full1940$mexican <- 0
# full1940$mexican[full1940$bpl == "MEXICO"] <- 1


##Some probably extraneous name-cleaning code.

full1940 <- full1940[full1940$city!="ARKANSAS CITY, KS" & full1940$city!="BRONXVILLE, NY" &
                                full1940$city!="CHESTER HILL, PA" & full1940$city!="COHOES, NY" &  
                                full1940$city!="LOCKPORT, NY" & full1940$city!="KINGSTON, NY" &
                                full1940$city!="MANCHESTER, PA" & full1940$city!="MIAMI BEACH, FL" & 
                                full1940$city!="NEW BRIGHTON, NY" & full1940$city!="NEWBURGH, NY" & 
                                full1940$city!="OGDENSBURG, NY" & full1940$city!="OSWEGO, NY" & 
                                full1940$city!="ROME, NY" & full1940$city!="SALEMBURG, NC" & 
                                full1940$city!="ST PAUL PARK, MN" & full1940$city!="VERNON, NY" & 
                                full1940$city!="WATERTOWN, NY" & full1940$city!="WEST CHESTER, PA" & 
                                full1940$city!="WEST CHICAGO, IL" & full1940$city!="WEST MILWAUKEE, WI" & 
                                full1940$city!="WEST MINNEAPOLIS, MN" & full1940$city!="WEST PATERSON, NJ" & 
                                full1940$city!="WEST READING, PA" & full1940$city!="WEST ST PAUL, MN" & 
                                full1940$city!="WEST TAMPA, FL" & full1940$city!="WEST YORK, PA" & 
                                full1940$city!="YORK SPRINGS, PA" & full1940$city!="YORKANA, PA" & 
                                full1940$city!="INDIANAPOLIS, IA" & full1940$city!="LONG ISLAND CITY, NY" &
                                full1940$city!="LOS ANGELES, LOS ANGELES" & full1940$city!="OKLAHOMA, OK" &
                                full1940$city!="WEST LINCOLN, NE" & full1940$city!="ROCHESTER, PA" &
                                full1940$city!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1940$city!="MISSING, MISSING" & full1940$city!="NORMAN, OK" &
                                full1940$city!="NEW YORK CITY, NY" & full1940$city!="NEW YORK MILLS, NY" &
                                full1940$city!="CHICAGO RIDGE, IL" & full1940$city!="PORTLAND, PORTLAND,",]

full1940 <- full1940[!(full1940$city=="ALLEGHENY, PA" & year==1910),]
 
full1940$city[full1940$city=="EAST ST. LOUIS, IL"] <- "EAST ST LOUIS, IL" 
full1940$city[full1940$city=="NEW YORK CITY, NY"] <- "NEW YORK, NY" 
full1940$city[full1940$city=="LACROSSE, WI"] <- "LA CROSSE, WI" 
full1940$city[full1940$city=="OAK PARK VILLAGE, IL"] <- "OAK PARK, IL" 
full1940$city[full1940$city=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, AZ" 
full1940$city[full1940$city=="SCHENECTEDY, NY"] <- "SCHENECTADY, NY" 
full1940$city[full1940$city=="SAINT LOUIS, IL"] <- "EAST ST LOUIS, IL" 
full1940$city[full1940$city=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DC"
full1940$city[full1940$city=="ST LOUIS, MO"] <- "SAINT LOUIS, MO"
full1940$city[full1940$city=="ST JOSEPH, MO"] <- "SAINT JOSEPH, MO"
full1940$city[full1940$city=="ST PAUL, MN"] <- "SAINT PAUL, MN"

		
fwrite(full1940,"/home/s4-data/LatestCities/SIS/revised_1940_extract.txt",sep="|",eol="\r\n") ##write out a pipe-delimited file
