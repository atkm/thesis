import scipy as sp
import scipy.optimize
import scipy.fftpack
import mpl_toolkits.mplot3d.axes3d as axs
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import matplotlib.patches as patch
import random
import time
from maps2d import *

# pylab.plot(xaxis, graph) to plot
# for example xaxis = sp.linspace(0,1,100)

class Shape:
    def __init__(self, kind, A, n):
        if kind == 'square':
             model = self.sqcover(A,n)

        self.name = kind + '_' + str(A) + '_' + str(n) + '_' + str(round(time.time())) + '.png'
        self.pts = model[0]
        self.rad = model[1]
        self.colors = model[2]
        self.resolution = len(self.pts) # total num of points 
        self.cover = (self.pts, self.rad, self.colors)

    # sqcover = a representation of square by patches.
    # Each patch is associated with a color.
    # squares consisting of patches == cover
    # a cover is a triple (U, r, c). 
    # U: a collection of n^2 points evenly distributed over a square. 
    # r: the "radius" of a subsquare
    # c: the color of each patch
    def sqcover(A,n):
        edge = sp.sqrt(A) # the length of an edge
        d = edge/n # the distance between two adjacent points
        r = d/2 # the "radius of "
        end = edge - r # end point
        base = sp.linspace(r, end, n)
        first_line = sp.transpose(sp.vstack((base, r*sp.ones(n))))
        increment = sp.transpose(sp.vstack((sp.zeros(n), d*sp.ones(n))))
        pts = first_line
        y_diff = increment
        for i in range(n-1):
            pts = sp.vstack((pts, first_line + y_diff))
            y_diff = y_diff + increment
        
        # Color matter
        colors = []
        for p in pts:
            cval = n*p[0] + p[1] # the x-coord has a higher weight
            cval = colormap.Spectral(cval/((n+1)*end)) # normalize by the max value that cval can take.
            colors.append(cval)
    
        colors = sp.array(colors)
    
        cover = (pts, r, colors)
        return cover


    # intgrid: return the xy coords of the points (including the walls) converted to integer representations
    def intgrid(self):
        n = self.resolution/4.0
        return sp.array(round_matrix(n * self.pts))

    # apply Kick Map with parameter (default 0.5)
    def kick(self, param=0.5):
        self.pts = vKick(self.pts, param)

    # apply Cat Map
    def cat(self, param=2):
        self.pts = vCat(self.pts, param)

    # apply Horseshoe Map
    def horse(self, param=(1.0/3, 3.0)):
        self.pts = vHorseshoe(self.pts, param)

    # mutation: either Cat or Kick map
    def mutate(self):
        self.pts = IterRand(self.pts)
    # mutation N times 
    def mutateN(self, N): # mutate N times
        self.pts = IterRandN(self.pts, N)

    # show plot in interactive mode
    def show(self):
        cvplot_nosave(self)

    # save plot in a png
    def save(self):
        cvplot(self,self.name)


