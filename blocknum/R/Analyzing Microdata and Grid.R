library(Hmisc)
library(foreign)
library(car)
library(plyr)
library(seg)
library(spdep)
library(rJava)
library(xlsx)
library(maptools)
library(rgdal)
library(haven)
library(rvest)
library(data.table)

trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"\\GIS_edited\\",sep="")
city_name <- args[2]

#Bring in Points
  points_dbf_file<-paste(dir_path,city_name,"_1930_Points.dbf",sep="")
  Points<-read.dbf(points_dbf_file)
#Bring in Street Grid
  grid_dbf_file<-paste(dir_path,city_name,"_1930_stgrid.dbf",sep="")
  grid30<-read.dbf(grid_dbf_file)
  
#Street Name Change List from Steve Morse 
  #Bring In Street Name Change File
  is.odd <- function(x) x %% 2 != 0
  
  theurl<-paste("http://stevemorse.org/census/changes/",city_name,"Changes.htm", sep="")
  html<- read_html(theurl)
  List<-html_nodes(html, xpath= "//td")
  List2<-html_text(List)
  List3<-data.table(List2)
  List3$List2<-trim(gsub("[?,.,Â,*]", "", List3$List2, perl=T))
  List4<-List3[!apply(List3 == "", 1, all),]
  
  #Making rows bind if there is an odd number of rows
  temprow <- matrix(c(rep.int(NA,length(List4))),nrow=1,ncol=length(List4))
  newrow <- data.frame(temprow)
  colnames(newrow)<-colnames(List4)

  #List5<-ifelse(is.odd(nrow(List4)), as.data.frame(rbind(List4,newrow)),List4)
  #ifelse(is.odd(nrow(List4)), as.data.frame(rbind(List4,newrow)),List4)
  List5<-if(is.odd(nrow(List4))){
    data.frame(rbind(List4, newrow))
  } else {
    data.frame(rbind(List4))
  }

  Odd<-as.data.frame(List5[c(T,F),])
  Odd<-plyr::rename(Odd, c("List5[c(T, F), ]"="Old"))
  
  Even<-as.data.frame(List5[c(F,T),])
  Even<-plyr::rename(Even, c("List5[c(F, T), ]"="New"))
  
  new<-cbind(Odd, Even)
  write.csv(new, paste(dir_path,city_name,"_StName_Change.csv",sep=""))

#Microdata file
  mdata<-read.csv(paste(dir_path,city_name,"_1930_Addresses.csv",sep=""), stringsAsFactors = F)
  #Count how many people are on each unique street
  mdata$Person<-car::recode(mdata$city,"\" \"=0; else=1")
  cnt<-tapply(mdata$Person, INDEX=list(mdata$fullname), FUN=sum)
  cnttot<-data.frame(fullname=names(cnt), PPSt=cnt)
  mdata<-merge(x=mdata, y=cnttot, by="fullname", all.x=T)
  
#Count percent matched and percent tied
  Points$Person<-car::recode(mdata$city,"\" \"=0; else=1")
  Points$Match<-(ifelse(Points$Status=="M",1,0))
  Points$Tie<-(ifelse(Points$Status=="T",1,0))
  
  perp<-tapply(Points$Person, INDEX =list(Points$fullname), FUN=sum)
  perptot<-data.frame(fullname=names(perp), PCnt=perp)
  perm<-tapply(Points$Match, INDEX=list(Points$fullname), FUN=sum)
  permtot<-data.frame(fullname=names(perm), MCnt=perm)
  pert<-tapply(Points$Tie, INDEX = list(Points$fullname), FUN=sum)
  perttot<-data.frame(fullname=names(pert), TCnt=pert)
  
  perptot<-merge(x=perptot, y=permtot, by="fullname", all.x=T)
  perptot<-merge(x=perptot, y=perttot, by="fullname", all.x=T)
  perptot$PerMatch<-perptot$MCnt/perptot$PCnt
  perptot$PerTie<-perptot$TCnt/perptot$PCnt
  perptot$priority<-ifelse(perptot$PerMatch>=0.5, 1, 0)
  perptot$priority<-ifelse(perptot$priority==0 & perptot$PerTie>=0.5, 2, perptot$priority)
  
  #Add these values to mdata
  mdata<-merge(x=mdata, y=perptot[c("priority", "fullname")], by="fullname", all.x=T)

#Make variable names lowercase
  names(grid30)<-tolower(names(grid30))
  names(grid30)
  names(mdata)<-tolower(names(mdata))
  names(mdata)
  #Not convinced this makes sense to do as a rule (Hartford "new" street names are not always street names) - Chris
  "
  #Grab all old street names before they were changed
    old<-as.character(new$Old)
  #Grab all new street names after they were changed  
    newest<-new$New
  #Standard street grid name
    st<-as.character(grid30$fullname)
  
  grid30$old_st_name<-st %in% old
  grid30$new_st_name<-st %in% newest
  
  table(grid30$old_st_name) 
  table(grid30$new_st_name)
  "
#Keep Unique MicroData Street Names
  m_st<-subset(mdata, !duplicated(mdata$fullname))
  myvars<-c("fullname", "ed", "ppst", "priority")
  m_st<-m_st[myvars]
  m_st1<-as.character(m_st$fullname)
  grid<-subset(grid30, !duplicated(grid30$fullname))
  grid1<-as.character(grid$fullname)
  
#Marking streets in the microdata and also in the grid
  m_st$ingrid<-m_st1%in% grid1
  table(m_st$ingrid)
#Keep only streets in microdata, but not in grid
  m<-m_st[which(m_st$ingrid=="FALSE"),]
  #Add if there is evidence of a street name change either as an old street name or a new one.
    st<-as.character(m$fullname)
    #Grab all old street names before they were changed
    old<-as.character(new$Old)
    #Grab all new street names after they were changed  
    newest<-new$New
  
  m$old_name_evidence<-st %in% old
  m$new_name_evidence<-st %in% newest
  
  write.csv(m, paste(dir_path,city_name,"_Streets_To_Check.csv",sep=""))
  
#Marking Streets in the grid, but not in the microdata
  grid$indata<-grid1 %in% m_st1
  table(grid$indata)
  g<-grid[which(grid$indata=="FALSE"),]
  myvars<-c("fullname")
  g<-g[myvars]
  write.csv(g, paste(dir_path,city_name,"_Streets_InGrid_NotInMdata.csv",sep=""))

  