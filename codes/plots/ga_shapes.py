import scipy as sp
import scipy.optimize
import scipy.fftpack
import mpl_toolkits.mplot3d.axes3d as axs
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import matplotlib.patches as patch
import random
import time

# pylab.plot(xaxis, graph) to plot
# for example xasix = sp.linspace(0,1,100)

class Shape:
    def __init__(self, kind, A, n):
        if kind == 'square':
             model = sqcover(A,n)

        self.name = kind + '_' + str(A) + '_' + str(n) + '_' + str(round(time.time())) + '.png'
        self.pts = model[0]
        self.rad = model[1]
        self.colors = model[2]
        self.resolution = len(self.pts) # total num of points 
        self.cover = (self.pts, self.rad, self.colors)

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

# circle
def circle(A, n):
    r = sp.sqrt(A) # the radius


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


# animation in interactive version
# NOT WORKING
def cvanimate(cover,N):
    cvplot_nosave(cover)
    for i in range(N):
        cover = vCat(cover,param)
        plt.cla()
        cvplot_nosave(cover)

# IterateN: Iterate function g N-times with the initial condition init.
def IterateN(g, init, N, param):
    result = init
    for i in range(N):
        result = g(result,param)

    # Return a numpy array
    return result

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


# GenShape: the simulation code
# Create a square of area A, resolution mxm, iterate it N times.
# Print out the result in a png
def GenShape(g, A, m, N, name):
    sq = sqcover(A, m)
    if (N!=0):
        new_shape = IterateN(vCat, sq, N)
    else:
        new_shape = sq

    cvplot(new_shape, name)

# Basic shape class: just shape class without mutation
# More geared towards consideration of shapes of walls 
# side = linear (ax: 0 deg = vertical, >0 deg = slant), nonlinear (x^n: )
# height = the height:width ratio
class BasicShape:
    def __init__(self, kind, A, n, side, height, param):
        if kind == 'square':
            model = self.sqshape(A,n)
            self.edge = sp.sqrt(A)
        if kind == 'circle':
            model = self.circshape(A,n)
            self.edge = 2 * sp.sqrt(A/sp.pi)

        self.name = 'basic' + kind + '_' + str(A) + '_' + str(n) + '_' + side + '_' + str(param) + '_' + str(round(time.time())) + '.png'
        self.pts = model
        self.height = height
        self.resolution = len(self.pts) # total num of points on the base. resolution == 4*n
        if side == 'linear':
            self.wall_graph = lambda x: x / param
        elif side == 'nonlinear':
            self.wall_graph = lambda x: x ** (1/param)
        else:
            raise Exception("wall has to be either linear or nonlinear")
        self.wall_func = lambda h: self.make_wall(self.pts, self.edge, h, self.wall_graph)

        self.wall = self.wall_func(height)


    # intgrid: return the xy coords of the points (including the walls) converted to integer representations
    def intgrid(self):
        n = self.resolution/4.0
        return sp.array(round_matrix(n * self.pts))

    # intgrid3d: return the xyz coords of the points (including the walls) converted to integer representations
    def intgrid3d(self):
        g3d = []
        n = round(self.resolution/4.0)
        basegrid = self.intgrid()
        height = round(self.height * n)
        diff = round(self.wall_graph(height))
        adddiff = lambda x, y, z: sp.array((x + diff, y + diff, z))
        for i in range(int(height)):
            layer = self.make_wall(basegrid, self.edge * n, i, self.wall_graph)
            layer = [adddiff(round(p[0]), round(p[1]), round(p[2])) for p in layer]
            g3d.append(layer)
        # translate all points so that the walls are also on a positive grid
        return sp.array(g3d)
        #basegrid = sp.vstack((sp.transpose(basegrid), sp.zeros(len(basegrid))))
        #basegrid = sp.transpose(basegrid)


    # xyzxyz: return a 2-tuple of the xyz coords of the bottom points and those for the top.
    def xyzxyz(self):
        top = self.wall
        bottom = sp.vstack((sp.transpose(self.pts), sp.zeros(self.resolution)))
        bottom = sp.transpose(bottom)
        return top, bottom

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
    def sqshape(self, A,n):
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
        base = sp.linspace(0, 2*sp.pi, 4*n+1)[:-1] # split up the circumference to n pieces
        pts = []
        for arg in base: # the coords are translated (+rad, +rad) to make it fit in the 1st quadrant
            x = rad*(sp.cos(arg) + 1)
            y = rad*(sp.sin(arg) + 1)
            pts.append((x,y))
        
        return sp.array(pts)

    # make_wall()
    def make_wall(self, pts, edge, height, func):
        wall = []
        for p in pts:
            if p[0] == 0: # the left edge
                if p[1] == 0: # the bottom left
                    wall.append([(-1)/sp.sqrt(2)*func(height), (-1)/sp.sqrt(2)*func(height), height])
                elif p[1] == edge: # the top left
                    wall.append([ p[0] + (-1)/sp.sqrt(2)*func(height), p[1] + func(height)/sp.sqrt(2), height])
                else: # others on the left edge
                    wall.append([ p[0] - func(height), p[1], height])
            elif p[1] == edge: # the top edge
                if p[0] == edge: # the top right
                    wall.append([ p[0] + func(height)/sp.sqrt(2), p[1] + func(height)/sp.sqrt(2), height])
                else: # others on the top edge
                    wall.append([ p[0], p[1] + func(height), height])
            elif p[0] == edge: # the right edge
                if p[1] == 0: # the bottom right
                    wall.append([ p[0] + func(height)/sp.sqrt(2), p[1] - func(height)/sp.sqrt(2), height])
                else: # others on the right edge
                    wall.append([ p[0] + func(height), p[1], height])
            else: # the bottom edge
                wall.append([ p[0], p[1] - func(height), height])

        return sp.array(wall)

    def shplot3d(self):
        fig = plt.figure()
        space = axs.Axes3D(fig)
        # plot the wall 
        points = self.xyzxyz()
        top = sp.transpose(points[0])
        space.scatter(top[0],top[1],top[2])
        # plot the pan bottom
        bottom = sp.transpose(points[1])
        space.scatter(bottom[0],bottom[1],bottom[2])
        plt.show()


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

    # show plot in interactive mode
    def show(self):
        self.shplot_nosave()

    # save plot in a png
    def save(self):
        #shplot(self,self.name)
        pass



