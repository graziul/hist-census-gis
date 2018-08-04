### Function to create dwelling groups
### Groups adjacent dwellings with common ID
### rows are repeated when belonging to different dwelling groups
### Does not group when next record has different street name or ED




library(data.table)
library(dplyr)
library(dtplyr)
library(tidyr)
library(stringr)
library(purrr)

# define neighbors for string of adjacent buildlings
neighbor_module <- function(adj){
  
  adj$front <- NA
  adj$back <- NA
  
  if(nrow(adj) > 2){
    # define neighbors if more than 2 buildings
    adj[1:nrow(adj)-1, "front"] <- adj[2:nrow(adj), "dwell_fixed"]
    adj[2:nrow(adj), "back"] <- adj[1:nrow(adj)-1, "dwell_fixed"]
  } 
  
  if (nrow(adj) == 2){
    # if only 2 buildings, just swap dwelling ids
    adj[1, "front"] <- adj[2, "dwell_fixed"]
    adj[2, "back"] <- adj[1, "dwell_fixed"]
  }
  
  # return full data frame
  adj
}

# This version uses "dwell_fixed" and splits by "hn" to separate sides of street
# Must be same ED and street to be a neighboring dwelling

# rows_in <- read_dta("~/Desktop/CamdenNJ.dta")

dwelling_group <- function(rows_in, drop_blank_street = FALSE, drop_blank_hn = FALSE){
  
  # definitely drop if missing both hn and street
  rows_in <- rows_in %>% 
    filter(is.na(hn) == F | street_final != "")
  
  # maybe drop blank house numbers
  if(drop_blank_hn == TRUE){
    rows_in <- rows_in %>% 
      filter(is.na(hn) == F)
  }
  
  # maybe drop blank street names
  if(drop_blank_street == TRUE){
    rows_in <- rows_in %>% 
      filter(street_final != "")
  }
  
  # start with city file
  dwels <- rows_in %>% 
    # keep vars describing dwellings
    select(ed, street_final, dwell_fixed, hn) %>% 
    # work only with unique dwellings
    unique() %>% 
    # are house numbers even or odd?
    mutate(even = if_else(hn %% 2 == 0, 1, 0)) %>% 
    # if all numbers for ed-street are even, make blank hn even, otherwise make odd
    # this number ensures all blank hn "dwellings" are first in row of buildings
    group_by(ed, street_final) %>% 
    mutate(st_even = if_else(sum(even, na.rm=T) == n(), 1, 0)) %>% 
    ungroup() %>%
    mutate(hn = case_when(is.na(hn) == F ~ hn,
                          is.na(hn) & st_even == 1 ~ 0,
                          is.na(hn) & st_even == 0 ~ 0.5)) %>% 
    # split into rows of adjacent buildings
    arrange(ed, street_final, even, hn) %>% 
    split(f = paste(.$ed, .$street_final, .$even, sep = "_")) %>% 
    # apply neighbor module to split data
    map(neighbor_module) %>% 
    # combine back into a single data frame
    bind_rows()
    
  #combine results and create dwelling-to-dwgroup crosswalk
  cw <- dwels %>% 
    mutate(dwgroup = dwell_fixed) %>%
    rename(focal = dwell_fixed) %>% 
    gather(side, dwell_fixed, focal, front, back) %>% 
    select(dwgroup, dwell_fixed) %>% 
    filter(is.na(dwell_fixed) == F)
  
  #return the join of this crosswalk to city microdata, duplicating rows for dwelling group double counts
  suppressWarnings(inner_join(as_tibble(rows_in), cw))
}





# This version only works in 1900
# It uses the Ancestry dwelling number that Lisa fixed
# You must sort by order of enumeration within each ED for it to work


dwelling_group_anc <- function(rows_in, drop_blank_street = FALSE){
  
  dwels <- rows_in %>% 
    arrange(ed, street_final, page_num, page_letter, line_num) %>% 
    select(ed, street_final, dwell_ancestry) %>% 
    unique()
  noname <- filter(dwels, street_final == "") %>% as_tibble()
  dwels <- filter(dwels, street_final != "") %>% as_tibble()
  
  #define neighbors for data with street names
  dwels$front <- ""
  dwels$front_ed <- as.numeric(NA)
  dwels$front_street <- ""
  dwels[1:nrow(dwels)-1, "front"] <- dwels[2:nrow(dwels), "dwell_ancestry"]
  dwels[1:nrow(dwels)-1, "front_ed"] <- dwels[2:nrow(dwels), "ed"]
  dwels[1:nrow(dwels)-1, "front_street"] <- dwels[2:nrow(dwels), "street_final"]
  
  dwels$back <- ""
  dwels$back_ed <- as.numeric(NA)
  dwels$back_street <- ""
  dwels[2:nrow(dwels), "back"] <- dwels[1:nrow(dwels)-1, "dwell_ancestry"]
  dwels[2:nrow(dwels), "back_ed"] <- dwels[1:nrow(dwels)-1, "ed"]
  dwels[2:nrow(dwels), "back_street"] <- dwels[1:nrow(dwels)-1, "street_final"]
  
  dwels$front <- if_else(dwels$street_final == dwels$front_street &
                           dwels$ed == dwels$front_ed, dwels$front, "")
  dwels$back <- if_else(dwels$street_final == dwels$back_street &
                          dwels$ed == dwels$back_ed, dwels$back, "")
  
  #define neighbors for data with no street names
  if(drop_blank_street == FALSE & nrow(noname) > 2){
    noname$front <- ""
    noname$front_ed <- as.numeric(NA)
    noname[1:nrow(noname)-1, "front"] <- noname[2:nrow(noname), "dwell_ancestry"]
    noname[1:nrow(noname)-1, "front_ed"] <- noname[2:nrow(noname), "ed"]
    
    noname$back <- ""
    noname$back_ed <- as.numeric(NA)
    noname[2:nrow(noname), "back"] <- noname[1:nrow(noname)-1, "dwell_ancestry"]
    noname[2:nrow(noname), "back_ed"] <- noname[1:nrow(noname)-1, "ed"]
    
    noname$front <- if_else(noname$ed == noname$front_ed, noname$front, "")
    noname$back <- if_else(noname$ed == noname$back_ed, noname$back, "")
  }
  
  #combine results and create dwelling-to-dwgroup crosswalk
  cw_1 <- dwels %>% 
    mutate(dwgroup = dwell_ancestry) %>%
    rename(focal = dwell_ancestry) %>% 
    gather(side, dwell_ancestry, focal, front, back) %>% 
    select(dwgroup, dwell_ancestry) %>% 
    filter(is.na(dwell_ancestry) == F)
  
  if(drop_blank_street == FALSE & nrow(noname) > 2){
    cw_2 <- noname %>% 
      mutate(dwgroup = dwell_ancestry) %>%
      rename(focal = dwell_ancestry) %>% 
      gather(side, dwell_ancestry, focal, front, back) %>% 
      select(dwgroup, dwell_ancestry) %>% 
      filter(is.na(dwell_ancestry) == F)
    
    cw <- rbind(cw_1, cw_2)
  } else{
    cw <- cw_1
  }
  
  #return the join of this crosswalk to city microdata, duplicating rows for dwelling group double counts
  suppressWarnings(inner_join(as_tibble(rows_in), cw))
}



#result <- dwelling_group(mo)

#result <- dwelling_group(mo) %>% pstar(dwgroup)
#pstar(mo, dwelling)
