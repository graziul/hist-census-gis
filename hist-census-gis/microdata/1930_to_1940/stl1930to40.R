##This script is the first attempt at applying student manual changes from 1930 to the same city in 1940
##It uses student-cleaned data for priority levels 1-3 in St. Louis, MO and applies them to a preliminary
##auto-cleaned file produced by Chris Graziul's auto-cleaning algorithm. 
##As currently written, it changes 2,532 cases based on 95 name changes. This is applying only "check_st"
##cases from 1930 to only "check_st" cases from 1940.

##Written by Nate Frey, July 2017. Last run July 10 2017.

library(data.table) ##data reading/subsetting for large data
library(dplyr) ##data manipulation
library(dtplyr) ##combine the above two
library(readstata13) ##read dta files from stata 13

setwd("/home/s4-data/LatestCities/1940/autocleaned/") ##this is where the files are on rhea/cs1

stl1940 <- fread("./V5/StLouisMO_AutoCleanedV5.csv") ##read in an autocleaned 1940 file from Chris Graziul
stl1940_check <- stl1940[stl1940$check_hn==TRUE,]
stl1940_short <- stl1940_check[,c("V1","street_precleanedHN"),with=FALSE] ##we're only using these in 1940
stl1940 <- stl1940_short ##rename it back to the easier name
rm(stl1940_short) ##remove the harder name
gc() ##return memory
#fwrite(stl1940,"stl1940short.txt",sep="|",eol="\r\n") ##write out the condensed file (only needs to be done once)
#stl1940 <- fread("stl1940short.txt") ##read the condensed file back in (if you don't want to redo the subsetting above)

stl1930 <- read.dta13("StLouis_foranaylsisV12.dta") ##read in the 1930 file where the students have cleaned priority levels 1-3
stl1930 <- as.data.table(stl1930) ##convert that to a data table so that it works better
stl1930_to_check <- stl1930[stl1930$check_st=="True",]
stl1930_stchg <- stl1930_to_check[stl1930_to_check$checked_st!="." & stl1930_to_check$checked_st!="",]
stl1930_short <- stl1930_stchg[,c("v1","pid","hn_raw","hn","street_precleanedhn","st_edit"),with=FALSE] ##cut some of those variables out
stl1930_shorter <- stl1930_short[,c("street_precleanedhn","st_edit"),with=FALSE] ##cut some more variables out
stl1930_shortest <- stl1930_shorter[!(duplicated(stl1930_shorter)),] ##remove duplicate student changes
stl1930_to_merge <- stl1930_shortest[!(duplicated(stl1930_shortest$street_precleanedhn) | duplicated(stl1930_shortest$street_precleanedhn,fromLast=TRUE)), ] ##subset those dups to only ones that have one and only one "solution"
stl1930_to_merge <- stl1930_to_merge[!(grepl("\\d",stl1930_to_merge$st_edit)),] ##this process is generally a bad idea for numbered streets
stl1930_to_merge <- stl1930_to_merge[!(grepl("\\d",stl1930_to_merge$street_precleanedhn)),] ##we don't want numbers here either
stl1930_to_merge <- stl1930_to_merge[!(grepl("\\?",stl1930_to_merge$street_precleanedhn)),] ##question marks are also bad

stl1930_to_merge$mergevar <- stl1930_to_merge$street_precleanedhn ##name a variable to merge on

#stl1940$corrector <- character()
stl1940$mergevar <- stl1940$street_precleanedHN ##name a variable to merge on
merge_years <- left_join(stl1940,stl1930_to_merge,by="mergevar") ##left join keeps all 1940 cases and appends 1930 info onto the ones that have it
merge_years <- as.data.table(merge_years) ##change it back into a data table because left_join turns it into a tibble and I don't like tibbles
check_data <- merge_years[!is.na(merge_years$st_edit),] ##just cases with changes to manually check results
check_data$V1 <- NULL ##get rid of a variable that is useless for this purpose
check_data <- check_data[!duplicated(check_data$mergevar),] ##unique cases
fwrite(check_data,"/home/s4-data/LatestCities/1940/autocleaned/matches_to_check_30_40_rev.csv",eol="\r\n") ##write out unique cases
#stl1940$corrector[stl1940$street_precleanedHN %in% stl1930_to_merge$street_precleanedhn] <- stl1930_to_merge$st_edit[stl1930_to_merge$street_precleanedhn %in% stl1940$street_precleanedHN]
