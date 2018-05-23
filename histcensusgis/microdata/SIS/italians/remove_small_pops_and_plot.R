##The purpose of this script is to restrict segregation analysis to only cities meeting pre-defined criteria
##Currently 30,000 total population plus 100 households headed by the group of interest
##It also outputs long and wide tables and a series of plots using ggplot2

##Last updated July 2017 by Nate Frey with cosmetic updates on 13 July 

library(data.table)
library(dplyr)
library(dtplyr)

full1880 <- fread("revised_1880_extract.txt")
full1880.head <- full1880[full1880$related==101,]
full1880.pkeep <- full1880[,.N>=30000,by=city][V1==TRUE,]
full1880.italkeep <- full1880.head[,sum(ital2gens)>=100,by=city][V1==TRUE,]
full1880.italkeep <- full1880.head[full1880.head$city %in% full1880.italkeep$city,]
full1880.italkeep.pkeep <- full1880.italkeep[full1880.italkeep$city %in% full1880.pkeep$city,]
cities1880 <- unique(full1880.italkeep.pkeep$city)
rm(full1880,full1880.head,full1880.pkeep,full1880.italkeep,full1880.italkeep.pkeep)

full1900 <- fread("revised_1900_extract.txt")
full1900.head <- full1900[full1900$self_empty_info_relationtohead == "Head",]
full1900.pkeep <- full1900[,.N>=30000,by=citystate][V1==TRUE,]
full1900.italkeep <- full1900.head[,sum(ital2gens)>=100,by=citystate][V1==TRUE,]
full1900.italkeep <- full1900.head[full1900.head$citystate %in% full1900.italkeep$citystate,]
full1900.italkeep.pkeep <- full1900.italkeep[full1900.italkeep$citystate %in% full1900.pkeep$citystate,]
cities1900 <- unique(full1900.italkeep.pkeep$citystate)
rm(full1900,full1900.head,full1900.pkeep,full1900.italkeep,full1900.italkeep.pkeep)

full1910 <- fread("revised_1910_extract.txt")
full1910.head <- full1910[full1910$RelationToHead=="Head",]
full1910.pkeep <- full1910[,.N>=30000,by=citystate][V1==TRUE,]
full1910.italkeep <- full1910.head[,sum(ital2gens)>=100,by=citystate][V1==TRUE,]
full1910.italkeep <- full1910.head[full1910.head$citystate %in% full1910.italkeep$citystate,]
full1910.italkeep.pkeep <- full1910.italkeep[full1910.italkeep$citystate %in% full1910.pkeep$citystate,]
cities1910 <- unique(full1910.italkeep.pkeep$citystate)
rm(full1910,full1910.head,full1910.pkeep,full1910.italkeep,full1910.italkeep.pkeep)

full1920 <- fread("revised_1920_extract.txt")
full1920.head <- full1920[full1920$relate=="Head/householder",]
full1920.pkeep <- full1920[,.N>=30000,by=citystate][V1==TRUE,]
full1920.italkeep <- full1920.head[,sum(ital2gens)>=100,by=citystate][V1==TRUE,]
full1920.italkeep <- full1920.head[full1920.head$citystate %in% full1920.italkeep$citystate,]
full1920.italkeep.pkeep <- full1920.italkeep[full1920.italkeep$citystate %in% full1920.pkeep$citystate,]
cities1920 <- unique(full1920.italkeep.pkeep$citystate)
rm(full1920,full1920.head,full1920.pkeep,full1920.italkeep,full1920.italkeep.pkeep)


full1930 <- fread("revised_1930_extract.txt")
full1930.head <- full1930[full1930$relate=="Head/householder",]
full1930.pkeep <- full1930[,.N>=30000,by=citystate][V1==TRUE,]
full1930.italkeep <- full1930.head[,sum(ital2gens)>=100,by=citystate][V1==TRUE,]
full1930.italkeep <- full1930.head[full1930.head$citystate %in% full1930.italkeep$citystate,]
full1930.italkeep.pkeep <- full1930.italkeep[full1930.italkeep$citystate %in% full1930.pkeep$citystate,]
cities1930 <- unique(full1930.italkeep.pkeep$citystate)
rm(full1930,full1930.head,full1930.pkeep,full1930.italkeep,full1930.italkeep.pkeep)

###Note that 1940 doesn't have 2 gens and therefore is calculating something somewhat different

full1940 <- fread("revised_1940_extract.txt")
full1940.head <- full1940[full1940$relate=="Head/householder",]
full1940.pkeep <- full1940[,.N>=30000,by=city][V1==TRUE,]
full1940.italkeep <- full1940.head[,sum(italian)>=100,by=city][V1==TRUE,]
full1940.italkeep <- full1940.head[full1940.head$city %in% full1940.italkeep$city,]
full1940.italkeep.pkeep <- full1940.italkeep[full1940.italkeep$city %in% full1940.pkeep$city,]
cities1940 <- unique(full1940.italkeep.pkeep$city)

cities.df <- as.data.table(cbind(cities1880,cities1900,cities1910,cities1920,cities1930,cities1940))
cities.df$cities1880[duplicated(cities.df$cities1880)] <- NA
cities.df$cities1900[duplicated(cities.df$cities1900)] <- NA
cities.df$cities1910[duplicated(cities.df$cities1910)] <- NA
cities.df$cities1920[duplicated(cities.df$cities1920)] <- NA
cities.df$cities1930[duplicated(cities.df$cities1930)] <- NA
cities.df$cities1940[duplicated(cities.df$cities1940)] <- NA
fwrite(cities.df,"italgen2citiesxyear.csv",eol="\r\n")

