##This script converts the full combined pipe-delimited house-person file from Stata into person-level state-by-state files.
##Last revised by NF on 13 April 2017; cosmetic revisions 13 July 2017

library(data.table) ##for large data manipulation
library(dplyr) ##for rename and join functions
library(dtplyr) ##to make dplyr play nice with data.table
full1920 <- fread("us1920out.txt",select=c("rectype","year","datanum","enumdist","serial","numprec","city","citypop","gq","gqtype","pageno","hhtype","cntry","ownershp","nmothers","nfathers",
					"statefip","headloc","nhgisjoin","yrstcounty","stcounty","county","dwseq","dwsize","stdmcd","stdcity","dwelling","reel","numperhh",
						"line","street","split","splithid","splitnum","datanump","serialp","pernum","rectypep","relate","race","marst","bpl","famsize","nchild",
						"age","sex","mtongue","fbpl","mbpl","nativity","citizen","bplstr","fbplstr","mbplstr","sei","occ1950","ind1950","lit","ID",
						"yrsusa1","yrsusa2","mtongstr","yrimmig", "us1920c_0042", "us1920c_0043"),fill=TRUE) ##Load the file
##Subset a large group of variables from the full file for use.
#fwrite(full1920,"full1920us.txt",sep="|",eol="\r\n") ##only use this line if you remove the "select" statement above and want to re-output the full file.
full1920$ID <- seq(1:length(full1920$rectype)) ##generate a unique ID var
to.out.1920 <- full1920
rm(full1920) ##No need to keep two names floating around out there
gc() ##Force return of that memory to the server

lookup.table <- to.out.1920[,c("serial","statefip","stdcity","stcounty","enumdist","dwseq","dwsize","dwelling"),with=FALSE] ##Create a lookup table to give the person records household attributes
lookup.table <- lookup.table[!is.na(lookup.table$serial),] ##Get rid of anything that isn't going to match (person records, missing values on key)

to.out.1920.p <- to.out.1920[to.out.1920$rectype=="P",] ##Create a person-file
to.out.1920.p.short <- to.out.1920.p[,c(35:63),with=FALSE] ##Keep only the columns associated with person records
to.out.1920.p.short <- rename(to.out.1920.p.short, serial = serialp) ##Rename person-serial to hh-serial for join
to.out.1920.p.short <- left_join(to.out.1920.p.short,lookup.table,by="serial") ##Left join (lookup table values appended to a as columns)
to.out.1920.p.short <- as.data.table(to.out.1920.p.short) ##left-join turns dt into a tibble, turn it back into a dt
fwrite(to.out.1920.p.short,"us1920personrecords.txt",sep="|",eol="\r\n") ##write out the person file

p.1920 <- to.out.1920.p.short ##Rename this dt now that it's no longer output
rm(to.out.1920.p.short) ##Remove the old one
statelist <- unique(p.1920$statefip) ##Create a vector of the state names that appear in the person file
for (i in 1:length(statelist)) { ##Initialize loop
p.1920.staterecs <- p.1920[statefip==statelist[i],] ##grab records for one state
filename.out <- paste0(statelist[i],"1920.txt") ##Create a state-specific file name
fwrite(p.1920.staterecs,filename.out,sep="|",eol="\r\n") ##Dump out the records to the file with that name
}

nyc.1920 <- p.1920[p.1920$stcounty==360050 | p.1920$stcounty==360470 | p.1920$stcounty==360610 | p.1920$stcounty==360810 | p.1920$stcounty==360850,] ##nyc is a special case and must be handled like one
fwrite(nyc.1920,"NYC1920.txt",sep="|",eol="\r\n") ##write out nyc file


##End -- next steps in gen_1920_extract.R