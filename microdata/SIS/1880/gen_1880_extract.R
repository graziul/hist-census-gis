###Begin code

##Clear out memory 
rm(list=ls())
gc()
library(data.table)
setwd("/home/s4-data/LatestCities/SIS/analysis_files")

orig.1880.data <- fread("/home/s4-data/LatestCities/1880/SIS/full1880us.txt",fill=TRUE) ##output from make1880fullfile.do
to.SIS.1880 <- orig.1880.data[,c("serial","serial80","year","dwsize","datanum","pernum","pernum80","city","stateicp","enumdist",
					"statefip","race","raced","bpl","bpld","fbpl","fbpld","mbpl","mbpld","sex","marst",
					"edscor50","erscor50","relate","related","famsize","famunit",
					"occ1950","ind1950","sei","age","bplstr","mbplstr","fbplstr"),with=FALSE] ##subset some vars
to.SIS.1880 <- to.SIS.1880[!duplicated(to.SIS.1880),] ##make sure there are no "true duplicates" in the data (generally not a problem except 1900-1910)
fwrite(to.SIS.1880,"sisdata1880.txt",sep="|",eol="\r\n") ##write out these subsetted data
rm(list=ls()) ##clear everything from memory

full1880 <- fread("sisdata1880.txt") ##read back in the thing you just wrote out
full1880$sisrace <- 0 ##initialize an empty sisrace variable
full1880$sisrace[full1880$race == "White"] <- 1 ##Dummy up the race (note this step is a little different than other yrs)
full1880$sisrace[full1880$race == "Black/Negro"] <- 2

full1880$city[full1880$city=="Allegheny, PA"] <- "Pittsburgh, PA" ##Allegheny is part of Pittsburgh in other years
full1880$city[full1880$city=="Brooklyn (only in census years before 1900)"] <- "New York, NY" ##Brooklyn is part of New York in other years


###This next section creates the race/ethnicity dummy variables needed for segregation analyses

full1880$black <- 0 ##initialize a "black" dummy variable
full1880$black[full1880$raced=="Black/Negro"] <- 1
full1880$black[full1880$raced=="Mulatto"] <- 1
full1880$white <- 0 ##Initialize a "white" dummy variable
full1880$white[full1880$raced=="White"] <- 1


full1880$bpl <- toupper(full1880$bpl) ##convert birthplace variables to uppercase for matching
full1880$mbpl <- toupper(full1880$mbpl)
full1880$fbpl <- toupper(full1880$fbpl)

states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ## read in list of states + abbreviations


##Dummy for the native-born to native-born parents
full1880$wnbnp <- 0 ##white native born to native parents
full1880$wnbnp[full1880$bpl %in% states$State & full1880$fbpl %in% states$State & 
		full1880$mbpl %in% states$State & full1880$sisrace==1] <- 1

##Dummy for born in Germany
full1880$german <- 0
full1880$german[full1880$bpl == "GERMANY" | full1880$bpl == "BAVARIA" | full1880$bpl == "SAXONY"
		| full1880$bpl == "BADEN" | full1880$bpl == "HANOVER" | full1880$bpl == "EAST GERMANY, N.E.C."
		| full1880$bpl == "PRUSSIA, N.E.C." | full1880$bpl == "WEST PRUSSIA" ] <- 1

full1880$german2gens <- 0
full1880$german2gens[full1880$bpl == "GERMANY" | full1880$bpl == "BAVARIA" | full1880$bpl == "SAXONY"
		| full1880$bpl == "BADEN" | full1880$bpl == "HANOVER" | full1880$bpl == "EAST GERMANY, N.E.C."
		| full1880$bpl == "PRUSSIA, N.E.C." | full1880$bpl == "WEST PRUSSIA" 
		| full1880$fbpl == "GERMANY" | full1880$fbpl == "BAVARIA" | full1880$fbpl == "SAXONY"
		| full1880$fbpl == "BADEN" | full1880$fbpl == "HANOVER" | full1880$fbpl == "EAST GERMANY, N.E.C."
		| full1880$fbpl == "PRUSSIA, N.E.C." | full1880$fbpl == "WEST PRUSSIA" 
		| full1880$mbpl == "GERMANY" | full1880$mbpl == "BAVARIA" | full1880$mbpl == "SAXONY"
		| full1880$mbpl == "BADEN" | full1880$mbpl == "HANOVER" | full1880$mbpl == "EAST GERMANY, N.E.C."
		| full1880$mbpl == "PRUSSIA, N.E.C." | full1880$mbpl == "WEST PRUSSIA" ] <- 1

