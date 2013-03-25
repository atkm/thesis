library('ggplot2')

dat = read.table('disk_transformation5-6.dat',header=TRUE)
# interactive
#print(
#      ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred')
#      )
# save to file
image = ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred')
ggsave(file="strip5-6.jpg", plot=image)
