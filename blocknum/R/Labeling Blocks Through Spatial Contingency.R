library(rgdal)
library(spdep)
library(plyr)
trim <- function( x ) {
  gsub("(^[[:space:]]+|[[:space:]]+$)", "", x)
}


#Set Folder Where Shapefiles Are Located
  setwd("C:/Users/Matthew/Google Drive/Maps/Shape Files/San Antonio 1930-40") #Home
  setwd("C:/Users/mmarti24/Google Drive/Maps/Shape Files/San Antonio 1930-40") #Work
  sa<-readOGR(dsn=getwd(), layer="PostGridEdit_Pblocks30", stringsAsFactors = F) #Shapefile
  myvars<-c("pblk_id")
  sa<-sa[myvars]
  View(sa@data)
  
#Make Spatial Weight Matrix - Queen Contiguity
  sa_queen<-poly2nb(sa, queen=F)
  summary(sa_queen)
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
  pblk_id<-neighs$pblk_id  #List of Physical Block ids to be used in loop
  FirstE<-neighs$FirstE   #List of Choices from automated ED-Block numbering
  max_replace<-length(FirstE) #Number of replacements loops runs through

  #Create new variables equal to maximum number of neighbors
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
  }  
  