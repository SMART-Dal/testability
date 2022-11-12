data <- read.csv(file="rq4/rq4_data_ontrack.csv", header=TRUE, sep=",")
testability_smells <- data[["TySmellDensity"]]
total_issuess <- data[["TotalIssues"]]
rq4.corr.test = cor.test(testability_smells, total_issuess, method="spearman")
print(rq4.corr.test)
pdf("rq4.pdf", width=8, height=6)
plot(testability_smells, total_issuess, xlab="Testability smells", ylab="Bugs", col=rgb(4, 136, 108, 50,maxColorValue=255), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(total_issuess ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()