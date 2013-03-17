from shapes import *

def sensitivity_test_disk(d, R, delta, bound, itrnum, ballnum):
    # d: The parameter for the inner circle
    # R: The radius of the outer circle
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
    sh.billard_setup_disk(R, delta, ballnum)
    maxdist = 0
    for i in range(itrnum):
        nrm = sh.billard_mod()
        if nrm > maxdist:
            maxdist = nrm
        if nrm > bound:
            return True, maxdist
    # otherwise, the system didn't show sensitive dependence on initial conditions.
    return False, maxdist


def run_test():
    R = 10
    dls = [0.5, 1.0, 1.5, 2.0]
    delta = 0.05
    eps = sp.finfo(float).eps
    bound = 1
    numitr=10000
       
    f = open('sensitivity_test_disk_result.txt', 'w')
    f.write('R: ')
    f.write(str(R))
    f.write("\n")
    f.write('dls: ')
    f.write(str(dls))
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
            p1 = (R*sp.cos(arg), R*sp.sin(arg))
            result, maxdist = sensitivity_test(d, R, bound, numitr, p1, dist)
            if result:
              f.write('Sensitive ')
            else:
              f.write('NotSensitive ')
            f.write(str(maxdist))
            f.write("\n")
    

# MAIN
#run_test()
    
