data2 <- read.csv(file="rq2_data.csv", header=TRUE, sep=",")
testability_smells <- data2[["TyS_normalized"]]
code_smells <- data2[["All_normalized"]]
rq2.corr.test = cor.test(testability_smells, code_smells, method="spearman")
print(rq2.corr.test)
pdf("rq2.pdf", width=8, height=6)
plot(testability_smells, code_smells, xlab="Testability smells", ylab="Code smells", col=rgb(4, 136, 108, 50,maxColorValue=255), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(code_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()

# 'Repo,TotalTestabilitySmells,TotalArchSmells,TotalDesignSmells,TotalImplSmells,TotalCodeSmells,LOC,TyS_normalized,AS_normalized,DS_normalized,IS_normalized,All_normalized\n')

arch_smells <- data2[["AS_normalized"]]
rq2.1.corr.test = cor.test(testability_smells, arch_smells, method="spearman")
print(rq2.1.corr.test)
pdf("rq2.1.pdf", width=8, height=6)
plot(testability_smells, arch_smells, xlab="Testability smells", ylab="Architecture smells", col=rgb(4, 136, 108, 50,maxColorValue=255), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(arch_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()

design_smells <- data2[["DS_normalized"]]
rq2.2.corr.test = cor.test(testability_smells, design_smells, method="spearman")
print(rq2.2.corr.test)
pdf("rq2.2.pdf", width=8, height=6)
plot(testability_smells, design_smells, xlab="Testability smells", ylab="Design smells", col=rgb(4, 136, 108, 50,maxColorValue=255),  pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(design_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()

impl_smells <- data2[["IS_normalized"]]
rq2.3.corr.test = cor.test(testability_smells, impl_smells, method="spearman")
print(rq2.3.corr.test)
pdf("rq2.3.pdf", width=8, height=6)
plot(testability_smells, impl_smells, xlab="Testability smells", ylab="Implementation smells", col=rgb(4, 136, 108, 50,maxColorValue=255),  pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(impl_smells ~ testability_smells), col="red", lwd=3, lty=2)
dev.off()
