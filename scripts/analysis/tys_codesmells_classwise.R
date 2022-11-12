data <- read.csv(file= "tys_cs_summary_classwise.csv", header=TRUE, sep=",")
testability_smells <- data[["TyS_N"]]
code_smells <- data[["CS_N"]]
rq5.corr.test = cor.test(testability_smells, code_smells, method="spearman")
print(rq5.corr.test)
pdf("tys_cs_classwise.pdf", width=8, height=6)
plot(testability_smells, code_smells, xlab="Testability smells density", ylab="Code smells density", col=rgb(4, 136, 108, 50,maxColorValue=255),  xlim=c(0,5000), ylim=c(0,5000), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(code_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()
