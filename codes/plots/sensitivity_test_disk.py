from shapes import *

def sensitivity_test_disk(d, R, delta, bound, numitr, ballnum):
    # d: The parameter for the inner circle
    # R: The radius of the outer circle
    # bound: what is the minimum distance that the 
    """
    Sensitivity Test for a Disk:
        For each point do iterations of the point and a nearby point under billard map.
        Stop as soon as the metric of the two reaches the bound.
        Also record the distances between the two.
    """
    sh = BasicShape('ray', d, 256)
    sh.billard_setup_disk(R, delta, ballnum)
    testpts = sh.balls # save the initial setup
    result = []
    maxdist = 0
    eps = sp.finfo(float).eps
    for b in sh.balls: # test sensitivity for each point
        other = rotation(b, -eps) # the other point is a point obtained by clockwise rotation by epsilon
        for i in range(numitr):
            nrm = sh.billard_mod()
            if nrm > maxdist:
                maxdist = nrm
            if nrm > bound:
                result.append(1)
        # otherwise, the system didn't show sensitive dependence on initial conditions.
        result.append(0)
    result = sp.array(result)
    result = sp.transpose(sp.vstack((testpts[:,0],testpts[:,1],result)))
    return result


def run_test():
    #R = 10
    #dls = [0.5, 1.0, 1.5, 2.0]
    #delta = 0.02
    #ballnum = 200
    #eps = sp.finfo(float).eps
    #bound = 1
    #numitr=10000
    R = 4
    dls = [0.5, 1.0]
    delta = 0.1
    ballnum = 10
    eps = sp.finfo(float).eps
    bound = 1
    numitr=200

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
        f.write('d: ')
        f.write(str(d))
        f.write(" ")
        result = sensitivity_test_disk(d, R, delta, bound, numitr, ballnum)
        for p in result:
            f.write(p)
            f.write("\n")
   

# MAIN
run_test()
    
