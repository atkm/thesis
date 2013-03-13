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
    sh = BasicShape('ray', d, numballs)
    other = 
    sh.balls = [init, ]
    # set up two points
    sh.billardN(itrnum)
    result = bounded(sh.balls, bound)
    maxd = max_norm(sh.balls)
    

d = 0.2
R = 4
arg = sp.pi/10
p1 = (R*sp.cos(arg), R*sp.sin(arg))
dist = sp.finfo(float).eps
result = sensitivity_test(d, R, 200, p1, dist)


f = open('bound_test_result.txt', 'w')
f.write('dls: ')
f.write(str(dls))
f.write("\n")
f.write('Rls: ')
f.write(str(Rls))
f.write("\n")
f.write('Bound: ')
f.write(str(bound))
f.write("\n")
f.write('Number of Iterations: ')
f.write(str(itrnum))
f.write("\n")
f.write('Number of Balls: ')
f.write(str(numballs))
f.write("\n")
f.write(str(maxd))
f.write("\n")

if result:
  f.write('Bounded ')
else:
  f.write('NotBounded ')

