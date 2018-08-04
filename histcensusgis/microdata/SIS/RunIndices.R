### this script runs SIS project indices on server in parallel

library(doParallel)
library(foreach)
library(randtests)
library(data.table)
library(dplyr)
library(dtplyr)
library(tidyr)
library(haven)
library(readr)
library(stringr)
library(tibble)

### define all functions

source("calc_seg_sis.R")

#############
#############

# start running numbers


years <- c(1900, 1910, 1920, 1930, 1940)

allfiles <- list()

# collect all file information to load
for(a in 1:5){
  yearfiles <- list.files(paste0("/home/s4-data/LatestCities/SIS/FinalData/", years[a]))
  hold <- list()
  for(b in 1:length(yearfiles)){
    hold[[b]] <- c(yearfiles[b], years[a])
  }
  allfiles <- c(allfiles, hold)
}


# calculate indices in parallel

#cl <- makeCluster(16) # using 16 processors on server
#registerDoParallel(cl)

#results <- foreach(x = allfiles, .combine = "bind_rows", 
#                   .packages = c("dplyr","haven","readr","stringr","tibble",
#                                 "data.table","dtplyr","randtests","tidyr")) %dopar% {
#  calc_seg_sis(x[1], x[2])
#}
#stop cluster
#stopCluster(cl)

for(x in 1:length(allfiles)){
  tryCatch({
    temp <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2])
  }, error=function(e){cat(conditionMessage(e), "Index: ", x, " \n")})
  if(x == 1){
    results <- temp
  } else {
    results <- bind_rows(results, temp)
  }
}

                   
write_csv(results, "sis_results_v1.csv")
