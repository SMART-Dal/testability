# Title     : TODO
# Objective : TODO
# Created by: Tushar
# Created on: 2022-02-23

data = read.csv("/Users/Tushar/Research/Testability/testability/analysis/rq2_detailed_data.csv", header=TRUE)
attach(data)

f2 <- "/Users/Tushar/Research/Testability/testability/analysis/rq2_detailed_Spearman.csv"
if (file.exists(f2)) file.remove(f2)

for(i in 36:39) {
  for (j in 2:35){
    test = cor.test(data[,i], data[,j], method="spearman")
    out <- capture.output(paste(colnames(data)[i], "and", colnames(data)[j], sep=" "))
    cat("----------------", out, file=f2, sep="\n", append=TRUE)
    out <- capture.output(test)
    cat("", out, file=f2, sep="\n", append=TRUE)
  }
}