full1880$german2gens[full1880$mbpl != "GERMANY" & full1880$mbpl != "BAVARIA" & full1880$mbpl != "SAXONY"
		& full1880$mbpl != "BADEN" & full1880$mbpl != "HANOVER" & full1880$mbpl != "EAST GERMANY, N.E.C."
		& full1880$mbpl != "PRUSSIA, N.E.C." & full1880$mbpl != "WEST PRUSSIA" &
		full1880$bpl != "GERMANY" & full1880$bpl != "BAVARIA" & full1880$bpl != "SAXONY"
		& full1880$bpl != "BADEN" & full1880$bpl != "HANOVER" & full1880$bpl != "EAST GERMANY, N.E.C."
		& full1880$bpl != "PRUSSIA, N.E.C." & full1880$bpl != "WEST PRUSSIA" & !(full1880$mbpl %in% states$State)
		& (full1880$fbpl == "GERMANY" | full1880$fbpl == "BAVARIA" | full1880$fbpl == "SAXONY"
		| full1880$fbpl == "BADEN" | full1880$fbpl == "HANOVER" | full1880$fbpl == "EAST GERMANY, N.E.C."
		| full1880$fbpl == "PRUSSIA, N.E.C." | full1880$fbpl == "WEST PRUSSIA")] <- 0


##Dummy for born in Britain
full1880$british <- 0
full1880$british[full1880$bpl == "ENGLAND" | full1880$bpl == "SCOTLAND" | full1880$bpl=="WALES"] <- 1

full1880$british2gens <- 0
full1880$british2gens[full1880$bpl == "ENGLAND" | full1880$bpl == "SCOTLAND" | full1880$bpl=="WALES"
		      | full1880$fbpl == "ENGLAND" | full1880$fbpl == "SCOTLAND" | full1880$fbpl=="WALES"
		      | full1880$mbpl == "ENGLAND" | full1880$mbpl == "SCOTLAND" | full1880$mbpl=="WALES"] <- 1
full1880$british2gens[full1880$mbpl!="ENGLAND" & full1880$mbpl!="SCOTLAND" & full1880$mbpl!="WALES" 
			& !(full1880$mbpl %in% states$State) & full1880$bpl != "ENGLAND" & full1880$bpl!="SCOTLAND" & 
			full1880$bpl!="WALES" & (full1880$fbpl=="IRELAND" | full1880$fbpl=="SCOTLAND" | full1880$fbpl=="WALES")] <- 0



##Dummy for born in Ireland
full1880$irish <- 0
full1880$irish[full1880$bpl == "IRELAND"] <- 1

full1880$irish2gens <- 0
full1880$irish2gens[full1880$bpl == "IRELAND" | full1880$fbpl == "IRELAND" | full1880$mbpl == "IRELAND"] <- 1
full1880$irish2gens[full1880$mbpl!="IRELAND" & full1880$bpl!="IRELAND" & !(full1880$mbpl %in% states$State) & full1880$fbpl=="IRELAND"] <- 0



##Dummy for born in Italy
full1880$italian <- 0
full1880$italian[full1880$bpl == "ITALY"] <- 1
full1880$ital2gens <- 0
full1880$ital2gens[(full1880$mbpl =="ITALY" | full1880$fbpl=="ITALY" | full1880$bpl=="ITALY")] <- 1
full1880$ital2gens[full1880$mbpl!="ITALY" & full1880$bpl!="ITALY" & !(full1880$mbpl %in% states$State) & full1880$fbpl=="ITALY"] <- 0


##The next set of variables are commented out because we're not currently analyzing them, but one could uncomment them 
##and use them later.

##Dummy for born in Austria
#full1880$austrian <- 0
#full1880$austrian[full1880$bpl == "AUSTRIA" | full1880$bpl == "AUSTRIA-VIENNA"  
#		  | full1880$bpl == "AUSTRIA-HUNGARY" | full1880$bpl == "AUSTRIA-TYROL"
#		  | full1880$bpl == "AUSTRIA-GRAZ" | full1880$bpl == "AUSTRIA-SALZBURG"
#		  | full1880$bpl == "AUSTRIA-KAERNTEN"] <- 1
#

##Dummy for born in Canada
#full1880$canadian <- 0
#full1880$canadian[full1880$bpl == "CANADA" | full1880$bpl == "NOVA SCOTIA" | full1880$bpl=="NEW BRUNSWICK" |
#		   full1880$bpl == "NEWFOUNDLAND" | full1880$bpl=="PRINCE EDWARD ISLAND" | 
#		   full1880$bpl == "FRENCH CANADA" | full1880$bpl=="ONTARIO" | full1880$bpl == "BRITISH COLUMBIA" | 
#		   full1880$bpl=="QUEBEC" | full1880$bpl == "CAPE BRETON" | full1880$bpl=="MANITOBA"] <- 1
#
##Dummy for born in Russia
#full1880$russian <- 0
#full1880$russian[full1880$bpl == "RUSSIA" | full1880$bpl == "OTHER USSR/RUSSIA"] <- 1
#
#
##Dummy for born in Sweden
#full1880$swedish <- 0
#full1880$swedish[full1880$bpl == "SWEDEN"] <- 1
#
##Dummy for born in Norway
#full1880$norwegian <- 0
#full1880$norwegian[full1880$bpl == "NORWAY"] <- 1
#
##Dummy for born in Hungary
#full1880$hungarian <- 0
#full1880$hungarian[full1880$bpl == "HUNGARY"] <- 1
#
##Dummy for born in Poland
#full1880$polish <- 0
#full1880$polish[full1880$bpl == "RUSSIAN POLAND" | full1880$bpl == "POLAND" | full1880$bpl == "PRUSSIAN POLAND" |
#		full1880$bpl == "GERMAN POLAND" | full1880$bpl == "AUSTRIAN POLAND" | full1880$bpl == "SLOVONIA"] <- 1
#
##Dummy for born in France
#full1880$french <- 0
#full1880$french[full1880$bpl == "FRANCE" | full1880$bpl == "ALSACE"] <- 1
#
##Dummy for born in Czechoslovakia/Bohemia
#full1880$czech <- 0
#full1880$czech[full1880$bpl == "BOHEMIA" | full1880$bpl == "CZECHOSLOVAKIA" | full1880$bpl == "BOHEMIA-MORAVIA"
#		| full1880$bpl == "CZECH REPUBLIC"] <- 1

