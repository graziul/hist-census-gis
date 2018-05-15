
setwd("Z:/Projects/1940Census/StLouis/GIS_edited/")
c<-readOGR(dsn=getwd(), layer="StLouis_1930_With_Contemp")

#c<-read.dbf("Z:/Projects/1940Census/StLouis/GIS_edited/StLouis_1930_With_Contemp.dbf")
names(c)
c<-rename(c, c("FULLNAME_1"="Street_Contemp"))
c<-rename(c, c("FULLNAME"="Street_1930"))

c$Street_1930<-as.character(c$Street_1930)
c$Street_Contemp<-as.character(c$Street_Contemp)
c$tofix<-ifelse(c$Street_1930==c$Street_Contemp, 1, ifelse(mapply(grepl, c$Street_1930, c$Street_Contemp), 2,3))

c$Street_Fix<-ifelse(c$tofix==2, c$Street_Contemp, c$Street_1930)
c$Street_Fix<-ifelse(is.na(c$Street_Fix), c$Street_1930, c$Street_Fix)

writeOGR(c, dsn=getwd(), "StLouis_1930_Added_Directions", check_exists = TRUE,
         overwrite_layer = TRUE, driver="ESRI Shapefile")
