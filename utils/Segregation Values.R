#Library List
  library(foreign)
  library(car)
  library(readstata13)
  library(plyr)
  library(seg)
  library(reshape)
  library(reshape2)
  library(rJava)
  library(xlsx)
  library(maptools)
  library(rgdal)
  library(haven)

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
  
  
  citylist<-read.csv(("Z:/Projects/Preparing 1880 Files/City Lists.csv"))
  citylist <- data.frame(lapply(citylist, as.character), stringsAsFactors=FALSE)
  #citylist<-subset(citylist, (citylist$Maps=="x"))
  
  Cityname<-citylist$Cityname
  Seg_ID<-citylist$Seg_ID
  Ex<-citylist$Ex
  SG<-citylist$SG
  Seg<-citylist$Seg
  hex150<-citylist$hex150
  hex225<-citylist$hex225
  Seg_ID<-citylist$Seg_ID
  seg_id1<-citylist$Seg_ID_1
  seggrid<-citylist$SegGrID
  seggrid_1<-citylist$SegGrID_1
  rows<-nrow(citylist)
  
  AllSegTable<-data.frame(City=character(), IsoHouse_g=numeric(), IsoBLD_g=numeric(), IsoSegside_g=numeric(),  
                          IsoSeg_g=numeric(), IsoOverSegG_g=numeric(), IsoOverEG_g=numeric(), IsoED_g=numeric(),IsoCity_g=numeric(),
                          IsoHouse_i=numeric(), IsoBLD_i=numeric(), IsoSegside_i=numeric(), IsoSeg_i=numeric(), IsoOverSegG_i=numeric(),
                          IsoOverEG_i=numeric(),IsoED_i=numeric(), IsoCity_i=numeric())
  
