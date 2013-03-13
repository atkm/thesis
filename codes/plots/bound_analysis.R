# R script to plot the bound.dat

## Make a data frame from two data set
#larged = read.table('bound_larged.dat')
#smalld = read.table('bound_smalld.dat')
#bd = merge(larged, smalld, all=TRUE) # merge the two tables

# Plot max and min norm for R = 1, ... , 5
#bd = read.table('bound_R_2-4.dat')
#d <- bd[,1]
#R <- bd[,2]
#Bound <- bd[,3]
#library('rgl')
#rgl.open()
#bg3d("lightcyan")
#plot3d(d, Bound, R, size=0.3, type='s', col='darkred') # the z-axis is the second argument in R

# Plot max and min norm for R = 2 (or 4)
bd = read.table('bound_R2.dat', header=TRUE)
library('ggplot2')
print(
ggplot(bd, aes(x=d, y=Bound)) + geom_point(shape=10, color='darkred', size=0.7)
)


### Linear Regression for slices of data sets
#dat1 = bd[bd$V1==3.0,] # data for d = 3.0
#dat1 = dat1[,c("V2","V3")] # remove the column for d
#r <- dat1[,1]
#bound <- dat1[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Result: Intercept=-0.7412; Slope= 0.8439
## -> Without the first row (R=1.0, when the circle doesn't grow):
## -> Intercept=-0.9178; Slope= 0.8575
#
#dat2 = bd[bd$V1==1.0,] # data for d = 1.0
#dat2 = dat2[,c("V2","V3")] # remove the column for d
#dat2 = dat2[-1,]
#r <- dat2[,1]
#bound <- dat2[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Result: Intercept=-0.3915; Slope= 0.8961
## -> Without the first row (R=1.0, when the circle doesn't grow):
## -> Intercept=-0.4802; Slope= 0.9035
#
#dat3 = bd[bd$V1<0.112 & bd$V1>0.111,] # data for d = 0.1110
#dat3 = dat3[,c("V2","V3")] # remove the column for d
#dat3 = dat3[-1,]
#r <- dat3[,1]
#bound <- dat3[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Without the first row (R=1.0, when the circle doesn't grow):
## -> Intercept=-0.6164; Slope= 1.0384
#
#dat4 = bd[bd$V2==2,] # data for R=2.
#dat4 = dat4[,c("V1","V3")] # remove the column for d
#r <- dat4[,1]
#bound <- dat4[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Intercept=-0.2746; Slope= 0.2833
#
#dat5 = bd[bd$V2==5,] # data for R=5.
#dat5 = dat5[,c("V1","V3")] # remove the column for d
#r <- dat5[,1]
#bound <- dat5[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Intercept=-5.1276; Slope= 0.9762
#
#dat6 = bd[bd$V2==10,] # data for R=10.
#dat6 = dat6[,c("V1","V3")] # remove the column for d
#r <- dat6[,1]
#bound <- dat6[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Intercept=-6.9287; Slope= 0.6815
#
#dat7 = bd[bd$V2==6,] # data for R=6.
#dat7 = dat7[,c("V1","V3")] # remove the column for d
#r <- dat7[,1]
#bound <- dat7[,2]
#linreg = lm(r~bound) # linear regression d vs Max norm
## -> Intercept=-5.7975; Slope= 0.9476


