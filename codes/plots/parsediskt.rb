version = '_1'
f = 'disk_transformation_result' + version + '.txt'
target = 'disk_transformation' + version + '.dat'
command = "echo 'x y' > #{target}"
system(command)
command = 'cat ' + f + " | tail -n +6 >> #{target}"
system(command)
