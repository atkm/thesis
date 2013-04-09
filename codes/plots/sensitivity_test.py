from shapes import *

# a version of sensitivity test that keeps track of the distance between two points
def sensitivity_test_verbose(d, R, bound, itrnum, init, dist):
    sh = BasicShape('ray', d, 256)
    other = rotation(init, -dist) # the other point is a point obtained by clockwise rotation by arg
    # set up two points
    sh.billard_setup(R)
    sh.balls = sp.array([init, other])
    distls = [sp.linalg.norm(init-other)]
    for i in range(itrnum):
        nrm = sh.billard_mod()
        distls.append(nrm)
        if nrm > bound:
            #print(distls)
            #return True
            return True, distls, nrm
    # otherwise, the system didn't show sensitive dependence on initial conditions.
    #print(distls)
    maxdist = max_norm(distls)
    return False, distls, maxdist


def sensitivity_test(d, R, bound, itrnum, init, dist):
    # R: The radius of the outer circle
    # d: The parameter for the inner circle
    # bound: what is the minimum distance that the 
    # dist: the distance between the init and point2.
    #       measured by angle.
    """
    Sensitivity Test:
        Do iterations of two point (nearby or not) under billard map.
        Stop as soon as the metric of the two reaches the bound.
        Also record the distances between the two.
    """
    sh = BasicShape('ray', d, 256)
    other = rotation(init, -dist) # the other point is a point obtained by clockwise rotation by arg
    # set up two points
    sh.billard_setup(R)
    sh.balls = sp.array([init, other])
    #distls = [sp.linalg.norm(init-other)]
    maxdist = 0
    for i in range(itrnum):
        nrm = sh.billard_mod()
        if nrm > maxdist:
            maxdist = nrm
        #distls.append(nrm)
        if nrm > bound:
            #print(distls)
            #return True
            #return True, distls, nrm
            return True, maxdist
    # otherwise, the system didn't show sensitive dependence on initial conditions.
    #print(distls)
    #maxdist = max_norm(distls)
    return False, maxdist


def run_test():
    R = 4
    dls = [1]
    argls = (sp.pi/10, sp.pi/4)
    #dls = sp.linspace(0.01, 3, 11)
    #argls = sp.linspace(0, sp.pi/2, 50)
    dist = sp.finfo(float).eps
    #dist = sp.pi # rotated 180 degrees
    # dist = sp.pi/2 # the other side
    bound = 8
    numitr=10000
       
    f = open('sensitivity_test_result.txt', 'w')
    f.write('R: ')
    f.write(str(R))
    f.write("\n")
    f.write('dls: ')
    f.write(str(dls))
    f.write("\n")
    f.write('argls: ')
    f.write(str(argls))
    f.write("\n")
    f.write('init dist: ')
    f.write(str(dist))
    f.write("\n")
    f.write('Bound: ')
    f.write(str(bound))
    f.write("\n")
    f.write('Number of Iterations: ')
    f.write(str(numitr))
    f.write("\n\n")
    
    for d in dls:
        for arg in argls:
            f.write('d: ')
            f.write(str(d))
            f.write(" ")
            f.write('arg: ')
            f.write(str(arg))
            f.write(" ")
            p1 = (R*sp.cos(arg), R*sp.sin(arg))
            result, maxdist = sensitivity_test(d, R, bound, numitr, p1, dist)
            if result:
              f.write('Sensitive ')
            else:
              f.write('NotSensitive ')
            f.write(str(maxdist))
            f.write("\n")
    

# MAIN
run_test()
    
