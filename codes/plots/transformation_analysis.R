library('ggplot2')

dat = read.table('disk_transformation4-5.dat',header=TRUE)
print(
      ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred')
      )
#ggsave(file="disk_transformation_1.svg", plot=image)
