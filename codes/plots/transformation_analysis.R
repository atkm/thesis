library('ggplot2')

dat = read.table('disk_transformation_1.dat',header=TRUE)
# interactive
#print(
#      ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred')
#      )
# save to file
image = ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.005,color='darkred')
ggsave(file="disk10.jpg", plot=image)
