##This script is the second attempt at applying student manual changes from 1930 to the same city in 1940
##It uses student-cleaned data for priority levels 1-2 in Philadelphia, PA and applies them to a preliminary
##auto-cleaned file produced by Chris Graziul's auto-cleaning algorithm. 
##As currently written, it changes 488 cases based on 44 name changes. This is applying only "check_st"
##cases from 1930 to only "check_st" cases from 1940.

##Written by Nate Frey, July 2017. Last run July 10 2017.


phl1940 <- fread("./V5/PhiladelphiaPA_AutoCleanedV5.csv") ##read in an autocleaned 1940 file from Chris Graziul
phl1940_check <- phl1940[phl1940$check_hn==TRUE,]
phl1940_short <- phl1940_check[,c("V1","street_precleanedHN"),with=FALSE] ##we're only using these in 1940
phl1940 <- phl1940_short ##rename it back to the easier name
rm(phl1940_short) ##remove the harder name
gc() ##return memory
#fwrite(phl1940,"phl1940short.txt",sep="|",eol="\r\n") ##write out the condensed file (only needs to be done once)
#phl1940 <- fread("phl1940short.txt") ##read the condensed file back in (if you don't want to redo the subsetting above)

phl1930 <- fread("PhiladelphiaPA_StudAuto.csv") ##read in the 1930 file where the students have cleaned priority levels 1-3
#phl1930 <- as.data.table(phl1930) ##convert that to a data table so that it works better
phl1930_to_check <- phl1930[phl1930$check_st==TRUE,]
phl1930_stchg <- phl1930_to_check[phl1930_to_check$checked_st!="." & phl1930_to_check$checked_st!="",]
phl1930_short <- phl1930_stchg[,c("V1","pid","hn_raw","hn","street_precleanedhn","st_edit"),with=FALSE] ##cut some of those variables out
phl1930_shorter <- phl1930_short[,c("street_precleanedhn","st_edit"),with=FALSE] ##cut some more variables out
phl1930_shortest <- phl1930_shorter[!(duplicated(phl1930_shorter)),] ##remove duplicate student changes
phl1930_to_merge <- phl1930_shortest[!(duplicated(phl1930_shortest$street_precleanedhn) | duplicated(phl1930_shortest$street_precleanedhn,fromLast=TRUE)), ] ##subset those dups to only ones that have one and only one "solution"
phl1930_to_merge <- phl1930_to_merge[!(grepl("\\d",phl1930_to_merge$st_edit)),] ##this process is generally a bad idea for numbered streets
phl1930_to_merge <- phl1930_to_merge[!(grepl("\\d",phl1930_to_merge$street_precleanedhn)),] ##we don't want numbers here either
phl1930_to_merge <- phl1930_to_merge[!(grepl("\\?",phl1930_to_merge$street_precleanedhn)),] ##question marks are also bad

phl1930_to_merge$mergevar <- phl1930_to_merge$street_precleanedhn ##name a variable to merge on

#phl1940$corrector <- character()
phl1940$mergevar <- phl1940$street_precleanedHN ##name a variable to merge on
merge_years <- left_join(phl1940,phl1930_to_merge,by="mergevar") ##left join keeps all 1940 cases and appends 1930 info onto the ones that have it
merge_years <- as.data.table(merge_years) ##change it back into a data table because left_join turns it into a tibble and I don't like tibbles
check_data <- merge_years[!is.na(merge_years$st_edit),] ##just cases with changes to manually check results
check_data$V1 <- NULL ##get rid of a variable that is useless for this purpose
check_data <- check_data[!duplicated(check_data$mergevar),] ##unique cases
fwrite(check_data,"/home/s4-data/LatestCities/1940/autocleaned/matches_to_check_30_40_rev.csv",eol="\r\n") ##write out unique cases
#phl1940$corrector[phl1940$street_precleanedHN %in% phl1930_to_merge$street_precleanedhn] <- phl1930_to_merge$st_edit[phl1930_to_merge$street_precleanedhn %in% phl1940$street_precleanedHN]