for(i in 1:40){
  tryCatch({
    Segment<-read.dta13(paste("Z:/Projects/Preparing 1880 Files/", Cityname[i],"/Match Address/", Cityname[i],".dta", sep=""))
    Points<-read.dta13(paste("Z:/Projects/1880Data/MicroData For Publication/", Cityname[i],".dta",sep=""))
    Off<-read.dbf(paste("Z:/Projects/Preparing 1880 Files/", Cityname[i], "/Off Street/", Cityname[i],"_OffStreet.dbf", sep=""))
    
    #Fix Names in Segment File
    names(Segment)<-tolower(names(Segment))
    Segment$serial<-as.character(Segment$serial)
    Segment<-subset(Segment, !duplicated(Segment$serial))
    ifelse(exists("street.1", where=Segment), (Segment$street_stnum=Segment$street.1), (Segment$street_stnum=Segment$street))
    
    #Make Changes to 'Off' data
    names(Off)<-tolower(names(Off))    
    Off<- data.frame(lapply(Off, as.character), stringsAsFactors=FALSE)

    Off<-subset(Off, !duplicated(Off$serial))
    Off$serial<-as.numeric(Off$serial)
    Off$nhn<-trim(laply(strsplit(as.character(Off$addr_match), split=" "), "[", 1))
    Off$street<-trim(laply(strsplit(as.character(Off$addr_match), split=","), "[", 1))
    Off$street<-trim(gsub("^[0-9]* ","",Off$street, perl=T))
  
    #Tag Unique Streets and Housenumbers - I.E. BUILDINGS
    Off<-Off[order(Off$street,Off$nhn),]
    Off$stnum_id<-id(Off[c("street","nhn")], drop=T)
    
    #Fix names in Points file
    names(Points)<-tolower(names(Points))
    ifelse(exists("bpldet", where=Points), (Points$bpldet=Points$bpldet), (Points$bpldet=Points$bp))
    ifelse(exists("fbpldtus", where=Points), (Points$fbpldtus=Points$fbpldtus), (Points$fbpldtus=Points$fbp))
    ifelse(exists("mbpldtus", where=Points), (Points$mbpldtus=Points$mbpldtus), (Points$mbpldtus=Points$mbp))
    Points$serial<-as.character(Points$serial)
    Points$bpldet<-as.character(Points$bpldet)
    Points$fbpldtus<-as.character(Points$fbpldtus)
    Points$mbpldtus<-as.character(Points$mbpldtus)
    
    All<-merge(Points[,c("bpldet", "fbpldtus", "mbpldtus","race","relate","age","occ50us","labforce","serial","enumdist")],
               Segment[,c("serial", "side", "segment_id", "building_id", "house_number", "street_stnum")], by="serial")
    #Trim leading zeros to match with OffStreet File
    All$serial<-as.numeric(All$serial)
    All<-merge(All, Off[,c("serial", "nhn", "stnum_id", "street")], by="serial", all.x=T)
    
    #Tag Unique Sides and Segments
      All$segside<-id(All[c("segment_id","side")], drop=T)
    #Create City Name Field
      All$City<-Cityname[i]
    #Create Person Counter for Aggregation  
      All$Person<-recode(All$serial,"\" \"=0; else=1")
      All<-subset(All, All$segment_id!=0)
    #Create Dummy of 18 Plus
      All$Above18<-recode(All$age,"c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,NA)=0; else=1")
    #Create Head of Household Variable
      All$hh<-recode(All$relate,"c(101)=1; else=0")
    #Unrelated Individuals
      All$UnRelate<-recode(All$relate,"c(1200,1202,1203,1204,1205,1206,1221,1222,1223,1230,1239)=1; else=0")
    #Servants
    #All$Serve<-recode(All$relate,"1210:1217=1; else=0")
      All$Serve2<-recode(All$occ50us, "700:720=1; else=0")
    #Unrelated and Over 18
      All$UnRelate18<-ifelse(All$UnRelate==1 & All$Above18==1,1,0)
    #Race
      All$race<-car::recode(All$race, "100='white';c(200, 210)='black';300='American Indian/Alaska Native';
                               400='Chinese';500='Japanese';else='Missing'")  
    #Birthplace
      bpl<-read.csv("Z:/Projects/Preparing 1880 Files/BPL_Codes.csv", stringsAsFactors = F)
      All<-merge(All, bpl[,c("Code", "Label")], by.x="bpldet", by.y="Code", all.x=T)
      All<-rename(All, c("Label"="BPL"))
    #Father's Birthplace
      fbpl<-read.csv("Z:/Projects/Preparing 1880 Files/FBPL_Codes.csv", stringsAsFactors = F)
      All<-merge(All, fbpl[,c("Code", "Label")], by.x="fbpldtus", by.y="Code", all.x=T)
      All<-rename(All, c("Label"="FBPL"))
    #Mother's Birthplace
      mbpl<-read.csv("Z:/Projects/Preparing 1880 Files/MBPL_Codes.csv", stringsAsFactors = F)
      All<-merge(All, mbpl[,c("Code", "Label")], by.x="mbpldtus", by.y="Code", all.x=T)
      All<-rename(All, c("Label"="MBPL"))
    #Native Born
      All$bpldet<-as.numeric(All$bpldet)
      All$native_b<-ifelse(All$bpldet<=9900, 1, 0)
    #Native Parents
      All$mbpldtus<-as.numeric((All$mbpldtus))
      All$fbpldtus<-as.numeric((All$fbpldtus))
      All$native_p<-ifelse(All$mbpldtus<=9900 | All$fbpldtus<=9900, 1, 0)
    #Native Born and Native Born Parents
      All$native_bp<-ifelse(All$native_b==1 & All$native_p==1, 1,0)
    #Native Born, Native Parents, White
      All$native_white<-ifelse(All$native_bp==1 & All$race=="white", 1, 0)
      
    #Germans (_f=first generation; _s=second generation; _t=total)
      #Disregard any person who has a mother that is Irish
      All$german_f<-ifelse((All$bpldet>=45300 & All$bpldet<=45362), 1,0)
      All$german_s<-ifelse(All$native_b==1 & ((All$mbpldtus>=45300 & All$mbpldtus<=45362) | 
                                              (All$fbpldtus>=45300 & All$fbpldtus<=45362)) & 
                                              (All$fbpldtus!=41400 | All$fbpldtus!=41410),1,0)
      #######Make Change to German Definition Here #####
      #All$german<-ifelse(All$german_f==1 | All$german_s==1, 1, 0)
      All$german<-ifelse(All$german_f==1, 1, 0)
      
    #Irish (_f=first generation; _s=second generation; _t=total)
      #Disregard any person who has a mother that is German
      All$irish_f<-ifelse((All$bpldet==41400 | All$bpldet==41410),1,0)
      All$irish_s<-ifelse(All$native_b==1 & ((All$mbpldtus==41400 | All$mbpldtus==41410) |
                                              (All$fbpldtus==41400 | All$fbpldtus==41410)) &
                                              (All$fbpldtus!=45300 | All$fbpldtus!=45362),1,0)
      #######Make Change to German Definition Here #####
      #All$irish<-ifelse(All$irish_f==1 | All$irish_s==1, 1, 0)
      All$irish<-ifelse(All$irish_f==1, 1, 0)
    #Keep only adults      
      All<-All[which(All$Above18==1),]
      
      t<-data.frame(table(All$german))
      All$german_t<-t[2,2]
      
      t<-data.frame(table(All$irish))
      All$irish_t<-t[2,2]

      #This shapefile has a list of segment ID's and their corresponding segments in the group.
      #Seg_ID_1 is the group id which gets dissolved.
      #Seg_ID is the segment that is part of each group.  So if there is seg_id=10, that means that segment id 10 is in
      #all of the segment groups listed in Seg_ID_1
      OverSeg_Join<-read.dbf(paste("Z:/Users/_Exchange/1880 Stuff/AllCities/",Cityname[i],"/",Cityname[i],"_OverSeg_Join.dbf", sep=""))
      names(OverSeg_Join)<-tolower(names(OverSeg_Join))
      OverSeg_Join$SegGrID<-eval(parse(text=(paste("OverSeg_Join$",seg_id1[i],sep=""))))
      OverSeg_Join$SegmentID<-eval(parse(text=(paste("OverSeg_Join$",Seg_ID[i],sep=""))))
      myvars<-c("SegmentID", "SegGrID")
      OverSeg_Join<-OverSeg_Join[myvars]
      OverSeg_Join$City<-Cityname[i]
      
      #This shapefile has a list of all segment group ID's and their corresponding segment groups in the extended segment group
      #SegGrID is the segment group id.  This value is repeated indicating the unique extended segment groups
      #that this segment group is part of.
      #SegGrID_1 is the focal segment group.
      ExtSeg_Join<-read.dbf(paste("Z:/Users/_Exchange/1880 Stuff/AllCities/",Cityname[i],"/",Cityname[i],"_ExtSeg_Join2.dbf", sep=""))
      names(ExtSeg_Join)<-tolower(names(ExtSeg_Join))
      ExtSeg_Join$ExtSegGrID<-eval(parse(text=(paste("ExtSeg_Join$",seggrid_1[i],sep=""))))
      ExtSeg_Join$SegGrID<-eval(parse(text=(paste("ExtSeg_Join$",seggrid[i],sep=""))))
      myvars<-c("ExtSegGrID","SegGrID")
      ExtSeg_Join<-ExtSeg_Join[myvars]
      ExtSeg_Join$City<-Cityname[i]
      
      Overlap<-merge(OverSeg_Join[,c("SegmentID", "SegGrID")], ExtSeg_Join, by="SegGrID", all=T)
      Overlap<-Overlap[order(Overlap$SegmentID),]
      Overlap2<-aggregate(Overlap$SegmentID, by=Overlap[c('SegmentID','ExtSegGrID')],length)
      Overlap2<-Overlap2[order(Overlap2$SegmentID),]
      myvars<-c("ExtSegGrID", "SegmentID")
      Overlap2<-Overlap2[myvars]
      Overlap2$City<-Cityname[i]
      
      
    #Create segregation table where output will be stored  
      SegTable<-as.data.frame(unique(All$City))
      SegTable<-rename(SegTable,c("unique(All$City)"="City"))
      
      ####### Population Totals ########
      #Pop_A is analytic sample Pop_t is city total
      All$Pop_t<-length((Points$serial))
      All$Pop_a<-length((All$Person))
      t<-data.frame(table(All$native_b))
      All$Pop_native<-t[2,2]
      
      #Calculate Household Totals
        ghh<-tapply(All$german, INDEX=list(All$serial), FUN=sum, na.rm=T)
        ghhtot<-data.frame(serial=names(ghh), german_hht=ghh)
        ihh<-tapply(All$irish, INDEX=list(All$serial), FUN=sum, na.rm=T)
        ihhtot<-data.frame(serial=names(ihh), irish_hht=ihh)
        thh<-tapply(All$Person, INDEX=list(All$serial), FUN=sum, na.rm=T)
        thhtot<-data.frame(serial=names(thh), hh_total=thh)
        
        hh<-merge(x=ghhtot, y=ihhtot, by="serial", all.x=TRUE)
        hh<-merge(x=hh, y=thhtot, by="serial", all.x=TRUE)
        hh<-merge(x=hh, y=All[,c("serial", "german_t","irish_t")], by="serial", all.x=T)
        hh<-subset(hh, !duplicated(hh$serial))
      
      #Isolation by Household
        hh$IsoHouse_g<-((hh$german_hht/hh$german_t)*(hh$german_hht/hh$hh_total))
        SegTable$IsoHouse_g<-sum(hh$IsoHouse_g)
      
        hh$IsoHouse_i<-((hh$irish_hht/hh$irish_t)*(hh$irish_hht/hh$hh_total))
        SegTable$IsoHouse_i<-sum(hh$IsoHouse_i)
      
#########Neighbors by Race ##########
    #Order by Address and House Number
    #  All<-All[order(All$street,All$house_number),]
    #Tag Unique Streets and Housenumbers - I.E. BUILDINGS
    #  All$stnum_id<-id(All[c("street","house_number")], drop=T)
        
    gbuild<-tapply(All$german, INDEX=list(All$stnum_id), FUN=sum, na.rm=T)
    gbuild2<-data.frame(stnum_id=names(gbuild), g_build=gbuild)
    ibuild<-tapply(All$irish, INDEX=list(All$stnum_id), FUN=sum, na.rm=T)
    ibuild2<-data.frame(stnum_id=names(ibuild), i_build=ibuild)
    tbuild<-tapply(All$Person, INDEX=list(All$stnum_id), FUN=sum, na.rm=T)
    totbuild<-data.frame(stnum_id=names(tbuild), t_build=tbuild)
    
    build<-merge(x=gbuild2, y=ibuild2, by="stnum_id", all.x=T)
    build<-merge(x=totbuild, y=build, by="stnum_id", all.x=T)
    build<-merge(y=build, x=All[,c("stnum_id","german_t", "irish_t", "Person")], by="stnum_id", all.x=T)
    build<-subset(build, !duplicated(build$stnum_id))
    build<-subset(build, !is.na(build$g_build))
    
    Neigh<-merge(y=build, x=All[,c("side", "stnum_id", "segment_id")], by="stnum_id", all.x=T)
    Neigh<-subset(Neigh, !duplicated(Neigh$stnum_id))
      
    #Divide by Side of Street
      sgright<-Neigh[which(Neigh$side=="R"),]
        sgright$side<-as.character(sgright$side)
        sgright$segment_id<-as.character(sgright$segment_id)
      sgleft<-Neigh[which(Neigh$side=="L"),]
        sgleft$side<-as.character(sgleft$side)
        sgleft$segment_id<-as.character(sgleft$segment_id)
    
    #Order
      sgright<-sgright[order(sgright$stnum_id),]
      sgleft<-sgleft[order(sgleft$stnum_id),]    
      
    #Position of observation
    #Create Neighbor Pairs
      sgright$N1<-shift(sgright$stnum_id, 1)
      sgright$N2<-shift(sgright$stnum_id, -1)
    #Create a sequence of numbers by segment id.  This code counts from 1 to N+1 for every unique segment id.
      sgright$Seq<-with(sgright, ave(sgright$segment_id,sgright$segment_id, FUN=seq_along))
    #Marks the maximum number in the sequence of numbers.  This is used to determine the last building on the segment
      sgright$Max<-with(sgright, ave(sgright$Seq, sgright$segment_id, FUN=function(x)
        seq_along(x)==which.max(x)))==1
    #Marking the first and last building of each segment
      sgright$N1<-ifelse(sgright$Max=="TRUE", "NA", sgright$N1)
      sgright$N2<-ifelse(sgright$Seq==1, "NA", sgright$N2)
      
    #Shift Building Totals;      
      sgright$N1gh<-shift(sgright$g_build,1)
        sgright$N1gh<-ifelse(sgright$Max=="TRUE", 0, sgright$N1gh)
      sgright$N1gh<-ifelse(is.na(sgright$N1gh), 1, sgright$N1gh)
      sgright$N2gh<-shift(sgright$g_build,-1)
        sgright$N2gh<-ifelse(sgright$Seq==1, 0, sgright$N2gh)
      sgright$N2gh<-ifelse(is.na(sgright$N2gh), 1, sgright$N2gh)   
      
      sgright$N1ih<-shift(sgright$i_build,1)
        sgright$N1ih<-ifelse(sgright$Max=="TRUE", 0, sgright$N1ih)
      sgright$N1ih<-ifelse(is.na(sgright$N1ih), 1, sgright$N1ih)
      sgright$N2ih<-shift(sgright$i_build, -1)
        sgright$N2ih<-ifelse(sgright$Seq==1, 0, sgright$N2ih)
      sgright$N2ih<-ifelse(is.na(sgright$N2ih), 1, sgright$N2ih)
        
      sgright$N1toth<-shift(sgright$t_build,1)
        sgright$N1toth<-ifelse(sgright$Max=="TRUE", 0, sgright$N1toth)
      sgright$N1toth<-ifelse(is.na(sgright$N1toth), 1, sgright$N1toth)
      sgright$N2toth<-shift(sgright$t_build,-1)
        sgright$N2toth<-ifelse(sgright$Seq==1, 0, sgright$N2toth)
      sgright$N2toth<-ifelse(is.na(sgright$N2toth), 1, sgright$N2toth)
      
      sgright$Ntotg<-as.numeric(sgright$N1gh + sgright$N2gh + sgright$g_build)
      sgright$Ntoti<-as.numeric(sgright$N1ih + sgright$N2ih + sgright$i_build)
      sgright$Ntott<-as.numeric(sgright$N1toth + sgright$N2toth + sgright$t_build)
      
      sgright$Ntotg2<-as.numeric(sgright$N1gh + sgright$N2gh)
      sgright$Ntoti2<-as.numeric(sgright$N1ih + sgright$N2ih)
      sgright$Ntott2<-as.numeric(sgright$N1toth + sgright$N2toth)  
      
    #Shift Housing Totals;      
      #Position of observation - Create Neighbor Pairs
        sgleft$N1<-shift(sgleft$stnum_id, 1)
        sgleft$N2<-shift(sgleft$stnum_id, -1)
      #Create a sequence of numbers by segment id.  This code counts from 1 to N+1 for every unique segment id.
        sgleft$Seq<-with(sgleft, ave(sgleft$segment_id,sgleft$segment_id, FUN=seq_along))
      #Marks the maximum number in the sequence of numbers.  This is used to determine the last building on the segment
        sgleft$Max<-with(sgleft, ave(sgleft$Seq, sgleft$segment_id, FUN=function(x)
          seq_along(x)==which.max(x)))==1
      #Marking the first and last building of each segment
        sgleft$N1<-ifelse(sgleft$Max=="TRUE", "NA", sgleft$N1)
        sgleft$N2<-ifelse(sgleft$Seq==1, "NA", sgleft$N2)
      
      sgleft$N1gh<-shift(sgleft$g_build,1)
        sgleft$N1gh<-ifelse(sgleft$Max=="TRUE", 0, sgleft$N1gh)
      sgleft$N1gh<-ifelse(is.na(sgleft$N1gh), 1, sgleft$N1gh)
      sgleft$N2gh<-shift(sgleft$g_build,-1)
        sgleft$N2gh<-ifelse(sgleft$Seq==1, 0, sgleft$N2gh)
      sgleft$N2gh<-ifelse(is.na(sgleft$N2gh), 1, sgleft$N2gh)   
      
      sgleft$N1ih<-shift(sgleft$i_build,1)
        sgleft$N1ih<-ifelse(sgleft$Max=="TRUE", 0, sgleft$N1ih)
      sgleft$N1ih<-ifelse(is.na(sgleft$N1ih), 1, sgleft$N1ih)
      sgleft$N2ih<-shift(sgleft$i_build, -1)
        sgleft$N2ih<-ifelse(sgleft$Seq==1, 0, sgleft$N2ih)
      sgleft$N2ih<-ifelse(is.na(sgleft$N2ih), 1, sgleft$N2ih)
      
      sgleft$N1toth<-shift(sgleft$t_build,1)
        sgleft$N1toth<-ifelse(sgleft$Max=="TRUE", 0, sgleft$N1toth)
      sgleft$N1toth<-ifelse(is.na(sgleft$N1toth), 1, sgleft$N1toth)
      sgleft$N2toth<-shift(sgleft$t_build,-1)
        sgleft$N2toth<-ifelse(sgleft$Seq==1, 0, sgleft$N2toth)
      sgleft$N2toth<-ifelse(is.na(sgleft$N2toth), 1, sgleft$N2toth)
      
      sgleft$Ntotg<-as.numeric(sgleft$N1gh + sgleft$N2gh + sgleft$g_build)
      sgleft$Ntoti<-as.numeric(sgleft$N1ih + sgleft$N2ih + sgleft$i_build)
      sgleft$Ntott<-as.numeric(sgleft$N1toth + sgleft$N2toth + sgleft$t_build)
      
      #Sans Self
      sgleft$Ntotg2<-as.numeric(sgleft$N1gh + sgleft$N2gh)
      sgleft$Ntoti2<-as.numeric(sgleft$N1ih + sgleft$N2ih)
      sgleft$Ntott2<-as.numeric(sgleft$N1toth + sgleft$N2toth)  
      
      hhfinal<-rbind(sgright,sgleft)
      hhfinal<-hhfinal[!duplicated(hhfinal$stnum_id),]
      
      #SUM NUMERATORs
      #Drop Cases where person = NA.  This would occur if a building were geocoded on two segments.
        hhfinal<-hhfinal[which(!is.na(hhfinal$Person)),]
        hhfinal$Person<-as.numeric(hhfinal$Person)

        gbg<-tapply(hhfinal$Ntotg, INDEX=list(hhfinal$Person), FUN=sum, na.rm=T)
        g_bg<-data.frame(Person=names(gbg), g_neigh=gbg)
        ibg<-tapply(hhfinal$Ntoti, INDEX=list(hhfinal$Person), FUN=sum, na.rm=T)
        i_bg<-data.frame(Person=names(ibg), i_neigh=ibg)
        tbg<-tapply(hhfinal$Ntott, INDEX=list(hhfinal$Person), FUN=sum, na.rm=T)
        t_bg<-data.frame(Person=names(tbg), t_neigh=tbg)
      
      #Sans Own Building  
        hhfinal2<-hhfinal[which(hhfinal$Ntott2!=0),]
        gbg2<-tapply(hhfinal2$Ntotg2, INDEX=list(hhfinal2$Person), FUN=sum, na.rm=T)
        g_bg2<-data.frame(Person=names(gbg2), g_neigh2=gbg2)
        ibg2<-tapply(hhfinal2$Ntoti2, INDEX=list(hhfinal2$Person), FUN=sum, na.rm=T)
        i_bg2<-data.frame(Person=names(ibg2), i_neigh2=ibg2)
        tbg2<-tapply(hhfinal2$Ntott2, INDEX=list(hhfinal2$Person), FUN=sum, na.rm=T)
        t_bg2<-data.frame(Person=names(tbg2), t_neigh2=tbg2)
      
        BLD<-merge(x=g_bg, y=i_bg, by="Person", all.x=T)
        BLD<-merge(x=t_bg, y=BLD, by="Person", all.x=T)
        BLD<-merge(x=g_bg2, y=BLD, by="Person", all.x=T)
        BLD<-merge(x=i_bg2, y=BLD, by="Person", all.x=T)
        BLD<-merge(x=t_bg2, y=BLD, by="Person", all.x=T)
        
        hhfinal<-merge(x=hhfinal, y=BLD, by="Person", all.x=T)
        hhfinal<-hhfinal[which(!is.na(hhfinal$Person)),]
        
        hhfinal2<-merge(x=hhfinal2, y=BLD, by="Person", all.x=T)
        hhfinal2<-hhfinal2[which(!is.na(hhfinal2$Person)),]
        
      #Calculate Exposure - # WEIGHT IS BUILDING (E_build/ETHNICITY_t)
      #At Building Level
        hhfinal$IsoBLD_g<-((hhfinal$g_build/hhfinal$german_t)*(hhfinal$g_build/hhfinal$t_build))
        SegTable$IsoBLD_g<-sum(hhfinal$IsoBLD_g)
        hhfinal$IsoBLD_i<-((hhfinal$i_build/hhfinal$irish_t)*(hhfinal$i_build/hhfinal$t_build))
        SegTable$IsoBLD_i<-sum(hhfinal$IsoBLD_i)
        
      #At Building Group Level
        hhfinal$IsoBLDGroup_g<-((hhfinal$g_build/hhfinal$german_t)*(hhfinal$Ntotg/hhfinal$Ntott))
        SegTable$IsoBLDGroup_g<-sum(hhfinal$IsoBLDGroup_g)
        hhfinal$IsoBLDGroup_i<-((hhfinal$i_build/hhfinal$irish_t)*(hhfinal$Ntoti/hhfinal$Ntott))
        SegTable$IsoBLDGroup_i<-sum(hhfinal$IsoBLDGroup_i)
        
      #At Building Level - SANS YOUR BUILDING
        hhfinal2$IsoBLDGroup2_g<-((hhfinal2$g_build/hhfinal2$german_t)*(hhfinal2$Ntotg2/hhfinal2$Ntott2))
        SegTable$IsoBLDGroup2_g<-sum(hhfinal2$IsoBLDGroup2_g, na.rm=T)
        hhfinal2$IsoBLDGroup2_i<-((hhfinal2$i_build/hhfinal2$irish_t)*(hhfinal2$Ntoti2/hhfinal2$Ntott2))
        SegTable$IsoBLDGroup2_i<-sum(hhfinal2$IsoBLDGroup2_i, na.rm=T)
      
        ######Segment Side by Race#####
        g_side<-tapply(All$german, INDEX=list(All$segside), FUN=sum, na.rm=T)
        g_side2<-data.frame(segside=names(g_side), g_side=g_side)
        i_side<-tapply(All$irish, INDEX=list(All$segside), FUN=sum, na.rm=T)
        i_side2<-data.frame(segside=names(i_side), i_side=i_side)
        t_side<-tapply(All$Person, INDEX=list(All$segside), FUN=sum, na.rm=T)
        t_side2<-data.frame(segside=names(t_side), t_side=t_side)
        
        Segside<-merge(x=g_side2, y=i_side2, by="segside", all.x=TRUE)
        Segside<-merge(x=Segside, y=t_side2, by="segside", all.x=TRUE)
        Segside<-merge(x=Segside, y=All[,c("segside", "german_t", "irish_t")], by="segside", all.x=T)
        Segside<-subset(Segside, !duplicated(Segside$segside))
        
        #ISOLATION
        Segside$IssoSegside_g<-((Segside$g_side/Segside$german_t)*(Segside$g_side/Segside$t_side))
        SegTable$IsoSegside_g<-sum(Segside$IssoSegside_g)
        Segside$IssoSegside_i<-((Segside$i_side/Segside$irish_t)*(Segside$i_side/Segside$t_side))
        SegTable$IsoSegside_i<-sum(Segside$IssoSegside_i)
      
      ##### Segment by Race #####
        gs<-tapply(All$german, INDEX=All$segment_id, FUN=sum, na.rm=T)
        g_seg<-data.frame(segment_id=names(gs), g_seg=gs)
        is<-tapply(All$irish, INDEX=All$segment_id, FUN=sum, na.rm=T)
        i_seg<-data.frame(segment_id=names(is), i_seg=is)
        tots<-tapply(All$Person, INDEX=All$segment_id, FUN=sum, na.rm=T)
        t_seg<-data.frame(segment_id=names(tots), t_seg=tots)
        
        Segment<-merge(x=g_seg, y=i_seg, by="segment_id", all.x=TRUE)
        Segment<-merge(x=Segment, y=t_seg, by="segment_id", all.x=TRUE)
        Segment<-merge(x=Segment, y=All[,c("segment_id", "german_t", "irish_t")], by="segment_id", all.x=TRUE)
        Segment<-subset(Segment, !duplicated(Segment$segment_id))
      
        #ISOLATION
        Segment$IssoSeg_g<-((Segment$g_seg/Segment$german_t)*(Segment$g_seg/Segment$t_seg))
        SegTable$IsoSeg_g<-sum(Segment$IssoSeg_g)
        Segment$IssoSeg_i<-((Segment$i_seg/Segment$irish_t)*(Segment$i_seg/Segment$t_seg))
        SegTable$IsoSeg_i<-sum(Segment$IssoSeg_i)

  ##### Overlapping Segment Group - ISOLATION #####
      #Bring in Segment which is aggregated by segment and merge it to overlapping segment groups
        OverSeg<-merge(x=Segment, y=OverSeg_Join[,c("SegmentID", "SegGrID")], by.x="segment_id", by.y="SegmentID",all.x=TRUE)
      #Aggregate by Segment Group
        g_overseg<-tapply(OverSeg$g_seg, INDEX=list(OverSeg$SegGrID), FUN=sum, na.rm=T)
        g_overseg2<-data.frame(OverSegGr=names(g_overseg), g_overseg=g_overseg)
        i_overseg<-tapply(OverSeg$i_seg, INDEX=list(OverSeg$SegGrID), FUN=sum, na.rm=T)
        i_overseg2<-data.frame(OverSegGr=names(i_overseg), i_overseg=i_overseg)
        t_overseg<-tapply(OverSeg$t_seg, INDEX=list(OverSeg$SegGrID), FUN=sum, na.rm=T)
        t_overseg2<-data.frame(OverSegGr=names(t_overseg), t_overseg=t_overseg)
        
      #Merge aggregate data to one dataframe (OverlappingSG)
        OverlappingSG<-merge(x=g_overseg2, y=i_overseg2, by="OverSegGr", all.x=T)
        OverlappingSG<-merge(x=OverlappingSG, y=t_overseg2, by="OverSegGr", all.x=T)  
        
      #Attach aggregated segment group information to OverSeg in order to do isolation calculations
        OverSeg<-merge(x=OverSeg, y=OverlappingSG, by.x="SegGrID", by.y="OverSegGr", all.x=TRUE)
      #Keep focal segments which are found if Seg_ID==SegGrID
        OverSeg<-OverSeg[which(OverSeg$SegGrID==OverSeg$segment_id),]
      
        #ISOLATION
        OverSeg$IssoOverSeg_g<-((OverSeg$g_seg/OverSeg$german_t)*(OverSeg$g_overseg/OverSeg$t_overseg))
        SegTable$IsoOverSeg_g<-sum(OverSeg$IssoOverSeg_g)
        OverSeg$IssoOverSeg_i<-((OverSeg$i_seg/OverSeg$irish_t)*(OverSeg$i_overseg/OverSeg$t_overseg))
        SegTable$IsoOverSeg_i<-sum(OverSeg$IssoOverSeg_i)
        
  ###### Overlapping Extended Segment Group - ISOLATION #####
      #Bring in Segment2 which is aggregated by segment and merge it to overlapping extended segment groups (Overlap2)
        ExtOverSeg<-merge(x=Segment, y=Overlap2[,c("SegmentID", "ExtSegGrID")], by.x="segment_id", by.y="SegmentID",all.x=TRUE)
      #Aggregate by Extended Segment Group
        g_overextseg<-tapply(ExtOverSeg$g_seg, INDEX=list(ExtOverSeg$ExtSegGrID), FUN=sum, na.rm=T)
        g_overextseg2<-data.frame(ExtOverSegGr=names(g_overextseg), g_overextseg=g_overextseg)
        i_overextseg<-tapply(ExtOverSeg$i_seg, INDEX=list(ExtOverSeg$ExtSegGrID), FUN=sum, na.rm=T)
        i_overextseg2<-data.frame(ExtOverSegGr=names(i_overextseg), i_overextseg=i_overextseg)
        t_overextseg<-tapply(ExtOverSeg$t_seg, INDEX=list(ExtOverSeg$ExtSegGrID), FUN=sum, na.rm=T)
        t_overextseg2<-data.frame(ExtOverSegGr=names(t_overextseg), t_overextseg=t_overextseg)

      #Merge aggregate data into one data frame (OverlappingExtSG)
        OverlappingExtSG<-merge(x=g_overextseg2, y=i_overextseg2, by="ExtOverSegGr", all.x=T)
        OverlappingExtSG<-merge(x=OverlappingExtSG, y=t_overextseg2, by="ExtOverSegGr", all.x=T)  
      #Attach aggregated segment group information to OverSeg in order to do isolation calculations
        ExtOverSeg<-merge(x=ExtOverSeg, y=OverlappingExtSG, by.x="ExtSegGrID", by.y="ExtOverSegGr", all.x=TRUE)
      #Keep focal segments which are found if Seg_ID==ExtSegGrID
        ExtOverSeg<-ExtOverSeg[which(ExtOverSeg$ExtSegGrID==ExtOverSeg$segment_id),]
        
        #ISOLATION
        ExtOverSeg$IssoOverSegEG_g<-((ExtOverSeg$g_seg/ExtOverSeg$german_t)*(ExtOverSeg$g_overextseg/ExtOverSeg$t_overextseg))
        SegTable$IsoOverEG_g<-sum(ExtOverSeg$IssoOverSegEG_g)
        ExtOverSeg$IssoOverSegEG_i<-((ExtOverSeg$i_seg/ExtOverSeg$irish_t)*(ExtOverSeg$i_overextseg/ExtOverSeg$t_overextseg))
        SegTable$IsoOverEG_i<-sum(ExtOverSeg$IssoOverSegEG_i)
        
      ##### ED #####
        ged<-tapply(All$german, INDEX=list(All$enumdist), FUN=sum, na.rm=T)
        g_ed<-data.frame(enumdist=names(ged), g_ed=ged)
        ied<-tapply(All$irish, INDEX=list(All$enumdist), FUN=sum, na.rm=T)
        i_ed<-data.frame(enumdist=names(ied), i_ed=ied)
        ted<-tapply(All$Person, INDEX=list(All$enumdist), FUN=sum, na.rm=T)
        t_ed<-data.frame(enumdist=names(ted), t_ed=ted)
        
        ed<-merge(x=g_ed, y=i_ed, by="enumdist", all.x=TRUE)
        ed<-merge(x=ed, y=t_ed, by="enumdist", all.x=TRUE)
        ed<-merge(x=ed, y=All[,c("enumdist", "german_t", "irish_t")], by="enumdist", all.x=TRUE)
        ed<-subset(ed, !duplicated(ed$enumdist))

        ed$IsoED_g<-((ed$g_ed/ed$german_t)*(ed$g_ed/ed$t_ed))
        SegTable$IsoED_g<-sum(ed$IsoED_g)
        ed$IsoED_i<-((ed$i_ed/ed$irish_t)*(ed$i_ed/ed$t_ed))
        SegTable$IsoED_i<-sum(ed$IsoED_i)
        
      #### City ####
        gcity<-tapply(All$german, INDEX=list(All$City), FUN=sum, na.rm=T)
        g_city<-data.frame(City=names(gcity), g_city=gcity)
        icity<-tapply(All$irish, INDEX=list(All$City), FUN=sum, na.rm=T)
        i_city<-data.frame(City=names(icity), i_city=icity)
        tcity<-tapply(All$Person, INDEX=list(All$City), FUN=sum, na.rm=T)
        t_city<-data.frame(City=names(tcity), t_city=tcity)
        
        city<-merge(x=g_city, y=i_city, by="City", all.x=TRUE)
        city<-merge(x=city, y=t_city, by="City", all.x=TRUE)
        city<-merge(x=city, y=All[,c("City", "german_t", "irish_t")], by="City", all.x=TRUE)
        city<-subset(city, !duplicated(city$City))
        
        city$IsoCity_g<-((city$g_city/city$german_t)*(city$g_city/city$t_city))
        SegTable$IsoCity_g<-sum(city$IsoCity_g)
        city$IsoCity_i<-((city$i_city/city$irish_t)*(city$i_city/city$t_city))
        SegTable$IsoCity_i<-sum(city$IsoCity_i)
 
        SegTable<-SegTable[,c(1,2,4,6,8,10,12,14,16,18,20,3,5,7,9,11,13,15,17,19,21)]
        AllSegTable<-rbind(AllSegTable, SegTable)      
  }, error=function(e){cat(conditionMessage(e))})
}

  AllSegTable<-rename(AllSegTable, c("City"="City","IsoHouse_g"="Household Isolation (German)","IsoBLD_g"="Building Isolation (German)",
                       "IsoBLDGroup_g"="Building Group Isolation (German)","IsoBLDGroup2_g"="Building Group Isolation - Sans Own Building (German)",
                       "IsoSegside_g"="Segment Side Isolation (German)","IsoSeg_g"="Segment Isolation (German)",
                       "IsoOverSeg_g"="Overlapping Segment Group (German)", "IsoOverEG_g"="Overlapping Extended Segment Group (German)",
                       "IsoED_g"="ED Isolation (German)", "IsoCity_g"="Citywide Isolation (German)","IsoHouse_i"="Household Isolation (Irish)",
                       "IsoBLD_i"="Building Isolation (Irish)", "IsoBLDGroup_i"="Building Group Isolation (Irish)",
                       "IsoBLDGroup2_i"="Building Group Isolation - Sans Own Building (Irish)", "IsoSegside_i"="Segment Side Isolation (Irish)",
                       "IsoSeg_i"="Segment Isolation (Irish)", "IsoOverSeg_i"="Overlapping Segment Group (Irish)",
                       "IsoOverEG_i"="Overlapping Extended Segment Group (Irish)","IsoED_i"="ED Isolation (Irish)","IsoCity_i"="Citywide Isolation (Irish)"))
  
  AllSeg_New<-AllSegTable
  write.csv(AllSegTable, "C:/Users/mmarti24/Dropbox/Papers/SIS - Early Arriving/Segregation_Results_1stGen.csv")
  write.xlsx(AllSegTable, file="C:/Users/mmarti24/Dropbox/Papers/SIS - Early Arriving/Segregation_Results_1stGen.xlsx")
  
