"""
Codes for Reed Scientific Computation Week 3:
    Differentiation: Solving ODEs
"""
import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D


def gravity(x, args):
    return -9.8

def Lorenz(xyz,args=(10, 28, 8.0/3)):
    """
    Lorenz system
    dx/dt = s * (y - x)
    dy/dt = x * (r - z) - y
    dz/dt = x * y - b * z
    (s: sigma, r: rho, b: beta)
    args = (sigma, rho, beta)
    """
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    s = args[0]
    r = args[1]
    b = args[2]
    return np.array((s * (y - x), x * (r - z) - y, x * y - b * z))

def Plot_rk4_3D(g, xyz, end, dt, args=()):
    result = rk4_3D(g, xyz, end, dt, args)
    fig = pylab.figure()
    ax = Axes3D(fig)
    ax.scatter(result[:,0], result[:,1], result[:,2], s=1)

def rk4_3D(g, xyz, end, dt, args=()):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    result = [np.array((x,y,z))]

    iteration = int(np.ceil(end / dt))
    for i in range(iteration):
        x0 = result[-1][0]
        y0 = result[-1][1]
        z0 = result[-1][2]
        result.append(rk4_3D_step(g, x0, y0, z0, dt, args))

    return np.vstack(result)

def rk4_3D_step(g, x,y,z, dt, args=()):
    now = np.array((x,y,z))
    k1 = dt * now
    k2 = dt * g(now + k1/2, args)
    k3 = dt * g(now + k2/2, args)
    k4 = dt * g(now + k3,args)
    new_xyz = np.array((x,y,z)) + (k1/2 + k2 + k3 + k4/2)/3
    return new_xyz

def verlet_solver(x0, v0, g, end, dt, args=()):
    """
    x0: initial position
    v0: initial velocity
    g : a function such that dx/dt = g(x)
    end: end time (start at t=0)
    dt: time step
    """
    seedx = x0 - dt * v0
    result = [seedx, x0]
    iteration = int(np.ceil(end / dt))
    for i in range(iteration):
        result.append(verlet_nextstep(result[-2], result[-1], g, dt, args))

    # return, excluding the seed x value
    return result[1:]


def plot_verlet_solver(x0, v0, g, end, dt, args=()):
    result = verlet_solver(x0, v0, g, end, dt, args)
    xaxis = np.arange(end / dt + 1) * dt
    pylab.plot(xaxis, result)
    pylab.show()


def verlet_nextstep(x0, x1, g, dt, args=()):
    """
    Compute the next step, i.e.
    x(t + dt) = 2 * x(t) - x(x - dt) + dt^2 * a(t)
    """
    return 2*x1 - x0 + g(x1,args) * (dt**2)
