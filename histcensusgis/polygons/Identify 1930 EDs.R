chooseCRANmirror(ind=1)
list.of.packages <- c("Hmisc","DataCombine","readstata13","gmodels","foreign","car","plyr","seg","reshape","reshape2","maptools","rgdal","shapefiles")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

#Load Neccessary Libraries
library(Hmisc)
library(foreign)
library(DataCombine)
library(readstata13)
library(gmodels)
library(foreign)
library(car)
library(plyr)
library(seg)
library(reshape)
library(reshape2)
library(maptools)
library(rgdal)
library(shapefiles)
#library(rJava)
#library(xlsx) 

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"\\GIS_edited\\",sep="")
city_name <- args[2]
decade <- args[3]

#Functions used:
trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}

#Bring in microdata points
  dbf_file<-paste(dir_path,city_name,"_",decade,"_Pblk_Points.dbf",sep="")
  Points<-read.dbf(dbf_file)$dbf
  tot_points<-length(Points[,1])  
#Make variable names lowercase
  names(Points)<-tolower(names(Points))
  names(Points)
#Delete points not geocoded
  Points<-Points[which(Points$status!="U"),]
  geocoded_points<-length(Points[,1])
#Report number of geocoded points
  print(paste(geocoded_points," of ",tot_points," (",round(100*geocoded_points/tot_points,1),"%) points geocoded",sep=""))
  
#Create Unique Household (Address) Indicator
  Points$build_id<-plyr::id(Points[c("hn","fullname")], drop=F)
  
#Keep only Unique Addresses
  EDs<-subset(Points, !duplicated(Points$build_id))
  
#Keep variables needed  
  myvars<-c("ed", "pblk_id", "build_id")
  EDs<-EDs[myvars]

#Create Unique Physical Block-ED_Block Ids
  EDs$Unique<-plyr::id(EDs[c("ed","pblk_id")], drop=T)  
  
#Adds a variable with the number 1 used to enumerate values throughout code
  EDs$one<-car::recode(EDs$ed,"\" \"=0; else=1")
  if (is.factor(EDs$one)==TRUE) {
  EDs$one<-as.numeric(levels(EDs$one))[EDs$one]
  }
  
#Remove pblk_id with '0';
  EDs<-EDs[which(EDs$pblk_id!=0),]
  
#Remove mblk with NA;
  EDs<-EDs[which(!is.na(EDs$ed)),]
  
#Count Number of Unique Eds (Microdata combinations of ED and Block #)
  EdCt<-tapply(as.numeric(EDs$one), INDEX=list(EDs$ed), FUN=sum)
  Ed_Count<-data.frame(ed=names(EdCt), Ed_Count=EdCt)
  EDs<-merge(x=EDs, y=Ed_Count, by="ed", all.x=T)
  
#Count Number of Unique Pblks (Physical Blocks from Shapefile)
  PblkCt<-tapply(EDs$one, INDEX=list(EDs$pblk_id), FUN=sum)
  Pblk_Count<-data.frame(pblk_id=names(PblkCt), Pblk_Count=PblkCt)
  EDs<-merge(x=EDs, y=Pblk_Count, by="pblk_id", all.x=T)
  
#Count Number of Unqiue EDs and Pblk Combinations
  Combo<-tapply(as.numeric(EDs$one), INDEX=list(EDs$Unique), FUN=sum)
  Combos<-data.frame(Unique=names(Combo), TotCombos=Combo)
  EDs<-merge(x=EDs, y=Combos, by="Unique", all.x=T)
  
#Percentage Matching PhysicalBlocks
  EDs$PerPblk<-(EDs$TotCombos/EDs$Pblk_Count)*100
  
#Convert variables into proper format
  EDs$Ed_Count<-as.numeric(EDs$Ed_Count)
  EDs$Pblk_Count<-as.numeric(EDs$Pblk_Count)
  EDs$TotCombos<-as.numeric(EDs$TotCombos)
  EDs$PerPblk<-as.numeric(EDs$PerPblk)
  
##Marks the maximum proportion in the P block.
  Pblk<-tapply(EDs$PerPblk, INDEX=list(EDs$pblk_id), FUN=max)
  Pblk2<-data.frame(pblk_id=names(Pblk), PMax=Pblk)
  EDs<-merge(x=EDs, y=Pblk2, by="pblk_id", all.x=T)
  
#Keep unique MBlock - PBlock Combos
  EDs$SeqCombo<-with(EDs, ave(EDs$Unique, EDs$Unique, FUN = seq_along))
  EDs$SeqCombo<-as.numeric(EDs$SeqCombo)
  
#New Dataset
  Combo<-EDs[which(EDs$SeqCombo==1),]
  
