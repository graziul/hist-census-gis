##This code will pull identifying information, race, birthplace, and parents' birthplace for 
##all cities in 1910. It takes a list of city-state pairs, combines it with raw state-by-state
##1910 census data files (PSV), and outputs PSVs for the cities of interest state-by-state.

##Nate Frey, last updated 12 April 2017; cosmetic updates 13 July 2017

###Begin code

##Clear out memory 
rm(list=ls())
gc()
library(data.table)

####Begin generalized code 

##Read in the list of city-state pairs for this analysis
allcities <- fread("/home/s4-data/LatestCities/1910/SIS/sis_cities_rev.csv")

##Initialize the big loop over all the states that have cities on the list
for (i in 1:length(unique(allcities$state))) ##Use the unique list to avoid redundancy -- we only need each state file once
  {
  filename <- paste0("/home/s4-data/LatestCities/1910/raw/Census1910_",unique(allcities$state)[i],".txt") ##What is the name of the psv file for this state?
  current.state <- fread(filename) ##using fread (data.table), read that psv into memory
  setkey(current.state,unique_identifier) ##set a key for data.table to make other data.table operations work properly
   current.state <- current.state[,c("ImageFileName","ImageNumber","unique_identifier","LivepID","StateCode","ResidenceState","ResidenceCounty","ResidenceCity","EnumerationDistrict","Age","AgeAlias_2","Race","RaceAlias_1","RaceAlias_2","Gender","GenderAlias_1","RelationToHead","RelationtoHeadAlias_1",
                                    "BirthPlace","BirthPlaceAlias_1","BirthPlaceAlias_2","FatherBirthPlace","FatherBirthPlaceAlias_1","MotherBirthPlace","MotherBirthPlaceAlias_1","MaritalStatus","MaritalStatusAlias_1","Institution","state",
                                    "YearsMarried","NumberofChildrenLiving","NativeTongue","Occupation","Industry","OutofWork","CanRead","CanWrite","OwnOrRentHome",
				    "os_SheetNumber","os_SheetLetter","LineNumber","ycord","FamilyNumber","DwellingNumber","Street","HouseNumber","mpcid"), with=FALSE] ##Drop some variables to save memory
  if(unique(allcities$state)[i] == "Ohio") {
  current.state$ResidenceCity[current.state$ResidenceCity=="Rockport"] <- "Lakewood"
  }
  cities.subset <- allcities[allcities$state==unique(allcities$state)[i],] ##Cities in the state we're working with
  current.cities <- cities.subset[[1]] ##Just a vector of the city names
  rm(cities.subset)
  for (j in 1:length(current.cities)) ##Initialize loop over the cities in this state
    {
  if (j == 1) {
    state.subset <- current.state[grep(current.cities[j],current.state$ResidenceCity),] ##create the data frame with values for one city, using grep for matches with extra words/characters   
  } 
    if (j > 1) {
    state.subset.temp <- current.state[grep(current.cities[j],current.state$ResidenceCity),] ##Create values for another city
    state.subset <- rbind(state.subset,state.subset.temp) ##Then combine with values from the previous city
  }
    }
  state.filename.towrite <- paste0("/home/s4-data/LatestCities/1910/SIS/",unique(allcities$state)[i],"_raw_forsis.txt") ##Name the output file for all cities in state
  state.filename.towrite.nodup <- paste0("/home/s4-data/LatestCities/1910/SIS/",unique(allcities$state)[i],"_raw_nd_forsis.txt") ##Name the output file for all cities in state if duplicates were eliminated
  state.subset.nodup <- state.subset[duplicated(state.subset)==FALSE,] ##Create a dataframe of non-duplicates
  if(length(state.subset$unique_identifier) == length(state.subset.nodup$unique_identifier)) { 
  print(paste0("no dups found in ",unique(allcities$state)[i])) ##If no duplicates found, print that to terminal
    fwrite(state.subset,state.filename.towrite,sep="|") ##then write out the file
  } else {
    fwrite(state.subset.nodup,state.filename.towrite.nodup,sep="|") ##If duplicates found, use the file name indicating that
  }
  rm(current.state,state.subset.temp,current.cities) 
  gc()  ##Some cleanup
  
  print(paste0("made it to ",unique(allcities$state)[i], " which is number ", i)) ##Print progress to terminal
  
}
rm(list=ls())

##Specific 1910 code to fix an issue with Indiana place names:
library(data.table)
indiana.to.correct <- fread("/home/s4-data/LatestCities/1910/SIS/Indiana_raw_nd_forsis.txt")
##Center Township, Indianapolis
indiana.corrected <- subset( indiana.to.correct, !( ResidenceCity == "Center" & ResidenceCounty != "Marion" ) )
##Pigeon Township, Evansville
indiana.corrected <- subset( indiana.to.correct, !( ResidenceCity == "Pigeon" & ResidenceCounty != "Vanderburgh" ) )
##Wayne Township, Fort Wayne
indiana.corrected <- subset( indiana.to.correct, !( ResidenceCity == "Wayne" & ResidenceCounty != "Allen" ) )
##Harrison Township, Terra Haute
indiana.corrected <- subset( indiana.to.correct, !( ResidenceCity == "Harrison" & ResidenceCounty != "Vigo" ) )
fwrite(indiana.corrected,"Indiana_raw_nd_corrected_forsis.txt",sep="|")


rm(list=ls())