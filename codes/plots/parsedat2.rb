#!/usr/bin/env ruby

# data parsing for bound test
f = File.open('sensitivity.orig', 'r')
newf = File.open('sensitivity_2.dat', 'w')
lns = f.readlines()
lns.collect do |l|
  unless l.include?('#')
    line = l.split(' ')
    newf.write(line[1]) # d
    newf.write(' ')
    newf.write(line[3]) # arg
    newf.write(' ')
    # test result
    if line[4] == 'Sensitive'
      newf.puts('1') 
    elsif line[4] == 'NotSensitive'
      newf.puts('0') 
    else line[4]
      puts(line[4])
      raise("something went wrong.")
    end
  end
end
