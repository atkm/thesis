#!/usr/bin/env ruby

f = File.open('bound.orig', 'r')
newf = File.open('bound_R_2-4.dat', 'w')
lns = f.readlines()
lns.collect do |l|
  unless l.include?('#')
    line = l.split(' ')
    newf.write(line[1])
    newf.write(' ')
    newf.write(line[3])
    newf.write(' ')
    newf.puts(line[6])
    newf.write(line[1])
    newf.write(' ')
    newf.write(line[3])
    newf.write(' ')
    newf.puts(line[8])
  end
end
