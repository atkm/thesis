"""
Codes for Reed Scientific Computation Week 3:
    Differentiation: Solving ODEs
"""
import scipy as sp
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D

def gravity(t, x, args):
    return -9.8

def logistic(t, x, mu):
    return mu * x * (1-x)

def logistic_accuracy(x, end, dt, mu):
    points = rk4_1D(logistic, x, end, dt, mu)
    plt.plot(sp.linspace(0, end, len(points)), points)

def Lorenz(t, xyz, args):
    """
    Lorenz system
    a chaotic args: (10, 28, 8.0/3)
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
    return sp.array((s * (y - x), x * (r - z) - y, x * y - b * z))

def Rossler(t, xyz, args):
    """
    Rossler system
    a chaotic args: (0.432, 2, 4)
    """
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    a = args[0]
    b = args[1]
    c = args[2]
    return sp.array(( -y - z, x + a*y, b + z*(x - c) ))

# Plot_rk4_3D(Rossler, (0.1, 0.2, 0.3), 10, 0.001, (0.432, 2, 4))
def Plot_rk4_3D(g, xyz, end, dt, args=()):
    result = rk4_3D(g, xyz, end, dt, args)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(result[:,0], result[:,1], result[:,2], s=1.4, color="gold")
    ax.w_xaxis.set_pane_color((0.12, 0.12, 0.12, 1.0))
    ax.w_yaxis.set_pane_color((0.12, 0.12, 0.12, 1.0))
    ax.w_zaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    plt.show()

def rk4_1D(g, x, end, dt, args=()):
    """
    RK4 1D version.
    Accuracy verified using 
    dx/dt = t^2, x(0) = 0;
    and dx/dt = 1/x, x(0) = 1;
    and dx/dt = x, x(0) = 1.
    """
    t = 0
    result = [x]
    iteration = int(sp.ceil(end / dt))
    for i in range(iteration):
        x0 = result[-1]
        result.append(rk4_1D_step(g, t, x0, dt, args))
        t += dt

    return sp.array(result)

def rk4_1D_step(g, t, x, dt, args=()):
    k1 = dt * g(t, x, args)
    k2 = dt * g(t + dt/2, x + k1/2, args)
    k3 = dt * g(t + dt/2, x + k2/2, args)
    k4 = dt * g(t + dt, x + k3,args)
    newx = x + (k1/2 + k2 + k3 + k4/2)/3
    return newx

def rk4_3D(g, xyz, end, dt, args=()):
    t = 0
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    result = [sp.array((x,y,z))]

    iteration = int(sp.ceil(end / dt))
    for i in range(iteration):
        x0 = result[-1][0]
        y0 = result[-1][1]
        z0 = result[-1][2]
        result.append(rk4_3D_step(g, t, x0, y0, z0, dt, args))

    return sp.vstack(result)

def rk4_3D_step(g, t, x,y,z, dt, args=()):
    now = sp.array((x,y,z))
    k1 = dt * g(t, now, args)
    k2 = dt * g(t + dt/2, now + k1/2, args)
    k3 = dt * g(t + dt/2, now + k2/2, args)
    k4 = dt * g(t + dt, now + k3,args)
    new_xyz = now + (k1/2 + k2 + k3 + k4/2)/3
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
    iteration = int(sp.ceil(end / dt))
    for i in range(iteration):
        result.append(verlet_nextstep(result[-2], result[-1], g, dt, args))

    # return, excluding the seed x value
    return result[1:]


def plot_verlet_solver(x0, v0, g, end, dt, args=()):
    result = verlet_solver(x0, v0, g, end, dt, args)
    xaxis = sp.arange(end / dt + 1) * dt
    plt.plot(xaxis, result)
    plt.show()


def verlet_nextstep(x0, x1, g, dt, args=()):
    """
    Compute the next step, i.e.
    x(t + dt) = 2 * x(t) - x(x - dt) + dt^2 * a(t)
    """
    return 2*x1 - x0 + g(x1,args) * (dt**2)
