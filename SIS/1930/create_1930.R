##This script converts the full combined pipe-delimited house-person file from Stata into a set of state-level files 
##containing only our cities of interest, similar to other decades

##Last updated by NF on 17 April 2017; cosmetic updates 13 July 2017

library(data.table) ##for large data manipulation
library(dplyr) ##for rename and join functions
library(dtplyr) ##to make dplyr play nice with data.table

to.out.1930 <- fread("full1930us.txt",fill=TRUE)
lookup.table <- to.out.1930[,c("serial","statefip","stdcity","stcounty","enumdist","dwelling","dwseq","dwsize","street","us1930d_0061","ownershp"),with=FALSE] ##Create a lookup table to give the person records household attributes
lookup.table <- lookup.table[!is.na(lookup.table$serial),] ##Get rid of anything that isn't going to match (person records, missing values on key)

to.out.1930.p <- to.out.1930[to.out.1930$rectype=="P",] ##Create a person-file
to.out.1930.p.short <- to.out.1930.p[,c(40:70),with=FALSE] ##Keep only the columns associated with person records
to.out.1930.p.short <- rename(to.out.1930.p.short, serial = serialp) ##Rename person-serial to hh-serial for join
to.out.1930.p.short <- left_join(to.out.1930.p.short,lookup.table,by="serial") ##Left join (lookup table values appended to a as columns)
to.out.1930.p.short <- as.data.table(to.out.1930.p.short) ##left-join turns dt into a tibble, turn it back into a dt
fwrite(to.out.1930.p.short,"us1930personrecords.txt",sep="|",eol="\r\n") ##write out the person file

p.1930 <- fread("us1930personrecords.txt",fill=TRUE)

#p.1930 <- to.out.1930.p.short ##Rename this dt now that it's no longer output
rm(to.out.1930.p.short) ##Remove the old one
statelist <- unique(p.1930$statefip) ##Create a vector of the state names that appear in the person file
for (i in 1:length(statelist)) { ##Initialize loop
p.1930.staterecs <- p.1930[statefip==statelist[i],] ##grab records for one state
filename.out <- paste0(statelist[i],"1930.txt") ##Create a state-specific file name
fwrite(p.1930.staterecs,filename.out,sep="|",eol="\r\n") ##Dump out the records to the file with that name
}


##End -- next steps will be in separate script