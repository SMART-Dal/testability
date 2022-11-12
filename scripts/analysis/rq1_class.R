data <- read.csv(file= "rq1_data_by_class.csv", header=TRUE, sep=",")
testability_smells <- data[["TyS_normalized"]]
test_smells <- data[["TS_normalized"]]
rq1.corr.test = cor.test(testability_smells, test_smells, method="spearman")
print(rq1.corr.test)
pdf("rq1_class.pdf", width=8, height=6)
plot(testability_smells, test_smells, xlab="Testability smells density", ylab="Test smells density", col=rgb(4, 136, 108, 50,maxColorValue=255),  xlim=c(0,100), ylim=c(0,3), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()
