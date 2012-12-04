# <nbformat>2</nbformat>
# <codecell>
"""Basic functionality for iterated maps"""

# <codecell>
import scipy as sp
import numpy as np
import scipy.optimize
import scipy.fftpack
import pylab

# <markdowncell>
# ***** Shared software, 
# ***** used by ChaosLyapunov, InvariantMeasure, FractalDimension, and 
# ***** PeriodDoubling exercises.

# <codecell>
def f(x, mu):
    """
    Logistic map f(x) = 4 mu x (1-x), which folds the unit interval (0,1)
    into itself.
    """
    return 4 * mu * x * (1-x)

def cubic(x, mu):
    """
    cubic map
    mu <= 27/4
    """
    return mu*(x-1)*x*(x-1)

def quartic(x, mu):
    """
    Quartic 
    """
    return mu*(-37.8671220000000*(x**4) + 68.3654940000000*(x**3) - 36.8028780000000*(x**2) + 6.30450600000000*x)

# <codecell>
def Iterate(g, x0, N, mu):
    """
    Iterate the function g(x,mu) N times, starting at x=x0.
    Return g(g(...(g(x))...)). Used to find a point on the attractor
    starting from some arbitrary point x0.

    Calling Iterate for the Feigenbaum map at mu=0.9 would look like
        Iterate(f, 0.1, 1000, 0.9)

    We'll later be using Iterate to study the sine map 
        fsin(x,B) = B sin(pi x)
    so passing in the function and arguments will be necessary for 
    comparing the logistic map f to fsin.
    
    Inside Iterate you'll want to apply g(x0, mu).
    """

    tmp = x0
    for i in range(N):
      tmp = g(tmp,mu)

    return tmp

# <codecell>
def IterateList(g, x0, N, mu):
    """
    Iterate the function g(x, mu) N-1 times, starting at x0, so that the
    full trajectory contains N points.
    Returns the entire list 
    (x, g(x), g(g(x)), ... g(g(...(g(x))...))). 

    Can be used to explore the dynamics starting from an arbitrary point 
    x0, or to explore the attractor starting from a point x0 on the 
    attractor (say, initialized using Iterate).

    For example, you can use Iterate to find a point xAttractor on the 
    attractor and IterateList to create a long series of points attractorXs
    (thousands, or even millions long, if you're in the chaotic region), 
    and then use
        pylab.hist(attractorXs, bins=500, normed=1)
        pylab.show()
    to see the density of points.
    """

    result = [x0]
    for i in range(N-1):
      result.append(g(result[-1],mu))

    # Return a numpy array
    return np.array(result)

def PlotGraph(g, args=()):
    """
    Plots g and the diagonal y=x
    """
    # Plot the graph of g
    xaxis = sp.linspace(0.0,1.0,200)
    graph = [g(i,args) for i in xaxis]
    pylab.plot(xaxis, graph)

    # Plot a diagonal line
    pylab.plot(xaxis, xaxis)


def PlotAttractors(g, xbounds, nTransient, nCycle, arg=()):
    """
    Given a function, xbounds = (xmin, xmax), and N number of iterations,
    plot a histogram of the last M points (=attractors).
    """
    xarray = np.arange(xbounds[0],xbounds[1],(xbounds[1]-xbounds[0])/1000)
    result = np.zeros((len(xarray),nCycle))
    for i in range(len(xarray)):
      x = xarray[i]
      seed = Iterate(g, x, nTransient, arg)
      result[i] = IterateList(g, seed, nCycle, arg)

    # histogram plot doesn't work.
    #pylab.hist(result,bins=100,normed=1)
    #pylab.show()
    pylab.plot(xarray,result)
    pylab.show()

# <codecell>
def BifurcationDiagram(g, x0, nTransient, nCycle, muArray, showPlot=True):
    """
    For each parameter value mu in muArray,
    iterate g nTransient times to find a point on the attractor, and then
    make a list nCycle long to explore the attractor.

    To generate muArray, it's convenient to use scipy.linspace: for example,
    BifurcationDiagram(f, 0.1, 500, 128, scipy.linspace(0.8, 1.0, 200))

    pylab.plot allows one to plot an entire array of abscissa-values versus an
    array of ordinate-values of the same shape. Our vertical axis (ordinate)
    is a list of arrays of attractor points of length nCycle (created by 
    IterateList after Iterating), one list per value of mu in muArray.
    Our horizontal axis (abscissa) should thus be a list of arrays 
        [mu, mu, mu, ...] = [mu]*nCycle = mu*scipy.ones(nCycle) 
    of length nCycle.
    Use
        pylab.plot(muMatrix, xMatrix, 'k,')
        pylab.show()
    to visualize the resulting bifurcation diagram, where 'k,' denotes 
    black pixels.
    """
    xMatrix = []
    for mu in muArray:
      tmp = x0
      tmp = Iterate(g, x0, nTransient, mu)
      attrPts = IterateList(g, tmp, nCycle, mu)
      xMatrix.append(attrPts)

    pylab.plot(muArray, xMatrix, 'k,')

"""
From PeriodDoubling
"""
def PlotIterate(g, x0, N, args=()):
    """
    Plots g, the diagonal y=x, and the boxes made of the segments
    [[x0,x0], [x0, g(x0)], [g(x0), g(x0)], [g(x0), g(g(x0))], ...
    """
    # Plot the graph of g
    xaxis = sp.linspace(0.0,1.0,200)
    graph = [g(i,args) for i in xaxis]
    pylab.plot(xaxis, graph)

    # Plot a diagonal line
    pylab.plot(xaxis, xaxis)

    # Line segments
    tmp = x0
    point1 = [x0, x0]
    for i in range(N):
      point2 = [point1[1], g(point1[0],args)]
      pylab.plot(point1,point2,color="brown")
      point1 = point2

"""
For Diff Eq version of logistic equation
"""
def PlotLogisticDiffEq(x0,mu,tbound):
    """
    Arguments are the initial value, mu, the growth rate,
    and the end time
    """
    t = sp.linspace(0.0, tbound, 100*tbound)
    xT = (x0 * np.exp(mu * t)) / (1 - x0 + x0 * np.exp(mu * t))
    pylab.plot(xT)
    pylab.show()

def PlotPowerSpectrum(g, x0, N, args=()):
    """
    Plot Fourier spectrum of N points (after 1000 transient points)
    """
    sig = IterateList(g, x0, N+1000, args)[1000:]
    sig_freq = sp.fftpack.fftfreq(sig.size, d=1)
    sig_fft  = sp.fftpack.fft(sig)
    pidxs    = np.where(sig_freq > 0)
    freqs, power = sig_freq[pidxs], np.abs(sig_fft)[pidxs]
    pylab.plot(freqs, power)
    pylab.xlabel('Frequency [Hz]')
    pylab.ylabel('Power')
    pylab.show()
    print("Peak Frequency:")
    print(freqs[power.argmax()])

#  <markdowncell>
# Copyright (C) Cornell University
# All rights reserved.
# Apache License, Version 2.0
