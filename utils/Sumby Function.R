#This function give sums by the needed aggregate value. For example, if you want to know the total number of 
#Blacks, Hispanics, and Whites in the street segment you would enter all x values using data[,c("var1", "var2", "varn")],
#and the y value which would be the street segment in this example.

#Example of using sumby function
#test<-sumby(hhfinal2[,c("white", "black", "irish")], hhfinal2$building) 
#names(test)

sumby<- function(x,y){
  y1<-deparse(substitute(y))
  y2<-unlist((strsplit(as.character(y1), "[$]")))[2]
  myvars<-"y"
  nrows<-length(x)
  df<-data.frame(x=numeric(), y=numeric())
  df<-rename(df, c(x=y2, y=y))
  for(i in 1:nrows){
    x2<-(colnames(x[i]))
    t<-(tapply(x[,i], INDEX=list(y), FUN=sum, na.rm=T))
    df2<-data.frame(x=names(t), y=t)
    df2<-rename(df2, c(x=y2, y=x2))
    df<-merge(df, df2, by=y2, all=T, accumulate=T)
    df<-df[!names(df) %in% myvars]
  }
  df
}

