chooseCRANmirror(ind=1)
list.of.packages <- c("Hmisc","DataCombine","readstata13","gmodels","foreign","car","plyr","dplyr","seg","reshape","reshape2","maptools","rgdal","rJava","xlsx","magrittr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

#Load Neccessary Libraries
  library(Hmisc)
  library(DataCombine)
  library(readstata13)
  library(gmodels)
  library(foreign)
  library(car)
  library(plyr)
  library(dplyr)
  library(seg)
  library(reshape)
  library(reshape2)
  library(maptools)
  library(rgdal)
  library(magrittr)

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"\\GIS_edited\\",sep="")
city_name <- args[2]
city_name <- gsub(" ","",city_name)
decade <- args[3]

#Functions used:
trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}

shift<-function(x,shift_by){
  stopifnot(is.numeric(shift_by))
  stopifnot(is.numeric(x))
  
  if (length(shift_by)>1)
    return(sapply(shift_by,shift, x=x))
  
  out<-NULL
  abs_shift_by=abs(shift_by)
  if (shift_by > 0 )
    out<-c(tail(x,-abs_shift_by),rep(0,abs_shift_by))
  else if (shift_by < 0 )
    out<-c(rep(0,abs_shift_by), head(x,-abs_shift_by))
  else
    out<-x
  out
}

#Bring in microdata points
  Points<-read.dbf(paste(dir_path,city_name,"_",decade,"_Pblk_Points.dbf",sep="")) # This was "Pblk_Points_2.dbf" but we're skipping Steps 6 and 7 currently
#Make variable names lowercase
  names(Points)<-tolower(names(Points))
  names(Points)
  
#Create Unique Household (Address) Indicator
  Points$build_id<-plyr::id(Points[c("hn","fullname")], drop=F)

#Keep only Unique Addresses
  Blocks<-subset(Points, !duplicated(Points$build_id))

#Generate mblk (all NA for some reason) using ed_block (generated in previous steps)
  Split <- strsplit(as.character(Blocks$ed_block),"-",fixed=TRUE)
  Blocks$mblk <- as.numeric(sapply(Split,"[",2))

#Keep variables needed  
  myvars<-c("ed", "mblk", "pblk_id", "build_id")
  Blocks<-Blocks[myvars]

#Create Unique Microdata Block/ED Ids - Blocks$ed_block - is from microdata
  Blocks<-Blocks[order(Blocks$pblk_id),]
  Blocks$ed_block<-paste(Blocks$ed, Blocks$mblk, sep="-")

#Create Unique Physical Block-ED_Block Ids
  Blocks$Unique<-plyr::id(Blocks[c("ed_block","pblk_id")], drop=T)  
  
#Adds a variable with the number 1 used to enumerate values throughout code
  Blocks$Build<-car::recode(Blocks$build_id,"\" \"=0; else=1")

#Remove pblk_id with '0';
  Blocks<-Blocks[which(Blocks$pblk_id!=0),]
  
#Remove mblk with NA;
  Blocks<-Blocks[which(!is.na(Blocks$mblk)),]
  
#Count Number of Unique Ed_Blocks (Microdata combinations of ED and Block #)
  EdCt<-tapply(Blocks$Build, INDEX=list(Blocks$ed_block), FUN=sum)
  Ed_Count<-data.frame(ed_block=names(EdCt), Ed_Count=EdCt)
  Blocks<-merge(x=Blocks, y=Ed_Count, by="ed_block", all.x=T)

#Count Number of Unique Pblks (Physical Blocks from Shapefile)
  PblkCt<-tapply(Blocks$Build, INDEX=list(Blocks$pblk_id), FUN=sum)
  Pblk_Count<-data.frame(pblk_id=names(PblkCt), Pblk_Count=PblkCt)
  Blocks<-merge(x=Blocks, y=Pblk_Count, by="pblk_id", all.x=T)

#Count Number of Unqiue Ed_Block and Pblk Combinations
  Combo<-tapply(Blocks$Build, INDEX=list(Blocks$Unique), FUN=sum)
  Combos<-data.frame(Unique=names(Combo), TotCombos=Combo)
  Blocks<-merge(x=Blocks, y=Combos, by="Unique", all.x=T)

#Name Change - M_Count - Microdata count; P_Count - Physical count
  Blocks<-plyr::rename(Blocks, c(Ed_Count="M_Count", Pblk_Count="P_Count"))

#Percentage Matching MicroBlocks
  Blocks$PerMblk<-(Blocks$TotCombos/Blocks$M_Count)*100

#Percentage Matching PhysicalBlocks
  Blocks$PerPblk<-(Blocks$TotCombos/Blocks$P_Count)*100

#Convert variables into proper format
  Blocks$ed_block<-as.character(Blocks$ed_block)
  Blocks$M_Count<-as.numeric(Blocks$M_Count)
  Blocks$P_Count<-as.numeric(Blocks$P_Count)
  Blocks$TotCombos<-as.numeric(Blocks$TotCombos)
  Blocks$PerMblk<-as.numeric(Blocks$PerMblk)
  Blocks$PerPblk<-as.numeric(Blocks$PerPblk)

