from shapes import *

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


d = 0.2
R = 4
arg = sp.pi/10
p1 = (R*sp.cos(arg), R*sp.sin(arg))
#dist = sp.finfo(float).eps
#dist = sp.pi # rotated 180 degrees
dist = sp.pi/2 # the other side
result, distls, maxdist = sensitivity_test(d, R, 10, 10000, p1, dist)

print(result)

#
#f = open('bound_test_result.txt', 'w')
#f.write('dls: ')
#f.write(str(dls))
#f.write("\n")
#f.write('Rls: ')
#f.write(str(Rls))
#f.write("\n")
#f.write('Bound: ')
#f.write(str(bound))
#f.write("\n")
#f.write('Number of Iterations: ')
#f.write(str(itrnum))
#f.write("\n")
#f.write('Number of Balls: ')
#f.write(str(numballs))
#f.write("\n")
#f.write(str(maxd))
#f.write("\n")
#if result:
#  f.write('Sensitive ')
#else:
#  f.write('NotSensitive ')

