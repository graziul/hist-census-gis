##This file:
##          1) generates all indices of interest for Italians (2-generations
##          2) exports them in a "long" text file format

##Last updated by Nate Frey in June 2017; cosmetic updates in July 2017

require(randtests)
require(data.table)
require(dplyr)
require(dtplyr)
require(ggplot2)

setwd("/home/s4-data/LatestCities/SIS/")

full1880 <- fread("revised_1880_extract.txt")

########ITALIANS
##Calculate SIS
list.of.runs.by.city <- list() ##Initialize List 

for (i in 1:length(unique(full1880$city))){ ##initialize loop over list of cities
city.sub <- full1880[full1880$city == unique(full1880$city)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$serial),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$relate == "Head/Householder",] ##Keep only householders
city.sub.hh.bw <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.bw$siseth <- 0
city.sub.hh.bw$siseth[city.sub.hh.bw$wnbnp==1] <- 1
city.sub.hh.bw$siseth[city.sub.hh.bw$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[4],unique(full1880$city)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}


sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1880.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated)


##Calculate Dissimilarity Index
diss.df <- as.data.frame(cbind(rep("city",length(unique(full1880$city))),rep(0,length(unique(full1880$city))))) ##empty df for values
names(diss.df) <- c("city","diss") ##name columns
diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
diss.df$diss <- as.character(diss.df$diss)

for (i in 1:length(unique(full1880$city))) { ##initialize loop over list of unique cities

city.sub <- full1880[full1880$city==unique(full1880$city)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate=="Head/Householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
diss.df[i,1] <- unique(full1880$city)[i] ##put the appropriate city name in output df
diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df

}

fwrite(diss.df,"./ital/diss1880.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated

##Same process for exposure/isolation indices
expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1880$city))),rep(0,length(unique(full1880$city)))
,rep(0,length(unique(full1880$city))),rep(0,length(unique(full1880$city))),rep(0,length(unique(full1880$city)))))
names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
expisol.df$expiw <- as.character(expisol.df$expiw)
expisol.df$expwi <- as.character(expisol.df$expwi)
expisol.df$isolii <- as.character(expisol.df$isolii)
expisol.df$isolww <- as.character(expisol.df$isolww)


for (i in 1:length(unique(full1880$city))) { ##initialize loop over list of unique cities

city.sub <- full1880[full1880$city==unique(full1880$city)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate=="Head/Householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
expisol.df[i,1] <- unique(full1880$city)[i] ##put the appropriate city name in output df
expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

}

fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1880.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())

#######1900

full1900 <- fread("revised_1900_extract.txt")
#######ITALIANS

list.of.runs.by.city <- list() ##Initialize List 

for (i in 1:length(unique(full1900$citystate))){ ##initialize loop over list of cities
city.sub <- full1900[full1900$citystate == unique(full1900$citystate)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$general_order_on_page),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$self_empty_info_relationtohead == "Head",] ##Keep only householders
city.sub.hh.bw <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.bw$siseth <- 0
city.sub.hh.bw$siseth[city.sub.hh.bw$wnbnp==1] <- 1
city.sub.hh.bw$siseth[city.sub.hh.bw$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[4],unique(full1900$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}

sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1900.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated)


#
####ITALIANS

diss.df <- as.data.frame(cbind(rep("city",length(unique(full1900$citystate))),rep(0,length(unique(full1900$citystate))))) ##empty df for values
names(diss.df) <- c("city","diss") ##name columns
diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
diss.df$diss <- as.character(diss.df$diss)

for (i in 1:length(unique(full1900$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1900[full1900$citystate==unique(full1900$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$self_empty_info_relationtohead == "Head",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(indexed_enumeration_district)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
diss.df[i,1] <- unique(full1900$citystate)[i] ##put the appropriate city name in output df
diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df

}

fwrite(diss.df,"./ital/diss1900.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated

##Same process for exposure/isolation indices
expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1900$citystate))),rep(0,length(unique(full1900$citystate)))
,rep(0,length(unique(full1900$citystate))),rep(0,length(unique(full1900$citystate))),rep(0,length(unique(full1900$citystate)))))
names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
expisol.df$expiw <- as.character(expisol.df$expiw)
expisol.df$expwi <- as.character(expisol.df$expwi)
expisol.df$isolii <- as.character(expisol.df$isolii)
expisol.df$isolww <- as.character(expisol.df$isolww)


