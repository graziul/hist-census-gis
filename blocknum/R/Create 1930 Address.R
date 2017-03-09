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

sa<-read.csv("Z:/Projects/1940Census/Block Creation/San Antonio/SA_AutoClean30.csv")
names(sa)<-tolower(names(sa))

vars<-c("overall_match", "ed", "type", "block","hn")
sa30<-sa[vars]

sa30<-plyr::rename(sa30, c(block="Mblk", overall_match="fullname"))
sa30$state<-"TX"
sa30$city<-"San Antonio"
sa30$address<-paste(sa30$hn, sa30$fullname, sep=" ")
names(sa30)
View(sa30)

write.csv(sa30, "Z:/Projects/1940Census/Block Creation/San Antonio/Add_30.csv")
