### This script contains custom functions to calculate Dissimilarity
### and Isolation indices for IPUMS microdata that has been formatted
### for SIS calculations, functions rely on "sisrace" variable

### Code by Ben Bellman
### Partly based on old code by Nate Frey 

### Also includes functions for SIS and Neighbor index,
### see notes for formatting before running function

library(data.table)
library(dplyr)
library(dtplyr)
library(randtests)

# rows = object of formatted microdata for one city
# unit = variable containing spatial unit information, no quotes!
diss <- function(rows, unit){
  unit <- enquo(unit)
  
  counts <- as_tibble(rows) %>%
    filter(sisrace == 1 | sisrace == 2) %>% 
    mutate(b = sisrace-1,
           w = abs(sisrace-2)) %>% 
    group_by(!!unit) %>%
    summarise(w_tot = sum(w),
              b_tot = sum(b))
    
  round(sum(abs(counts$w_tot/sum(counts$w_tot)-counts$b_tot/sum(counts$b_tot)))*0.5, 3)
}

# rows = object of formatted microdata
# unit = text string of variable containing spatial unit information
pstar <- function(rows, unit){
  unit <- enquo(unit)
  
  counts <- as_tibble(rows) %>%
    filter(sisrace == 1 | sisrace == 2) %>% 
    mutate(b = sisrace-1,
           w = abs(sisrace-2)) %>% 
    group_by(!!unit) %>%
    summarise(w_tot = sum(w),
              b_tot = sum(b),
              tot = w_tot + b_tot)
  
  sum((counts$b_tot / counts$tot)*(counts$b_tot / sum(counts$b_tot))) %>% 
    round(3)
}


### Must feed in data at desired level of analysis (e.g. household, dwelling)
### rename order var to splithid if not final IPUMS version
sis <- function(rows){
  test <- rows %>% 
    filter(sisrace < 3) %>% 
    arrange(splithid) %>% 
    .[["sisrace"]] %>% 
    runs.test("two.sided",threshold=1.1)
  round(1-((test$runs - 2) / (test$mu - 2)), 3)
}

### Must feed in data at desired level of analysis (e.g. household, dwelling)
### rename order var to splithid if not final IPUMS version
nbi <- function(rows){
  units <- rows %>% 
    #filter(sisrace < 3) %>% 
    mutate(b = if_else(sisrace == 2, 1, 0),
           w = if_else(sisrace == 1, 1, 0)) %>%
    arrange(splithid)
  
  if(sum(units$b, na.rm = T) > 0){
    w_neighs <- embed(units$w, 3)[,-2]
    units$w_neigh <- 0
    units$w_neigh[-c(1,nrow(units))] <- apply(w_neighs, 1, max)
    units$w_neigh[1] <- units$w[2]
    units$w_neigh[nrow(nrow(units))] <- units$w[nrow(units)-1]
    
    b_all <- sum(units$b, na.rm = T)
    w_all <- sum(units$w, na.rm = T)
    
    x_b <- filter(units, b == 1 & w_neigh == 1) %>% nrow()
    
    exp_max <- b_all*(1-((b_all-1)/(b_all-1+w_all))*((b_all-2)/(b_all-2+w_all)))
    exp_min <- 2
    
    round((exp_max - x_b)/(exp_max - exp_min), 3)
  } else {
    NA
  }
}

