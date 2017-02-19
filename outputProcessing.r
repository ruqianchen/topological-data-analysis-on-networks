name <- "google"
outputData <- read.table(paste(name,"C.txt", sep=""), sep = ",", header = TRUE)
count <- c()
for (c in c(1:max(outputData$Birth))){
  count <- append(count, sum(outputData$Birth>=c & outputData$Death<c))
}
lifespan <- outputData$Birth -  outputData$Death
png(filename=paste(name,"Lifespan.png", sep=""))
plot(sort(lifespan[lifespan!=0]),main=paste(name,"Lifespan"))
lines(c(1:max(lifespan)),col="green")
dev.off()

png(filename=paste(name,"Count.png",sep=""))
plot(count, main=paste(name,"Count"))
dev.off()
