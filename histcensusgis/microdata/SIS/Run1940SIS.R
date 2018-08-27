## Run "no_blanks" version of indices for 1940

source("calc_seg_sis.R")
library(stringr)

years <- c(1940)

allfiles <- list()

# collect all file information to load
for(a in 1:length(years)){
  yearfiles <- list.files(paste0("/home/s4-data/LatestCities/SIS/FinalData/", years[a]))
  hold <- list()
  for(b in 1:length(yearfiles)){
    hold[[b]] <- c(yearfiles[b], years[a])
  }
  allfiles <- c(allfiles, hold)
}

# run the numbers
for(x in 1:length(allfiles)){
  tryCatch({
    temp1 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], "full")
    temp2 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], "nosrv")
    temp3 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], "nosrvblnk")
    if(x == 1){
      results <- bind_rows(temp1, temp2, temp3)
    } else {
      results <- bind_rows(results, temp1, temp2, temp3)
    }
  }, error=function(e){cat(conditionMessage(e), "Error on ", allfiles[[x]][1], " in ", allfiles[[x]][2], " \n")})
}


write_csv(results, paste0("SIS1940ResultsBW.csv"))
