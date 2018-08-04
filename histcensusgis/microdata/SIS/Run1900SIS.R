## Run "no_blanks" version of indices for 1900

source("calc_seg_sis.R")
library(stringr)

years <- c(1900)

allfiles <- list()

# collect all file information to load
for(a in 1:length(years)){
  yearfiles <- list.files(paste0("/home/s4-data/LatestCities/SIS/FinalData/", years[a]))
  yearfiles <- yearfiles[!str_detect(yearfiles, "_black_n_WH")]
  hold <- list()
  for(b in 1:length(yearfiles)){
    hold[[b]] <- c(yearfiles[b], years[a])
  }
  allfiles <- c(allfiles, hold)
}



for(x in 1:length(allfiles)){
  tryCatch({
    temp <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2])
    if(x == 1){
      results <- temp
    } else {
      results <- bind_rows(results, temp)
    }
  }, error=function(e){cat(conditionMessage(e), "Error on ", allfiles[[x]][1], " in ", allfiles[[x]][2], " \n")})
}


write_csv(results, paste0("SIS1900ResultsBW.csv"))
