library(readstata13)
library(plyr)

args <- commandArgs(trailingOnly = TRUE)
dir_path <- args[1]
city_name <- args[2]
file_name <- args[3]
state_abbr <- args[4]

if (substr(file_name,nchar(file_name)-3+1,nchar(file_name)) == "dta") {
  city<-read.dta13(file_name)
  vars<-c("st_best_guess", "ed", "type", "block","hn")
  names(city)<-tolower(names(city))
  city30<-city[vars]
  city30<-plyr::rename(city30, c(block="Mblk", st_best_guess="fullname"))  
} else {
  city<-read.csv(file_name)
  vars<-c("overall_match", "ed", "type", "block","hn")
  names(city)<-tolower(names(city))
  city30<-city[vars]
  city30<-plyr::rename(city30, c(block="Mblk", overall_match="fullname"))
}
 

city30$state<-state_abbr
city30$city<-city_name
city30$address<-paste(city30$hn, city30$fullname, sep=" ")
#names(city30)
#View(city30)

setwd(paste(dir_path,"\\GIS_edited",sep=""))
write.csv(city30, paste(city_name,"_1930_Addresses.csv",sep=""))
