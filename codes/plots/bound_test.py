from shapes import *

dls = sp.linspace(0.1, 1, 10)
Rls = sp.linspace(1.25, 10, 10)
bound = 10**3
itrnum = 10**3
numballs = 128

f = open('bound_test_result.txt', 'w')
for d in dls:
    for R in Rls:
        f.write('d: ' + str(d) + ' R: ' + str(R) + ' ')
        sh = BasicShape('ray', d, numballs)
        sh.billard_setup(R)
        sh.billardN(itrnum)
        result = bounded(sh.balls, bound)
        if result:
          f.write('Bounded')
        else:
          f.write('Not Bounded')
        f.write("\n")
