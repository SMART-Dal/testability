data <- read.csv(file="rq1_second_granularity_data.csv", header=TRUE, sep="," )
attach(data)
header <- read.csv(file="rq1_second_granularity_data.csv", nrows = 1, header=TRUE, sep=",")[- 1, ]

for(i in 2:5) {
    for(j in 6:26) {
        test = cor.test(data[,i], data[,j], method="spearman")

        print(paste(colnames(data)[i], "and", colnames(data)[j], "results", test.rho, sep=" "))
    }
}