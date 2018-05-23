
##Calculation of the Neighbor Index for 1880
##Based on Appendix A of Logan & Parman NBER Working Paper 20934 (2015)
##The easiest way to understand the logic is to read that Appendix
##I feel pretty good about the 1880 part of this code, not sure about 1900, no other years attempted
##NF Feb 2017, cosmetic changes July 2017

library(dplyr)
library(dtplyr)
library(data.table)
library(randtests)

full1880 <- fread("bpl_1880.txt")  ##Read 1880 data

full1880.hh <- full1880[full1880$relate=="Head/Householder",] ##subset hh heads
rm(full1880) ##clear out full file

##Dummies for white/black heads of household
full1880.hh$whh <- 0
full1880.hh$whh[full1880.hh$race=="White"] <- 1
full1880.hh$bhh <- 0
full1880.hh$bhh[full1880.hh$race=="Black/Negro"] <- 1

list.of.ni <- list() ##initialize a list into which results will be placed

for(i in 1:length(unique(full1880.hh$city))) {   ##initialize city loop
city.sub <- full1880.hh[full1880.hh$city==unique(full1880.hh$city)[i]]  ##select a city
city.sub <- city.sub[order(city.sub$serial),]  ##sort by serial
city.sub$neighbors <- 2  ##how many neighbors will a person have? (Normally, two.)
city.sub$neighbors[1] <- 1 ##the first person in the sequence will only have one neighbor
city.sub$neighbors[length(unique(city.sub$serial))] <- 1 ##same for the last

##I had an idea about how to do this with an adjacency matrix, which seemed elegant, but I never got there
##adjacency.matrix <- matrix(rep(integer(0),length(unique(city.sub$serial))^2),nrow=length(unique(city.sub$serial)),ncol=length(unique(city.sub$serial)))
##neighbor.radius <- 1


##the logic of this section may or may not be right
##initialize an NA indicator
##for everyone but the first and last person in the sequence, assign the number of black headed households including theirs & those on either side
##binarize that variable for later use by setting it to 1 where the head of household is black but the other value is less than 3 (meaning there's a non-black neighbor)

city.sub$indicator.var <- 99 
city.sub$indicator.var[city.sub$indicator.var==99] <- NA #initialize a numeric NA
city.sub$indicator.var[-(1:1)] <- rowSums(embed(city.sub$bhh,3)) ##Implements the logic described above. Not sure WHY this works anymore, but pretty sure it does
city.sub$indicator.var[length(city.sub$indicator.var)] <- NA ##Final value of indicator variable must be NA
city.sub$indicator.var.bin <- 0  ##set up a binary indicator
city.sub$indicator.var.bin[city.sub$indicator.var<3 & city.sub$bhh==1] <- 1 ##Uses the indicator created above to get a binary indicator of whether the black household has non-black neighbors

bldiffrace <- sum(city.sub$indicator.var.bin) ##Sum the binary indicator (city-wide sum)

##adjacency.matrix[seq(1, length(a), 2)] ##Not used, part of the aforementioned attempt to make this work on an adjacency matrix


whh <- sum(city.sub$whh) ##Constant for all white headed households
bhh <- sum(city.sub$bhh) ##Constant for all black headed households
bhh.one.neighbor <- sum(city.sub$bhh[city.sub$neighbors==1]) ##constant for black-headed households w/ one neighbor
bhh.two.neighbor <- sum(city.sub$bhh[city.sub$neighbors==2]) ##constant for black-headed households w/ two neighbors


##Max value of index in an area (see eq 5 in logan & parman paper)
two.neighbor.exp <- bhh.two.neighbor*(1-(((bhh-1)/(bhh-1+whh))*((bhh-2)/(bhh-2+whh)))) #one of the max terms
one.neighbor.exp <- bhh.one.neighbor*(1-((bhh-1)/(bhh-1+whh))) #other of the max terms
maxexp <- two.neighbor.exp + one.neighbor.exp ##combine terms to get the actual max expectation

##Min value of index in an area (eqs 8-10 in logan & parman paper)
city.sub$product.term <- 0 ##initialize the variable
 
city.sub$product.term <- (bhh-seq(from=1,to=length(city.sub$product.term))-2) / (bhh-seq(from=1,to=length(city.sub$product.term))) ##term is the most complicated part of the min formula, easiest to assign it at person level first

product.term <- prod(city.sub$product.term[is.finite(city.sub$product.term)]) ##...and then actually generate the product for the whole population

minexp <- ((bhh.two.neighbor/bhh)+(bhh.one.neighbor/bhh)* ((1/(0.5*(bhh+1)))*(1-product.term)) + (2*(1-(1/(0.5*(bhh+1))))*(1-product.term))) ##minimum expected value

ni <- (maxexp - bldiffrace) / (maxexp - minexp) ##calculate the NI

list.of.ni[[i]] <- cbind(unique(city.sub$city),ni) ##make this output the i-th element of list.of.ni

print(paste0("Completed ",unique(city.sub$city))) ##print the city that just finished to the terminal
rm(city.sub)
}

