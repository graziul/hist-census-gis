#### This script calculates indices for the SIS project
# Ben Bellman

## Input: One data files for each city (dta for now)
## Output: Data frame of one row summarizing the city

source("microdata_seg_func.R")
source("dwelling_group.R")


library(dplyr)
library(haven)
library(readr)
library(stringr)
library(tibble)


# Planned changes for V4:
# Get both full race pop counts
# Drop black live-in servants (after Lisa's STATA code, is that saved in files already?)
# calculate adjusted black population
# calculate all indices with live-in cases removed
# calculate eta^2 transformations with adjusted blackpop
# Finally, drop eta transformation when combining results
# re-write this with doParallel for server




# "method" is currently not part of function
# dwelling and dwgroup interpolation is not ready yet
# 8/3/2018

calc_seg_sis <- function(file_name, year){
  df <- paste0("/home/s4-data/LatestCities/SIS/FinalData/", year, "/", file_name) %>% 
    read_dta() %>% 
    filter(street_final != "" | is.na(hn) == F)
  
  
  # remove cases to keep population consistent across measures
  
  #if(method == "no_blanks"){
  #  df <- filter(df, street_final != "" & is.na(hn) == F)
  #}
  
  #if(method == "ancestry" & year == 1900){
  #  df <- filter(df, is.na(dwell_ancestry) == F) %>% 
  #    mutate(page_num = as.numeric(str_replace_all(anc_page_num, "[A-Z]", "")),
  #           page_letter = str_replace_all(anc_page_num, "[0-9]", ""),
  #           dwell_ancestry = paste(ed, street_fixed, dwell_ancestry, sep = "_"))
  #}
  
  year <- as.numeric(year)
  
  # new columns
  if("sisrace" %in% names(df) == F){
    df$sisrace <- case_when(df$race == 100 ~ 1,
                            df$race == 200 | df$race == 210 ~ 2,
                            df$race != 100 | df$race != 200 | df$race != 210 ~ 3)
  }
  
  if("head" %in% names(df) == F){
    df$head <- if_else(df$relate == 101, 1, 0)
  }
  
  # ED-street combo
  df$ed_street <- paste(df$ed, df$street_final, sep = " X ")
  
  # rename serial if splithid isn't in data
  if("splithid" %in% names(df) == F){
    df$splithid <- df$serial
  }
  
  ### calculate values
  
  # city info
  #city_code <- ifelse(is.numeric(df$city), unique(df$city), as.numeric(NA))
  
  state <- str_extract(file_name, "[A-Z][A-Z].dta") %>% 
    str_replace(".dta", "")
  
  city <- str_replace(file_name, "[A-Z][A-Z].dta", "") %>% 
    gsub("([a-z])([A-Z])", "\\1 \\2", .) %>% 
    str_replace("St ", "St. ") %>% 
    paste(state, sep = ", ")
  
  totalpop <- nrow(df) %>% as.numeric()

  blackpop <- filter(df, sisrace == 2) %>% nrow() %>% as.numeric()
  
  pctblack <- round(blackpop / totalpop, 3) * 100
  
  # segregation values
  D_ed <- diss(df, ed)
  
  D_ed_st <- diss(df, ed_street)
  
  #if(year == 1900 & method == "ancestry"){
  #  D_dwell <- diss(df, dwell_ancestry)
  #} else {
  #  D_dwell <- diss(df, dwell_fixed)
  #}
  
  D_hh <- filter(df, is.na(splithid)==F) %>% diss(splithid)
  
  p_ed <- pstar(df, ed)
  
  p_ed_st <- pstar(df, ed_street)
  
  #if(year == 1900 & method == "ancestry"){
  #  p_dwgroup <- dwelling_group_anc(df) %>% pstar(dwgroup)
  #} else {
  #  p_dwgroup <- dwelling_group(df) %>% pstar(dwgroup)
  #}
  
  #if(year == 1900 & method == "ancestry"){
  #  p_dwell <- pstar(df, dwell_ancestry)
  #} else {
  #  p_dwell <- pstar(df, dwell_fixed)
  #}
  
  p_hh <- filter(df, is.na(splithid)==F) %>% pstar(splithid)
  
  sis <- filter(df, head == 1) %>% sis()
  
  nis <- filter(df, head == 1) %>% nbi()
  
  # return a df of results with one row
  tibble(city, state, year, totalpop, blackpop, pctblack, D_ed, D_ed_st, D_hh,
         p_ed, p_ed_st, p_hh, sis, nis)
}
