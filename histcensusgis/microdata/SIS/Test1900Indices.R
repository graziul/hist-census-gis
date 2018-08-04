## Run 3 different versions of 1900

# 1) Ancestry method, drop all records without ancestry dwelling
# 2) House number method, keeping blanks
# 3) House number method, dropping all blank streets or hn

source("calc_seg_sis.R")


years <- c(1900)

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



for(x in 1:length(allfiles)){
  tryCatch({
    temp1 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], method = "ancestry")
    temp2 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], method = "blanks")
    temp3 <- calc_seg_sis(allfiles[[x]][1], allfiles[[x]][2], method = "no_blanks")
    if(x == 1){
      results <- bind_rows(temp1, temp2, temp3)
    } else {
      results <- bind_rows(results, temp1, temp2, temp3)
    }
  }, error=function(e){cat(conditionMessage(e), "Error on ", allfiles[[x]][1], " in ", allfiles[[x]][2], " \n")})
}


write_csv(results, "compare_1900_results_long.csv")

wide <- dcast(setDT(results), city ~ method, value.var = names(df[,6:19])) 

write_csv(wide, "compare_1900_results_wide.csv")

