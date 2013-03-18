from shapes import *
import pprocess as pproc
import time

eps = sp.finfo(float).eps

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
                break
        # otherwise, the system didn't show sensitive dependence on initial conditions.
        if not(nrm > bound):
            result.append(0)

    result = sp.array(result)
    result = sp.transpose(sp.vstack((testpts[:,0],testpts[:,1],result)))
    return result

# parallel version of sensitivity test on a disk
def p_sensitivity_test(d, R, delta, bound, numitr, ballnum):
    sh = BasicShape('ray', d, 256)
    sh.billard_setup_disk(R, delta, ballnum)
    testpts = sh.balls # save the initial setup
    result = pproc.Map(limit=10, reuse=1)
    p_billard = result.manage(pproc.MakeReusable(p_sensitivity_test_helper))
    for b in sh.balls: # test sensitivity for each point
        p_billard(sh, b, d, delta, bound, numitr)
    
    return result

def p_sensitivity_test_helper(shape, ball, d, delta, bound, numitr):
        other = rotation(ball, -eps) # the other point is a point obtained by clockwise rotation by epsilon
        maxdist = 0
        for i in range(numitr):
            nrm = shape.billard_mod()
            if nrm > maxdist:
                maxdist = nrm
            if nrm > bound:
                return 1
        # otherwise, the system didn't show sensitive dependence on initial conditions.
        return 0


def run_test(parallel=False):
    #R = 10
    #dls = [0.5, 1.0, 1.5, 2.0]
    #delta = 0.02
    #ballnum = 200
    #eps = sp.finfo(float).eps
    #bound = 1
    #numitr=10000
    R = 4
    dls = [0.5,1.0]
    delta = 0.2
    ballnum = 6
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
        f.write("\n")
        if parallel:
            result = p_sensitivity_test(d, R, delta, bound, numitr, ballnum)
        else:
            result = sensitivity_test_disk(d, R, delta, bound, numitr, ballnum)
        for p in result:
            f.write(str(p))
            f.write("\n")
   

# MAIN
#t = time.time()
#run_test(parallel=True)
#print("Parallel: ")
#print(str(time.time() - t))
#t = time.time()
#run_test()
#print("Not parallel: ")
#print(str(time.time() - t))
   
# run it in parallel
run_test(parallel=True)