# Basic shape class: boundary point representation of shapes
class BasicShape:
    def __init__(self, kind, A, n, param=1):
        if kind == 'square':
            model = self.sqshape(A,n)
            self.edge = sp.sqrt(A)
        if kind == 'circle':
            model = self.circshape(A,n)
            self.edge = 2 * sp.sqrt(A/sp.pi)
        if kind == 'ray':
            model = self.rayshape(A,param,n)

        self.name = 'basic' + kind + '_' + str(A) + '_' + str(n) + '_' + str(round(time.time())) + '.png'
        self.pts = model
        self.resolution = len(self.pts) # total num of points on the base. resolution == 4*n

    # sqshape == a representation of square by boundary points
    # Create a square of area A with n points on one edge
    # (0,0) is the bottom left corner
    # Build points in this order:
    # bottom left -> top left -> top right -> bottom right -> bottom left
    # top, left, bottom, right are defined as:
    #  t t t t r    
    #  l       r     
    #  l       r   
    #  l       r   
    #  l b b b b   
    #
    def sqshape(self, A, n):
        edge_len = sp.sqrt(A) # the length of each edge
        base = sp.linspace(0, edge_len, n+1) # n+1 points, equally spaced
        # create left edge
        left = sp.transpose(sp.vstack((sp.zeros(n), base[0:-1])) )
        # top edge
        top_y = base[-1] # the height of the square
        top = sp.transpose(sp.vstack((base[0:-1],top_y * sp.ones(n))))
        # bottom edge
        bottom = sp.transpose((base[1:], sp.vstack((sp.zeros(n)))))

        # right edge
        right_x = top_y # the x-coordinate of the right edge
        right = sp.transpose(sp.vstack((right_x * sp.ones(n), top_y - base[0:-1])))
        
        return sp.vstack((left, top, right, bottom[::-1])) # bottom is reversed for consistency

    def circshape(self, A, n):
        rad = sp.sqrt(A/sp.pi) # the radius 
        base = sp.linspace(0, 2*sp.pi, 4*n+1)[:-1] # split up the circumference to 4n pieces
        pts = []
        for arg in base: 
            x = rad*(sp.cos(arg))
            y = rad*(sp.sin(arg))
            pts.append((x,y))
        
        return sp.array(pts)

    # Shape proposed by Ray
    def rayshape(self, A, d, n):
        # We'll get 4n+4 points, but there are duplicates at the four corners.
        # So, total = 4n
        rad = sp.sqrt(A/sp.pi) # the radius of the base circle
        base = sp.linspace(-sp.pi/4, sp.pi/4, n+1) # split up a quarter of the circumference to n pieces (omitting the point at pi/4)
        C1 = []
        for arg in base:
            x = -d + (rad+d)*sp.cos(arg)
            y = (rad+d)*sp.sin(arg)
            C1.append((x,y))
        # Construct C3, which is the image of C1 by rotation by pi.
        C3 = []
        for pt in C1:
            C3.append((-pt[0] , -pt[1]))
        # Now construct C2
        base = sp.linspace(sp.pi/4, 3*sp.pi/4, n+1) # split up a quarter of the circumference to n pieces
        C2 = []
        for arg in base:
            x = (rad+d)*sp.cos(arg)
            y = -d + (rad+d)*sp.sin(arg)
            C2.append((x,y))
        # Construct C4 from C2 by applying rotation by pi.
        C4 = []
        for pt in C2:
            C4.append((-pt[0] , -pt[1]))

        return sp.vstack((C1, C2, C3, C4)) 

    # apply Horseshoe Map
    def billard(self, param=(1.0/3, 3.0)):
        self.pts = vBillard(self.pts, param)

    def shplot_nosave(self):
    # plot points
        shape = self.pts
        plt.plot(shape[:,0], shape[:,1],'o', color='red')
        # plot line segments
        pt1 = shape[0]
        for i in range(len(shape)-1):
            pt2 = shape[i + 1]
            ptm = sp.vstack((pt1,pt2))
            plt.plot(ptm[:,0], ptm[:,1])
            pt1 = pt2

    # intgrid: return the xy coords of the points (including the walls) converted to integer representations
    def intgrid(self):
        n = self.resolution/4.0
        return sp.array(round_matrix(n * self.pts))

    # show plot in interactive mode
    def show(self):
        self.shplot_nosave()

    # save plot in a png
    def save(self):
        #shplot(self,self.name)
        pass




def round_matrix(pts):
    m = []
    for arr in pts:
        m.append([round(p) for p in arr])
    return m

# cvplot: plot a shape
def cvplot(shape, name):
    n = sp.sqrt(shape.resolution) # num of points per line
    pts = shape.pts
    r   = shape.rad
    colors = shape.colors
    for i in range(int(n**2)):
        # Plot the point
        p = pts[i]
        # Figure out the color of its patch
        cval = colors[i]
        plt.plot((p[0]),(p[1]),'o', markersize = 40/n, color='black')
        subsq = patch.Rectangle(p - [r,r], 2*r, 2*r,color=cval)
        plt.gca().add_patch(subsq)
        plt.savefig(name)

# interactive version
def cvplot_nosave(shape):
    n = sp.sqrt(shape.resolution) # num of points per line
    pts = shape.pts
    r   = shape.rad
    colors = shape.colors
    for i in range(int(n**2)):
        # Plot the point
        p = pts[i]
        # Figure out the color of its patch
        cval = colors[i]
        plt.plot((p[0]),(p[1]),'o', markersize = 40/n, color='black')
        subsq = patch.Rectangle(p - [r,r], 2*r, 2*r,color=cval)
        plt.gca().add_patch(subsq)
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.show()



# IterateN: Iterate function g N-times with the initial condition init.
def IterateN(g, init, N, param):
    result = init
    for i in range(N):
        result = g(result,param)

    # Return a numpy array
    return result

" JUNK ??? "

# animation in interactive version
# NOT WORKING
def cvanimate(cover,N):
    cvplot_nosave(cover)
    for i in range(N):
        cover = vCat(cover,param)
        plt.cla()
        cvplot_nosave(cover)

# IterRand: Do one iteration of Cat or Kick map
def IterRand(init):
    rnum = random.randint(0,2) # generate 0 or 1
    if rnum==1:
        g = vCat
        param = 10*random.random() # generate a parameter between 0 and 10
    else:
        g = vKick
        param = 2*sp.pi*random.random() # generate a parameter between 0 and 2pi

    return g(init,param)


# IterRandN: Randomly iterate N times
def IterRandN(init, N):
    result = init
    for i in range(N):
        result = IterRand(result)
    return result


