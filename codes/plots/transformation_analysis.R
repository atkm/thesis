dat = read.table('disk_transformation_1.dat',header=TRUE)

library('ggplot2')
image = ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred')
ggsave(file="disk_transformation_1.svg", plot=image)