for (i in 1:length(unique(full1900$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1900[full1900$citystate==unique(full1900$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$self_empty_info_relationtohead=="Head",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(indexed_enumeration_district)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
expisol.df[i,1] <- unique(full1900$citystate)[i] ##put the appropriate city name in output df
expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

}

fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1900.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())

#####1910


full1910 <- fread("revised_1910_extract.txt")
full1910 <- full1910[!duplicated(full1910),]

######ITALIANS


#MPC suggested sort version 
list.of.runs.by.city <- list() ##Initialize List 

for (i in 1:length(unique(full1910$citystate))){ ##initialize loop over list of cities
city.sub <- full1910[full1910$citystate == unique(full1910$citystate)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$ImageFileName, city.sub$LineNumber,city.sub$ycord),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$RelationToHead == "Head",] ##Keep only householders
city.sub.hh.bw <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.bw$siseth <- 0
city.sub.hh.bw$siseth[city.sub.hh.bw$wnbnp==1] <- 1
city.sub.hh.bw$siseth[city.sub.hh.bw$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[4],unique(full1910$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}

sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1910.ital2gens.mpcversion.txt",sep="|",eol="\r\n") ##Output (pipe separated)


######ITALIANS


#MPC suggested sort version 
list.of.runs.by.city <- list() ##Initialize List 

for (i in 1:length(unique(full1910$citystate))){ ##initialize loop over list of cities
city.sub <- full1910[full1910$citystate == unique(full1910$citystate)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$ImageFileName, city.sub$LineNumber,city.sub$ycord),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$RelationToHead == "Head",] ##Keep only householders
city.sub.hh.bw <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.bw$siseth <- 0
city.sub.hh.bw$siseth[city.sub.hh.bw$wnbnp==1] <- 1
city.sub.hh.bw$siseth[city.sub.hh.bw$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.bw$siseth,"two.sided",threshold=1.1)[4],unique(full1910$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}

sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1910.ital2gens.mpcversion.txt",sep="|",eol="\r\n") ##Output (pipe separated)

######ITALIANS

diss.df <- as.data.frame(cbind(rep("city",length(unique(full1910$citystate))),rep(0,length(unique(full1910$citystate))))) ##empty df for values
names(diss.df) <- c("city","diss") ##name columns
diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
diss.df$diss <- as.character(diss.df$diss)


for (i in 1:length(unique(full1910$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1910[full1910$citystate==unique(full1910$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$RelationToHead == "Head",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(EnumerationDistrict)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
diss.df[i,1] <- unique(full1910$citystate)[i] ##put the appropriate city name in output df
diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df

}

fwrite(diss.df,"./ital/diss1910.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated

expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1910$citystate))),rep(0,length(unique(full1910$citystate)))
,rep(0,length(unique(full1910$citystate))),rep(0,length(unique(full1910$citystate))),rep(0,length(unique(full1910$citystate)))))
names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
expisol.df$expiw <- as.character(expisol.df$expiw)
expisol.df$expwi <- as.character(expisol.df$expwi)
expisol.df$isolii <- as.character(expisol.df$isolii)
expisol.df$isolww <- as.character(expisol.df$isolww)



for (i in 1:length(unique(full1910$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1910[full1910$citystate==unique(full1910$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$RelationToHead=="Head",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(EnumerationDistrict)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
expisol.df[i,1] <- unique(full1910$citystate)[i] ##put the appropriate city name in output df
expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

}

fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1910.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())
gc()

#######1920

full1920 <- fread("revised_1920_extract.txt") 
full1920 <- full1920[!duplicated(full1920),]
library(bit64)



##ITALIANS


list.of.runs.by.city <- list() ##Initialize List 

for (i in 1:length(unique(full1920$citystate))){ ##initialize loop over list of cities
city.sub <- full1920[full1920$citystate == unique(full1920$citystate)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$serial),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$relate == "Head/householder",] ##Keep only householders
city.sub.hh.eth <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.eth$siseth <- 0
city.sub.hh.eth$siseth[city.sub.hh.eth$wnbnp==1] <- 1
city.sub.hh.eth$siseth[city.sub.hh.eth$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[4],unique(full1920$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}


sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1920.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated)
#fwrite(list.of.sis,"NYCsis1920.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated) ##NYC as special case output




diss.df <- as.data.frame(cbind(rep("city",length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate))))) ##empty df for values
names(diss.df) <- c("city","diss") ##name columns
diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
diss.df$diss <- as.character(diss.df$diss)

for (i in 1:length(unique(full1920$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1920[full1920$citystate==unique(full1920$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
diss.df[i,1] <- unique(full1920$citystate)[i] ##put the appropriate city name in output df
diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df


}

fwrite(diss.df,"./ital/diss1920.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated

#fwrite(diss.df,"nycdiss1920.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated



expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate)))
,rep(0,length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate)))))
names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
expisol.df$expiw <- as.character(expisol.df$expiw)
expisol.df$expwi <- as.character(expisol.df$expwi)
expisol.df$isolii <- as.character(expisol.df$isolii)
expisol.df$isolww <- as.character(expisol.df$isolww)


for (i in 1:length(unique(full1920$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1920[full1920$citystate==unique(full1920$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
expisol.df[i,1] <- unique(full1920$citystate)[i] ##put the appropriate city name in output df
expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

}


fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1920.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())

#############NYC 1920 (special case)
#full1920 <- fread("nyc_bpl_1920.txt") ##NYC is a special case and must be run separately
#
#
#list.of.runs.by.city <- list() ##Initialize List 

#for (i in 1:length(unique(full1920$citystate))){ ##initialize loop over list of cities
#city.sub <- full1920[full1920$citystate == unique(full1920$citystate)[i],] ##subset current city
#city.sub <- city.sub[order(city.sub$serial),] ##sort current city by serial #
#city.sub.hh <- city.sub[city.sub$relate == "Head/householder",] ##Keep only householders
#city.sub.hh.eth <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
#city.sub.hh.eth$siseth <- 0
#city.sub.hh.eth$siseth[city.sub.hh.eth$wnbnp==1] <- 1
#city.sub.hh.eth$siseth[city.sub.hh.eth$ital2gens==1] <- 2
#rm(city.sub, city.sub.hh) ##get rid of these
#list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[4],unique(full1920$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
#}


#sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
#list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

#list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
#cbind(
#x,
#sisval=(1-((x$runs - 2) / (x$mu - 2)))
#)
#})

#list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
#names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

#fwrite(list.of.sis,"NYCsis1920.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated) ##NYC as special case output




#diss.df <- as.data.frame(cbind(rep("city",length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate))))) ##empty df for values
#names(diss.df) <- c("city","diss") ##name columns
#diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
#diss.df$diss <- as.character(diss.df$diss)

#for (i in 1:length(unique(full1920$citystate))) { ##initialize loop over list of unique cities

#city.sub <- full1920[full1920$citystate==unique(full1920$citystate)[i],] ##subset city i
#city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
#city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
#names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
#city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
#city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
#diss.df[i,1] <- unique(full1920$citystate)[i] ##put the appropriate city name in output df
#diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df


#}

#fwrite(diss.df,"nycdiss1920.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated



#expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate)))
#,rep(0,length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate))),rep(0,length(unique(full1920$citystate)))))
#names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
#expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
#expisol.df$expiw <- as.character(expisol.df$expiw)
#expisol.df$expwi <- as.character(expisol.df$expwi)
#expisol.df$isolii <- as.character(expisol.df$isolii)
#expisol.df$isolww <- as.character(expisol.df$isolww)


#for (i in 1:length(unique(full1920$citystate))) { ##initialize loop over list of unique cities

#city.sub <- full1920[full1920$citystate==unique(full1920$citystate)[i],] ##subset city i
#city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
#city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
#names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
#city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
#city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
#city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
#city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
#city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
#city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
#city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
#city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
#expisol.df[i,1] <- unique(full1920$citystate)[i] ##put the appropriate city name in output df
#expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
#expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
#expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
#expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

#}


#fwrite(expisol.df[order(expisol.df$city),],"nycexpisol1920.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())

#########1930

full1930 <- fread("revised_1930_extract.txt",integer64="character")
full1930 <- full1930[!duplicated(full1930),]


###ITALIANS
list.of.runs.by.city <- list() ##Initialize List 


for (i in 1:length(unique(full1930$citystate))){ ##initialize loop over list of cities
city.sub <- full1930[full1930$citystate == unique(full1930$citystate)[i],] ##subset current city
city.sub <- city.sub[order(city.sub$serial),] ##sort current city by serial #
city.sub.hh <- city.sub[city.sub$relate == "Head/householder",] ##Keep only householders
city.sub.hh.eth <- city.sub.hh[city.sub.hh$wnbnp == 1 | city.sub.hh$ital2gens == 1,] ##Keep only two race categories
city.sub.hh.eth$siseth <- 0
city.sub.hh.eth$siseth[city.sub.hh.eth$wnbnp==1] <- 1
city.sub.hh.eth$siseth[city.sub.hh.eth$ital2gens==1] <- 2
rm(city.sub, city.sub.hh) ##get rid of these
list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[4],unique(full1930$citystate)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
}



sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
cbind(
x,
sisval=(1-((x$runs - 2) / (x$mu - 2)))
)
})

list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

fwrite(list.of.sis,"./ital/sis1930.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated)


####ITALIANS

diss.df <- as.data.frame(cbind(rep("city",length(unique(full1930$citystate))),rep(0,length(unique(full1930$citystate))))) ##empty df for values
names(diss.df) <- c("city","diss") ##name columns
diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
diss.df$diss <- as.character(diss.df$diss)

for (i in 1:length(unique(full1930$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1930[full1930$citystate==unique(full1930$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
diss.df[i,1] <- unique(full1930$citystate)[i] ##put the appropriate city name in output df
diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df

}

fwrite(diss.df,"./ital/diss1930.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-separated


expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1930$citystate))),rep(0,length(unique(full1930$citystate)))
,rep(0,length(unique(full1930$citystate))),rep(0,length(unique(full1930$citystate))),rep(0,length(unique(full1930$citystate)))))
names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
expisol.df$expiw <- as.character(expisol.df$expiw)
expisol.df$expwi <- as.character(expisol.df$expwi)
expisol.df$isolii <- as.character(expisol.df$isolii)
expisol.df$isolww <- as.character(expisol.df$isolww)


for (i in 1:length(unique(full1930$citystate))) { ##initialize loop over list of unique cities

city.sub <- full1930[full1930$citystate==unique(full1930$citystate)[i],] ##subset city i
city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
city.sub.agg <- city.sub[,.(sum(ital2gens),sum(wnbnp),.N),by=.(enumdist)] ##aggregate counts to ED
names(city.sub.agg) <- c("enumdist","ital2gens","wnbnp","N") ##name variables that lost their names
city.sub.agg$iI <- city.sub.agg$ital2gens/sum(city.sub.agg$ital2gens) ##calculate fraction of total city black pop in ED
city.sub.agg$wW <- city.sub.agg$wnbnp/sum(city.sub.agg$wnbnp) ##calculate fraction of total city white pop in ED
city.sub.agg$it <- city.sub.agg$ital2gens/city.sub.agg$N
city.sub.agg$wt <- city.sub.agg$wnbnp/city.sub.agg$N
city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
expisol.df[i,1] <- unique(full1930$citystate)[i] ##put the appropriate city name in output df
expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

}


fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1930.ital2gens.txt",sep="|",eol="\r\n")

rm(list=ls())

# ###########1940 -- not run, no gen2!
 
 # full1940 <- fread("revised_1940_extract.txt",integer64="character")

# full1940 <- full1940[!duplicated(full1940),]

# ######ITALIANS


# list.of.runs.by.city <- list() ##Initialize List 

# for (i in 1:length(unique(full1940$city))){ ##initialize loop over list of cities
# city.sub <- full1940[full1940$city == unique(full1940$city)[i],] ##subset current city
# city.sub <- city.sub[order(city.sub$serial),] ##sort current city by serial #
# city.sub.hh <- city.sub[city.sub$relate == "Head/householder",] ##Keep only householders
# city.sub.hh.eth <- city.sub.hh[city.sub.hh$wnb == 1 | city.sub.hh$italian == 1,] ##Keep only two race categories
# city.sub.hh.eth$siseth <- 0
# city.sub.hh.eth$siseth[city.sub.hh.eth$wnb==1] <- 1
# city.sub.hh.eth$siseth[city.sub.hh.eth$italian==1] <- 2
# rm(city.sub, city.sub.hh) ##get rid of these
# list.of.runs.by.city[[i]] <- cbind(runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[3],runs.test(city.sub.hh.eth$siseth,"two.sided",threshold=1.1)[4],unique(full1940$city)[i]) ##The [3] pulls the n(runs) value, the [4] pulls the mu value
# }

# sis.colnames <- c("runs","mu","city") ##what should the names of the DF columns be in the list
# list.of.runs.by.city <- lapply(list.of.runs.by.city,setNames,sis.colnames) ##use lapply to make it happen

# list.of.sis <- lapply(list.of.runs.by.city,function(x){ ##give each DF a new SIS value column
# cbind(
# x,
# sisval=(1-((x$runs - 2) / (x$mu - 2)))
# )
# })

# list.of.sis <- rbindlist(list.of.sis) ##turn that back into a df
# names(list.of.sis) <- c("runs","mu","city","sisvalue") ##rename the variables

# fwrite(list.of.sis,"./ital/sis1940.ital2gens.txt",sep="|",eol="\r\n") ##Output (pipe separated)


# ####ITALIANS

# diss.df <- as.data.frame(cbind(rep("city",length(unique(full1940$city))),rep(0,length(unique(full1940$city))))) ##empty df for values
# names(diss.df) <- c("city","diss") ##name columns
# diss.df$city <- as.character(diss.df$city) ##these gen as factor for some reason
# diss.df$diss <- as.character(diss.df$diss)

# for (i in 1:length(unique(full1940$city))) { ##initialize loop over list of unique cities

# city.sub <- full1940[full1940$city==unique(full1940$city)[i],] ##subset city i
# city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
# city.sub.agg <- city.sub[,.(sum(italian),sum(wnb),.N),by=.(enumdist)] ##aggregate counts to ED
# names(city.sub.agg) <- c("enumdist","italian","wnb","N") ##name variables that lost their names
# city.sub.agg$iI <- city.sub.agg$italian/sum(city.sub.agg$italian) ##calculate fraction of total city black pop in ED
# city.sub.agg$wW <- city.sub.agg$wnb/sum(city.sub.agg$wnb) ##calculate fraction of total city white pop in ED
# diss.df[i,1] <- unique(full1940$city)[i] ##put the appropriate city name in output df
# diss.df[i,2] <- 0.5 * sum(abs(city.sub.agg$iI - city.sub.agg$wW)) ##calculate the dissimilarity index and place it in output df

# }

# fwrite(diss.df,"./ital/diss1940.italian.txt",sep="|",eol="\r\n") ##write out pipe-separated


# expisol.df <- as.data.frame(cbind(rep("city",length(unique(full1940$city))),rep(0,length(unique(full1940$city)))
# ,rep(0,length(unique(full1940$city))),rep(0,length(unique(full1940$city))),rep(0,length(unique(full1940$city)))))
# names(expisol.df) <- c("city","expiw","expwi","isolii","isolww")
# expisol.df$city <- as.character(expisol.df$city) ##these gen as factor for some reason
# expisol.df$expiw <- as.character(expisol.df$expiw)
# expisol.df$expwi <- as.character(expisol.df$expwi)
# expisol.df$isolii <- as.character(expisol.df$isolii)
# expisol.df$isolww <- as.character(expisol.df$isolww)


# for (i in 1:length(unique(full1940$city))) { ##initialize loop over list of unique cities

# city.sub <- full1940[full1940$city==unique(full1940$city)[i],] ##subset city i
# city.sub <- city.sub[city.sub$relate == "Head/householder",] ##subset householders for comparability w/ SIS
# city.sub.agg <- city.sub[,.(sum(italian),sum(wnb),.N),by=.(enumdist)] ##aggregate counts to ED
# names(city.sub.agg) <- c("enumdist","italian","wnb","N") ##name variables that lost their names
# city.sub.agg$iI <- city.sub.agg$italian/sum(city.sub.agg$italian) ##calculate fraction of total city black pop in ED
# city.sub.agg$wW <- city.sub.agg$wnb/sum(city.sub.agg$wnb) ##calculate fraction of total city white pop in ED
# city.sub.agg$it <- city.sub.agg$italian/city.sub.agg$N
# city.sub.agg$wt <- city.sub.agg$wnb/city.sub.agg$N
# city.sub.agg$iwexp <- city.sub.agg$iI*city.sub.agg$wt
# city.sub.agg$wiexp <- city.sub.agg$wW*city.sub.agg$it
# city.sub.agg$iiisol <- city.sub.agg$iI*city.sub.agg$it
# city.sub.agg$wwisol <- city.sub.agg$wW*city.sub.agg$wt
# expisol.df[i,1] <- unique(full1940$city)[i] ##put the appropriate city name in output df
# expisol.df[i,2] <-  sum(city.sub.agg$iwexp) ##calculate the bw exposure index and place it in output df
# expisol.df[i,3] <-  sum(city.sub.agg$wiexp) ##calculate the wb exposure index and place it in output df
# expisol.df[i,4] <-  sum(city.sub.agg$iiisol) ##calculate the bb isolation index and place it in output df
# expisol.df[i,5] <-  sum(city.sub.agg$wwisol) ##calculate the ww isolation index and place it in output df

# }

# fwrite(expisol.df[order(expisol.df$city),],"./ital/expisol1940.italian.txt",sep="|",eol="\r\n")


# rm(list=ls())
# gc()

#######COMBINE FILES

setwd("/home/s4-data/LatestCities/SIS/ital")
list.of.diss <- list.files(".",pattern="diss.*ital2gens\\.txt") ##name all dissimilarity files in the directory with the correct string
list.of.diss <- lapply(list.of.diss,fread)
#list.of.diss[[4]] <- rbind(list.of.diss[[4]],list.of.diss[[7]]) ##this binds the main 1920 file with the nyc file
#list.of.diss[[7]] <- NULL ##get rid of NYC now that it's part of the main 1920 file
years <- list(1880,1900,1910,1920,1930)#,1940) 
list.of.diss <- Map(cbind,list.of.diss,year=years) ##give each df a column for the year
diss.df <- rbindlist(list.of.diss) ##create a single df for all values
diss.df$city <- toupper(diss.df$city) ##standardize the city

list.of.expisol <- list.files(".",pattern="expisol.*ital2gens\\.txt")
list.of.expisol <- lapply(list.of.expisol,fread)
#list.of.expisol[[4]] <- rbind(list.of.expisol[[4]],list.of.expisol[[7]])
#list.of.expisol[[7]] <- NULL
years <- list(1880,1900,1910,1920,1930)#,1940)
list.of.expisol <- Map(cbind,list.of.expisol,year=years)
expisol.df <- rbindlist(list.of.expisol)
expisol.df$city <- toupper(expisol.df$city) 

conventional.measures.df <- merge(diss.df,expisol.df,by=c("city","year")) ##merge by unique IDs
conventional.measures.df$city <- toupper(conventional.measures.df$city)

list.of.sis <- list.files(".",pattern="sis.*ital2gens*\\.txt")
list.of.sis <- lapply(list.of.sis,fread)
#list.of.sis[[5]] <- rbind(list.of.sis[[5]],list.of.sis[[1]]) ##same thing to [[4]] and [[7]] above
#list.of.sis[[1]] <- NULL
years <- list(1880,1900,1910,1920,1930)#,1940)
list.of.sis <- Map(cbind,list.of.sis,year=years)
sis.df <- rbindlist(list.of.sis)
sis.df$city <- toupper(sis.df$city)
sis.df$city[sis.df$city=="WASHINGTON, DC" & sis.df$year==1900] <- "WASHINGTON, DISTRICT OF COLUMBIA" ##fix a formatting issue

all.measures.df <- merge(conventional.measures.df,sis.df,by=c("city","year")) ##merge by unique IDs
fwrite(all.measures.df,"allcitiesallyearsallmeasures.ital2gens.txt",sep="|",eol="\r\n") ##write out pipe-delimited


all.measures <- fread("allcitiesallyearsallmeasures.ital2gens.txt") ########Just fix the file syntax
all.measures$city[all.measures$city=="NEW YORK CITY, NEW YORK"] <- "NEW YORK, NEW YORK"
statexwalk <- fread("stateabbrev_eth.csv")
all.measures <- rename(all.measures,citystate = city)
statexwalk <- rename(statexwalk,state=State)
statexwalk$state <- toupper(statexwalk$state)


all.measures$city <- gsub("\\,.*","",all.measures$citystate)
all.measures$state <- gsub("^.*\\, ","",all.measures$citystate)

all.measures.merge <- merge(all.measures,statexwalk,by="state",all.x=TRUE)

all.measures.merge$state[!is.na(all.measures.merge$stateclean)] <- all.measures.merge$stateclean[!is.na(all.measures.merge$stateclean)]

all.measures.merge$stateclean <- NULL

all.measures.merge$citystate <- paste0(all.measures.merge$city,", ",all.measures.merge$state)
all.measures.merge$citystate <- toupper(all.measures.merge$citystate)

all.measures.merge$citystate[all.measures.merge$citystate=="BROOKLYN (ONLY IN CENSUS YEARS BEFORE 1900), BROOKLYN (ONLY IN CENSUS YEARS BEFORE 1900)"] <- "BROOKLYN, NY"

all.measures.to.analyze <- all.measures.merge[,c(2:11)]

all.measures.melted <- melt(all.measures.to.analyze,id.vars=c("citystate","year"))

fwrite(all.measures.melted,"meltedmeasures.ital2gens.txt",sep="|",eol="\r\n")



meltedmeasures <- fread("meltedmeasures.txt")
meltedmeasures <- meltedmeasures[meltedmeasures$variable!="runs" & meltedmeasures$variable != "mu"]

