# Original code by Matt Martinez
# Inital update by Ben Bellman, Sept 10, 2018
# Major refactoring by Ben Bellman, Oct 11, 2018

# Install missing packages
chooseCRANmirror(ind=1)
list.of.packages <- c("foreign","dplyr","sf")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0){install.packages(new.packages)}

# Load Neccessary Libraries
library(foreign)
library(dplyr)
library(sf)

args <- commandArgs(trailingOnly = TRUE)
dir_path <- paste(args[1],"/GIS_edited/",sep="")
city_name <- args[2]
city_name <- gsub(" ","",city_name)
decade <- args[3]

### Start Processing


# Bring in microdata points
Blocks <- read.dbf(paste(dir_path,city_name,"_",decade,"_Pblk_Points.dbf",sep=""), as.is = T) %>% 
  # make column names lower case
  rename_all(tolower) %>% 
  # create building id
  mutate(build_id = paste(hn, fullname, sep = "_")) %>% 
  # keep unique addresses
  filter(!duplicated(build_id)) %>% 
  # drop cases without associated pblk
  filter(pblk_id != 0) %>% 
  # keep only needed variables
  select(ed_block, pblk_id, build_id) %>% 
  
  ### Count numbers of addresses in each mblk, pblk, and combination between the two
  # ED-blocks
  group_by(ed_block) %>% 
  mutate(M_Count = n_distinct(build_id)) %>% 
  # pblks
  group_by(pblk_id) %>% 
  mutate(P_Count = n_distinct(build_id)) %>% 
  # combination of the two
  group_by(ed_block, pblk_id) %>% 
  mutate(TotCombos = n_distinct(build_id)) %>% 
  # ungroup, calculate proportions
  ungroup() %>% 
  mutate(PerMblk = TotCombos / M_Count,
         PerPblk = TotCombos / P_Count) %>% 
  # group by ed_block, get max proportions
  group_by(ed_block) %>%
  mutate(MMax = max(PerMblk)) %>% 
  # group by pblk, get max proportions
  group_by(pblk_id) %>%
  mutate(PMax = max(PerPblk)) %>% 
  ungroup()

# evaluate ed_block and pblk combos, apply match criteria, format to merge with polygon file
Combo <- Blocks %>% 
  select(-build_id) %>% 
  # one row for each block-ed combo
  unique() %>% 
  mutate(One = ifelse(M_Count<=2, "Yes", "No"),
         Match75 = ifelse(PerMblk>=0.75 & PerPblk==1 & One=="No", "Yes", "No"),
         MBID = ifelse(PerMblk==1 & PerPblk==1 & One=="No", ed_block, NA),
         MBID2 = ifelse(is.na(MBID) & Match75=="Yes", ed_block, NA),
         MBID3 = ifelse(is.na(MBID) & is.na(MBID2) & PerMblk>=0.75 & PerPblk>=0.75 & One=="No", ed_block, NA)) %>%  
  # choose variables for output
  select(pblk_id, MBID, MBID2, MBID3)

# keep set of pblks with at least one MBID value
hits <- filter(Combo, MBID!="" | MBID2!="" | MBID3!="")

# combine rows with pblks with no geocode guess
BlockC <- Combo %>% 
  select(pblk_id) %>% 
  filter(pblk_id %in% hits$pblk_id == F) %>% 
  unique() %>% 
  bind_rows(hits)

#Attach to Original Shapefile
BlockMap <- st_read(paste(dir_path,city_name,"_",decade,"_Pblk.shp",sep=""))
names(BlockMap) <- tolower(names(BlockMap))

#Merge
BlockMap <- merge(x=BlockMap, y=BlockC, by="pblk_id", all.x=TRUE)

#Export Map
st_write(BlockMap, paste0(dir_path, city_name, "_", decade, "_block_geo.shp"))

#########