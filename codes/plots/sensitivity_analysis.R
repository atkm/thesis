sd = read.table('sensitivity_2.dat',header=TRUE)
#sd = sd[sd$d==0.01,] # just do it for a single d value for now
d <- sd[,1]
arg <- sd[,2]
result <- sd[,3]
x <- cos(arg) * d
y <- sin(arg) * d
dat = cbind(x,y,result)
dat = data.frame(dat)

library('ggplot2')
print(
      ggplot(dat, aes(x = x, y = y))
      + geom_point(aes(color = result))
)
