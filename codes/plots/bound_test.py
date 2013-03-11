from shapes import *

dls = sp.linspace(0.01, 0.9, 20)
Rls = sp.linspace(1,15,15)
bound = 10**2
itrnum = 150
numballs = 64

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

for d in dls:
    for R in Rls:
        f.write('d: ' + str(d) + ' R: ' + str(R) + ' ')
        sh = BasicShape('ray', d, numballs)
        sh.billard_setup(R)
        sh.billardN(itrnum)
        result = bounded(sh.balls, bound)
        if result:
          f.write('Bounded ')
        else:
          f.write('Not Bounded ')
        maxd = max_norm(sh.balls)
        f.write(str(maxd))
        f.write("\n")
