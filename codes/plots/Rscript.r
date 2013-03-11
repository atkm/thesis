# R script to plot the bound.dat
bd = read.table('bound.dat')
d <- bd[,1]
R <- bd[,2]
Bound <- bd[,3]
rgl.open()
bg3d("lightcyan")
plot3d(d, Bound, R, size=0.3, type='s', col='darkred') # the z-axis is the second argument in R
dat1 = bd[bd$V1==3.0,] # data for d = 3.0
dat1 = dat1[,c("V2","V3")] # remove the column for d
r <- dat1[,1]
bound <- dat1[,2]
linreg = lm(r~bound) # linear regression d vs Max norm
# -> Result: Intercept=-0.7412; Slope= 0.8439
# -> Without the first row (R=1.0, when the circle doesn't grow):
# -> Intercept=-0.9178; Slope= 0.8575

dat2 = bd[bd$V1==1.0,] # data for d = 3.0
dat2 = dat2[,c("V2","V3")] # remove the column for d
r <- dat2[,1]
bound <- dat2[,2]
linreg = lm(r~bound) # linear regression d vs Max norm
# -> Result: Intercept=-0.3915; Slope= 0.8961
# -> Without the first row (R=1.0, when the circle doesn't grow):
# -> Intercept=-0.4802; Slope= 0.9035