########TO DO: CLEAN THIS UP
statexwalk <- fread("stateabbrev_eth.csv")
cities.df$city1900 <- gsub("\\,.*","",cities.df$cities1900)
cities.df$state1900 <- gsub("^.*\\, ","",cities.df$cities1900)
statexwalk <- rename(statexwalk,state1900 = State)
statexwalk$state1900 <- toupper(statexwalk$state1900)
cities.df <- merge(cities.df,statexwalk,by="state1900",all.x=TRUE)

cities.df$state1900[!is.na(cities.df$stateclean)] <- cities.df$stateclean[!is.na(cities.df$stateclean)]

cities.df$stateclean <- NULL

cities.df$cities1900 <- paste0(cities.df$city1900,", ",cities.df$state1900)
cities.df$cities1900 <- toupper(cities.df$cities1900)
cities.df$state1900 <- NULL
cities.df$city1900 <- NULL


statexwalk <- fread("stateabbrev_eth.csv")
cities.df$city1910 <- gsub("\\,.*","",cities.df$cities1910)
cities.df$state1910 <- gsub("^.*\\, ","",cities.df$cities1910)
statexwalk <- rename(statexwalk,state1910 = State)
statexwalk$state1910 <- toupper(statexwalk$state1910)
cities.df <- merge(cities.df,statexwalk,by="state1910",all.x=TRUE)

cities.df$state1910[!is.na(cities.df$stateclean)] <- cities.df$stateclean[!is.na(cities.df$stateclean)]

cities.df$stateclean <- NULL

cities.df$cities1910 <- paste0(cities.df$city1910,", ",cities.df$state1910)
cities.df$cities1910 <- toupper(cities.df$cities1910)

cities.df$city1910 <- NULL
cities.df$state1910 <- NULL


statexwalk <- fread("stateabbrev_eth.csv")
cities.df$city1920 <- gsub("\\,.*","",cities.df$cities1920)
cities.df$state1920 <- gsub("^.*\\, ","",cities.df$cities1920)
statexwalk <- rename(statexwalk,state1920 = State)
statexwalk$state1920 <- toupper(statexwalk$state1920)
cities.df <- merge(cities.df,statexwalk,by="state1920",all.x=TRUE)

cities.df$state1920[!is.na(cities.df$stateclean)] <- cities.df$stateclean[!is.na(cities.df$stateclean)]

cities.df$stateclean <- NULL

cities.df$cities1920 <- paste0(cities.df$city1920,", ",cities.df$state1920)
cities.df$cities1920 <- toupper(cities.df$cities1920)

cities.df$city1920 <- NULL
cities.df$state1920 <- NULL


statexwalk <- fread("stateabbrev_eth.csv")
cities.df$city1930 <- gsub("\\,.*","",cities.df$cities1930)
cities.df$state1930 <- gsub("^.*\\, ","",cities.df$cities1930)
statexwalk <- rename(statexwalk,state1930 = State)
statexwalk$state1930 <- toupper(statexwalk$state1930)
cities.df <- merge(cities.df,statexwalk,by="state1930",all.x=TRUE)

cities.df$state1930[!is.na(cities.df$stateclean)] <- cities.df$stateclean[!is.na(cities.df$stateclean)]

cities.df$stateclean <- NULL

cities.df$cities1930 <- paste0(cities.df$city1930,", ",cities.df$state1930)
cities.df$cities1930 <- toupper(cities.df$cities1930)

cities.df$city1930 <- NULL
cities.df$state1930 <- NULL


cities.df[cities.df=="NA, NA"] <- NA

fwrite(cities.df,"citiesxyear.ital.txt",sep="|",eol="\r\n")

##I spent a lot of time trying to loop this bit up, but due to idiosyncracies of data.table it wasn't working and eventually I gave up
meltedmeasures <- fread("./ital/meltedmeasures.ital2gens.txt")
temp.df <- meltedmeasures[meltedmeasures$year==1880,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1880,]
rebuild_melted_measures <- temp.df

temp.df <- meltedmeasures[meltedmeasures$year==1900,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1900,]
rebuild_melted_measures <- rbind(rebuild_melted_measures,temp.df)

temp.df <- meltedmeasures[meltedmeasures$year==1910,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1910,]
rebuild_melted_measures <- rbind(rebuild_melted_measures,temp.df)

temp.df <- meltedmeasures[meltedmeasures$year==1920,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1920,]
rebuild_melted_measures <- rbind(rebuild_melted_measures,temp.df)

temp.df <- meltedmeasures[meltedmeasures$year==1930,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1930,]
rebuild_melted_measures <- rbind(rebuild_melted_measures,temp.df)

temp.df <- meltedmeasures[meltedmeasures$year==1940,]
temp.df <- temp.df[temp.df$citystate %in% cities.df$cities1940,]
rebuild_melted_measures <- rbind(rebuild_melted_measures,temp.df)

fwrite(rebuild_melted_measures,"./ital/meltedmeasures.ital2gens.crit.txt",sep="|",eol="\r\n")

meltedmeasures <- fread("./ital/meltedmeasures.ital2gens.crit.txt")

meltedmeasures <- meltedmeasures[meltedmeasures$variable!="mu" & meltedmeasures$variable!="runs",]

#meltedmeasures <- rebuild_melted_measures


unmelt <- dcast(meltedmeasures, citystate + year ~ variable) ##variables "wide", everything else "long"
unmelt2 <- dcast(meltedmeasures,citystate ~ variable + year) ##Fully "wide" table (cities on y axis)


facet.plot <- ggplot(data=meltedmeasures, aes(x=year, y = value, colour = variable, group = variable)) + 
  geom_line() + geom_point() + facet_wrap(~citystate)
ggsave("allfacetplots.ital2gens.png",plot=facet.plot,width=18,height=12,units="in")

