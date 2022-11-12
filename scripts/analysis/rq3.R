data3 <- read.csv(file="rq3_data.csv", header=TRUE, sep=",")
testability_smells <- data3[["TestabilitySmellsDensity"]]
test_density <- data3[["TestDensity"]]
rq3.corr.test = cor.test(testability_smells, test_density, method="spearman")
print(rq3.corr.test)
pdf("rq3.pdf", width=8, height=6)
plot(testability_smells, test_density, xlab="Testability smells density", ylab="Test density", col=rgb(4, 136, 108, 50,maxColorValue=255), xlim=c(0,100), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_density ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()