##Dummy for born in Denmark
#full1880$danish <- 0
#full1880$danish[full1880$bpl == "DENMARK"] <- 1

##Dummy for born in Mexico
#full1880$mexican <- 0
#full1880$mexican[full1880$bpl == "MEXICO"] <- 1

full1880$city <- toupper(full1880$city) ##Convert city names to uppercase for matching later

##This next bunch of code was developed for 1900 and 1910 where the files aren't cleaned by IPUMS but I left it in for
##every year, even though it might be superfluous
		
full1880 <- full1880[full1880$city!="ARKANSAS CITY, KS" & full1880$city!="BRONXVILLE, NY" &
                                full1880$city!="CHESTER HILL, PA" & full1880$city!="COHOES, NY" &  
                                full1880$city!="LOCKPORT, NY" & full1880$city!="KINGSTON, NY" &
                                full1880$city!="MANCHESTER, PA" & full1880$city!="MIAMI BEACH, FL" & 
                                full1880$city!="NEW BRIGHTON, NY" & full1880$city!="NEWBURGH, NY" & 
                                full1880$city!="OGDENSBURG, NY" & full1880$city!="OSWEGO, NY" & 
                                full1880$city!="ROME, NY" & full1880$city!="SALEMBURG, NC" & 
                                full1880$city!="ST PAUL PARK, MN" & full1880$city!="VERNON, NY" & 
                                full1880$city!="WATERTOWN, NY" & full1880$city!="WEST CHESTER, PA" & 
                                full1880$city!="WEST CHICAGO, IL" & full1880$city!="WEST MILWAUKEE, WI" & 
                                full1880$city!="WEST MINNEAPOLIS, MN" & full1880$city!="WEST PATERSON, NJ" & 
                                full1880$city!="WEST READING, PA" & full1880$city!="WEST ST PAUL, MN" & 
                                full1880$city!="WEST TAMPA, FL" & full1880$city!="WEST YORK, PA" & 
                                full1880$city!="YORK SPRINGS, PA" & full1880$city!="YORKANA, PA" & 
                                full1880$city!="INDIANAPOLIS, IA" & full1880$city!="LONG ISLAND CITY, NY" &
                                full1880$city!="LOS ANGELES, LOS ANGELES" & full1880$city!="OKLAHOMA, OK" &
                                full1880$city!="WEST LINCOLN, NE" & full1880$city!="ROCHESTER, PA" &
                                full1880$city!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP), NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1880$city!="NOT IN IDENTIFIABLE CITY (OR SIZE GROUP)" &
                                full1880$city!="MISSING, MISSING" & full1880$city!="NORMAN, OK" &
                                full1880$city!="NEW YORK CITY, NY" & full1880$city!="NEW YORK MILLS, NY" &
                                full1880$city!="CHICAGO RIDGE, IL" & full1880$city!="PORTLAND, PORTLAND,",]

full1880 <- full1880[!(full1880$city=="ALLEGHENY, PA" & year==1910),]
 
full1880$city[full1880$city=="EAST ST. LOUIS, IL"] <- "EAST ST LOUIS, IL" 
full1880$city[full1880$city=="NEW YORK CITY, NY"] <- "NEW YORK, NY" 
full1880$city[full1880$city=="LACROSSE, WI"] <- "LA CROSSE, WI" 
full1880$city[full1880$city=="OAK PARK VILLAGE, IL"] <- "OAK PARK, IL" 
full1880$city[full1880$city=="PHOENIX, ARIZONA TERRITORY"] <- "PHOENIX, AZ" 
full1880$city[full1880$city=="SCHENECTEDY, NY"] <- "SCHENECTADY, NY" 
full1880$city[full1880$city=="ST LOUIS, IL"] <- "EAST ST LOUIS, IL" 
full1880$city[full1880$city=="WASHINGTON, DISTRICT OF COLUMBIA"] <- "WASHINGTON, DC"
full1880$city[full1880$city=="ST LOUIS, MO"] <- "SAINT LOUIS, MO"
full1880$city[full1880$city=="ST JOSEPH, MO"] <- "SAINT JOSEPH, MO"
full1880$city[full1880$city=="ST PAUL, MN"] <- "SAINT PAUL, MN"
##END CODE BLOCK DESCRIBED ABOVE
	

fwrite(full1880,"/home/s4-data/LatestCities/SIS/revised_1880_extract.txt",sep="|",eol="\r\n") ##write out the extract file
 

