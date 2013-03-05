import scipy as sp
import numpy as np
import scipy.optimize
import matplotlib.pyplot

def vec2(func, pts, param):
    return sp.array([func(p,param) for p in pts])

def Henon(init, args):
    """
    args = (a,b)
    init = (x0, y0)
    Henon map 
    f(x,y) = y + 1 - ax^n
    g(x,y) = b*x
    """
    a = args[0]
    b = args[1]
    x0 = init[0]
    y0 = init[1]
    x = y0 + 1 - a*(x0**2)
    y = b * x0
    return (x,y)

# Chirikov standard map
# K > 1 is pretty chaotic. 
# use K = 0.5 as a default
def Kick(init,param):
    k = param
    x0 = init[0] * 2*sp.pi
    y0 = init[1] * 2*sp.pi
    # tweaked from the default: y = sp.mod(y0 + k * sp.sin(x0), 2*sp.pi)
    y = sp.mod(1.05 * sp.pi + y0 + k * sp.sin(x0), 2*sp.pi)
    x = sp.mod(x0 + y, 2*sp.pi)
    return (x/(2*sp.pi),y/(2*sp.pi))

def vKick(pts, param):
    return vec2(Kick, pts, param)

# Arnold's cat map
# default param = 2
def Cat(init,param=2):
    a  = param
    b  = a - 1
    x0 = init[0]
    y0 = init[1]
    x  = sp.mod(a*x0 + b*y0, 1)
    y  = sp.mod(x0 + y0, 1)
    return (x,y)

# vCat: Arnold's cat map vectorized.
# element-wise application of Cat (for patch representation)
# Increasing param would increase the x-orientation of the distortion
def vCat(pts,param=2):
    return vec2(Cat, pts, param)

# horseshoe map
def Horseshoe(init, param):
    """
    Following Wiggins (p. 421)
    0 < a < 1/2
    2 < u
    """
    x0 = init[0]
    y0 = init[1]
    a = param[0] # lambda in Wiggins
    u = param[1] # mu
    if (y0 <= 1/u):
      x = a * x0
      y = u * y0
    elif (y0 >= 1 - 1/u):
      x = 1 - x0 * a
      y = u * (1 - y0)
    else: # otherwise collapse it to (0,0)
      x = 0
      y = 0

    return (x,y)

def vHorseshoe(pts, param):
    return vec2(Horseshoe, pts, param)

def IterateList2D(g, init, N, args=()):
    """
    Iterate the function g(x, mu) N-1 times, starting at x0, so that the
    full trajectory contains N points.
    Returns the entire list 
    (x, g(x), g(g(x)), ... g(g(...(g(x))...))). 

    use
        pylab.hist(attractorXs, bins=500, normed=1)
        pylab.show()
    to see the density of points.
    """
    x0 = init[0]
    y0 = init[1]

    result = [(x0, y0)]
    for i in range(N-1):
      result.append(g(result[-1],args))

    # Return a numpy array
    return np.array(result)

def PlotIterate2D(g, init, N, args=()):
    """
    Plots g, the diagonal y=x, and the boxes made of the segments
    [[x0,x0], [x0, g(x0)], [g(x0), g(x0)], [g(x0), g(g(x0))], ...
    """
    points = IterateList2D(g, init, N, args)
    matplotlib.pyplot.scatter(points[:,0], points[:,1], s=0.1, color='darkblue')
