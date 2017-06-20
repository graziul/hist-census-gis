library(rgdal)
library(spdep)
library(plyr)

trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}

modefunc <- function(x){
  tabresult <- tabulate(x)
  themode <- which(tabresult == max(tabresult))
  if(sum(tabresult == max(tabresult))>1) themode <- NA
  return(themode)
}

#Set Folder Where Shapefiles Are Located
  setwd("C:/Users/mmarti24/Google Drive/Maps/Shape Files/San Antonio 1930-40") #Work
  sa<-readOGR(dsn=getwd(), layer="PostGridEdit_Pblocks30", stringsAsFactors = F) #Shapefile
  myvars<-c("pblk_id")
  sa<-sa[myvars]

#Make Spatial Weight Matrix - Queen Contiguity
  sa_queen<-poly2nb(sa, queen=F)
  
#Create List of Neighbors
  neighs<-data.frame(matrix(sa_queen, byrow=T))
  names(neighs)[1]<-"Full_List"  #Change column name to something usable
  neighs$Full_List<-gsub("[c|(|)]", "", neighs$Full_List, perl = T) #Remove special characters from list
  neighs$region.id<-seq(1, nrow(neighs)) #Create Region.id
  neighs$pblk_id<-sa$pblk_id
  neighs$Full_List<-gsub(1511, 15112, neighs$Full_List) #Just for San Antonio
  neighs$Full_List<-gsub(4633, 15111, neighs$Full_List) #Just for San Antonio
  
  #Post Edit ED Choice Map
  post<-read.dbf("C:/Users/mmarti24/Google Drive/Maps/Shape Files/San Antonio 1930-40/SanAntonio_1930_ED_Choice_Map_PostEdit.dbf")
  neighs$FirstE<-post$FirstE #Add First ED Choice to Neighbor Map

  neighs$Num_neigh<-str_count(neighs$Full_List, ",") + 1 #Counts nunmber of commas then adds 1 for total neigbors
  max<-max(neighs$Num_neigh) #Maximum number of neighbors = maximum number of columns
  max_replace<-length(neighs$FirstE) #Number of replacements loops runs through
  Start<-0  #These numbers must not be identical in order for the loop to work
  End<-1
  cnt<-0
  Iteration_FirstE<-data.frame(pblk_id)
  
 while (Start!=End){
  #Create new variables equal to maximum number of neighbors
  for (q in 1:1){
    pblk_id<-neighs$pblk_id  #List of Physical Block ids to be used in loop
    FirstE<-neighs$FirstE   #List of Choices from automated ED-Block numbering
    for (j in 1:max){
      eval(parse(text = paste0('neighs$Region.Neigh_', j, ' <- trim(sapply(strsplit(as.character(neighs$Full_List),\',\'), "[", j))')))
      eval(parse(text = paste0('neighs$ED.Neigh_', j, ' <-eval(parse(text = paste0(\'neighs$Region.Neigh_\', j)))')))
      eval(parse(text = paste0('neighs$Replace_', j, '<-0')))
    #Label Neighbors
      for (i in 1:max_replace){
        eval(parse(text = paste0('neighs$Replace_', j, 
                               '<-ifelse(pblk_id[i]==eval(parse(text = paste0(\'neighs$Region.Neigh_\', j))), (i), 
                               eval(parse(text = paste0(\'neighs$Replace_\', j))))')))
        eval(parse(text = paste0('neighs$ED.Neigh_', j,
                               '<-ifelse(pblk_id[i]==eval(parse(text = paste0(\'neighs$Region.Neigh_\', j))) & 
                               eval(parse(text = paste0(\'neighs$Replace_\', j)))==(i), 
                               gsub(neighs$pblk_id[i], FirstE[i], eval(parse(text = paste0(\'neighs$ED.Neigh_\', j)))), 
                               eval(parse(text = paste0(\'neighs$ED.Neigh_\', j))))')))
        }
    
      #Delete Variables No Longer needed *Region.Neigh & Replace
        myvars<-c(paste('Replace_', j, sep = ""), paste('Region.Neigh_', j, sep=""))
        neighs<-neighs[!names(neighs) %in% myvars]
      #Change to Numeric
        eval(parse(text = paste0('neighs$ED.Neigh_', j, '<-as.numeric(eval(parse(text = paste0(\'neighs$ED.Neigh_\', j))))')))
    }
    
    #Subset data for only blocks yet to be labeled
     filled<-subset(neighs, neighs$FirstE!=0)
     missing<-subset(neighs, neighs$FirstE==0)
    
    #Calculate Summary Statistics of ED-Block Choices. This must be done in a loop like this in order to run
    #rowSums and discard missing values that are sure to exist
    myvars<-NULL
    for (x in 1:max){
      myvars1<-c(paste('ED.Neigh_', x, sep = ""))
      myvars<-cbind(myvars1,myvars)
      
    }

    missing$Total<-rowSums(missing[,myvars], na.rm=T)
    missing$Max<-apply(missing[,myvars], 1, max ,na.rm=T)
    missing$Min<-apply(missing[,myvars], 1, min, na.rm=T)
    missing$Means<-round(rowMeans(missing[,myvars], na.rm=T),0)
    missing$Means_Comp<-round(((missing$Total - (missing$Max+missing$Min))/(missing$Num_neigh-2)), 2)
    missing$Mode<-apply(missing[,myvars], 1, modefunc)
    
    #Start Renaming Blocks
    missing$FirstE<-ifelse(missing$Means==missing$Mode & !is.na(missing$Mode), missing$Mode, missing$FirstE)
    missing$FirstE<-ifelse(missing$Means_Comp==missing$Mode & !is.na(missing$Mode & missing$FirstE==0), missing$Mode, missing$FirstE)
    #Keep Only PID and FirstE
    myvars<-c("pblk_id", "FirstE")
    missing<-missing[myvars]
    filled<-filled[myvars]
    All<-rbind(filled, missing)
    
    Start<-table(neighs$FirstE!=0)
    Start<-as.numeric(Start[2])
    End<-table(All$FirstE!=0)
    End<-as.numeric(End[2])
    
    #Test Iterations of FirstE
    neighs$Orig<-neighs$FirstE #Keep FirstE in Separate Column

    myvars<-c("FirstE")
    neighs<-neighs[!names(neighs) %in% myvars]
    neighs<-merge(x=neighs, y=All, by="pblk_id", all.x=T)
    
    neighs$Changed<-ifelse(neighs$FirstE==neighs$Orig, 0, 1)
    myvars<-c("pblk_id", "FirstE", "Changed")
    FE<-neighs[myvars]
    Iteration_FirstE<-merge(x=Iteration_FirstE, y=FE, by="pblk_id", all.x=T)
    
    cnt=cnt+1
    print(paste("Interation ", cnt))
    print(paste("Number of Blocks Labeled ", End))
  }
}