list.of.ni <- lapply(list.of.ni,as.data.frame) ##make the list elements data frames
df.of.ni <- rbindlist(list.of.ni) ##rbind them into a single table
names(df.of.ni) <- c("city","ni") ##restore column names

fwrite(df.of.ni,"ni1880.bw.txt",sep="|",eol="\r\n") ##write out pipe-delimited file




#####1900 --- NOT SURE IF THIS (OR THE SUBSEQUENT 1900 CODE BLOCK) ACTUALLY WORK
full1900 <- fread("bpl_1900.txt")


full1900.hh <- full1900[full1900$self_empty_info_relationtohead == "Head",]
rm(full1900)

full1900.hh$whh <- 0
full1900.hh$whh[full1900.hh$sisrace==1] <- 1
full1900.hh$bhh <- 0
full1900.hh$bhh[full1900.hh$sisrace==2] <- 1

list.of.ni <- list()


for(i in 1:length(unique(full1900.hh$citystate))) {
city.sub <- full1900.hh[full1900.hh$citystate==unique(full1900.hh$citystate)[i]]
city.sub <- city.sub[order(city.sub$general_order_on_page),]
city.sub$neighbors <- 2
city.sub$neighbors[1] <- 1 ##the first person in the sequence will only have one neighbor
city.sub$neighbors[length(unique(city.sub$general_order_on_page))] <- 1 ##same for the last
##adjacency.matrix <- matrix(rep(integer(0),length(unique(city.sub$serial))^2),nrow=length(unique(city.sub$serial)),ncol=length(unique(city.sub$serial)))
##neighbor.radius <- 1


##the logic of this section may or may not be right
##initialize an NA indicator
##for everyone but the first and last person in the sequence, assign the number of black headed households including theirs & those on either side
##binarize that variable for later use by setting it to 1 where the head of household is black but the other value is less than 3 (meaning there's a non-black neighbor)

city.sub$indicator.var <- 99
city.sub$indicator.var[city.sub$indicator.var==99] <- NA
city.sub$indicator.var[-(1:1)] <- rowSums(embed(city.sub$bhh,3)) ##I need to come back to this and check the logic, it might be wrong
city.sub$indicator.var[length(city.sub$indicator.var)] <- NA
city.sub$indicator.var.bin <- 0
city.sub$indicator.var.bin[city.sub$indicator.var<3 & city.sub$bhh==1] <- 1 ##Ditto

bldiffrace <- sum(city.sub$indicator.var.bin)

##adjacency.matrix[seq(1, length(a), 2)] ##every other element, not used


whh <- sum(city.sub$whh) ##Constant for all white headed households
bhh <- sum(city.sub$bhh) ##Constant for all black headed households
bhh.one.neighbor <- sum(city.sub$bhh[city.sub$neighbors==1]) ##constant for black-headed households w/ one neighbor
bhh.two.neighbor <- sum(city.sub$bhh[city.sub$neighbors==2]) ##constant for black-headed households w/ two neighbors


##Max value of index in an area (eq 5)
two.neighbor.exp <- bhh.two.neighbor*(1-(((bhh-1)/(bhh-1+whh))*((bhh-2)/(bhh-2+whh)))) #one of the max terms
one.neighbor.exp <- bhh.one.neighbor*(1-((bhh-1)/(bhh-1+whh))) #other of the max terms
maxexp <- two.neighbor.exp + one.neighbor.exp ##combine terms to get the actual max expectation

##Min value of index in an area (8-10)
city.sub$product.term <- 0 ##initialize the variable
city.sub$product.term <- (bhh-seq(from=1,to=length(city.sub$product.term))-2) / (bhh-seq(from=1,to=length(city.sub$product.term)))

product.term <- prod(city.sub$product.term[is.finite(city.sub$product.term)]) ##...and then actually generate the product for the whole population

minexp <- ((bhh.two.neighbor/bhh)+(bhh.one.neighbor/bhh)* ((1/(0.5*(bhh+1)))*(1-product.term)) + (2*(1-(1/(0.5*(bhh+1))))*(1-product.term)))

ni <- (maxexp - bldiffrace) / (maxexp - minexp)

list.of.ni[[i]] <- cbind(unique(city.sub$citystate),ni)

print(paste0("Completed ",unique(city.sub$citystate)))
rm(city.sub)
}

