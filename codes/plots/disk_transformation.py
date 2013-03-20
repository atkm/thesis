from shapes import *

sh = BasicShape('ray', 1.0, 128)
#sh.billard_setup_disk(10, 0.02, 400)
sh.billard_setup_disk(10, 0.1, 40)
#sh.billardN(400)
sh.billard()
result = sh.balls
f = open('disk_transformation_result.txt', 'w')
for b in result:
  f.write(str(b[0]))
  f.write(" ")
  f.write(str(b[1]))
  f.write("\n")
