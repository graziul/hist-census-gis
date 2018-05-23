library(Hmisc)
library(DataCombine)
library(readstata13)
library(foreign)
library(car)
library(plyr)
library(seg)
library(spdep)
library(reshape)
library(reshape2)
library(rJava)
library(xlsx)
library(maptools)
library(rgdal)
library(haven)

args <- commandArgs(trailingOnly = TRUE)
dir_path <- args[1]
city_name <- args[2]
file_name <- args[3]
state_abbr <- args[4]

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"\\GIS_edited\\",sep="")
city_name <- args[2]

city<-read.dta13(file_name, stringsAsFactors = F)
## STOPPED HERE
changes<-read.csv("Z:/Projects/1940Census/Block Creation/San Antonio/Streets To Be Changed.csv", stringsAsFactors = F)
names(city)<-tolower(names(city))
names(changes)<-tolower(names(changes))

#Change Only Microdata Streets Without a North/South direction
  changes<-subset(changes, changes$change2=="")
  changes<-subset(changes, changes$change1!="OUTSIDE CITY LIMITS")

vars<-c("overall_match", "ed", "type", "block","hn", "self_empty_info_race", "self_birth_place_empty")
city30<-city[vars]

city30<-plyr::rename(city30, c(block="Mblk", overall_match="fullname"))
city30$state<-state_abbr
city30$city<-city_name

#Change Microdata Names where they are noted in SteveMorse
  #Order By Fullname
city30<-city30[order(city30$fullname),]
  changes<-changes[order(changes$from),]
  #Make Changes
  city30$fullname<-ifelse(city30$fullname %in% changes$from, changes$change1, city30$fullname)

#Create New Address File
  city30$address<-paste(city30$hn, city30$fullname, sep=" ")
  names(city30)

  write.csv(city30, paste(dir_path,"\\GIS_edited\\",city_name,"_1930_Addresses_2nd.csv",sep=""))
  