#How many microdata EDs are in physical blocks
  Combo$SeqCombo2<-with(Combo, ave(Combo$pblk_id, Combo$pblk_id, FUN = seq_along))
  Combo$SeqCombo2<-as.numeric(Combo$SeqCombo2)
  Seq<-tapply(Combo$SeqCombo2, INDEX=list(Combo$pblk_id), FUN=max)
  Seq2<-data.frame(pblk_id=names(Seq), SeqMax=Seq)
  Combo<-merge(x=Combo, y=Seq2, by="pblk_id", all.x=T)
  
#Create The matches      
  Combo$ED_ID1a<-ifelse(Combo$PerPblk==100, Combo$ed, NA)
  Combo$ED_ID2a<-ifelse((is.na(Combo$ED_ID1a) & Combo$PerPblk>=75), Combo$ed, NA)
  Combo$ED_ID3a<-ifelse((is.na(Combo$ED_ID1a) & (is.na(Combo$ED_ID2a)) & Combo$PerPblk==Combo$PMax), Combo$ed, NA)

#Attach data to all fields if dupliated so we can only have one ed per phyiscal block  
  ID1<-tapply(Combo$ED_ID1a, INDEX=list(Combo$pblk_id), FUN=max, na.rm=T)
  ID_1<-data.frame(pblk_id=names(ID1), ED_ID=ID1)
  Combo<-merge(x=Combo, y=ID_1, by="pblk_id", x.all=T)
  
  ID2<-tapply(Combo$ED_ID2a, INDEX=list(Combo$pblk_id), FUN=max, na.rm=T)
  ID_2<-data.frame(pblk_id=names(ID2), ED_ID2=ID2)
  Combo<-merge(x=Combo, y=ID_2, by="pblk_id", x.all=T)

  ID3<-tapply(Combo$ED_ID3a, INDEX=list(Combo$pblk_id), FUN=max, na.rm=T)
  ID_3<-data.frame(pblk_id=names(ID3), ED_ID3=ID3)
  Combo<-merge(x=Combo, y=ID_3, by="pblk_id", x.all=T)
  
  #Delete Inf and -Inf from data as this is a product of calculation on missing
  Combo$ED_ID<-ifelse((Combo$ED_ID==Inf | Combo$ED_ID==-Inf), NA, Combo$ED_ID)
  Combo$ED_ID2<-ifelse((Combo$ED_ID2==Inf | Combo$ED_ID2==-Inf), NA, Combo$ED_ID2)
  Combo$ED_ID3<-ifelse((Combo$ED_ID3==Inf | Combo$ED_ID3==-Inf), NA, Combo$ED_ID3)
  
#Keep Variables
  myvars<-c("pblk_id", "ed", "PerPblk", "PMax", "ED_ID", "ED_ID2", "ED_ID3")
  Combo<-Combo[myvars]
  
#Flag where the Physical Block has less than a majority of one microdata id within it.
  Combo$PBflag<-ifelse(Combo$PMax<=49.99, 1, 0)

#Keep only unique block numbers
  Combo<-subset(Combo, !duplicated(Combo$pblk_id))
  
#WRITE FILE  
  write.csv(Combo, file=paste(dir_path,city_name,"_",decade,"_ED_Choices.csv",sep=""), row.names=F)
  
#Attach to Original Shapefile
  library(shapefiles)
  BlockMap<-readOGR(paste(dir_path,city_name,"_",decade,"_Pblk.shp",sep=""))
  names(BlockMap)<-tolower(names(BlockMap))
  detach("package:shapefiles", unload=TRUE)
  
#Merge Final Results to Shapefile
  #Quality Assurance Check
    Combo<-Combo[order(Combo$pblk_id),]
    pblk_id<-Combo$pblk_id
    pblk_map<-BlockMap$pblk_id
    Combo$inmap<-pblk_id %in% pblk_map
    print(table(Combo$inmap))
  #Merge
    BlockMap<-merge(x=BlockMap, y=Combo, by="pblk_id", all.x=TRUE)
    
#Add Field where First Edits Will Occur
  BlockMap$FirstE<-BlockMap$ED_ID
  BlockMap$FirstE<-ifelse(is.na(BlockMap$FirstE) & is.na(BlockMap$FirstE) & !is.na(BlockMap$ED_ID2),
                          BlockMap$ED_ID2, BlockMap$FirstE)
  
#Make Variables have proper format
  BlockMap$PMax<-as.numeric(BlockMap$PMax)
  BlockMap$ED_ID<-as.numeric(BlockMap$ED_ID)
  BlockMap$ED_ID2<-as.numeric(BlockMap$ED_ID2)
  BlockMap$ED_ID3<-as.numeric(BlockMap$ED_ID3)
  BlockMap$PBflag<-as.numeric(BlockMap$PBflag)
  BlockMap$FirstE<-as.numeric(BlockMap$FirstE)
  
  #Export Map
  dir_path_export<-substr(dir_path,1,nchar(dir_path)-1)
  writeOGR(obj=BlockMap, dsn=dir_path_export, layer=paste(city_name,"_",decade,"_ed_geo",sep=""), driver="ESRI Shapefile",overwrite_layer = TRUE)
  