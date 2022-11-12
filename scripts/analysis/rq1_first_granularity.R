data <- read.csv(file="test_and_testability_smells.csv", header=TRUE, sep=",")
hwd <- data[["HWD_N"]]
gs <- data[["GS_N"]]
ed <- data[["ED_N"]]
ldv <- data[["LDV_N"]]
test_smells <- data[["Total_TS_N"]]

# 'Repo,HWD_N,GS_N,ED_N,LDV_N,Total_TyS_N,AR_N,CTL_N,CI_N,ET_N,ET_N,EH_N,IT_N,UT_N,Total_TS_N\n')
# HWD and test smells
hwd_ts.corr.test = cor.test(hwd, test_smells, method="spearman")
print(hwd_ts.corr.test)
pdf("rq1_hwd_and_test_smells.pdf", width=8, height=6)
plot(hwd, test_smells, xlab="Hard-Wired Depedencies", ylab="Test smells", col=rgb(4, 136, 108, 50,maxColorValue=255), ylim=c(0,400), xlim=c(0,200), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_smells ~ hwd), col="red", lwd=3, lty=2)

# GS and test smells
gs_ts.corr.test = cor.test(gs, test_smells, method="spearman")
print(gs_ts.corr.test)
pdf("rq1_gs_and_test_smells.pdf", width=8, height=6)
plot(gs, test_smells, xlab="Hard-Wired Depedencies", ylab="Test smells", col=rgb(4, 136, 108, 50,maxColorValue=255), ylim=c(0,400), xlim=c(0,200), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_smells ~ gs), col="red", lwd=3, lty=2)

# ED and test smells
ed_ts.corr.test = cor.test(ed, test_smells, method="spearman")
print(ed_ts.corr.test)
pdf("rq1_ed_and_test_smells.pdf", width=8, height=6)
plot(ed, test_smells, xlab="Hard-Wired Depedencies", ylab="Test smells", col=rgb(4, 136, 108, 50,maxColorValue=255), ylim=c(0,400), xlim=c(0,200), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_smells ~ ed), col="red", lwd=3, lty=2)

# LDV and test smells
ldv_ts.corr.test = cor.test(ldv, test_smells, method="spearman")
print(ldv_ts.corr.test)
pdf("rq1_ldv_and_test_smells.pdf", width=8, height=6)
plot(ldv, test_smells, xlab="Hard-Wired Depedencies", ylab="Test smells", col=rgb(4, 136, 108, 50,maxColorValue=255), ylim=c(0,400), xlim=c(0,200), pch=16, cex.lab=1.5, cex.axis=1.5, cey.lab=1.5, cey.axis=1.5)
abline(lm(test_smells ~ ldv), col="red", lwd=3, lty=2)

dev.off()