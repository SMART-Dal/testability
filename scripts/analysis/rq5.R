data5 <- read.csv(file="rq5_data.csv", header=TRUE, sep=",")
testability_density <- data5[["TestabilitySmellsDensity"]]
loc <- data5[["LOC"]]
rq5.corr.test = cor.test(testability_density, loc, method="spearman")
print(rq5.corr.test)
pdf("rq5.pdf", width=8, height=6)
plot(testability_density, loc, xlab="Testability smells", ylab="LOC", col=rgb(4, 136, 108, 50,maxColorValue=255),  pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
dev.off()