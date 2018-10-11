# Original code by Matt Martinez
# Inital update by Ben Bellman, Sept 11, 2018
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
EDs <- read.dbf(paste(dir_path,city_name,"_",decade,"_Pblk_Points.dbf",sep=""), as.is = T) %>% 
  # make column names lower case
  rename_all(tolower) %>% 
  # create building id
  mutate(build_id = paste(hn, fullname, sep = "_")) %>% 
  # keep unique addresses
  filter(!duplicated(build_id)) %>% 
  # drop cases without associated pblk
  filter(pblk_id != 0) %>% 
  # keep only needed variables
  select(ed, pblk_id, build_id) %>% 
  
  ### Count numbers of addresses in each mblk, pblk, and combination between the two
  # ED
  group_by(ed) %>% 
  mutate(M_Count = n_distinct(build_id)) %>% 
  # pblks
  group_by(pblk_id) %>% 
  mutate(P_Count = n_distinct(build_id)) %>% 
  # combination of the two
  group_by(ed, pblk_id) %>% 
  mutate(TotCombos = n_distinct(build_id)) %>% 
  # ungroup, calculate proportions
  ungroup() %>% 
  mutate(PerMblk = TotCombos / M_Count,
         PerPblk = TotCombos / P_Count) %>% 
  # group by ed, get max proportions
  group_by(ed) %>%
  mutate(MMax = max(PerMblk)) %>% 
  # group by pblk, get max proportions
  group_by(pblk_id) %>%
  mutate(PMax = max(PerPblk)) %>% 
  ungroup()

# evaluate ed and pblk combos, apply match criteria, format to merge with polygon file
Combo <- EDs %>% 
  select(-build_id) %>% 
  # one row for each pblk-ed combo
  unique() %>% 
  mutate(ED_ID = ifelse(PerPblk==1, ed, NA),
         ED_ID2 = ifelse(is.na(ED_ID) & PerPblk>=0.75, ed, NA),
         ED_ID3 = ifelse(is.na(ED_ID) & is.na(ED_ID2) & PerPblk==PMax, ed, NA)) %>%  
  # keep only the conditions
  select(pblk_id, ED_ID, ED_ID2, ED_ID3)

# keep set of pblks with at least one MBID value
hits <- filter(Combo, ED_ID!="" | ED_ID2!="" | ED_ID3!="")

# combine rows with pblks with no geocode guess
EDC <- Combo %>% 
  select(pblk_id) %>% 
  filter(pblk_id %in% hits$pblk_id == F) %>% 
  unique() %>% 
  bind_rows(hits)

#Attach to Original Shapefile
EDMap <- st_read(paste(dir_path,city_name,"_",decade,"_Pblk.shp",sep=""))
names(EDMap) <- tolower(names(EDMap))

#Merge
EDMap <- merge(x=EDMap, y=EDC, by="pblk_id", all.x=TRUE)

#Export Map
st_write(EDMap, paste0(dir_path, city_name, "_", decade, "_ed_geo.shp"))

#########
