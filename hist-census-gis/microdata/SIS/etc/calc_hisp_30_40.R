library(data.table)
library(dplyr)
library(dtplyr)

full1940 <- fread("revised_1940_extract.txt")

##generate some dummy variables for mexicans, puerto ricans, and hispanics
full1940$mex <- 0
full1940$mex[full1940$bpl=="MEXICO"] <- 1
full1940$pr <- 0
full1940$pr[full1940$bpl=="PUERTO RICO"] <- 1
full1940$hisp_dum <- 0
full1940$hisp_dum[full1940$hispan!="Not Hispanic"] <- 1

##get counts by city
hisp_tabs_1940 <- full1940[,.(sum(mex),sum(pr),sum(hisp_dum),.N),by="city"] ##aggregate populations to the city level
names(hisp_tabs_1940) <- c("city","n_mex","n_pr","n_hisp","city_pop") ##you lose variable names in the previous line, give them some reasonable names

fwrite(hisp_tabs_1940,"hispanic_tabs_1940.csv",eol="\r\n") ##write out a csv of the result

rm(list=ls()) ##get that stuff out of memory

full1930 <- fread("revised_1930_extract.txt")
full1930$mex <- 0
full1930$mex[full1930$bpl=="MEXICO"] <- 1
full1930$pr <- 0
full1930$pr[full1930$bpl=="PUERTO RICO"] <- 1

##Combined 1st & 2nd-gen, not possible in 1940

states <- fread("/home/s4-data/LatestCities/SIS/stateabbrev_eth.csv") ##list of states, needed to establish nativity

full1930$mex_2gens <- 0
full1930$mex_2gens[full1930$mex==1 | full1930$mbpl == "MEXICO" | full1930$fbpl == "MEXICO"] <- 1
full1930$mex_2gens[full1930$mbpl!="MEXICO" & full1930$bpl!="MEXICO" & !(full1930$mbpl %in% states$State) & full1930$fbpl=="MEXICO"] <- 0

full1930$pr_2gens <- 0
full1930$pr_2gens[full1930$pr==1 | full1930$mbpl == "PUERTO RICO" | full1930$fbpl == "PUERTO RICO"] <- 1
full1930$pr_2gens[full1930$mbpl!="PUERTO RICO" & full1930$bpl!="PUERTO RICO" & !(full1930$mbpl %in% states$State) & full1930$fbpl=="PUERTO RICO"] <- 0

hisp_tabs_1930 <- full1930[,.(sum(mex),sum(pr),sum(mex_2gens),sum(pr_2gens),.N),by="citystate"]
names(hisp_tabs_1930) <- c("city","n_mex","n_pr","n_mex2gen","n_pr2gen","citypop")

fwrite(hisp_tabs_1930,"hispanic_tabs_1930.csv",eol="\r\n")
