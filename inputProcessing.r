## RUNTIME: O(n log(n) + e log(e))
dev.off
rm(list=ls(all=TRUE))
library(data.table)

name <- "google"

data <- read.table(paste(name,"A.txt", sep=""), header = FALSE) 
backupData <- data
data <- data[,c(1,2)]
n <- max(data) # the vertices
e <- nrow(data)

######### RUN ONLY IF GRAPH: DIRECTED / DUPLICATE EDGES #########
swap <- function(vec){ v<- vec; v[1] <- min(vec[1],vec[2]); v[2] <- max(vec[2],vec[1]); return (v);}
for (i in c(1:e)){ # this needs to be simplified
  if(data[i,1]>data[i,2]) {data[i,] = swap(data[i,])}
}
data <- unique(data[ , 1:2 ])
#################################################################

e <- nrow(data)
sortByFrequency <- sort(table(append(data[,1], data[,2])),decreasing=T) ## RUNTIME: sort n numbers O(n logn)
degree <- c(1:n)
for (i in c(1:n)){ ## RUNTIME: scanning. Total for loop: O(n)
  degree[ as.numeric(names(sortByFrequency)[i])] <- sortByFrequency[i] 
}

edgeWeight <- as.numeric(lapply(c(1:e), function(x){ min(degree[data[x,1]],degree[data[x,2]])})) ## RUNTIME: O(e)
edgeWeightSorted <- sort(edgeWeight, index.return = TRUE) ## sort e numbers RUNTIME O(e log e)
edgePQ <- rev(edgeWeightSorted$ix) 

x <- c(n,e)
x <- append(x,c(t(as.matrix(data))))
x <- append(x,degree)
x <- append (x,edgeWeight)
x <- append(x,edgePQ)
x <- as.data.table(x)
fwrite(x, paste(name,"B.txt",sep=""), row.names=FALSE,col.names = FALSE)

#summary
edgeInfo <- cbind(edgeWeight, edgePQ)