#Marks the maximum proportion in the M and P block.
  Mblk<-tapply(Blocks$PerMblk, INDEX=list(Blocks$ed_block), FUN=max)
  Mblk2<-data.frame(ed_block=names(Mblk), MMax=Mblk)
  Blocks<-merge(x=Blocks, y=Mblk2, by="ed_block", all.x=T)
  
  Pblk<-tapply(Blocks$PerPblk, INDEX=list(Blocks$pblk_id), FUN=max)
  Pblk2<-data.frame(pblk_id=names(Pblk), PMax=Pblk)
  Blocks<-merge(x=Blocks, y=Pblk2, by="pblk_id", all.x=T)

#Keep unique MBlock - PBlock Combos
  #Create sequence for all mblock-pblock combos
  Blocks$SeqCombo<-with(Blocks, ave(Blocks$Unique, Blocks$Unique, FUN = seq_along))
  Blocks$SeqCombo<-as.numeric(Blocks$SeqCombo)

#New Dataset
  Combo<-Blocks[which(Blocks$SeqCombo==1),]

#How many unique microdata blocks are in physical blocks
  Combo$SeqCombo2<-with(Combo, ave(Combo$pblk_id, Combo$pblk_id, FUN = seq_along))
  Combo$SeqCombo2<-as.numeric(Combo$SeqCombo2)
  Seq<-tapply(Combo$SeqCombo2, INDEX=list(Combo$pblk_id), FUN=max)
  Seq2<-data.frame(pblk_id=names(Seq), SeqMax=Seq)
  Combo<-merge(x=Combo, y=Seq2, by="pblk_id", all.x=T)

#Create The matches
  Combo$One<-ifelse(Combo$M_Count<=2, "Yes", "No")
  Combo$Match75<-ifelse(Combo$PerMblk>=70 & Combo$PerPblk>=100 & Combo$One=="No", "Yes", "No")
  Combo$MBID<-ifelse(Combo$PerMblk==100 & Combo$PerPblk==100 & Combo$One=="No", Combo$ed_block, NA)
  Combo$MBID2<-ifelse((is.na(Combo$MBID) & Combo$Match75=="Yes"), Combo$ed_block, NA)
  Combo$MBID3<-ifelse(is.na(Combo$MBID) & is.na(Combo$MBID2) & Combo$PerMblk>=70 & Combo$PerPblk>=70
                                                & Combo$One=="No", Combo$ed_block, NA)

  #Flag where the Physical Block has less than a majority of one microdata id within it.
    Combo$PBflag<-ifelse(Combo$PMax<=49.99, 1, 0)
    
  #Replace missing values in group
    Choice_1<-inner_join(Combo["pblk_id"], Combo[!is.na(Combo$MBID) | !is.na(Combo$MBID2) | !is.na(Combo$MBID3),], by="pblk_id") %>% mutate(id=row_number()) %>% 
      select(pblk_id, ed, Unique, build_id, M_Count, P_Count, TotCombos, PerMblk, PerPblk, MMax, PMax, MBID, MBID2, MBID3, PBflag)
    Choice_1<-subset(Choice_1, !duplicated(Choice_1$pblk_id))
    Choice_2<-inner_join(Combo["pblk_id"], Combo[is.na(Combo$MBID) & is.na(Combo$MBID2) & is.na(Combo$MBID3) & !(Combo$pblk_id %in% Choice_1$pblk_id),],
                         by="pblk_id") %>% mutate(id=row_number()) %>% 
      select(pblk_id, ed, Unique, build_id, M_Count, P_Count, TotCombos, PerMblk, PerPblk, MMax, PMax, MBID, MBID2, MBID3, PBflag)
    Choice_2<-subset(Choice_2, !duplicated(Choice_2$pblk_id))
    
    BlockC<-rbind(Choice_1, Choice_2)
    
#Attach to Original Shapefile
    library(shapefiles)
    BlockMap<-readOGR(paste(dir_path,city_name,"_",decade,"_Pblk.shp",sep=""))
    names(BlockMap)<-tolower(names(BlockMap))
    detach("package:shapefiles", unload=TRUE)

#Merge
  BlockMap<-merge(x=BlockMap, y=BlockC, by="pblk_id", all.x=TRUE)
    
#Add Field where First Edits Will Occur
  BlockMap$FirstE<-BlockMap$MBID
  BlockMap$FirstE<-ifelse(is.na(BlockMap$FirstE) & is.na(BlockMap$MBID) & !is.na(BlockMap$MBID2),
                        BlockMap$MBID2, BlockMap$FirstE)
  BlockMap$FirstE<-ifelse(is.na(BlockMap$FirstE) & is.na(BlockMap$MBID) & is.na(BlockMap$MBID2)
                          & !is.na(BlockMap$MBID3), BlockMap$MBID3, BlockMap$FirstE)
  BlockMap$Edit_1<-BlockMap$FirstE

#Mark Block ID with Choices in the Physical Block Map
  pblk_id<-BlockC$pblk_id
  pblk_map<-BlockMap$pblk_id
  BlockMap$inmap<-ifelse(pblk_map %in% pblk_id, 1, 0)

#Export Map
  dir_path_export<-substr(dir_path,1,nchar(dir_path)-1)
  writeOGR(BlockMap, dsn=dir_path_export,layer=paste(city_name,"_",decade,"_block_geo",sep=""), driver="ESRI Shapefile", overwrite_layer = TRUE)
  
#########################################
  