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
    def __init__(self, kind, A, n):
        if kind == 'square':
            model = self.sqshape(A,n)
            self.edge = sp.sqrt(A)
        if kind == 'circle':
            model = self.circshape(A,n)
            self.edge = 2 * sp.sqrt(A/sp.pi)
        if kind == 'ray':
            self.param = A
            self.edge = (-A + sp.sqrt(A**2 + 4*A + 2))/2 # the x,y coordinates of the corner
            model = self.rayshape(A,n)

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
    #e.g. BasicShape('ray', sp.pi, 10, 0.25)
    def rayshape(self, d, n):
        # We will obtain the shape by constructing C1 then rotating by pi/2 three times.
        # determine the first arc
        C1 = []
        for y in sp.linspace(-self.edge, self.edge, n):
            x = -d + sp.sqrt((1+d)**2 - y**2) # the rad/12 is to make the diagram look better
            pt = (x,y)
            C1.append(pt)
        C2 = vrotation(C1, -sp.pi/2)
        C3 = vrotation(C2, -sp.pi/2)
        C4 = vrotation(C3, -sp.pi/2)
            
        return sp.vstack((C1, C2, C3, C4)) 

    # set up the circle for playing billard
    # also figure out the slopes of the corners
    def billard_setup(self, R):
        # R determines the ratio of the radius of the circle to the radius of the base circle (which is one)
        # need to determine the area to utilize the pre-defined function
        area = sp.pi * R**2
        self.balls = self.circshape(area, self.resolution/4)
        self.corner_slopes()

    def corner_slopes(self):
        h = self.edge
        d = self.param
        # We only need the first three to define the billard!!!
        # C1 bottom right
        self.c1br = 1 + d/h
        # C1 top right
        self.c1tr = -self.c1br
        # C2 top right
        self.c2tr = 1/self.c1tr

    def billard(self):
        # determine the limit tangent points of the first corner (bottom right)
        result = []
        for pt in self.balls:
            # shoot the ball depending on the region.
            region = self.get_region(pt)
            new = self.shoot(pt,region)
            result.append(new)
        self.balls = sp.array(result)

    def shoot(self,pt,region):
        quad = region[1] - 1
        if region == 'inside':
            return pt
        elif region[0] == 1:
            tang = self.find_tang(rotation(pt, -sp.pi/2 * quad))
            new = rotation(tang, sp.pi/2 * quad)
        else:
            tang = rotation((self.edge, self.edge), sp.pi/2 * quad)
            new = tang + (tang - pt)
        return new
        
    # find the tangent point for an exterior point in C1
    def find_tang(self, pt):
        x = pt[0]
        y = pt[1]
        d = self.param
        k = sp.sqrt((x+d)**2 + y**2 - (1+d)**2)
        theta = sp.arctan(k/(1+d))
        # translation by d, rotation by 2*theta, then translate back by d
        x += d
        x, y = rotation((x,y), 2*theta)
        x -= d
        return sp.array((x,y))

    # returns 'inside' or a tuple of two ints
    # tuple[0] = 1 means tangent point is on an arc
    # tuple[0] = 2 means tangent point is a corner
    # tuple[1] designates which quadrant the point is on
    def get_region(self,pt):
        if self.in_table(pt):
            # leave it as is if the point is in the table
            return 'inside'
        else:
            for i in range(4):
                arg = -i * sp.pi/2
                if self.in_region1(rotation(pt,arg)):
                    return (1,i+1)
                if self.in_region2(rotation(pt,arg)):
                    return (2,i+1)

    # inside the table
    def in_table(self,pt):
        for i in range(4):
            arg = i * sp.pi/2
            if self.in_C1(rotation(pt,arg)):
                return True
        return False

    # inside the C1 part of the table
    def in_C1(self,pt):
        x = pt[0]
        y = pt[1]
        d = self.param
        h = self.edge
        # inside the C1 circle and inside the (45deg clockwise rotated) first quadrant
        if (((x + d)**2 + y**2 <= (1+d)**2) and y <= x and y >= -x):
            return True
        else:
            return False
    
            
    # the region where the ball deflect off C1
    def in_region1(self,pt):
        x = pt[0]
        y = pt[1]
        h = self.edge
        if ((y <= self.c1br * (x-h) - h) and (y <= self.c1tr * (x-h) + h)):
            return True
        elif ((x > self.edge) and (not self.in_C1(pt)) and (y >= self.c1br * (x-h) - h) and (y <= self.c1tr * (x-h) + h)): # take care of the remaining small region
            return True
        else:
            return False

    # the region where the ball deflect off the top right corner
    def in_region2(self,pt):
        x = pt[0]
        y = pt[1]
        h = self.edge
        if ((y >= self.c1tr * (x-h) + h) and (y <= self.c2tr * (x-h) + h)):
            return True
        else:
            return False

    # for testing
    def draw_regions(self):
        h = self.edge
        grid = sp.linspace(-2,2,100)
        # bottom right
        plt.plot(grid, (lambda x: (self.c1br * (x-h) - h))(grid))
        plt.plot(grid, (lambda x: (1/self.c1br * (x-h) - h))(grid))
        # top right
        plt.plot(grid, (lambda x: (self.c1tr * (x-h) + h))(grid))
        plt.plot(grid, (lambda x: (self.c2tr * (x-h) + h))(grid))
        # top left
        plt.plot(grid, (lambda x: (-1/self.c1tr * (x+h) + h))(grid))
        plt.plot(grid, (lambda x: (-1/self.c2tr * (x+h) + h))(grid))
        # bottom left
        plt.plot(grid, (lambda x: (-1/self.c1br * (x+h) - h))(grid))
        plt.plot(grid, (lambda x: (-self.c1br * (x+h) - h))(grid))


    def show_billard(self):
    # plot points
        shape = self.balls
        plt.plot(shape[:,0], shape[:,1],'o', color='blue',markersize=3)

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

    def showpts(self):
    # plot points
        shape = self.pts
        plt.plot(shape[:,0], shape[:,1],'o', color='red',markersize=1)

    # save plot in a png
    def save(self,name):
        plt.savefig(name)



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

def rotation(pt,arg):
    x = pt[0]
    y = pt[1]
    return sp.array((x * sp.cos(arg) - y * sp.sin(arg), x * sp.sin(arg) + y * sp.cos(arg)))

def vrotation(pts,arg):
    return sp.array([rotation(pt, arg) for pt in pts])

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

# Shape proposed by Ray
def rayshape_old(self, A, d, n):
    # We'll get 4n+4 points, but there are duplicates at the four corners.
    # So, total = 4n
    rad = sp.sqrt(A/sp.pi) # the radius of the base circle
    angle = sp.arcsin(1/(sp.sqrt(2) * (1+d))) # each quadrant isn't -pi/4 < theta < pi/4. A bit less than that.
    base = sp.linspace(-angle, angle, n+1) # split up a quarter of the circumference to n pieces (omitting the point at pi/4)
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
    base = sp.linspace(sp.pi/2 - angle, sp.pi/2 + angle, n+1) # split up a quarter of the circumference to n pieces
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
 
