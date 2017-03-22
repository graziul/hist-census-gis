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
library(readstata13)

trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"\\GIS_edited\\",sep="")
city_name <- args[2]
file_name <- args[3]
state_abbr <- args[4]

#Bring in New 1930 Street Grid
  library(shapefiles)
  grid30<-readOGR(paste(dir_path,city_name,"_1930_stgrid.shp",sep=""))
  detach("package:shapefiles", unload=TRUE)
  
#Bring in Clean Microdata File  
  mdata<-read.dta13(file_name)
  names(mdata)<-tolower(names(mdata))
  vars<-c("autostud_street", "ed", "type", "block","hn")
  mdata<-mdata[vars]
  mdata<-plyr::rename(mdata, c(block="Mblk", autostud_street="fullname"))
  mdata$state<-state_abbr
  mdata$city<-city_name
  mdata$address<-paste(mdata$hn, mdata$fullname, sep=" ")
  
#Street Name Change List from Steve Morse
  change<-read.csv(paste(dir_path,city_name,"_StName_Change.csv",sep=""))
  change$New<-trim(gsub("[*]", "", change$New, perl=T))  

#Make variable names lowercase and Change Type to String
  names(grid30)<-tolower(names(grid30))
  names(mdata)<-tolower(names(mdata))

#Add State and City to New Streets from Edited Grid - This Helps in Geocoding Later
  grid30$state<-ifelse(is.na(grid30$state), state_abbr, as.character(grid30$state))
  grid30$city<-ifelse(is.na(grid30$city), city_name, as.character(grid30$city))
  
#Add Street Ranges to New Streets & Streets 
  grid30$addrange<-ifelse(is.na(grid30$ltoadd) & is.na(grid30$lfromadd) 
                          & is.na(grid30$rtoadd) & is.na(grid30$rfromadd) 
                          & is.na(grid30$state) & is.na(grid30$fullname), 1, 0)
  grid_nochange<-subset(grid30, grid30$addrange==0)
  grid_change<-subset(grid30, grid30$addrange==1)
    #Check streets in 'grid_change' to make sure they also do not appear in 'grid_nochange'. This
    #indicates that a street segment was added to the grid and not an entirely new street.
    nochange<-as.character(grid_nochange$fullname)
    change<-as.character(grid_change$fullname)
    grid_change$st_exist<-change %in% nochange
    
    #These are the streets for which ranges will be added.
    addranges<-subset(grid_change, grid_change$st_exist==0)
    addranges<-as.character(addranges$fullname)

  #Grab House Numbers from microdata streets to form min/max ranges
    m<-as.character(mdata$fullname)
    mdata$range<-m %in% addranges
    mdata<-subset(mdata, mdata$range=="TRUE")

    #Adding Variable to Original Grid File to indicate which streets ultimately have new ranges
    m<-as.character(mdata$fullname)
    grid30_names<-as.character(grid30$fullname)
    grid30$new_range<-grid30_names %in% m
    
    #Create odd and even hn's
    is.odd <- function(x) x %% 2 != 0
    is.even <- function(x) x %% 2 == 0
    
    mdata$hn_odd<-ifelse(is.odd(mdata$hn), mdata$hn, NA)
    mdata$hn_even<-ifelse(is.even(mdata$hn), mdata$hn, NA)
    
    #Mark Maximum and minimum house number in street by odd and even
    maxodd<-tapply(mdata$hn_odd, INDEX=list(mdata$fullname), FUN=max, na.rm=T)
    maxodd2<-data.frame(fullname=names(maxodd), max_odd=maxodd)
    
    maxeven<-tapply(mdata$hn_even, INDEX=list(mdata$fullname), FUN=max, na.rm=T)
    maxeven2<-data.frame(fullname=names(maxeven), max_even=maxeven)
    
    minodd<-tapply(mdata$hn_odd, INDEX=list(mdata$fullname), FUN=min, na.rm=T)
    minodd2<-data.frame(fullname=names(minodd), min_odd=minodd)
    
    mineven<-tapply(mdata$hn_even, INDEX=list(mdata$fullname), FUN=min, na.rm=T)
    mineven2<-data.frame(fullname=names(mineven), min_even=mineven)
    
    mdata<-merge(x=mdata, y=maxodd2, by="fullname")
    mdata<-merge(x=mdata, y=maxeven2, by="fullname")
    mdata<-merge(x=mdata, y=minodd2, by="fullname")
    mdata<-merge(x=mdata, y=mineven2, by="fullname")
    
    #Delete Inf and -Inf from data as this is a product of calculation on missing
    mdata$max_odd<-ifelse((mdata$max_odd==Inf | mdata$max_odd==-Inf), NA, mdata$max_odd) 
    mdata$max_even<-ifelse((mdata$max_even==Inf | mdata$max_even==-Inf), NA, mdata$max_even) 
    mdata$min_odd<-ifelse((mdata$min_odd==Inf | mdata$min_odd==-Inf), NA, mdata$min_odd) 
    mdata$min_even<-ifelse((mdata$min_even==Inf | mdata$min_even==-Inf), NA, mdata$min_even) 
    
    #Keep only one unique street
    mdata<-subset(mdata, !duplicated(mdata$fullname))    
    mdata<-plyr::rename(mdata, c(min_even="lfromadd", max_even="ltoadd", min_odd="rfromadd", max_odd="rtoadd"))
    
    #Keep Only variables to join to stgrid
    myvar<-c("fullname", "lfromadd", "ltoadd", "rfromadd", "rtoadd")
    mdata<-mdata[myvar]
    
    #Change all to character including 'fullname'
    grid30$lfromadd<-as.character(grid30$lfromadd)
    mdata$lfromadd<-as.character(mdata$lfromadd)
    
    grid30$ltoadd<-as.character(grid30$ltoadd)
    mdata$ltoadd<-as.character(mdata$ltoadd)
    
    grid30$rfromadd<-as.character(grid30$rfromadd)
    mdata$rfromadd<-as.character(mdata$rfromadd)
    
    grid30$rtoadd<-as.character(grid30$rtoadd)
    mdata$rtoadd<-as.character(mdata$rtoadd)
    
    grid30$fullname<-as.character(grid30$fullname)
    mdata$fullname<-as.character(mdata$fullname)
    
    #Order by fullname
      grid30<-grid30[order(grid30$fullname),]
      mdata<-mdata[order(mdata$fullname),]
    
    grid30_nochange<-subset(grid30, grid30$new_range=="FALSE")
    grid30_change<-subset(grid30, grid30$new_range=="TRUE")
    
    grid30_change$lfromadd<-ifelse(grid30_change$fullname==mdata$fullname, mdata$lfromadd, grid30_change$lfromadd)
    grid30_change$ltoadd<-ifelse(grid30_change$fullname==mdata$fullname, mdata$ltoadd, grid30_change$ltoadd)
    grid30_change$rfromadd<-ifelse(grid30_change$fullname==mdata$fullname, mdata$rfromadd, grid30_change$rfromadd)
    grid30_change$rtoadd<-ifelse(grid30_change$fullname==mdata$fullname, mdata$rtoadd, grid30_change$rtoadd)
    
    new_grid<-rbind(grid30_nochange, grid30_change)
    
    #Export Map
    dir_path_export<-substr(dir_path,1,nchar(dir_path)-1)
    writeOGR(new_grid, dsn=dir_path_export,layer=paste(city_name,"_1930_stgrid_edit",sep=""), driver="ESRI Shapefile", overwrite_layer = TRUE)
    