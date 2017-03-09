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

sa<-read.csv("Z:/Projects/1940Census/Block Creation/San Antonio/SA_AutoClean30.csv", stringsAsFactors = F)
changes<-read.csv("Z:/Projects/1940Census/Block Creation/San Antonio/Streets To Be Changed.csv", stringsAsFactors = F)
names(sa)<-tolower(names(sa))
names(changes)<-tolower(names(changes))

#Change Only Microdata Streets Without a North/South direction
  changes<-subset(changes, changes$change2=="")
  changes<-subset(changes, changes$change1!="OUTSIDE CITY LIMITS")

vars<-c("overall_match", "ed", "type", "block","hn", "self_empty_info_race", "self_birth_place_empty")
sa30<-sa[vars]

sa30<-plyr::rename(sa30, c(block="Mblk", overall_match="fullname"))
sa30$state<-"TX"
sa30$city<-"San Antonio"

#Change Microdata Names where they are noted in SteveMorse
  #Order By Fullname
  sa30<-sa30[order(sa30$fullname),]
  changes<-changes[order(changes$from),]
  #Make Changes
  sa30$fullname<-ifelse(sa30$fullname %in% changes$from, changes$change1, sa30$fullname)

#Create New Address File
  sa30$address<-paste(sa30$hn, sa30$fullname, sep=" ")
  names(sa30)

write.csv(sa30, "Z:/Projects/1940Census/Block Creation/San Antonio/Add_30_2nd.csv")
