### Function to create dwelling groups
### Groups adjacent dwellings (sorted by serial)
### Does not group when next record has different street name 

### Make sure that house numbers are removed!!!


library(data.table)
library(dplyr)
library(dtplyr)
library(tidyr)

dwelling_group <- function(rows_in){
  dwels <- rows_in %>% 
    select(dwelling, street) %>% 
    arrange(street, dwelling) %>%
    unique()
  noname <- filter(dwels, street == "") %>% as_tibble()
  dwels <- filter(dwels, street != "") %>% as_tibble()
  
  #define neighbors for data with street names
  dwels$front <- as.integer(NA)
  dwels$front_street <- ""
  dwels[1:nrow(dwels)-1, "front"] <- dwels[2:nrow(dwels), "dwelling"]
  dwels[1:nrow(dwels)-1, "front_street"] <- dwels[2:nrow(dwels), "street"]
  
  dwels$back <- as.integer(NA)
  dwels$back_street <- ""
  dwels[2:nrow(dwels), "back"] <- dwels[1:nrow(dwels)-1, "dwelling"]
  dwels[2:nrow(dwels), "back_street"] <- dwels[1:nrow(dwels)-1, "street"]
  
  dwels$front <- if_else(dwels$street == dwels$front_street, dwels$front, as.integer(NA))
  dwels$back <- if_else(dwels$street == dwels$back_street, dwels$back, as.integer(NA))
  
  #define neighbors for data with no street names
  if(nrow(noname) > 0){
    noname$front <- as.integer(NA)
    noname[1:nrow(noname)-1, "front"] <- noname[2:nrow(noname), "dwelling"]
  
    noname$back <- as.integer(NA)
    noname[2:nrow(noname), "back"] <- noname[1:nrow(noname)-1, "dwelling"]
  
    noname$front <- if_else(noname$front == noname$dwelling+1, noname$front, as.integer(NA))
    noname$back <- if_else(noname$front == noname$dwelling-1, noname$front, as.integer(NA))
  }
  
  #combine results and create dwelling-to-dwgroup crosswalk
  cw_1 <- dwels %>% 
    mutate(dwgroup = dwelling) %>%
    rename(focal = dwelling) %>% 
    gather(side, dwelling, focal, front, back) %>% 
    select(dwgroup, dwelling) %>% 
    filter(is.na(dwelling) == F)
  
  if(nrow(noname) > 0){
    cw_2 <- noname %>% 
      mutate(dwgroup = dwelling) %>%
      rename(focal = dwelling) %>% 
      gather(side, dwelling, focal, front, back) %>% 
      select(dwgroup, dwelling) %>% 
      filter(is.na(dwelling) == F)
  
    cw <- rbind(cw_1, cw_2)
  } else{
    cw <- cw_1
  }
  
  #return the join of this crosswalk to city microdata, duplicating rows for dwelling group double counts
  inner_join(as_tibble(rows_in), cw)
}



#result <- dwelling_group(mo)

#result <- dwelling_group(mo) %>% pstar(dwgroup)
#pstar(mo, dwelling)
