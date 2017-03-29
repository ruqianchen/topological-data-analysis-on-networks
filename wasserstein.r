
library("TDA")
library("base")

files <- list.files(pattern = "randBhbd*")
matrices <- list()
i = 1
for (currfile in files){
  if (as.numeric(substr(currfile,9,11)) > 0.04){
    nam <- paste("mat",substr(currfile,9,12) , sep = "")
    MyData <- as.matrix(read.csv(file=currfile, header=FALSE, sep=","))
    assign(nam, MyData)
    matrices[[i]] <- MyData
    i=i+1
  }
}

#wasserstein distance matrix
len <- length(matrices)
wdm <- matrix(0,len,len)
i <- 1
while(i<=len){
  j <- i
  while(j<=len){
    wdm[i,j] <- wasserstein(matrices[[i]],matrices[[j]], p = 2,dimension = 1)
    wdm[j,i] <- wdm[i,j]
    j <- j+1
  }
  i <- i+1
}
