from logistic_plots import *
"""
From ChaosLyapunov
"""
def TrajectoryDifference(g, x1, x2, N, args=()):
    """
    Calculates the difference between two trajectories that start
    at two points x1 and x2, presumably close to one another.
    Returns list of length N+1,
    [x2-x1, g(x2)-g(x1), g(g(x2))-g(g(x1)), ...]

    Used for illustrating sensitive dependence on initial conditions for
    chaotic regions, and for calculating Lyapunov exponents.

    You can usefully pick x2-x1 comparable to machine precision (seventeen
    digits). Don't choose x1 or x2 to equal zero or one in the logistic 
    map: zero is an unstable fixed point.

    """
    L1 = IterateList(g, x1, N+1, args)
    L2 = IterateList(g, x2, N+1, args)
    return np.abs(L1 - L2)
    # The minimum precision: 0.2 - 0.2000000000000001 != 0.0


def PlotTrajectoryDifference(g, x1, x2, N, args=()):
    """
    Calls TrajectoryDifference to find the difference, then plots the 
    absolute value of the difference using 
        pylab.semilogy(scipy.fabs(dx)).
    (Given just one array, pylab assumes the other axis is just the
    index into the array.)

    Notice that the differences stop growing when they become of order 
    one (naturally). Don't use such long trajectories to calculate the 
    Lyapunov exponents: it will bias the results downward.
    """
    diff = TrajectoryDifference(g, x1, x2, N, args)
    pylab.semilogy(diff)
    pylab.show()


def LyapunovFitFunc(p, traj_diff):
    """
    Given a trajectory difference traj_diff and a tuple
        p = (lyapExponent, lyapLogPrefactor)
    returns the residuals 
        log(|y_n|) - log( exp(lyapLogPrefactor + lyapExponent * n) )
     == log(|y_n|) - (lyapLogPrefactor + lyapExponent * n) (avoids overflow)

    The residual is the difference between the data and the fit:
    if the residuals were zero, the trajectory difference would be 
    perfectly described as a growing exponential.
    That is, the growth of the difference between two trajectories is 
    expected to be of the form
        |x_n - y_n| \sim lyapPrefactor * exp(lyapExponent n)

    We take the log of the difference so that the least--squares fit
    will emphasize the initial points and final points roughly equally.
    We use the log of the lyapPrefactor because it must be positive:
    it's a standard trick in nonlinear fitting to change variables like
    this to enforce ranges in parameters.

    Used by FitLyapunovExponent to generate a least-squares fit for 
    the Lyapunov exponent and prefactor.
    """
    size = len(traj_diff)
    lyapE = p[0]
    lyapPrefactor = p[1]
    traj_diff = np.log(traj_diff)
    traj_diff = traj_diff - lyapPrefactor 
    for i in range(size):
      traj_diff[i] = traj_diff[i] - i*lyapE

    return traj_diff
    # by trial and error, exponent = -0.27, log-prefactor = 10**(-8) seem to be the best fit

def LyapunovLeastSquare(p,traj_diff):
    residual = LyapunovFitFunc(p,traj_diff)
    return np.sum(residual ** 2)

def FitLyapunovExponent(traj_diff, p0=(1.,-13.)):
    """
    Given a trajectory difference and an initial guess 
    p0=(lyapExponent, lyapPrefactor) for the Lyapunov exponent and 
    prefactor, uses scipy.optimize.leastsq to do a best fit for 
    these two constants, and returns them.

    The return value will likely include a warning message, even though
    the fit seems fine and the warning meaningless. You'll likely need 
    to delete it before using PlotFit.
    """
    return sp.optimize.leastsq(LyapunovFitFunc, p0, args=(traj_diff))
    #This is not fitting well
    #size = len(traj_diff)
    #coeff = np.ones((size,2))
    #for i in range(size):
    #  coeff[i][1] += i
    # 
    #print(coeff)
    #
    #ordinate = np.log(traj_diff)
    #print(ordinate)
    #result = sp.linalg.lstsq(coeff,ordinate)

def PlotFit(traj_diff, p):
    """
    Given a trajectory difference and p=(lyapExponent, lyapPrefactor),
    plot |traj_diff| and the fit on a semilog y axis.
    """
    fit = np.arange(0,len(traj_diff))
    fit = p[1] + p[0]*fit
    pylab.semilogy(np.exp(fit))
    pylab.plot(traj_diff)
    pylab.show()

def LyapunovXdependence(g,xbounds,N,arg=()):
    """
    Given a function, a tuple xbounds = (xmin, xmax) and trajectory length
    plot Lyapunov Exponent for values in xarray.
    """
    xarray = np.arange(xbounds[0],xbounds[1],(xbounds[1]-xbounds[0])/1000)
    result = np.zeros(len(xarray))
    for i in range(len(xarray)):
      x = xarray[i]
      diff = TrajectoryDifference(g, x, x+0.0000000000001, N, arg)
      fit = FitLyapunovExponent(diff)
      result[i] = fit[0][0]
    pylab.hist(result,bins=500,normed=1)
    pylab.show

def LyapunovXdependenceHist(g,xbounds,N,arg=()):
    """
    Given a function, a tuple xbounds = (xmin, xmax) and trajectory length
    plot Lyapunov Exponent for values in xarray.
    """
    xarray = np.arange(xbounds[0],xbounds[1],(xbounds[1]-xbounds[0])/1000)
    result = np.zeros(len(xarray))
    for i in range(len(xarray)):
      x = xarray[i]
      diff = TrajectoryDifference(g, x, x+0.0000000000001, N, arg)
      fit = FitLyapunovExponent(diff)
      result[i] = fit[0][0]
    pylab.plot(xarray,result,'o')
    pylab.show