list.of.ni <- lapply(list.of.ni,as.data.frame)
df.of.ni <- rbindlist(list.of.ni)
names(df.of.ni) <- c("city","ni")

fwrite(df.of.ni,"ni1900.bw.txt",sep="|",eol="\r\n")




#####1900
full1900 <- fread("bpl_1900.txt")


full1900.hh <- full1900[full1900$self_empty_info_relationtohead == "Head",]
rm(full1900)

full1900.hh$whh <- 0
full1900.hh$whh[full1900.hh$sisrace==1] <- 1
full1900.hh$bhh <- 0
full1900.hh$bhh[full1900.hh$sisrace==2] <- 1

list.of.ni <- list()


for(i in 1:length(unique(full1900.hh$citystate))) {
city.sub <- full1900.hh[full1900.hh$citystate==unique(full1900.hh$citystate)[i]]
city.sub <- city.sub[order(city.sub$general_order_on_page),]
city.sub$neighbors <- 2
city.sub$neighbors[1] <- 1 ##the first person in the sequence will only have one neighbor
city.sub$neighbors[length(unique(city.sub$general_order_on_page))] <- 1 ##same for the last
##adjacency.matrix <- matrix(rep(integer(0),length(unique(city.sub$serial))^2),nrow=length(unique(city.sub$serial)),ncol=length(unique(city.sub$serial)))
##neighbor.radius <- 1


##the logic of this section may or may not be right
##initialize an NA indicator
##for everyone but the first and last person in the sequence, assign the number of black headed households including theirs & those on either side
##binarize that variable for later use by setting it to 1 where the head of household is black but the other value is less than 3 (meaning there's a non-black neighbor)

city.sub$indicator.var <- 99
city.sub$indicator.var[city.sub$indicator.var==99] <- NA
city.sub$indicator.var[-(1:1)] <- rowSums(embed(city.sub$bhh,3)) ##I need to come back to this and check the logic, it might be wrong
city.sub$indicator.var[length(city.sub$indicator.var)] <- NA
city.sub$indicator.var.bin <- 0
city.sub$indicator.var.bin[city.sub$indicator.var<3 & city.sub$bhh==1] <- 1 ##Ditto

bldiffrace <- sum(city.sub$indicator.var.bin)

##adjacency.matrix[seq(1, length(a), 2)] ##every other element, not used


whh <- sum(city.sub$whh) ##Constant for all white headed households
bhh <- sum(city.sub$bhh) ##Constant for all black headed households
bhh.one.neighbor <- sum(city.sub$bhh[city.sub$neighbors==1]) ##constant for black-headed households w/ one neighbor
bhh.two.neighbor <- sum(city.sub$bhh[city.sub$neighbors==2]) ##constant for black-headed households w/ two neighbors


##Max value of index in an area (eq 5)
two.neighbor.exp <- bhh.two.neighbor*(1-(((bhh-1)/(bhh-1+whh))*((bhh-2)/(bhh-2+whh)))) #one of the max terms
one.neighbor.exp <- bhh.one.neighbor*(1-((bhh-1)/(bhh-1+whh))) #other of the max terms
maxexp <- two.neighbor.exp + one.neighbor.exp ##combine terms to get the actual max expectation

##Min value of index in an area (8-10)
city.sub$product.term <- 0 ##initialize the variable
city.sub$product.term <- (bhh-seq(from=1,to=length(city.sub$product.term))-2) / (bhh-seq(from=1,to=length(city.sub$product.term)))

product.term <- prod(city.sub$product.term[is.finite(city.sub$product.term)]) ##...and then actually generate the product for the whole population

minexp <- ((bhh.two.neighbor/bhh)+(bhh.one.neighbor/bhh)* ((1/(0.5*(bhh+1)))*(1-product.term)) + (2*(1-(1/(0.5*(bhh+1))))*(1-product.term)))

ni <- (maxexp - bldiffrace) / (maxexp - minexp)

list.of.ni[[i]] <- cbind(unique(city.sub$citystate),ni)

print(paste0("Completed ",unique(city.sub$citystate)))
rm(city.sub)
}

list.of.ni <- lapply(list.of.ni,as.data.frame)
df.of.ni <- rbindlist(list.of.ni)
names(df.of.ni) <- c("city","ni")

fwrite(df.of.ni,"ni1900.bw.txt",sep="|",eol="\r\n")



